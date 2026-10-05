"""PDF-to-text extraction core (Python 3.10+, PyMuPDF).

Serial single-file extraction plus process-pool parallel batch extraction.
Multiprocessing-safe: the worker function :func:`_extract_one` is module-level
and picklable, and no pool is created at import time (``__main__`` guard).
"""

from __future__ import annotations

import concurrent.futures as futures
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

import fitz  # PyMuPDF


@dataclass
class ExtractResult:
    """Outcome of extracting one PDF to text."""

    src: Path
    dst: Path | None
    ok: bool
    chars: int
    pages: int
    error: str | None
    scanned_like: bool


def _extract_one(
    pdf_path: str,
    txt_path: str | None,
    out_dir: str | None,
    layout: bool,
) -> dict:
    """Extract a single PDF to a .txt file. Module-level so it is picklable.

    Args:
        pdf_path: Source PDF file path.
        txt_path: Explicit destination .txt path, or None for default.
        out_dir: Directory for default ``<stem>.txt`` naming, or None to
            place beside the PDF.
        layout: When True, use ``page.get_text("blocks")`` sorted by
            (y0, x0) and join pages with ``"\\n\\n--- page N ---\\n\\n"``
            markers; otherwise ``page.get_text("text")`` joined with
            ``"\\n\\n"``.

    Returns:
        Plain dict with keys src, dst, ok, chars, pages, error,
        scanned_like. ``scanned_like`` is True when pages > 0 and
        chars / pages < 20 (likely a scanned/image-only PDF).
        Failures (missing file, empty/encrypted/corrupt PDF) return
        ``ok=False`` with an error string instead of raising.
    """
    src = Path(pdf_path)
    if txt_path:
        dst = Path(txt_path)
    elif out_dir:
        dst = Path(out_dir) / (src.stem + ".txt")
    else:
        dst = src.with_suffix(".txt")

    def _fail(msg: str, pages: int = 0) -> dict:
        return {
            "src": str(src),
            "dst": str(dst),
            "ok": False,
            "chars": 0,
            "pages": pages,
            "error": msg,
            "scanned_like": False,
        }

    if not src.is_file():
        return _fail(f"FileNotFoundError: {src} does not exist")

    doc: fitz.Document | None = None
    try:
        try:
            doc = fitz.open(pdf_path)
        except FileNotFoundError:
            return _fail(f"FileNotFoundError: {src} does not exist")
        except Exception as exc:  # corrupt / unreadable
            return _fail(f"{type(exc).__name__}: {exc}")

        # Encrypted check (attribute name differs across versions).
        try:
            needs_pass = doc.needs_pass  # type: ignore[attr-defined]
            if callable(needs_pass):
                needs_pass = needs_pass()
        except Exception:
            needs_pass = bool(getattr(doc, "is_encrypted", False))
        if needs_pass:
            return _fail(f"Encrypted PDF (password required): {src}")

        if doc.page_count == 0:
            return _fail(f"Empty PDF (0 pages): {src}")

        parts: list[str] = []
        for page in doc:
            if layout:
                try:
                    blocks = page.get_text("blocks")
                except Exception:
                    blocks = []
                blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
                parts.append("\n".join(str(b[4]) for b in blocks))
            else:
                parts.append(page.get_text("text"))

        if layout:
            chunks: list[str] = []
            for n, text in enumerate(parts, start=1):
                chunks.append(f"\n\n--- page {n} ---\n\n{text}")
            full_text = "".join(chunks).lstrip("\n")
        else:
            full_text = "\n\n".join(parts)

        chars = len(full_text)
        pages = doc.page_count
        scanned_like = pages > 0 and (chars / pages) < 20

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(full_text, encoding="utf-8")

        return {
            "src": str(src),
            "dst": str(dst),
            "ok": True,
            "chars": chars,
            "pages": pages,
            "error": None,
            "scanned_like": scanned_like,
        }
    except Exception as exc:  # never let one file kill a batch
        return _fail(f"{type(exc).__name__}: {exc}")
    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


def extract_pdf_to_text(
    pdf_path: str | Path,
    txt_path: str | Path | None = None,
    *,
    layout: bool = False,
) -> ExtractResult:
    """Serial wrapper: extract one PDF to text.

    Args:
        pdf_path: Source PDF path.
        txt_path: Optional explicit destination .txt path.
        layout: Preserve rough reading order via sorted text blocks plus
            page-break markers.

    Returns:
        ExtractResult describing the outcome.
    """
    d = _extract_one(
        str(pdf_path),
        str(txt_path) if txt_path is not None else None,
        None,
        layout,
    )
    return ExtractResult(
        src=Path(d["src"]),
        dst=Path(d["dst"]) if d["dst"] is not None else None,
        ok=d["ok"],
        chars=d["chars"],
        pages=d["pages"],
        error=d["error"],
        scanned_like=d["scanned_like"],
    )


def extract_many_parallel(
    pdf_paths: Sequence[str | Path] | Iterable[str | Path],
    out_dir: str | Path | None,
    *,
    workers: int | None = None,
    layout: bool = False,
    on_done: Callable[[ExtractResult], None] | None = None,
) -> list[ExtractResult]:
    """Extract many PDFs in parallel using a process pool.

    Args:
        pdf_paths: PDFs to extract (one task per PDF).
        out_dir: Directory for default ``<stem>.txt`` outputs, or None to
            place each .txt beside its PDF.
        workers: Pool size; defaults to ``min(len(pdfs), os.cpu_count() or 4)``.
        layout: Forwarded to :func:`_extract_one`.
        on_done: Optional callback invoked with each ExtractResult as it
            completes (exceptions in the callback are swallowed).

    Returns:
        List of ExtractResult in input order; per-file failures are
        isolated into ``ok=False`` results rather than raising.
    """
    pdfs = [str(p) for p in pdf_paths]
    if not pdfs:
        return []
    if workers is None:
        workers = min(len(pdfs), os.cpu_count() or 4)
    workers = max(1, workers)
    out_s = str(out_dir) if out_dir is not None else None

    ordered: list[ExtractResult | None] = [None] * len(pdfs)
    with futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_idx = {
            executor.submit(_extract_one, pdfs[i], None, out_s, layout): i
            for i in range(len(pdfs))
        }
        for fut in futures.as_completed(future_to_idx):
            idx = future_to_idx[fut]
            try:
                d = fut.result()
                r = ExtractResult(
                    src=Path(d["src"]),
                    dst=Path(d["dst"]) if d["dst"] is not None else None,
                    ok=d["ok"],
                    chars=d["chars"],
                    pages=d["pages"],
                    error=d["error"],
                    scanned_like=d["scanned_like"],
                )
            except Exception as exc:  # isolate worker/callback failures
                r = ExtractResult(
                    src=Path(pdfs[idx]),
                    dst=None,
                    ok=False,
                    chars=0,
                    pages=0,
                    error=f"{type(exc).__name__}: {exc}",
                    scanned_like=False,
                )
            ordered[idx] = r
            if on_done is not None:
                try:
                    on_done(r)
                except Exception:
                    pass
    return [r for r in ordered if r is not None]


if __name__ == "__main__":  # pragma: no cover - manual demo CLI
    import argparse

    ap = argparse.ArgumentParser(description="Extract PDF(s) to .txt via PyMuPDF.")
    ap.add_argument("pdfs", nargs="+", help="PDF file(s) and/or directories to extract (directories expand to their *.pdf members)")
    ap.add_argument("--out-dir", default=None, help="Output directory for .txt files")
    ap.add_argument("--layout", action="store_true", help="Layout/block mode")
    ap.add_argument("--workers", type=int, default=None, help="Parallel workers")
    args = ap.parse_args()

    expanded: list[str] = []
    for p in args.pdfs:
        if Path(p).is_dir():
            expanded.extend(sorted(str(f) for f in Path(p).glob("*.pdf")))
        else:
            expanded.append(p)
    if not expanded:
        ap.error("No PDFs found (directory contained no *.pdf files).")

    results = extract_many_parallel(
        expanded, args.out_dir, workers=args.workers, layout=args.layout
    )
    for r in results:
        status = "OK" if r.ok else f"FAIL: {r.error}"
        print(f"{r.src} -> {r.dst} [{status}] chars={r.chars} pages={r.pages}")
