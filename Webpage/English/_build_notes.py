# ponytail: md -> html builder for the Class 11 English revision notes (study-docu-web-ui design system)
# Reads every "(Revision Notes).md" file in the English Markdown folder and emits one page per file,
# plus the index. Replaces the older chapter-page pipeline.
import re
import pathlib

SRC_DIR = pathlib.Path(r"F:\Study OS\English Markdown")
ROOT = pathlib.Path(r"F:\Study OS\Webpage\English")

# (source .md filename, output .html, chapter/poem number, book) — order controls the index
PAGES = [
    ("Ch 1 - The Portrait of a Lady (Revision Notes).md",        "Chapter-1-The-Portrait-of-a-Lady.html",                  "Chapter 1", "Hornbill"),
    ("Ch 2 - We're Not Afraid to Die (Revision Notes).md",       "Chapter-2-Were-Not-Afraid-to-Die.html",                  "Chapter 2", "Hornbill"),
    ("Ch 3 - Discovering Tut (Revision Notes).md",               "Chapter-3-Discovering-Tut.html",                         "Chapter 3", "Hornbill"),
    ("Ch 4 - The Ailing Planet (Revision Notes).md",             "Chapter-4-The-Ailing-Planet.html",                       "Chapter 4", "Hornbill"),
    ("Ch 5 - The Adventure (Revision Notes).md",                 "Chapter-5-The-Adventure.html",                           "Chapter 5", "Hornbill"),
    ("Ch 6 - Silk Road (Revision Notes).md",                     "Chapter-6-Silk-Road.html",                               "Chapter 6", "Hornbill"),
    ("Ch 1 - The Summer of the Beautiful White Horse (Revision Notes).md", "Chapter-1-The-Summer-of-the-Beautiful-White-Horse.html", "Chapter 1", "Snapshots"),
    ("Ch 2 - The Address (Revision Notes).md",                   "Chapter-2-The-Address.html",                             "Chapter 2", "Snapshots"),
    ("Ch 3 - Mother's Day (Revision Notes).md",                  "Chapter-3-Mothers-Day.html",                             "Chapter 3", "Snapshots"),
    ("Ch 4 - Birth (Revision Notes).md",                         "Chapter-4-Birth.html",                                   "Chapter 4", "Snapshots"),
    ("Ch 5 - The Tale of Melon City (Revision Notes).md",        "Chapter-5-The-Tale-of-Melon-City.html",                  "Chapter 5", "Snapshots"),
    ("Poem 1 - A Photograph (Revision Notes).md",                "Poem-1-A-Photograph.html",                               "Poem 1",    "Hornbill"),
    ("Poem 2 - The Laburnum Top (Revision Notes).md",            "Poem-2-The-Laburnum-Top.html",                           "Poem 2",    "Hornbill"),
    ("Poem 3 - The Voice of the Rain (Revision Notes).md",       "Poem-3-The-Voice-of-the-Rain.html",                      "Poem 3",    "Hornbill"),
    ("Poem 4 - Childhood (Revision Notes).md",                   "Poem-4-Childhood.html",                                  "Poem 4",    "Hornbill"),
    ("Poem 5 - Father to Son (Revision Notes).md",               "Poem-5-Father-to-Son.html",                              "Poem 5",    "Hornbill"),
]

BR_TAG = "\x00BR\x00"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = s.replace("<br>", BR_TAG).replace("<br/>", BR_TAG).replace("<br />", BR_TAG)
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s.replace(BR_TAG, "<br>")


def clean_label(t):
    return inline(re.sub(r"\*+", "", t))


def slug(t):
    t = re.sub(r"\*+", "", t)
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def parse(md):
    lines = md.splitlines()
    title = lines[0].lstrip("# ").strip()
    subtitle = ""
    sections = []
    cur = None
    para, quote, table = [], [], []

    def target():
        return cur["blocks"] if cur else []

    def flush_para():
        nonlocal para
        if para:
            if all(l.strip().startswith("- ") for l in para):
                items = "".join(f"<li>{inline(l.strip()[2:])}</li>" for l in para)
                target().append(("html", f"<ul>{items}</ul>"))
            else:
                # join first, then apply inline markup — emphasis may span a line break
                text = inline("<br>".join(l.strip() for l in para))
                kind = "callout" if re.match(r"^\*\*Last-minute revision hook", text) else "p"
                target().append((kind, text))
            para = []

    def flush_quote():
        nonlocal quote
        if quote:
            # join first, then apply inline markup — a poem's *"..."* spans every quoted line
            target().append(("quote", inline("<br>".join(l.lstrip("> ").strip() for l in quote))))
            quote = []

    def flush_table():
        nonlocal table
        if table:
            rows = []
            for r in table:
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    continue
                rows.append(cells)
            if rows:
                target().append(("table", rows))
            table = []

    def flush_all():
        flush_para(); flush_quote(); flush_table()

    for raw in lines[1:]:
        s = raw.strip()
        if s.startswith("|"):
            flush_para(); flush_quote(); table.append(s); continue
        if s.startswith(">"):
            flush_para(); flush_table(); quote.append(s); continue
        flush_quote(); flush_table()
        if not s:
            flush_para(); continue
        if s == "---":
            flush_para(); continue
        if not subtitle and re.match(r"^\*\*(Author|Authors|Poet)s?:", s):
            subtitle = inline(s); continue
        m2 = re.match(r"^###\s+(.*)$", s)
        mh2 = re.match(r"^##\s+(.*)$", s)
        mh1 = re.match(r"^#\s+(.*)$", s)
        if m2 and cur:
            flush_para()
            t = m2.group(1).strip()
            # split a trailing "<br>*[n marks]*" off the heading so it renders as a badge
            marks = ""
            mm = re.search(r"<br>\s*\*\[(.+?)\]\*\s*$", t)
            if mm:
                marks = mm.group(1)
                t = t[:mm.start()].strip()
            sid = slug(t)
            cur["blocks"].append(("h3", (t, sid, marks)))
            continue
        if mh2 or (mh1 and sections):
            flush_all()
            t = (mh2.group(1) if mh2 else mh1.group(1)).strip()
            cur = {"title": t, "id": slug(t), "blocks": []}
            sections.append(cur)
            continue
        para.append(s)
    flush_all()
    return title, subtitle, sections


CSS = """
:root{--accent:#1a5e4a;--accent-light:#e8f0ec;--bg:#faf8f5;--surface:#ffffff;--text:#1b1b1b;--muted:#6b6b6b;--border:#e8e4de}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:15.5px}
.nav{position:fixed;top:0;left:0;right:0;height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;background:rgba(250,248,245,.85);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--border);z-index:300}
.logo{font-family:'Playfair Display',serif;font-weight:600;font-size:20px;color:var(--accent);text-decoration:none}
.meta{font-size:13px;color:var(--muted)}
#progress{position:fixed;top:60px;left:0;height:2px;width:0;background:var(--accent);z-index:300}
.wrap{display:flex;gap:44px;max-width:1200px;margin:0 auto;padding:104px 28px 40px}
aside{width:270px;flex-shrink:0;position:sticky;top:84px;max-height:calc(100vh - 110px);overflow-y:auto;padding-right:6px}
aside::-webkit-scrollbar{width:4px}
aside::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
aside .toc-title{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding:0 12px 10px;font-weight:600}
aside a{display:block;padding:6px 12px;font-size:13.5px;color:var(--muted);text-decoration:none;border-left:2px solid transparent;line-height:1.45}
aside a.sub{padding-left:26px;font-size:12.8px}
aside a:hover,aside a.active{color:var(--accent);border-left-color:var(--accent)}
main{flex:1;min-width:0;max-width:830px}
.hero{margin-bottom:36px}
.badge{display:inline-block;background:var(--accent-light);color:var(--accent);font-size:11px;text-transform:uppercase;letter-spacing:.08em;font-weight:600;padding:5px 14px;border-radius:999px;margin-bottom:16px}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:38px;letter-spacing:-.025em;line-height:1.2;margin-bottom:12px}
.subtitle{font-size:15px;color:var(--muted)}
section{scroll-margin-top:84px}
h2{font-family:'Playfair Display',serif;font-weight:600;font-size:26px;border-bottom:1px solid var(--border);padding-bottom:10px;margin:14px 0 22px;line-height:1.3}
h3{font-family:'Playfair Display',serif;font-weight:600;font-size:19px;margin:30px 0 12px;line-height:1.35;color:var(--accent)}
.mk{display:inline-block;background:var(--accent-light);color:var(--accent);font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;padding:2px 9px;border-radius:999px;vertical-align:middle;margin-left:6px;letter-spacing:.02em}
.pager a{color:var(--accent);text-decoration:none;font-weight:600}
.pager a:hover{text-decoration:underline}
p{margin:0 0 16px}
ul{margin:0 0 16px;padding-left:22px}
li{margin-bottom:8px}
blockquote{background:var(--accent-light);border-left:3px solid var(--accent);padding:14px 18px;border-radius:0 8px 8px 0;font-family:'Playfair Display',serif;font-style:italic;font-size:16px;margin:18px 0;line-height:1.75}
blockquote p{margin:0}
.callout{background:#fff8e5;border-left:3px solid #d4a12a;padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0 18px;font-size:14.5px}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:10px;box-shadow:0 1px 3px rgba(27,27,27,.05);margin:14px 0 22px;background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:14px}
th{background:var(--accent-light);color:var(--accent);font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;text-align:left;padding:10px 14px}
td{padding:10px 14px;vertical-align:top;border-top:1px solid var(--border)}
td:last-child{white-space:nowrap;font-weight:600;color:var(--accent)}
tbody tr:hover td{background:#f5f3ef}
hr{border:none;height:1px;background:var(--border);margin:38px 0}
footer{text-align:center;padding:34px 20px 42px;color:var(--muted);font-size:13px;border-top:1px solid var(--border)}
.fade-in{animation:fadeUp .6s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
#tocBtn{display:none;position:fixed;bottom:22px;right:22px;width:50px;height:50px;border-radius:50%;background:var(--accent);color:#fff;border:none;font-size:19px;z-index:320;box-shadow:0 4px 14px rgba(26,94,74,.35);cursor:pointer}
@media(max-width:900px){
 .wrap{flex-direction:column;padding:96px 20px 40px}
 aside{position:fixed;left:0;right:0;bottom:0;top:auto;width:100%;max-height:58vh;background:var(--surface);border-top:1px solid var(--border);box-shadow:0 -6px 24px rgba(27,27,27,.12);transform:translateY(102%);transition:transform .3s ease;z-index:310;padding:14px 20px 22px}
 aside.open{transform:none}
 #tocBtn{display:block}
}
@media(max-width:600px){
 h1{font-size:28px} h2{font-size:22px} h3{font-size:17px}
 th,td{font-size:13px;padding:8px 10px}
 .meta{display:none} body{font-size:15px}
}
"""

JS = """
const bar=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.documentElement;bar.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';let cur=null;document.querySelectorAll('aside a').forEach(a=>{const t=document.getElementById(a.getAttribute('href').slice(1));if(t&&t.offsetTop-120<=h.scrollTop)cur=a});document.querySelectorAll('aside a').forEach(a=>a.classList.toggle('active',a===cur));},{passive:true});
const aside=document.querySelector('aside'),btn=document.getElementById('tocBtn');
btn.addEventListener('click',()=>aside.classList.toggle('open'));
aside.addEventListener('click',e=>{if(e.target.tagName==='A')aside.classList.remove('open')});
"""
SPY_TAG = '<script src="../assets/toc-scrollspy.js"></script>'


def page_html(title, subtitle, sections, label, book, prev_link, next_link):
    toc = ['<div class="toc-title">Contents</div>']
    body = []
    n = 0
    nav = []
    if prev_link:
        nav.append(f'<a href="{prev_link[0]}">&larr; {esc(prev_link[1])}</a>')
    if next_link:
        nav.append(f'<a href="{next_link[0]}" style="text-align:right;margin-left:auto">{esc(next_link[1])} &rarr;</a>')
    for sec in sections:
        n += 1
        d = min(0.06 * n, 0.5)
        toc.append(f'<a href="#{sec["id"]}">{clean_label(sec["title"])}</a>')
        parts = [f'<h2 id="{sec["id"]}">{inline(sec["title"])}</h2>']
        for kind, payload in sec["blocks"]:
            if kind == "h3":
                t, sid, marks = payload
                toc.append(f'<a class="sub" href="#{sid}">{clean_label(t)}</a>')
                badge = f' <span class="mk">{inline(marks)}</span>' if marks else ""
                parts.append(f'<h3 id="{sid}">{inline(t)}{badge}</h3>')
            elif kind == "p":
                parts.append(f"<p>{payload}</p>")
            elif kind == "callout":
                parts.append(f'<div class="callout">{payload}</div>')
            elif kind == "html":
                parts.append(payload)
            elif kind == "quote":
                parts.append(f"<blockquote><p>{payload}</p></blockquote>")
            elif kind == "table":
                rows = payload
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body_rows = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                    for r in rows[1:])
                parts.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table></div>')
        body.append(f'<section class="fade-in" style="animation-delay:{d:.2f}s">{"".join(parts)}</section>')
    nav_html = ""
    if nav:
        nav_html = ('<div class="pager" style="display:flex;gap:14px;margin:34px 0 8px;font-size:14px">'
                    + "".join(nav) + "</div>")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__PAGETITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>
<nav class="nav"><a class="logo" href="index.html">English Notes</a><span class="meta">__META__</span></nav>
<div id="progress"></div>
<div class="wrap">
<aside>__TOC__</aside>
<main>
<div class="hero fade-in" style="animation-delay:.05s">
<span class="badge">__BADGE__</span>
<h1>__H1__</h1>
<p class="subtitle">__SUBTITLE__</p>
</div>
__BODY__
__PAGER__
</main>
</div>
<button id="tocBtn" aria-label="Open contents">&#9776;</button>
<footer>Source: NCERT __BOOK__ (Class XI) &middot; English Notes</footer>
<script>__JS__</script>
__SPY__
</body>
</html>"""
    for k, v in {
        "__PAGETITLE__": esc(re.sub(r"^#\s*", "", title)),
        "__CSS__": CSS,
        "__META__": f"Class XI &middot; {book} &middot; {label}",
        "__TOC__": "\n".join(toc),
        "__BADGE__": f"{book} &middot; Class XI &middot; {label}",
        "__H1__": inline(title), "__SUBTITLE__": subtitle, "__BODY__": "\n".join(body),
        "__PAGER__": nav_html,
        "__JS__": JS, "__SPY__": SPY_TAG, "__BOOK__": book,
    }.items():
        html = html.replace(k, v)
    return html


INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>English Notes &middot; Class XI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>
<nav class="nav"><span class="logo">English Notes</span><span class="meta">Class XI &middot; Hornbill &amp; Snapshots</span></nav>
<div class="wrap" style="display:block;max-width:940px">
<div class="hero fade-in" style="animation-delay:.05s">
<span class="badge">NCERT English Core &middot; Class XI</span>
<h1>English Revision Notes</h1>
<p class="subtitle">Summary, keywords, theme and character sketch with full exam answers &mdash; one page per chapter and per poem.</p>
</div>
__GROUPS__
</div>
<footer>Source: NCERT Hornbill &amp; Snapshots (Class XI) &middot; English Notes</footer>
</body>
</html>"""


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    metas = []
    for i, (src, out, label, book) in enumerate(PAGES):
        path = SRC_DIR / src
        if not path.exists():
            print(f"!! MISSING SOURCE: {src}")
            continue
        title, subtitle, sections = parse(path.read_text(encoding="utf-8"))
        prev_link = (PAGES[i - 1][1], PAGES[i - 1][2]) if i > 0 else None
        next_link = (PAGES[i + 1][1], PAGES[i + 1][2]) if i + 1 < len(PAGES) else None
        (ROOT / out).write_text(
            page_html(title, subtitle, sections, label, book, prev_link, next_link),
            encoding="utf-8")
        metas.append((out, label, title, subtitle, book))
        print(f"{out}: {len(sections)} sections")

    groups = []
    for bi, book in enumerate(["Hornbill", "Snapshots"]):
        cards = []
        for out, label, title, subtitle, bk in [m for m in metas if m[4] == book]:
            short = re.sub(r"^(Ch|Poem)\s*\d+\s*[—-]\s*", "", title)
            kind = "Poem" if label.startswith("Poem") else f"{book} &middot; {label}"
            cards.append(
                f'<a class="card fade-in" style="animation-delay:.{min(len(cards) + 1, 9)}s" href="{out}">'
                f'<span class="badge">{kind}</span>'
                f'<h2 style="border:none;margin:10px 0 8px">{inline(short)}</h2>'
                f'<p style="margin:0;color:var(--muted);font-size:13.5px">{subtitle}</p></a>')
        groups.append(f'<h2 style="font-size:20px;margin:{0 if bi == 0 else 34}px 0 14px">{book}</h2>\n'
                      f'<div class="cards">\n' + "\n".join(cards) + "\n</div>")
    idx = INDEX.replace("__CSS__", CSS).replace("__GROUPS__", "\n".join(groups))
    idx = idx.replace(
        "</style>",
        ".cards{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}"
        ".card{display:block;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 24px;text-decoration:none;color:var(--text);box-shadow:0 1px 3px rgba(27,27,27,.05);transition:box-shadow .2s,transform .2s}"
        ".card:hover{box-shadow:0 6px 18px rgba(27,27,27,.09);transform:translateY(-2px)}"
        "h2{font-size:20px}</style>")
    (ROOT / "index.html").write_text(idx, encoding="utf-8")
    print(f"index.html written ({len(metas)} pages)")


if __name__ == "__main__":
    build()
