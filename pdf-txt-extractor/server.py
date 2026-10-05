"""FastAPI app serving UI + PDF text-extraction API.

Run via: uvicorn server:app --port 8000
"""
from __future__ import annotations

import asyncio
import io
import tempfile
import time
import zipfile
from pathlib import Path

import fitz  # PyMuPDF
from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response

VERSION = "1.0.0"

MAX_SINGLE_BYTES = 50 * 1024 * 1024      # 50 MB per file
MAX_TOTAL_BYTES = 200 * 1024 * 1024      # 200 MB per batch
MAX_FILES = 20
MAX_CHARS = 1_000_000

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/octet-stream",
    "binary/octet-stream",
}

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"
INDEX_HTML = UI_DIR / "index.html"

app = FastAPI(title="pdf-txt-extractor", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiError(HTTPException):
    def __init__(self, status_code: int, message: str, code: str):
        super().__init__(status_code=status_code, detail=message)
        self.code = code


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    # Normalize unexpected HTTPExceptions to {detail, code} shape.
    detail = exc.detail
    if isinstance(detail, dict) and "message" in detail:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail.get("message"), "code": detail.get("code", "error")},
        )
    if isinstance(detail, dict):
        return JSONResponse(status_code=exc.status_code, content=detail)
    code = {400: "bad-type", 413: "too-large", 422: "corrupt-pdf"}.get(exc.status_code, "error")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(detail), "code": code},
    )


# ---------------------------------------------------------------- UI / health


@app.get("/", include_in_schema=False)
async def root():
    if INDEX_HTML.is_file():
        return FileResponse(str(INDEX_HTML), media_type="text/html")
    return PlainTextResponse(
        "UI not found: build the frontend into ui/index.html.",
        status_code=200,
    )


@app.get("/api/health")
async def health():
    return {"ok": True, "version": VERSION}


# ---------------------------------------------------------------- helpers

def _stem(filename: str) -> str:
    name = (filename or "document.pdf").strip() or "document.pdf"
    stem = Path(name).stem.strip() or "document"
    # Keep attachment filenames safe.
    safe = "".join(c if (c.isalnum() or c in ("-", "_", ".", " ")) else "_" for c in stem).strip()
    return safe or "document"


def _validate_pdf_type(filename: str, content_type: str | None) -> None:
    if not filename or not filename.lower().endswith(".pdf"):
        raise ApiError(400, f"Bad file type: expected a .pdf file, got {filename!r}.", "bad-type")
    if content_type and content_type.split(";")[0].strip().lower() not in ALLOWED_CONTENT_TYPES:
        raise ApiError(400, f"Bad content type: {content_type!r}; expected application/pdf.", "bad-type")


def _page_text(page: "fitz.Page", layout: bool) -> str:
    if layout:
        try:
            blocks = page.get_text("blocks")  # (x0,y0,x1,y1,text,block_no,block_type)
            blocks = sorted(blocks, key=lambda b: (round(b[1]), round(b[0])))
            return "\n".join(b[4] for b in blocks if b[4])
        except Exception:
            pass
    return page.get_text("text", sort=layout)


def _extract_sync(data: bytes, layout: bool) -> tuple[int, str]:
    """Extract text from PDF bytes via a temp file. Returns (pages, full_text).

    Raises ValueError on corrupt/invalid PDFs.
    """
    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            doc = fitz.open(tmp_path)
        except Exception as e:
            raise ValueError(f"Corrupt or unreadable PDF: {e}") from e
        with doc:
            # Encrypted check (attribute name differs across versions),
            # mirroring extractor.py so locked PDFs fail instead of
            # returning ok with empty text.
            try:
                needs_pass = doc.needs_pass  # type: ignore[attr-defined]
                if callable(needs_pass):
                    needs_pass = needs_pass()
            except Exception:
                needs_pass = bool(getattr(doc, "is_encrypted", False))
            if needs_pass:
                raise ValueError("Encrypted PDF (password required)")
            pages = doc.page_count
            parts: list[str] = []
            for page in doc:
                parts.append(_page_text(page, layout))
                parts.append("\n")
            return pages, "".join(parts)
    finally:
        if tmp_path:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass


def _cap(text: str) -> tuple[str, bool]:
    if len(text) > MAX_CHARS:
        return text[:MAX_CHARS], True
    return text, False


def _scanned_like(full_text: str, pages: int) -> bool:
    if pages <= 0:
        return False
    stripped = full_text.strip()
    if not stripped:
        return True
    # Heuristic: very few extractable chars per page suggests scanned images.
    # Threshold matches extractor.py (<20 chars/page).
    return len(full_text) < 20 * pages


# ---------------------------------------------------------------- single


@app.post("/api/extract")
async def extract(
    file: UploadFile = File(...),
    layout: bool = Query(default=False),
    download: bool = Query(default=False),
    layout_form: str | None = Form(default=None, alias="layout"),
):
    filename = file.filename or "document.pdf"
    _validate_pdf_type(filename, file.content_type)
    # UI sends layout as a FormData field in fallback single mode, not as a
    # query param; honor either source.
    use_layout = layout or (
        layout_form is not None and layout_form.strip().lower() in ("1", "true", "on", "yes")
    )

    data = await file.read()
    if len(data) > MAX_SINGLE_BYTES:
        raise ApiError(413, f"File too large: {len(data)} bytes exceeds 50MB limit.", "too-large")
    if not data:
        raise ApiError(422, "Empty or corrupt PDF: no content received.", "corrupt-pdf")

    try:
        pages, full_text = await asyncio.to_thread(_extract_sync, data, use_layout)
    except ValueError as e:
        raise ApiError(422, str(e), "corrupt-pdf")
    except Exception as e:
        raise ApiError(422, f"Failed to extract PDF: {e}", "corrupt-pdf")

    text, truncated = _cap(full_text)

    if download:
        stem = _stem(filename)
        return Response(
            content=text,
            media_type="text/plain; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{stem}.txt"'},
        )

    return {
        "filename": filename,
        "pages": pages,
        "chars": len(full_text),
        "text": text,
        "scanned_like": _scanned_like(full_text, pages),
        "truncated": truncated,
        "error": None,
    }


# ---------------------------------------------------------------- batch


def _extract_one_sync(data: bytes, layout: bool) -> tuple[int, str]:
    return _extract_sync(data, layout)


@app.post("/api/extract-batch")
async def extract_batch(
    files: list[UploadFile] = File(...),
    workers: int = Query(default=8, ge=1, le=32),
    zip: bool = Query(default=False),
    layout: bool = Query(default=False),
    layout_form: str | None = Form(default=None, alias="layout"),
):
    # UI also appends layout as a FormData field; honor either source.
    use_layout = layout or (
        layout_form is not None and layout_form.strip().lower() in ("1", "true", "on", "yes")
    )
    if not files:
        raise ApiError(400, "No files provided; expected multipart files[].", "bad-type")
    if len(files) > MAX_FILES:
        raise ApiError(400, f"Too many files: {len(files)} exceeds limit of {MAX_FILES}.", "bad-type")

    # Read all uploads up-front to enforce the total-size cap.
    payloads: list[tuple[str, bytes, str | None]] = []
    total = 0
    for f in files:
        data = await f.read()
        total += len(data)
        payloads.append((f.filename or "document.pdf", data, f.content_type))

    if total > MAX_TOTAL_BYTES:
        raise ApiError(413, f"Batch too large: {total} bytes exceeds 200MB total limit.", "too-large")

    # Validate types before extracting.
    for filename, data, content_type in payloads:
        _validate_pdf_type(filename, content_type)
        if len(data) > MAX_SINGLE_BYTES:
            raise ApiError(413, f"File too large: {filename!r} exceeds 50MB limit.", "too-large")

    started = time.perf_counter()
    sem = asyncio.Semaphore(max(1, workers))

    async def run_one(item: tuple[str, bytes, str | None]) -> dict:
        filename, data, _ct = item
        async with sem:
            if not data:
                return {
                    "filename": filename, "pages": 0, "chars": 0, "text": "",
                    "ok": False, "error": "Empty or corrupt PDF.", "scanned_like": False,
                }
            try:
                # Server-context safe: thread pool via to_thread, no process spawn per request.
                pages, full_text = await asyncio.to_thread(_extract_one_sync, data, use_layout)
            except ValueError as e:
                return {
                    "filename": filename, "pages": 0, "chars": 0, "text": "",
                    "ok": False, "error": str(e), "scanned_like": False,
                }
            except Exception as e:
                return {
                    "filename": filename, "pages": 0, "chars": 0, "text": "",
                    "ok": False, "error": f"Failed to extract PDF: {e}", "scanned_like": False,
                }
            text, truncated = _cap(full_text)
            return {
                "filename": filename,
                "pages": pages,
                "chars": len(full_text),
                "text": text,
                "ok": True,
                "error": None,
                "truncated": truncated,
                "scanned_like": _scanned_like(full_text, pages),
            }

    # Bound concurrency with the semaphore above; each extraction runs in a
    # worker thread via asyncio.to_thread (no per-request pool to manage).
    results = list(await asyncio.gather(*(run_one(p) for p in payloads)))

    took_ms = int((time.perf_counter() - started) * 1000)
    errors = sum(1 for r in results if not r.get("ok"))

    if zip:
        buf = io.BytesIO()
        used: set[str] = set()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in results:
                base = _stem(r["filename"])
                name = f"{base}.txt"
                i = 1
                while name in used:
                    i += 1
                    name = f"{base}-{i}.txt"
                used.add(name)
                zf.writestr(name, r.get("text", ""))
        buf.seek(0)
        return Response(
            content=buf.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="extracted.zip"'},
        )

    return {"results": results, "took_ms": took_ms, "errors": errors}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)
