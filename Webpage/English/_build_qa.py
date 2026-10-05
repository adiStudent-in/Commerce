import re, pathlib
MD = pathlib.Path(r"F:\Study OS\English Markdown\Class-11-English-Important-Questions-with-Answers.md")
REF = pathlib.Path(r"F:\Study OS\Webpage\English\Chapter-1-The-Portrait-of-a-Lady.html")
OUT = pathlib.Path(r"F:\Study OS\Webpage\English\Important-Questions-with-Answers.html")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

def slug(t):
    t = re.sub(r"\*+", "", t)
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def clean_label(t):
    return inline(re.sub(r"\*+", "", t))

ref = REF.read_text(encoding="utf-8")
m_css = re.search(r"<style>(.*?)</style>", ref, re.S)
m_js = re.search(r"<script>(.*?)</script>", ref, re.S)
CSS = m_css.group(1) if m_css else ""
JS = m_js.group(1) if m_js else ""
# Q&A polish on top of identical system
CSS += "\n.qa-answer{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:0 10px 10px 0;padding:14px 18px;margin:12px 0 26px}\n.qa-answer p{margin:0}\n.qnum{color:var(--accent)}\n"

lines = MD.read_text(encoding="utf-8").splitlines()
title = lines[0].lstrip("# ").strip()
subtitle = ""
sections = []
cur = None
para, quote = [], []
contents_skip = True

def flush_para():
    global para
    if para:
        if all(l.strip().startswith("- ") for l in para):
            items = "".join(f"<li>{inline(l.strip()[2:])}</li>" for l in para)
            cur["blocks"].append(("html", f"<ul>{items}</ul>"))
        else:
            text = "<br>".join(inline(l.strip()) for l in para)
            # Answer paragraphs get card styling
            if cur is not None and text.lstrip().startswith("<strong>Answer"):
                cur["blocks"].append(("answer", text))
            else:
                cur["blocks"].append(("p", text))
        para = []

def flush_quote():
    global quote
    if quote:
        cur["blocks"].append(("quote", "<br>".join(inline(l.lstrip("> ").strip()) for l in quote)))
        quote = []

for raw in lines[1:]:
    s = raw.strip()
    if not cur and (s.startswith("**Hornbill") or s.startswith("**Class") or s.startswith("**NCERT")):
        subtitle = inline(s.strip("* "))
        continue
    if s.startswith("**Contents:**"):
        continue
    if s.startswith(">") and not cur:
        continue  # skip top how-to-use quote (kept as hero note below via subtitle)
    if s.startswith(">"):
        flush_para()
        quote.append(raw.strip())
        continue
    flush_quote()
    if not s:
        flush_para()
        continue
    if s == "---":
        flush_para()
        continue
    if s.startswith("*End of file"):
        flush_para()
        continue
    mh2 = re.match(r"^##\s+(.*)$", s)
    mh3 = re.match(r"^###\s+(.*)$", s)
    if mh2:
        flush_para()
        cur = {"title": mh2.group(1).strip(), "id": slug(mh2.group(1)), "blocks": []}
        sections.append(cur)
        continue
    if mh3 and cur is not None:
        flush_para()
        t = mh3.group(1).strip()
        cur["blocks"].append(("h3", (t, slug(t))))
        continue
    if cur is None:
        continue
    para.append(raw.rstrip())
flush_para()

toc = ['<div class="toc-title">Contents</div>']
body = []
for i, sec in enumerate(sections):
    d = min(0.05 * (i + 1), 0.5)
    toc.append(f'<a href="#{sec["id"]}">{clean_label(sec["title"])}</a>')
    parts = [f'<h2 id="{sec["id"]}">{inline(sec["title"])}</h2>']
    for kind, payload in sec["blocks"]:
        if kind == "h3":
            t, sid = payload
            toc.append(f'<a class="sub" href="#{sid}">{clean_label(t)}</a>')
            parts.append(f'<h3 id="{sid}"><span class="qnum">Q.</span> {inline(t)}</h3>')
        elif kind == "p":
            parts.append(f"<p>{payload}</p>")
        elif kind == "answer":
            parts.append(f'<div class="qa-answer"><p>{payload}</p></div>')
        elif kind == "html":
            parts.append(payload)
        elif kind == "quote":
            parts.append(f"<blockquote><p>{payload}</p></blockquote>")
    body.append(f'<section class="fade-in" style="animation-delay:{d:.2f}s">{"".join(parts)}</section>')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="nav"><a class="logo" href="index.html">English Notes</a><span class="meta">Class XI &middot; Hornbill &amp; Snapshots &middot; Questions</span></nav>
<div id="progress"></div>
<div class="wrap">
<aside>
{chr(10).join(toc)}
</aside>
<main>
<div class="hero fade-in" style="animation-delay:.05s">
<span class="badge">Hornbill &amp; Snapshots &middot; Class XI &middot; Question Bank</span>
<h1>{inline(title)}</h1>
<p class="subtitle">{subtitle}</p>
</div>
<div class="callout">Indirect, exam-style questions — <strong>8 per unit (72 total)</strong> — framed as <em>why / how / justify / contrast</em>, with full-marks NCERT-accurate answers. Use the sidebar to jump to any chapter or poem.</div>
{chr(10).join(body)}
</main>
</div>
<button id="tocBtn" aria-label="Open contents">&#9776;</button>
<footer>Source: NCERT Hornbill &amp; Snapshots (Class XI) chapter notes &middot; English Notes</footer>
<script>{JS}</script>
</body>
</html>"""
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT.name}: {len(sections)} sections, {sum(1 for s in sections for k,_ in s['blocks'] if k=='h3')} questions")
