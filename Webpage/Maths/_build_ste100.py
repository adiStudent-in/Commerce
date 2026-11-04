#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_ste100.py — one-shot md -> html builder for the STE100 revision page.

Reads:  F:\\Study OS\\Maths Markdown\\Chapter <n> - <Title> (STE100 Revision Notes).md
Shell:  F:\\Study OS\\Webpage\\Maths\\Chapter-<n>-<slug>.html  (head styles, nav,
        mobile-TOC script, scrollspy script, KaTeX renderer are reused VERBATIM)
Writes: F:\\Study OS\\Webpage\\Maths\\Chapter-<n>-<slug>-STE100.html

Usage:  python _build_ste100.py seq     (default) -> Chapter 8 Sequences and Series
        python _build_ste100.py binom             -> Chapter 7 Binomial Theorem
        python _build_ste100.py lines             -> Chapter 9 Straight Lines

Formulas are authored as LaTeX in data-tex attributes and rendered with KaTeX;
the Unicode text inside each .tex element is the offline fallback.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(r"F:\Study OS")
MD = ROOT / "Maths Markdown" / "Chapter 8 - Sequences and Series (STE100 Revision Notes).md"
DONOR = ROOT / "Webpage" / "Maths" / "Chapter-8-Sequences-and-Series.html"
OUT = ROOT / "Webpage" / "Maths" / "Chapter-8-Sequences-and-Series-STE100.html"

PAGE_TITLE = "Chapter 8 \u2014 Sequences and Series (Revision Notes) | Maths Class 11"
META_DESC = ("Class 11 Maths Chapter 8 Sequences and Series \u2014 STE100 easy revision "
             "notes: plain-English GP formulas, formula wall, common traps and 42 solved "
             "practice questions for CBSE 2026-27.")
NAV_META = "Class 11 \u00b7 Chapter 8 \u00b7 Revision"
BADGE = "Chapter 8 \u00b7 STE100 Revision Notes"
H1 = "Sequences and Series"
SUBTITLE = "Class 11 Mathematics \u2014 Easy Revision Notes (STE100) \u00b7 CBSE 2026-27"
CHAPTER_ID = "maths-8-ste"

# (number, anchor id, sidebar label, emoji)
SECTIONS = [
    (1,  "syllabus",      "Syllabus Check",              "\U0001F5FA\uFE0F"),
    (2,  "key-words",     "Key Words",                   "\U0001F4D6"),
    (3,  "sequence",      "Sequence",                    "\U0001F522"),
    (4,  "series",        "Series & \u03a3 Notation",    "\u2795"),
    (5,  "gp",            "GP \u2014 General Term",      "\u2716\uFE0F"),
    (6,  "gp-sum",        "GP \u2014 Sum of n Terms",    "\U0001F9EE"),
    (7,  "infinite-gp",   "Infinite GP",                 "\u267E\uFE0F"),
    (8,  "gm",            "Geometric Mean",              "\U0001F4D0"),
    (9,  "am-gm",         "A.M., G.M. & A \u2265 G",     "\u2696\uFE0F"),
    (10, "formula-wall",  "Formula Wall",                "\u26A1"),
    (11, "traps",         "Common Traps",                "\U0001FAA4"),
    (12, "exam-types",    "Exam Question Types",         "\U0001F3AF"),
    (13, "practice",      "Practice Bank \u2014 42 Qs",  "\U0001F4AA"),
    (14, "writing-tips",  "Exam Writing Tips",           "\u270D\uFE0F"),
    (15, "recap",         "One-Page Recap",              "\U0001F504"),
    (16, "appendix",      "Appendix A \u2014 Deleted Topics", "\U0001F4E6"),
]

EXTRA_CSS = """  <style>
    /* \u2500\u2500\u2500 STE100 revision page additions (additive \u2014 shell untouched) \u2500\u2500\u2500 */
    .cb { color: var(--accent); font-weight: 700; margin-right: 6px; }
    blockquote .tex-block { margin: 4px 0; }
  </style>
"""

MINDMAP_MD = """# Sequences and Series \u2014 Easy Revision (STE100)

## Syllabus (CBSE 2026-27)
- In syllabus: sequence, series, \u03a3 notation, GP term + sum, infinite GP, G.M., A.M., A \u2265 G
- Formative only: special sums \u03a3k, \u03a3k\u00b2, \u03a3k\u00b3
- Deleted 2023: full AP theory

## Sequence
- Ordered list a1, a2, ..., an; order matters
- Three ways: formula for an, recurrence (Fibonacci), words (primes)
- Finite (stops) vs infinite (never stops)
- Sequence = function on N

## Series and \u03a3
- Series = terms joined by + signs (indicated sum)
- Sum of series = the number Sn
- an = Sn \u2212 S(n\u22121); a1 = S1

## GP \u2014 general term
- Multiply by fixed r (\u2260 0) every step; an = a\u00b7r^(n\u22121)
- Ratio test: equal consecutive ratios
- Two terms known: divide bigger equation by smaller
- Which term = value? match powers of the same base

## GP \u2014 sum of n terms
- Sn = a(1\u2212r\u207f)/(1\u2212r) = a(r\u207f\u22121)/(r\u22121) for r \u2260 1
- r = 1: Sn = n\u00b7a (never divide by zero)
- Last term form: Sn = (a \u2212 lr)/(1\u2212r)

## Infinite GP
- Check |r| < 1 FIRST; S\u221e = a/(1\u2212r)
- Repeating decimal \u2192 split into infinite GP
- |r| \u2265 1: no sum to infinity

## Geometric Mean
- a, G, b in GP: G = +\u221a(ab) for positive a, b
- Insert n G.M.s: r = (b/a)^(1/(n+1))
- Product of inserted G.M.s = (ab)^(n/2)

## A.M. and A \u2265 G
- A = (a+b)/2; proof A \u2212 G = (\u221aa \u2212 \u221ab)\u00b2/2 \u2265 0
- Needs positive numbers; equality iff a = b
- Min-value and max-product questions

## Traps
- Series \u2260 sum; r \u2260 0; power is n\u22121
- Never use fraction sum formula at r = 1
- Infinite sum only when |r| < 1
- G.M. in textbook is the positive root
"""

# ---------------------------------------------------------------- chapter selection
# Usage:  python _build_ste100.py seq    (default) -> Chapter 8 STE100 page
#         python _build_ste100.py binom            -> Chapter 7 STE100 page

FOOTER = ("Source: NCERT Class XI Mathematics (Rationalised), Chapter 8 \u00b7 "
          "CBSE 2026-27 syllabus (041) \u00b7 Easy-language revision notes (STE100 style)")

BINOM_MD = ROOT / "Maths Markdown" / "Chapter 7 - Binomial Theorem (STE100 Revision Notes).md"
BINOM_OUT = ROOT / "Webpage" / "Maths" / "Chapter-7-Binomial-Theorem-STE100.html"

# (number, anchor id, sidebar label, emoji)
BINOM_SECTIONS = [
    (1,  "syllabus",       "Syllabus Check",                   "\U0001F5FA\uFE0F"),
    (2,  "key-words",      "Key Words",                        "\U0001F4D6"),
    (3,  "theorem",        "The Binomial Theorem",             "\U0001F511"),
    (4,  "proof",          "Why It Works \u2014 The Proof",    "\U0001F3D7\uFE0F"),
    (5,  "pascal",         "Pascal's Triangle",                "\U0001F53A"),
    (6,  "coefficients",   "Binomial Coefficients",            "\U0001F3B2"),
    (7,  "expansions",     "Writing Expansions",               "\U0001F9E9"),
    (8,  "applications",   "Simple Applications",              "\u2699\uFE0F"),
    (9,  "general-middle", "General & Middle Term",            "\U0001F4DD"),
    (10, "formula-wall",   "Formula Wall",                     "\u26A1"),
    (11, "traps",          "Common Traps",                     "\U0001FAA4"),
    (12, "exam-types",     "Exam Question Types",              "\U0001F3AF"),
    (13, "practice",       "Practice Bank \u2014 42 Qs",       "\U0001F4AA"),
    (14, "writing-tips",   "Exam Writing Tips",                "\u270D\uFE0F"),
    (15, "recap",          "One-Page Recap",                   "\U0001F504"),
    (16, "appendix",       "Appendix A \u2014 Reference Only", "\U0001F4E6"),
]

BINOM_MINDMAP_MD = """# Binomial Theorem \u2014 Easy Revision (STE100)

## Syllabus (CBSE 2026-27)
- In syllabus: historical perspective, theorem + proof, Pascal's triangle, simple applications
- Formative only: general and middle term in binomial expansion
- Not in syllabus: approximation, negative or fractional index

## The theorem
- (a+b)^n = nC0 a^n + nC1 a^(n\u22121) b + \u2026 + nCn b^n for every positive integer n
- n + 1 terms; powers of a fall n to 0; powers of b rise 0 to n
- power of a + power of b = n in every term

## Proof by induction
- Base: n = 1 gives a + b on both sides
- Step: assume for n, multiply by (a+b), combine with Pascal's rule nCr + nC(r\u22121) = (n+1)Cr

## Pascal's triangle
- Row n gives the coefficients of (a+b)^n (n = 0, 1, 2, \u2026)
- Each number = sum of the two above
- Row n has n + 1 numbers; rows start and end with 1; rows are symmetric

## Coefficient toolbox
- nC0 = nCn = 1; nC1 = n; nCr = nC(n\u2212r)
- C0 + C1 + \u2026 + Cn = 2^n
- C0 + C2 + \u2026 = C1 + C3 + \u2026 = 2^(n\u22121)
- C0 \u2212 C1 + C2 \u2212 \u2026 = 0 for n \u2265 1

## Simple applications
- Big powers: write 99 = 100 \u2212 1, expand, add carefully
- Which is larger: expand two or three terms and compare
- Divisibility: 9^(n+1) \u2212 8n \u2212 9 = 64 \u00d7 integer
- Identities: put a = b = 1, or b = \u22121, or b = 3

## General and middle term (formative)
- T(r+1) = nCr a^(n\u2212r) b^r \u2014 b^r tells the position
- n even: one middle term, position n/2 + 1
- n odd: two middle terms
- Independent term: set the power of x to 0

## Traps
- Number of terms is n + 1, not n
- (a \u2212 b)^n: odd power of b \u2192 minus sign
- nC0 = 1, never 0
- 2^n only when a = b = 1
- Term carries powers; coefficient is only the number
"""

# ---------------------------------------------------------------- Chapter 9 constants

LINES_MD = ROOT / "Maths Markdown" / "Chapter 9 - Straight Lines (STE100 Revision Notes).md"
LINES_OUT = ROOT / "Webpage" / "Maths" / "Chapter-9-Straight-Lines-STE100.html"

# (number, anchor id, sidebar label, emoji)
LINES_SECTIONS = [
    (1,  "syllabus",        "Syllabus Check",                 "\U0001F5FA\ufe0f"),
    (2,  "key-words",       "Key Words",                      "\U0001F4D6"),
    (3,  "recall",          "Recall \u2014 Four Formulas",    "\U0001F9F1"),
    (4,  "slope",           "Slope of a Line",                "\U0001F4C8"),
    (5,  "parallel",        "Parallel & Perpendicular",       "\u2702\ufe0f"),
    (6,  "angle",           "Angle Between Two Lines",        "\U0001F4D0"),
    (7,  "collinear",       "Collinearity",                   "\U0001F4CF"),
    (8,  "forms",           "Forms of a Line Equation",       "\U0001F9E9"),
    (9,  "distance-point",  "Distance of a Point",            "\U0001F4E2"),
    (10, "distance-parallel","Distance Between Parallel Lines","\u2194\ufe0f"),
    (11, "formula-wall",    "Formula Wall",                   "\u26a1"),
    (12, "traps",           "Common Traps",                   "\U0001FAA4"),
    (13, "exam-types",      "Exam Question Types",            "\U0001F3AF"),
    (14, "practice",        "Practice Bank \u2014 77 Qs",     "\U0001F4AA"),
    (15, "writing-tips",    "Exam Writing Tips",              "\u270d\ufe0f"),
    (16, "recap",           "One-Page Recap",                 "\U0001F504"),
    (17, "appendix",        "Appendix A \u2014 Beyond Board", "\U0001F4E6"),
]

LINES_MINDMAP_MD = """# Straight Lines \u2014 Easy Revision (STE100)

## Syllabus (CBSE 2026-27)
- In syllabus: slope, angle between lines, six forms of the line equation, distance of a point from a line
- Formative only: normal form, general equation of a line
- Not in syllabus: shifting of origin, family of lines, image of a point

## Slope
- Inclination \u03b8: angle with +x-axis, anticlockwise, 0\u00b0 \u2264 \u03b8 \u2264 180\u00b0
- Slope m = tan \u03b8, not defined at \u03b8 = 90\u00b0
- From two points: m = (y2 \u2212 y1)/(x2 \u2212 x1), x1 \u2260 x2
- Horizontal \u2192 m = 0; vertical \u2192 m not defined

## Two lines
- Parallel: m1 = m2
- Perpendicular: m1 m2 = \u22121 (negative reciprocals)
- Acute angle: tan \u03b8 = |(m2 \u2212 m1)/(1 + m1 m2)|, 1 + m1 m2 \u2260 0
- Collinear: slope AB = slope BC

## Forms of a line
- Parallel to x-axis: y = a; parallel to y-axis: x = b
- Point-slope: y \u2212 y0 = m(x \u2212 x0)
- Two-point: y \u2212 y1 = ((y2\u2212y1)/(x2\u2212x1))(x \u2212 x1)
- Slope-intercept: y = mx + c; with x-intercept d: y = m(x \u2212 d)
- Intercept form: x/a + y/b = 1
- Normal form (formative): x cos\u03c9 + y sin\u03c9 = p

## Distance
- Point to line: d = |Ax1 + By1 + C| / \u221a(A\u00b2 + B\u00b2)
- Parallel lines: d = |C1 \u2212 C2| / \u221a(A\u00b2 + B\u00b2), after equalising A and B
- Slope form: d = |c1 \u2212 c2| / \u221a(1 + m\u00b2)

## Traps
- Vertical line: slope is NOT DEFINED, never \u221e
- Perpendicular is the NEGATIVE RECIPROCAL, not just the negative
- Distance denominator uses only A and B, never C
- Rearrange to Ax + By + C = 0 before finding a distance
- Equalise A and B before subtracting constants
- An angle question usually has TWO answers (the absolute value opens two cases)
"""

def select_chapter(key):
    """Re-bind the module-level chapter constants for the requested build."""
    global MD, OUT, PAGE_TITLE, META_DESC, NAV_META, BADGE, H1, SUBTITLE, CHAPTER_ID
    global SECTIONS, MINDMAP_MD, FOOTER
    if key == "seq":
        return
    if key == "binom":
        MD = BINOM_MD
        OUT = BINOM_OUT
        PAGE_TITLE = "Chapter 7 \u2014 Binomial Theorem (Revision Notes) | Maths Class 11"
        META_DESC = ("Class 11 Maths Chapter 7 Binomial Theorem \u2014 STE100 easy revision "
                     "notes: plain-English theorem, Pascal's triangle, formula wall, common "
                     "traps and 42 solved practice questions for CBSE 2026-27.")
        NAV_META = "Class 11 \u00b7 Chapter 7 \u00b7 Revision"
        BADGE = "Chapter 7 \u00b7 STE100 Revision Notes"
        H1 = "Binomial Theorem"
        SUBTITLE = "Class 11 Mathematics \u2014 Easy Revision Notes (STE100) \u00b7 CBSE 2026-27"
        CHAPTER_ID = "maths-7-ste"
        SECTIONS = BINOM_SECTIONS
        MINDMAP_MD = BINOM_MINDMAP_MD
        FOOTER = ("Source: NCERT Class XI Mathematics (Rationalised), Chapter 7 \u00b7 "
                  "CBSE 2026-27 syllabus (041) \u00b7 Easy-language revision notes (STE100 style)")
        return
    if key == "lines":
        MD = LINES_MD
        OUT = LINES_OUT
        PAGE_TITLE = "Chapter 9 \u2014 Straight Lines (Revision Notes) | Maths Class 11"
        META_DESC = ("Class 11 Maths Chapter 9 Straight Lines \u2014 STE100 easy revision "
                     "notes: slope, angle between lines, the six forms of a line equation, "
                     "distance formulas, formula wall, traps and 77 solved questions for "
                     "CBSE 2026-27.")
        NAV_META = "Class 11 \u00b7 Chapter 9 \u00b7 Revision"
        BADGE = "Chapter 9 \u00b7 STE100 Revision Notes"
        H1 = "Straight Lines"
        SUBTITLE = "Class 11 Mathematics \u2014 Easy Revision Notes (STE100) \u00b7 CBSE 2026-27"
        CHAPTER_ID = "maths-9-ste"
        SECTIONS = LINES_SECTIONS
        MINDMAP_MD = LINES_MINDMAP_MD
        FOOTER = ("Source: NCERT Class XI Mathematics (Rationalised), Chapter 9 \u00b7 "
                  "CBSE 2026-27 syllabus (041) \u00b7 Easy-language revision notes (STE100 style)")
        return
    raise SystemExit("unknown chapter %r (use: seq | binom | lines)" % key)

# ---------------------------------------------------------------- LaTeX -> Unicode fallback

TOKEN_REPL = [
    (r"\left\lvert", "|"), (r"\right\rvert", "|"),
    (r"\left", ""), (r"\right", ""),
    (r"\big", ""), (r"\Big", ""), (r"\bigg", ""),
    (r"\displaystyle", ""),
    (r"\emptyset", "\u2205"),
    (r"\Sigma", "\u03a3"), (r"\sum", "\u03a3"), (r"\infty", "\u221e"),
    (r"\times", "\u00d7"), (r"\cdot", "\u00b7"), (r"\div", "\u00f7"),
    (r"\dots", "\u2026"), (r"\ldots", "\u2026"),
    (r"\geq", "\u2265"), (r"\ge", "\u2265"),
    (r"\leq", "\u2264"), (r"\le", "\u2264"),
    (r"\neq", "\u2260"), (r"\ne", "\u2260"), (r"\pm", "\u00b1"), (r"\approx", "\u2248"),
    (r"\Rightarrow", "\u21d2"), (r"\implies", "\u2192"), (r"\iff", "\u21d4"),
    (r"\Leftrightarrow", "\u21d4"), (r"\leftrightarrow", "\u2194"),
    (r"\therefore", "\u2234"), (r"\because", "\u2235"),
    (r"\parallel", "\u2225"), (r"\nparallel", "\u2226"),
    (r"\perp", "\u22a5"), (r"\triangle", "\u25b3"),
    (r"\circ", "\u00b0"), (r"\angle", "\u2220"), (r"\degree", "\u00b0"),
    (r"\theta", "\u03b8"), (r"\varphi", "\u03c6"), (r"\phi", "\u03d5"),
    (r"\alpha", "\u03b1"), (r"\beta", "\u03b2"), (r"\gamma", "\u03b3"),
    (r"\delta", "\u03b4"), (r"\lambda", "\u03bb"), (r"\mu", "\u03bc"),
    (r"\pi", "\u03c0"), (r"\omega", "\u03c9"), (r"\Omega", "\u03a9"),
    (r"\sec", "sec"), (r"\csc", "cosec"), (r"\cot", "cot"),
    (r"\sin", "sin"), (r"\cos", "cos"), (r"\tan", "tan"),
    (r"\log", "log"), (r"\ln", "ln"),
    (r"\lvert", "|"), (r"\rvert", "|"),
    (r"\blacksquare", "\u220e"), (r"\square", "\u25a1"),
    (r"\qquad", " "), (r"\quad", " "),
    (r"\,", " "), (r"\;", " "), (r"\!", ""), (r"\ ", " "),
]


def read_group(s, i):
    """s[i] must be '{'. Return (content_without_braces, next_index)."""
    assert s[i] == "{", "read_group expects { at %d: %r" % (i, s[max(0, i - 20):i + 20])
    depth = 1
    j = i + 1
    start = j
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[start:j], j + 1
        j += 1
    raise ValueError("unbalanced braces: " + s)


def _replace_frac(s, cmd):
    out = []
    i = 0
    while True:
        k = s.find(cmd, i)
        if k == -1:
            out.append(s[i:])
            break
        out.append(s[i:k])
        j = k + len(cmd)
        while j < len(s) and s[j] == " ":
            j += 1
        if j < len(s) and s[j] == "{":
            num, j = read_group(s, j)
            while j < len(s) and s[j] == " ":
                j += 1
            if j < len(s) and s[j] == "{":
                den, j = read_group(s, j)
                out.append("(" + _replace_frac(num, cmd) + ")/(" + _replace_frac(den, cmd) + ")")
                i = j
                continue
        out.append(cmd)
        i = k + len(cmd)
    return "".join(out)


def _replace_sqrt(s):
    out = []
    i = 0
    while True:
        k = s.find(r"\sqrt", i)
        if k == -1:
            out.append(s[i:])
            break
        out.append(s[i:k])
        j = k + 5
        if j < len(s) and s[j] == "{":
            g, j = read_group(s, j)
            out.append("\u221a(" + _replace_sqrt(g) + ")")
        elif j < len(s):
            out.append("\u221a" + s[j])
            j += 1
        else:
            out.append("\u221a")
        i = j
    return "".join(out)


def _replace_overline(s):
    out = []
    i = 0
    while True:
        k = s.find(r"\overline", i)
        if k == -1:
            out.append(s[i:])
            break
        out.append(s[i:k])
        j = k + 9
        if j < len(s) and s[j] == "{":
            g, j = read_group(s, j)
            out.append(_replace_overline(g) + "\u0304")  # combining macron
        i = j
    return "".join(out)


def _replace_groupcmd(s, cmd, transform):
    """Replace cmd{...} with transform(content)."""
    out = []
    i = 0
    while True:
        k = s.find(cmd, i)
        if k == -1:
            out.append(s[i:])
            break
        out.append(s[i:k])
        j = k + len(cmd)
        if j < len(s) and s[j] == "{":
            g, j = read_group(s, j)
            out.append(transform(g))
        i = j
    return "".join(out)


def _replace_supsub(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in "^_":
            tag = "sup" if c == "^" else "sub"
            j = i + 1
            if j < len(s) and s[j] == "{":
                g, j = read_group(s, j)
                g = _replace_supsub(g)
            elif j < len(s):
                g = s[j]
                j += 1
            else:
                out.append(c)
                i += 1
                continue
            out.append("<%s>%s</%s>" % (tag, g, tag))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def latex_to_fallback(tex):
    t = tex
    t = t.replace("\x01", "").replace("\x02", "")  # safety strip
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = t.replace("{}", "")  # empty group, as in {}^nC_r
    t = _replace_frac(t, r"\dfrac")
    t = _replace_frac(t, r"\frac")
    t = _replace_frac(t, r"\tfrac")
    t = _replace_sqrt(t)
    t = _replace_overline(t)
    t = _replace_groupcmd(t, r"\mathbb", lambda g: g)
    t = _replace_groupcmd(t, r"\text", lambda g: g)
    # protect escaped braces
    t = t.replace(r"\{", "\x01").replace(r"\}", "\x02")
    for a, b in TOKEN_REPL:
        t = t.replace(a, b)
    t = _replace_supsub(t)
    t = t.replace("\x01", "{").replace("\x02", "}")
    t = t.replace("-", "\u2212")
    t = re.sub(r"<(sup|sub)>\s+", r"<\1>", t)
    t = re.sub(r"\s+</(sup|sub)>", r"</\1>", t)
    t = re.sub(r"[ \t]{2,}", " ", t).strip()
    return t


def esc_attr(t):
    return (t.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- markdown -> html

MATH_INLINE_RE = re.compile(r"\$([^$]+?)\$")
RE_CHECK = re.compile(r"^(\s*)-\s+\[ \]\s+(.*)$")
RE_BULLET = re.compile(r"^(\s*)[-*]\s+(.*)$")
RE_ORDERED = re.compile(r"^(\s*)\d+\.\s+(.*)$")


def inline(s):
    maths = []

    def stash(m):
        maths.append(m.group(1))
        return "\x03%d\x03" % (len(maths) - 1)

    s = MATH_INLINE_RE.sub(stash, s)
    # escape stray ampersands (leave entities like &gt; &nbsp; alone)
    s = re.sub(r"&(?!(?:amp|lt|gt|quot|nbsp|hellip|mdash|ndash|#\d+|#x[0-9A-Fa-f]+);)", "&amp;", s)
    # escape stray '<' that cannot start a tag
    s = re.sub(r"<(?![A-Za-z/])", "&lt;", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)

    def restore(m):
        raw = maths[int(m.group(1))]
        return ('<span class="tex" data-tex="%s">%s</span>'
                % (esc_attr(raw), latex_to_fallback(raw)))

    return re.sub("\x03(\\d+)\x03", restore, s)


def display_math(raw):
    return ('<div class="tex tex-block" data-tex="%s">%s</div>'
            % (esc_attr(raw.strip()), latex_to_fallback(raw.strip())))


def split_pipe(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_list_line(s):
    return bool(RE_CHECK.match(s) or RE_BULLET.match(s) or RE_ORDERED.match(s))


def convert_blockquote(lines, i):
    parts = []
    n = len(lines)
    while i < n and lines[i].strip().startswith(">"):
        raw = lines[i].strip()[1:].strip()
        if raw == "":
            parts.append("")
            i += 1
            continue
        m = re.match(r"^\$\$(.+)\$\$$", raw)
        if m:
            parts.append(display_math(m.group(1)))
        else:
            parts.append(inline(raw))
        i += 1
    return "<blockquote>" + "<br>".join(parts) + "</blockquote>", i


def convert_table(lines, i):
    rows = []
    n = len(lines)
    while i < n and lines[i].strip().startswith("|"):
        rows.append(split_pipe(lines[i]))
        i += 1

    def is_sep(cells):
        return all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != "")

    header = rows[0]
    body = [r for r in rows[1:] if not is_sep(r)]
    out = ['<div class="table-wrap">', "<table>", "<thead><tr>"]
    for c in header:
        out.append("<th>%s</th>" % inline(c))
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>")
        for c in r:
            out.append("<td>%s</td>" % inline(c))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out), i


def convert_list(lines, i):
    items = []  # (level, kind, text)
    n = len(lines)
    while i < n:
        s = lines[i]
        m = RE_CHECK.match(s)
        if m:
            items.append((len(m.group(1)) // 2 + 1, "check", m.group(2)))
            i += 1
            continue
        m = RE_BULLET.match(s)
        if m:
            items.append((len(m.group(1)) // 2 + 1, "ul", m.group(2)))
            i += 1
            continue
        m = RE_ORDERED.match(s)
        if m:
            items.append((len(m.group(1)) // 2 + 1, "ol", m.group(2)))
            i += 1
            continue
        break

    def build(pos, level):
        tag = "ol" if items[pos][1] == "ol" else "ul"
        out = ["<%s>" % tag]
        while pos < len(items):
            lv, kind, text = items[pos]
            if lv < level:
                break
            pos += 1
            sub = ""
            if pos < len(items) and items[pos][0] > level:
                sub, pos = build(pos, items[pos][0])
            if kind == "check":
                prefix = '<span class="cb">\u2610</span> '
            else:
                prefix = ""
            out.append("<li>%s%s%s</li>" % (prefix, inline(text), sub))
        out.append("</%s>" % tag)
        return "".join(out), pos

    html, _ = build(0, items[0][0])
    return html, i


def convert_details(lines, i):
    i += 1  # skip <details>
    while lines[i].strip() == "":
        i += 1
    s = lines[i].strip()
    if not (s.startswith("<summary>") and s.endswith("</summary>")):
        raise ValueError("expected <summary> right after <details>: " + s)
    summary = s[len("<summary>"):-len("</summary>")]
    i += 1
    inner = []
    while i < len(lines) and lines[i].strip() != "</details>":
        inner.append(lines[i])
        i += 1
    if i >= len(lines):
        raise ValueError("unclosed <details> block")
    i += 1  # skip </details>
    inner_html = convert_blocks(inner)
    return ('<details class="qa"><summary>%s</summary><div class="sol">\n%s\n</div></details>'
            % (inline(summary.strip()), inner_html)), i


def convert_blocks(lines):
    out = []
    i = 0
    n = len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith("<details"):
            block, i = convert_details(lines, i)
            out.append(block)
            continue
        if stripped.startswith(("<summary", "</details")):
            i += 1
            continue
        if stripped.startswith("#### "):
            out.append("<h4>%s</h4>" % inline(stripped[5:]))
            i += 1
            continue
        if stripped.startswith("### "):
            out.append("<h3>%s</h3>" % inline(stripped[4:]))
            i += 1
            continue
        if stripped.startswith("## "):
            i += 1
            continue
        m = re.match(r"^\$\$(.+)\$\$$", stripped)
        if m:
            out.append(display_math(m.group(1)))
            i += 1
            continue
        if stripped.startswith(">"):
            block, i = convert_blockquote(lines, i)
            out.append(block)
            continue
        if stripped.startswith("|"):
            block, i = convert_table(lines, i)
            out.append(block)
            continue
        if is_list_line(lines[i]):
            block, i = convert_list(lines, i)
            out.append(block)
            continue
        # paragraph (join consecutive plain lines)
        para = [stripped]
        i += 1
        while i < n:
            l2 = lines[i].strip()
            if (not l2 or l2 == "---" or l2.startswith(("## ", "### ", "#### ", "<details", "<summary", "</details", "$$", ">", "|")) or is_list_line(lines[i])):
                break
            para.append(l2)
            i += 1
        out.append("<p>%s</p>" % " ".join(inline(x) for x in para))
    return "\n".join(out)


# ---------------------------------------------------------------- plain text (for JSON data)

SUB_TRANS = str.maketrans({
    "0": "\u2080", "1": "\u2081", "2": "\u2082", "3": "\u2083", "4": "\u2084",
    "5": "\u2085", "6": "\u2086", "7": "\u2087", "8": "\u2088", "9": "\u2089",
    "+": "\u208a", "-": "\u208b", "\u2212": "\u208b", "=": "\u208c",
    "(": "\u208d", ")": "\u208e", "n": "\u2099", "k": "\u2096", "i": "\u1d62",
})
SUP_TRANS = str.maketrans({
    "0": "\u2070", "1": "\u00b9", "2": "\u00b2", "3": "\u00b3", "4": "\u2074",
    "5": "\u2075", "6": "\u2076", "7": "\u2077", "8": "\u2078", "9": "\u2079",
    "+": "\u207a", "-": "\u207b", "\u2212": "\u207b", "=": "\u207c",
    "(": "\u207d", ")": "\u207e", "n": "\u207f",
})


def plain_text(s):
    s = re.sub(r"\$([^$]+?)\$", lambda m: latex_to_fallback(m.group(1)), s)
    s = s.replace("**", "").replace("*", "")
    s = re.sub(r"<sub>(.*?)</sub>", lambda m: m.group(1).translate(SUB_TRANS), s)
    s = re.sub(r"<sup>(.*?)</sup>", lambda m: m.group(1).translate(SUP_TRANS), s)
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&lt;", "<").replace("&gt;", ">")
          .replace("&amp;", "&").replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- page assembly

def main():
    md_raw = MD.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = md_raw.split("\n")
    donor_raw = DONOR.read_bytes().decode("utf-8")
    crlf = "\r\n" in donor_raw
    donor = donor_raw.replace("\r\n", "\n")

    # ---------- split md: top matter + sections
    first = next(i for i, l in enumerate(lines) if l.startswith("## "))
    top, body = lines[:first], lines[first:]
    if not top[0].startswith("# "):
        raise SystemExit("md must start with an '# ' title")
    if not top[2].startswith("### "):
        raise SystemExit("md line 3 should carry the subtitle '### ...'")

    top_kept = []
    for l in top[3:]:
        s = l.strip()
        if not s or s == "**Contents**":
            continue
        if re.match(r"^\d+\.\s+\[.+\]\(#.+\)$", s):
            continue  # drop the old-numbered contents list (sidebar replaces it)
        top_kept.append(l)
    intro_html = convert_blocks(top_kept)

    sections = []  # (num, heading_text, content_lines)
    cur = None
    for l in body:
        m = re.match(r"^##\s+(\d+)\.\s+(.+)$", l)
        if m:
            cur = [int(m.group(1)), m.group(2).strip(), []]
            sections.append(cur)
        else:
            if cur is None:
                if l.strip():
                    raise SystemExit("content before the first '## ' heading: " + l)
            else:
                cur[2].append(l)

    nums = [s[0] for s in sections]
    expected = [s[0] for s in SECTIONS]
    if nums != expected:
        raise SystemExit("section numbers %s != expected %s" % (nums, expected))

    sec_lines = {s[0]: s[2] for s in sections}
    sid_map = {s[0]: s[1] for s in SECTIONS}
    emoji_map = {s[0]: s[3] for s in SECTIONS}

    # ---------- build body
    body_parts = [intro_html]
    for num, text, content in sections:
        content_html = convert_blocks(content)
        body_parts.append(
            '      <section id="%s" class="fade-in">\n'
            '        <h2>%d. %s %s</h2>\n%s\n'
            "      </section>" % (sid_map[num], num, emoji_map[num], inline(text), content_html))
    body_html = "\n\n".join(body_parts)

    # ---------- key terms for the data script
    term_rows = [l for l in sec_lines[2] if l.strip().startswith("|")]
    terms = []
    for row in term_rows[2:]:
        cells = split_pipe(row)
        if len(cells) >= 2 and cells[0]:
            terms.append({"term": plain_text(cells[0]), "definition": plain_text(cells[1])})

    # ---------- shell from donor
    i_nav = donor.index("<!-- Nav -->")
    i_layout = donor.index("<!-- Layout -->")
    i_aside = donor.index('<aside class="toc" id="toc">')
    i_aside_open_end = donor.index(">", i_aside) + 1
    i_aside_end = donor.index("</aside>")
    i_hero = donor.index("<!-- Hero -->")
    i_script = donor.rindex("<script>", 0, donor.index("// \u2500\u2500\u2500 Mobile TOC toggle"))
    i_tail = donor.rfind("\n", 0, i_script) + 1

    head = donor[:i_nav]
    nav = donor[i_nav:i_layout]
    layout_open = donor[i_layout:i_aside]
    aside_open = donor[i_aside:i_aside_open_end]
    main_open = donor[i_aside_end + len("</aside>"):i_hero].rstrip(" ")
    scripts_tail = donor[i_tail:]

    head = re.sub(r"<title>.*?</title>",
                  "<title>%s</title>" % PAGE_TITLE.replace("\\", "\\\\"), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  lambda m: m.group(1) + META_DESC + m.group(2), head, count=1)
    head = head.replace('content="maths-8"', 'content="%s"' % CHAPTER_ID, 1)
    head = head.replace("</head>", EXTRA_CSS + "</head>", 1)

    nav = re.sub(r'<span class="meta">[^<]*</span>',
                 '<span class="meta">%s</span>' % NAV_META, nav, count=1)

    sidebar = [aside_open, "      <h3>Contents</h3>"]
    for num, sid, label, _emoji in SECTIONS:
        sidebar.append('      <a href="#%s" class="toc-h2">%d. %s</a>' % (sid, num, label))
    sidebar.append("    </aside>")
    sidebar_html = "\n".join(sidebar)

    hero = ('      <!-- Hero -->\n'
            '      <header class="hero fade-in">\n'
            '        <span class="chapter-badge">%s</span>\n'
            "        <h1>%s</h1>\n"
            '        <p class="subtitle">%s</p>\n'
            "      </header>" % (BADGE, H1, SUBTITLE))

    key_terms_script = ('      <script>\n'
                        "        const KEY_TERMS_DATA = %s;\n"
                        "      </script>" % json.dumps(terms, ensure_ascii=False))

    footer = ('      <footer>\n'
              "        <p>" + FOOTER + "</p>\n"
              "      </footer>")

    doc = "".join([
        head, nav, layout_open, sidebar_html, main_open,
        hero, "\n\n", body_html, "\n\n",
        key_terms_script, "\n\n", footer, "\n\n",
        "    </main>\n  </div>\n\n", scripts_tail,
    ])

    # swap the mindmap payload
    doc = re.sub(r'(<script id="chapter-mindmap-data" type="application/json">).*?(</script>)',
                 lambda m: m.group(1) + json.dumps(MINDMAP_MD, ensure_ascii=False) + m.group(2),
                 doc, count=1, flags=re.S)

    # ---------- validations
    problems = []
    if "$" in body_html:
        problems.append("leftover '$' found in body html")
    if doc.count("<details") != doc.count("</details>"):
        problems.append("unbalanced <details> tags")
    if doc.count("<summary") != doc.count("</summary>"):
        problems.append("unbalanced <summary> tags")
    for num, sid, label, _emoji in SECTIONS:
        if ('id="%s"' % sid) not in doc:
            problems.append("missing section id: " + sid)
        if ('href="#%s"' % sid) not in doc:
            problems.append("missing toc link: " + sid)
    for m in re.finditer(r'data-tex="([^"]*)"', doc):
        v = m.group(1)
        if v.count("{") != v.count("}"):
            problems.append("brace mismatch in data-tex: " + v)
    leftovers = set()
    for m in re.finditer(r'data-tex="[^"]*">(.*?)</(?:span|div)>', doc):
        for c in re.findall(r"\\[A-Za-z]+", m.group(1)):
            leftovers.add(c)
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        raise SystemExit(1)

    out = doc
    if crlf:
        out = out.replace("\n", "\r\n")
    OUT.write_bytes(out.encode("utf-8"))

    # ---------- report
    print("wrote:", OUT)
    print("sections:", len(sections))
    print("details blocks:", doc.count("<details"))
    print("tex formulas (span div):",
          doc.count('<span class="tex"') + doc.count('<div class="tex tex-block"'))
    print("key terms:", len(terms))
    if leftovers:
        print("WARN leftover latex cmds inside fallbacks:", sorted(leftovers))


if __name__ == "__main__":
    select_chapter(sys.argv[1] if len(sys.argv) > 1 else "seq")
    main()
