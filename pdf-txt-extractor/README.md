# PDF TXT Extractor

Extract clean text from one PDF or a batch of PDFs. CLI + FastAPI server + browser UI.

## Quickstart

```powershell
cd "F:/Code Playground/Projects/Websites/pdf-txt-extractor"
pip install -r requirements.txt
```

### CLI — single file

```powershell
python cli.py one input.pdf [-o out.txt] [--layout]
# or via the core module directly:
python extractor.py input.pdf --out-dir output
```

### CLI — batch directory (parallel)

```powershell
python cli.py batch ./pdfs -o ./output --workers 8 [--layout] [--json manifest.json]
# --json - prints a machine-readable manifest to stdout (for AI agents)
# or via the core module directly:
python extractor.py ./pdfs --out-dir output --workers 4
```

### Server

```powershell
uvicorn server:app --port 8000
```

- UI: http://localhost:8000
- Health: http://localhost:8000/api/health

### API examples

Single file extract (returns JSON with text):

```bash
curl -F "file=@sample.pdf" http://localhost:8000/api/extract
```

Batch extract with 4 workers (returns JSON object `{results, took_ms, errors}`):

```bash
curl -F "files=@a.pdf" -F "files=@b.pdf" "http://localhost:8000/api/extract-batch?workers=4"
```

Batch extract as ZIP file (save to all.zip):

```bash
curl -F "files=@a.pdf" -F "files=@b.pdf" "http://localhost:8000/api/extract-batch?zip=true" -o all.zip
```

### Agent JSON schema

Single `/api/extract` response:

```json
{
  "filename": "sample.pdf",
  "pages": 3,
  "chars": 12345,
  "text": "...extracted text..."
}
```

Batch `/api/extract-batch` response (zip=false):

```json
{
  "results": [
    { "filename": "a.pdf", "pages": 2, "chars": 500, "text": "...", "ok": true },
    { "filename": "b.pdf", "pages": 1, "chars": 100, "text": "...", "error": null }
  ],
  "took_ms": 12,
  "errors": 0
}
```

With `?zip=true` the response is `application/zip` (one `.txt` per PDF).

### Scanned-PDF note (OCR)

This extractor reads embedded text layers via PyMuPDF. Scanned/image-only
PDFs have no text layer and will return empty output. For those, run OCR
first (e.g. Tesseract / ocrmypdf) to add a text layer, then extract.

## Acceptance criteria

- [ ] `pip install -r requirements.txt` succeeds
- [ ] CLI single file writes `output/*.txt`
- [ ] CLI batch extracts a directory with `--workers 4`
- [ ] `uvicorn server:app --port 8000` serves UI at http://localhost:8000
- [ ] `POST /api/extract` returns `{filename, pages, chars, text}`
- [ ] `POST /api/extract-batch?workers=4` returns `{results, took_ms, errors}`
- [ ] `POST /api/extract-batch?zip=true` returns a ZIP (`-o all.zip`)

## Notes

- Extracted text files go in `output/` (created on first run, ignored by git except `.gitkeep`).
