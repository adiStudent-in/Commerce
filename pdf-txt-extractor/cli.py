"""CLI for pdf-txt-extractor (user + AI-agent friendly).

Single file:
    python cli.py one input.pdf [-o out.txt] [--layout]

Batch directory / many files (parallel):
    python cli.py batch ./pdfs -o ./output --workers 8 [--layout] [--json manifest.json]

The batch path calls extractor.extract_many_parallel (ProcessPoolExecutor,
one task per PDF), so N PDFs extract in parallel. --json emits a
machine-readable manifest for AI agents.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from extractor import extract_many_parallel, extract_pdf_to_text


def cmd_one(args: argparse.Namespace) -> int:
    r = extract_pdf_to_text(args.pdf, args.o, layout=args.layout)
    if r.ok:
        print(f"OK: {r.src} -> {r.dst}  pages={r.pages} chars={r.chars}")
        if r.scanned_like:
            print("NOTE: scanned-like PDF (very little embedded text) — OCR may be needed.")
        return 0
    print(f"FAIL: {r.src}: {r.error}", file=sys.stderr)
    return 1


def cmd_batch(args: argparse.Namespace) -> int:
    pdfs: list[str] = []
    for p in args.inputs:
        if Path(p).is_dir():
            pdfs.extend(sorted(str(f) for f in Path(p).glob("*.pdf")))
        else:
            pdfs.append(p)
    if not pdfs:
        print("No PDFs found (directory contained no *.pdf files).", file=sys.stderr)
        return 2

    out_dir = Path(args.o)
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    results = extract_many_parallel(pdfs, out_dir, workers=args.workers, layout=args.layout)
    took = time.perf_counter() - t0

    ok = sum(1 for r in results if r.ok)
    print(f"{'source':60} {'pages':>6} {'chars':>9}  status")
    for r in results:
        status = "OK" if r.ok else f"FAIL: {r.error}"
        print(f"{str(r.src):60} {r.pages:6d} {r.chars:9d}  {status}")
    print(f"\n{ok}/{len(results)} ok in {took:.2f}s (workers={args.workers or 'auto'})")

    if args.json:
        manifest = [
            {
                "pdf": str(r.src),
                "txt": str(r.dst) if r.dst else None,
                "chars": r.chars,
                "pages": r.pages,
                "ok": r.ok,
                "error": r.error,
            }
            for r in results
        ]
        text = json.dumps(manifest, indent=2)
        if args.json == "-":
            print(text)
        else:
            Path(args.json).write_text(text, encoding="utf-8")
            print(f"manifest -> {args.json}")
    return 0 if ok == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extract PDF(s) to .txt (parallel batch).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_one = sub.add_parser("one", help="Extract a single PDF.")
    p_one.add_argument("pdf", help="Input .pdf file")
    p_one.add_argument("-o", default=None, help="Output .txt (default: beside PDF)")
    p_one.add_argument("--layout", action="store_true")
    p_one.set_defaults(func=cmd_one)

    p_batch = sub.add_parser("batch", help="Extract many PDFs in parallel.")
    p_batch.add_argument("inputs", nargs="+", help="PDF files and/or directories")
    p_batch.add_argument("-o", default="output", help="Output dir for .txt files")
    p_batch.add_argument("--workers", type=int, default=None)
    p_batch.add_argument("--layout", action="store_true")
    p_batch.add_argument("--json", default=None, help="Manifest path (or - for stdout)")
    p_batch.set_defaults(func=cmd_batch)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
