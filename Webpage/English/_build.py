# ponytail: one-shot md->html builder for the 3 English notes pages (study-docu-web-ui design system)
import re, pathlib

ROOT = pathlib.Path(r"F:\Study OS\Webpage\English")
CHAPTERS = [
    (r"F:\Study OS\English Markdown\Ch 1 - The Portrait of a Lady (Rewritten Notes).md",
     "Chapter-1-The-Portrait-of-a-Lady.html", 1, "Hornbill"),
    (r"F:\Study OS\English Markdown\Ch 2 - We're Not Afraid to Die (Rewritten Notes).md",
     "Chapter-2-Were-Not-Afraid-to-Die.html", 2, "Hornbill"),
    (r"F:\Study OS\English Markdown\Ch 3 - Discovering Tut (Rewritten Notes).md",
     "Chapter-3-Discovering-Tut.html", 3, "Hornbill"),
    (r"F:\Study OS\English Markdown\Ch 1 - The Summer of the Beautiful White Horse (Rewritten Notes).md",
     "Chapter-1-The-Summer-of-the-Beautiful-White-Horse.html", 1, "Snapshots"),
    (r"F:\Study OS\English Markdown\Ch 2 - The Address (Rewritten Notes).md",
     "Chapter-2-The-Address.html", 2, "Snapshots"),
    (r"F:\Study OS\English Markdown\Ch 3 - Mother's Day (Rewritten Notes).md",
     "Chapter-3-Mothers-Day.html", 3, "Snapshots"),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

def slug(t):
    t = t.replace("**", "").replace("*", "")
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def clean_label(t):
    return inline(t.replace("**", "").replace("*", ""))

def parse(md):
    lines = md.splitlines()
    title = lines[0].lstrip("# ").strip()
    subtitle = ""
    sections = []          # {title, id, blocks:[(kind,payload)]}
    pre_blocks = []        # content before the first heading (hero extras)
    cur = None
    para, quote, table = [], [], []
    hr_seen = False
    hook_next = False

    def target():
        return cur["blocks"] if cur else pre_blocks

    def flush_para():
        nonlocal para, hook_next
        if para:
            if all(l.strip().startswith("- ") for l in para):
                items = "".join(f"<li>{inline(l.strip()[2:])}</li>" for l in para)
                target().append(("html", f"<ul>{items}</ul>"))
            else:
                text = "<br>".join(inline(l.strip()) for l in para)
                kind = "callout" if hook_next else "p"
                target().append((kind, text))
            para = []
            hook_next = False

    def flush_quote():
        nonlocal quote
        if quote:
            target().append(("quote", "<br>".join(inline(l.lstrip("> ").strip()) for l in quote)))
            quote = []

    def flush_table():
        nonlocal table
        if table:
            rows = []
            for r in table:
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    continue
                rows.append(cells)
            target().append(("table", rows))
            table = []

    def flush_all():
        flush_para(); flush_quote(); flush_table()

    for raw in lines[1:]:
        line = raw.rstrip()
        s = line.strip()
        if s.startswith("|"):
            flush_para(); flush_quote(); table.append(s); continue
        if s.startswith(">"):
            flush_para(); flush_table(); quote.append(s); continue
        flush_quote(); flush_table()
        if not s:
            flush_para(); continue
        if s == "---":
            flush_para()
            if not hr_seen and len(sections) == 0:
                hr_seen = True
                continue
            cur["blocks"].append(("hr", "")); continue
        if s.startswith("**Contents:**"):
            continue
        if s.startswith("**Author"):
            subtitle = inline(s); continue
        m2 = re.match(r"^###\s+(.*)$", s)
        mh2 = re.match(r"^##\s+(.*)$", s)
        mh1 = re.match(r"^#\s+(.*)$", s)
        if m2 and cur:
            flush_para()
            t = m2.group(1).strip()
            if t.startswith("Last-minute revision hook"):
                hook_next = True
            cur["blocks"].append(("h3", (t, slug(t))))
            continue
        if mh2 or (mh1 and sections):
            flush_all()
            t = (mh2.group(1) if mh2 else mh1.group(1)).strip()
            cur = {"title": t, "id": slug(t), "blocks": []}
            sections.append(cur)
            continue
        if s.startswith("*Best-answer point:*"):
            flush_para()
            target().append(("callout", inline(s)))
            continue
        para.append(s)
    flush_all()
    return title, subtitle, sections, pre_blocks

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
aside{width:260px;flex-shrink:0;position:sticky;top:84px;max-height:calc(100vh - 110px);overflow-y:auto;padding-right:6px}
aside::-webkit-scrollbar{width:4px}
aside::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
aside .toc-title{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding:0 12px 10px;font-weight:600}
aside a{display:block;padding:6px 12px;font-size:13.5px;color:var(--muted);text-decoration:none;border-left:2px solid transparent;line-height:1.45}
aside a.sub{padding-left:26px;font-size:12.8px}
aside a:hover,aside a.active{color:var(--accent);border-left-color:var(--accent)}
main{flex:1;min-width:0;max-width:820px}
.hero{margin-bottom:36px}
.badge{display:inline-block;background:var(--accent-light);color:var(--accent);font-size:11px;text-transform:uppercase;letter-spacing:.08em;font-weight:600;padding:5px 14px;border-radius:999px;margin-bottom:16px}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:38px;letter-spacing:-.025em;line-height:1.2;margin-bottom:12px}
.subtitle{font-size:16px;color:var(--muted)}
section{scroll-margin-top:84px}
h2{font-family:'Playfair Display',serif;font-weight:600;font-size:26px;border-bottom:1px solid var(--border);padding-bottom:10px;margin:14px 0 22px;line-height:1.3}
h3{font-family:'Playfair Display',serif;font-weight:600;font-size:20px;margin:30px 0 12px;line-height:1.35}
p{margin:0 0 16px}
ul{margin:0 0 16px;padding-left:22px}
li{margin-bottom:8px}
blockquote{background:var(--accent-light);border-left:3px solid var(--accent);padding:14px 18px;border-radius:0 8px 8px 0;font-family:'Playfair Display',serif;font-style:italic;font-size:16px;margin:18px 0;line-height:1.65}
blockquote p{margin:0}
.callout{background:#fff8e5;border-left:3px solid #d4a12a;padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0 18px;font-size:14.5px}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:10px;box-shadow:0 1px 3px rgba(27,27,27,.05);margin:18px 0 22px;background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:14px}
th{background:var(--accent-light);color:var(--accent);font-size:13px;text-transform:uppercase;letter-spacing:.04em;text-align:left;padding:10px 14px}
td{padding:10px 14px;vertical-align:top;border-top:1px solid var(--border)}
tbody tr:hover td{background:#f5f3ef}
td:first-child{font-weight:600;white-space:nowrap}
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
 h1{font-size:28px} h2{font-size:22px} h3{font-size:18px}
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

def page_html(ch, title, subtitle, sections, pre_blocks, book):
    toc = ['<div class="toc-title">Contents</div>']
    body = []
    n = 0
    for kind, payload in pre_blocks:
        if kind == "quote":
            body.append(f"<blockquote><p>{payload}</p></blockquote>")
        elif kind == "p":
            body.append(f"<p>{payload}</p>")
        elif kind == "callout":
            body.append(f'<div class="callout">{payload}</div>')
        elif kind == "html":
            body.append(payload)
    for sec in sections:
        n += 1
        d = min(0.06 * n, 0.5)
        toc.append(f'<a href="#{sec["id"]}">{clean_label(sec["title"])}</a>')
        parts = [f'<h2 id="{sec["id"]}">{inline(sec["title"])}</h2>']
        for kind, payload in sec["blocks"]:
            if kind == "h3":
                t, sid = payload
                toc.append(f'<a class="sub" href="#{sid}">{clean_label(t)}</a>')
                parts.append(f'<h3 id="{sid}">{inline(t)}</h3>')
            elif kind == "p":
                parts.append(f"<p>{payload}</p>")
            elif kind == "html":
                parts.append(payload)
            elif kind == "callout":
                parts.append(f'<div class="callout">{payload}</div>')
            elif kind == "quote":
                parts.append(f"<blockquote><p>{payload}</p></blockquote>")
            elif kind == "table":
                rows = payload
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body_rows = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                    for r in rows[1:])
                parts.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table></div>')
            elif kind == "hr":
                parts.append("<hr>")
        body.append(f'<section class="fade-in" style="animation-delay:{d:.2f}s">{"".join(parts)}</section>')
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
</main>
</div>
<button id="tocBtn" aria-label="Open contents">&#9776;</button>
<footer>__FOOT__</footer>
<script>__JS__</script>
</body>
</html>"""
    for k, v in {
        "__PAGETITLE__": esc(title), "__CSS__": CSS,
        "__META__": f"Class XI &middot; {book} &middot; Chapter {ch}",
        "__TOC__": "\n".join(toc),
        "__BADGE__": f"{book} &middot; Class XI &middot; Chapter {ch}",
        "__H1__": inline(title), "__SUBTITLE__": subtitle, "__BODY__": "\n".join(body), "__JS__": JS,
        "__FOOT__": f"Source: NCERT {book} (Class XI) chapter notes &middot; English Notes",
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
<div class="wrap" style="display:block;max-width:900px">
<div class="hero fade-in" style="animation-delay:.05s">
<span class="badge">NCERT English Core &middot; Class XI</span>
<h1>English Chapter Notes</h1>
<p class="subtitle">Rewritten study notes from the chapter PDFs &mdash; summaries, exam answers, vocabulary and themes.</p>
</div>
__GROUPS__
</div>
<footer>Source: NCERT Hornbill &amp; Snapshots (Class XI) chapter notes &middot; English Notes</footer>
</body>
</html>"""

def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    metas = []
    for src, out, ch, book in CHAPTERS:
        title, subtitle, sections, pre_blocks = parse(pathlib.Path(src).read_text(encoding="utf-8"))
        (ROOT / out).write_text(page_html(ch, title, subtitle, sections, pre_blocks, book), encoding="utf-8")
        metas.append((out, ch, title, subtitle, book))
        print(f"{out}: {len(sections)} sections")
    groups = []
    for bi, book in enumerate(["Hornbill", "Snapshots"]):
        cards = []
        for out, ch, title, subtitle, bk in [m for m in metas if m[4] == book]:
            short = re.sub(r"^Ch\s*\d+\s*[—-]\s*", "", title)
            cards.append(
                f'<a class="card fade-in" style="animation-delay:.{len(cards)+1}s" href="{out}">'
                f'<span class="badge">Chapter {ch}</span>'
                f'<h2 style="border:none;margin:10px 0 8px">{inline(short)}</h2>'
                f'<p style="margin:0;color:var(--muted);font-size:14px">{subtitle}</p></a>')
        groups.append(f'<h2 style="font-size:20px;margin:{0 if bi == 0 else 30}px 0 14px">{book}</h2>\n'
                      f'<div class="cards">\n' + "\n".join(cards) + "\n</div>")
    idx = INDEX.replace("__CSS__", CSS).replace("__GROUPS__", "\n".join(groups))
    idx = idx.replace("</style>", ".cards{display:grid;gap:18px}.card{display:block;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 24px;text-decoration:none;color:var(--text);box-shadow:0 1px 3px rgba(27,27,27,.05);transition:box-shadow .2s}.card:hover{box-shadow:0 6px 18px rgba(27,27,27,.09)}h2{font-size:23px}</style>")
    (ROOT / "index.html").write_text(idx, encoding="utf-8")
    print("index.html written")

build()
