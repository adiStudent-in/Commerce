# _build.py — one-shot md->html builder for the Maths Sequences & Series page.
# Reuses the BST Chapter-1 page shell (style + inline scripts) VERBATIM so the
# design system stays identical; only title/nav/TOC/content/footer data differs.
# Formulas are authored as LaTeX in data-tex attributes and rendered with KaTeX;
# the Unicode text inside each .tex element is the offline fallback.
import json
import pathlib
import re

ROOT = pathlib.Path(r"F:\Study OS\Webpage\Maths")
BST_REF = pathlib.Path(r"F:\Study OS\Webpage\BST\Chapter-1-Business-Trade-and-Commerce.html")

PAGE_TITLE = "Chapter 8 \u2014 Sequences and Series | Maths Class 11"
META_DESC = ("Class 11 Maths Chapter 8 Sequences and Series: concept-first master notes — "
             "sequences, series, GP general term and sum, infinite GP, GM, AM-GM relation, "
             "formula wall, traps and exam question types.")
NAV_LOGO = "\u2190 Maths <span>Notes</span>"
NAV_META = "Class 11 \u00b7 Chapter 8"
BADGE = "Chapter 8 \u00b7 NCERT Rationalized"
H1 = "Sequences and Series"
SUBTITLE = "Class 11 Mathematics \u2014 Concept-First Master Notes"
FOOTER = "Source: NCERT Mathematics Class XI, Chapter 8 (Rationalized) \u00b7 Reprint 2026-27"

KATEX_VERSION = "0.16.11"
HEAD_EXTRA = (
    '<link rel="stylesheet" '
    f'href="https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.css">\n'
    f'  <script defer src="https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.js"></script>'
)
TEX_CSS = """<style>
    /* ─── LaTeX formulas (KaTeX; additive — BST shell untouched) ─── */
    .tex-block { display: block; text-align: center; padding: 8px 4px; overflow-x: auto; }
    .katex { font-size: 1.06em; }
    .katex-display { margin: 0; }
    /* ─── Practice dropdowns (additive — BST shell untouched) ─── */
    details.qa { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); margin: 12px 0; box-shadow: var(--shadow-sm); }
    details.qa summary { cursor: pointer; padding: 12px 16px; font-weight: 600; font-size: 15px; color: var(--text); list-style: none; line-height: 1.55; }
    details.qa summary::-webkit-details-marker { display: none; }
    details.qa summary::marker { content: ""; }
    details.qa summary::before { content: "+"; color: var(--accent); font-weight: 700; margin-right: 10px; }
    details.qa[open] summary::before { content: "\\2013"; }
    details.qa summary:hover { color: var(--accent); }
    details.qa[open] { border-left: 3px solid var(--accent); }
    details.qa .sol { padding: 2px 16px 14px 42px; }
    details.qa .sol p, details.qa .sol ul, details.qa .sol ol { margin-bottom: 10px; }
    details.qa .sol ul, details.qa .sol ol { padding-left: 22px; }
    details.qa .sol li { margin-bottom: 6px; }
  </style>"""
RENDER_JS = """<script>
    // ─── Render LaTeX (data-tex) with KaTeX; Unicode fallback stays if CDN fails ───
    function renderTex() {
      if (!window.katex) return;
      document.querySelectorAll('.tex[data-tex]').forEach(function (el) {
        if (el.dataset.rendered) return;
        try {
          el.innerHTML = window.katex.renderToString(el.getAttribute('data-tex'), {
            displayMode: el.classList.contains('tex-block'),
            throwOnError: false
          });
          el.dataset.rendered = '1';
        } catch (e) { /* keep Unicode fallback */ }
      });
    }
    document.addEventListener('DOMContentLoaded', renderTex);
    window.addEventListener('load', renderTex);
  </script>"""

TOC = [
    ("big-picture", "Big Picture", "toc-h2"),
    ("scope", "Syllabus Scope", "toc-h2"),
    ("sequences", "Sequences", "toc-h2"),
    ("series", "Series and Sigma Notation", "toc-h2"),
    ("gp", "Geometric Progression", "toc-h2"),
    ("gp-sum", "Sum of n Terms of a GP", "toc-h2"),
    ("infinite-gp", "Infinite GP and Its Sum", "toc-h2"),
    ("gm", "Geometric Mean", "toc-h2"),
    ("am-gm", "Relation Between AM and GM", "toc-h2"),
    ("formula-wall", "Formula Wall", "toc-h2"),
    ("traps", "Ten Traps", "toc-h2"),
    ("exam-types", "Standard Exam Question Types", "toc-h2"),
    ("practice-questions", "Practice Questions + Solutions", "toc-h2"),
    ("appendix-r", "Appendix R (Removed Topics)", "toc-h2"),
    ("key-terms", "Key Terms", "toc-h2"),
    ("quick-recap", "Quick Recap", "toc-h2"),
]

KEY_TERMS = [
    ("Sequence", "Ordered list a\u2081, a\u2082, \u2026; the nth term gives any term directly"),
    ("Finite / Infinite sequence", "Stops after k terms (domain {1\u2026k}) vs goes on forever (domain N)"),
    ("Recurrence", "Rule building each term from previous ones (e.g. Fibonacci)"),
    ("Series", "Sequence joined by + signs \u2014 the indicated sum, not the number"),
    ("Sigma (\u03a3) notation", "\u03a3(k=1 to n) a\u2096 abbreviates a\u2081+\u2026+a\u2099"),
    ("GP (Geometric Progression)", "Non-zero terms with constant ratio r \u2260 0"),
    ("Common ratio (r)", "a\u2096\u208a\u2081/a\u2096; general term a\u2099 = a\u00b7r\u207f\u207b\u00b9"),
    ("Infinite GP sum", "a/(1\u2212r), strictly only when |r| < 1"),
    ("GM (Geometric Mean)", "G = \u221a(ab) for a, b > 0; G\u00b2 = ab"),
    ("AM (Arithmetic Mean)", "A = (a+b)/2; AM \u2265 GM with equality iff a = b"),
]

MINDMAP_MD = """# Sequences and Series

## 1. Sequences
- Ordered list a1, a2, ..., an
- Finite (stops) vs Infinite (goes on)
- Given by formula / recurrence / description
- Fibonacci: 1, 1, 2, 3, 5, 8, 13
- Primes have no formula

## 2. Series and Sigma
- Series = terms joined by + (indicated sum)
- Sum of series = the number (don't mix them)
- Sigma: sum a1..an = Σ(k=1 to n) ak

## 3. GP
- Non-zero terms, constant ratio r (r ≠ 0)
- a, ar, ar², ..., ar^(n-1)
- nth term: an = a·r^(n-1) (exponent n-1!)
- Ratio test: equal consecutive ratios

## 4. Sum of n terms
- Trick: S − rS cancels middle terms
- r ≠ 1: Sn = a(1−r^n)/(1−r) = a(r^n−1)/(r−1)
- r = 1: Sn = n·a (no division by zero)

## 5. Infinite GP
- Powers shrink to 0 ONLY if |r| < 1
- S∞ = a/(1−r), check |r| < 1 first
- |r| ≥ 1 → no sum (exam trap)

## 6. GM
- a, G, b in GP (a,b > 0): G = +√(ab)
- n GMs: r = (b/a)^(1/(n+1)), Gk = a·r^k
- 1 and 256 → r = ±4

## 7. AM vs GM
- A = (a+b)/2, G = √(ab), a,b positive
- A ≥ G; proof: A−G = (√a−√b)²/2 ≥ 0
- Equality iff a = b

## 8. Formula Wall
- an = ar^(n-1) | Sn fractions (r≠1), na (r=1)
- S∞ = a/(1−r) for |r|<1
- G = √(ab) | A = (a+b)/2 | A ≥ G

## 9. Traps
- Series ≠ sum; r ≠ 0; exponent n−1
- Never fraction-sum at r = 1
- Infinite needs |r| < 1
- GM is +√(ab); AM–GM needs positives
"""


def extract_shell(ref_html: str):
    m = re.search(r"<style>.*?</style>", ref_html, re.DOTALL)
    assert m, "style block not found in reference page"
    assert ref_html.count("<style>") == 1, "expected exactly one style block"
    style = m.group(0)
    m2 = re.search(r"<script>\n    // \u2500\u2500\u2500 Mobile TOC toggle.*?</script>",
                   ref_html, re.DOTALL)
    assert m2, "legacy inline script not found in reference page"
    inline_js = m2.group(0)
    return style, inline_js


def toc_html():
    parts = ["<h3>Contents</h3>"]
    for anchor, label, cls in TOC:
        parts.append(f'<a href="#{anchor}" class="{cls}">{label}</a>')
    return "\n      ".join(parts)


BODY = """<!-- Big Picture -->
      <section id="big-picture" class="fade-in">
        <h2>&#x1f4cc; Big Picture</h2>
        <blockquote>
          A <strong>sequence</strong> is a list of numbers written in order. A <strong>series</strong> is the same list with <strong>+ signs</strong> between the terms.<br>
          Most of this chapter is about one special list \u2014 the <strong>Geometric Progression (GP)</strong>, where every step <strong>multiplies by the same number</strong> \u2014 plus one famous comparison: <span class="tex" data-tex="A \\geq G">AM \u2265 GM</span>.
        </blockquote>
        <p><strong>How to use these notes:</strong> read sections 1\u20137 in order (each one needs the previous). Every formula has a <strong>"why"</strong> line \u2014 learn the why and you can rebuild the formula in the exam even if you forget it. Section 8 is the formula wall for last-day revision. Section 9 lists the exact traps examiners set.</p>
      </section>

      <!-- 0. Syllabus scope -->
      <section id="scope" class="fade-in">
        <h2>0. &#x1f5fa;&#xfe0f; Syllabus Scope (read first)</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Status</th><th>Topics</th></tr></thead>
            <tbody>
              <tr><td>&#x2705; IN (board syllabus)</td><td>Sequences; Series and sigma notation; <strong>GP</strong> \u2014 general term, sum of n terms, <strong>infinite GP and its sum</strong>; <strong>GM</strong> (single + n GMs); <strong>AM</strong> \u2014 single arithmetic mean; <strong>relation between AM and GM</strong></td></tr>
              <tr><td>&#x23ed;&#xfe0f; OUT (deleted 2023)</td><td>Full <strong>AP theory</strong> (nth term, sum formulas, AP properties as examinable topics); <strong>special sums</strong> <span class="tex" data-tex="\\sum n,\\ \\sum n^2,\\ \\sum n^3">\u03a3n, \u03a3n\u00b2, \u03a3n\u00b3</span></td></tr>
              <tr><td>&#x1f4dd; Practice only</td><td>Special sums <span class="tex" data-tex="\\sum k,\\ \\sum k^2,\\ \\sum k^3">\u03a3k, \u03a3k\u00b2, \u03a3k\u00b3</span> (practice material \u2014 deleted from board summative assessment)</td></tr>
            </tbody>
          </table>
        </div>
        <blockquote>CBSE 2026-27 scope, Unit II-5: Sequence and Series; Arithmetic Mean (A.M.); GP \u2014 general term, sum of n terms, infinite GP and its sum; GM; relation between AM and GM.</blockquote>
        <p>The words "Arithmetic Mean" survive only because Section 7 defines <span class="tex" data-tex="A = \\frac{a+b}{2}">A = (a+b)/2</span>. Full AP theory is gone from the book. <strong>Appendix R</strong> at the end covers the deleted AP + special-sum material as clearly-marked <strong>reference only</strong> (useful for school tests based on old books \u2014 not board-required).</p>
      </section>

      <!-- 1. Sequences -->
      <section id="sequences" class="fade-in">
        <h2>1. &#x1f522; Sequences \u2014 ordered lists</h2>
        <blockquote><strong>Sequence</strong> = terms written in a fixed order: <span class="tex" data-tex="a_1,\\ a_2,\\ a_3,\\ \\dots,\\ a_n,\\ \\dots">a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>, \u2026, a<sub>n</sub>, \u2026</span><br>Each entry is a <strong>term</strong>. The <strong>nth term</strong> (general term) is the rule that produces any term directly.</blockquote>
        <h3>Finite vs infinite</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Type</th><th>Meaning</th><th>Example</th></tr></thead>
            <tbody>
              <tr><td>Finite</td><td>Stops after some fixed number of terms</td><td>2, 4, 6, 8 (4 terms)</td></tr>
              <tr><td>Infinite</td><td>Goes on forever (\u2026 at the end)</td><td>2, 4, 6, 8, \u2026</td></tr>
            </tbody>
          </table>
        </div>
        <h3>Three ways a sequence can be given</h3>
        <p><strong>1. By a formula for a<sub>n</sub></strong> (most common in exams)</p>
        <ul>
          <li>Even numbers: <span class="tex" data-tex="a_n = 2n">a<sub>n</sub> = 2n</span> \u2192 2, 4, 6, 8, \u2026</li>
          <li>Odd numbers: <span class="tex" data-tex="a_n = 2n - 1">a<sub>n</sub> = 2n \u2212 1</span> \u2192 1, 3, 5, 7, \u2026</li>
          <li>Worked check: <span class="tex" data-tex="a_n = (n-1)(2-n)(3+n)">a<sub>n</sub> = (n\u22121)(2\u2212n)(3+n)</span> gives <span class="tex" data-tex="a_1 = 0,\\ a_2 = 0,\\ a_3 = -12">a<sub>1</sub> = <strong>0</strong>, a<sub>2</sub> = <strong>0</strong>, a<sub>3</sub> = <strong>\u221212</strong></span></li>
        </ul>
        <p><strong>2. By recurrence</strong> (each term built from previous ones)</p>
        <ul>
          <li><strong>Fibonacci:</strong> <span class="tex" data-tex="a_1 = a_2 = 1,\\quad a_n = a_{n-1} + a_{n-2}\\ \\ (n > 2)">a<sub>1</sub> = a<sub>2</sub> = 1, a<sub>n</sub> = a<sub>n\u22121</sub> + a<sub>n\u22122</sub> for n &gt; 2</span> \u2192 <strong>1, 1, 2, 3, 5, 8, 13</strong>, \u2026</li>
        </ul>
        <p><strong>3. By description only</strong> (no formula exists \u2014 and that is fine)</p>
        <ul>
          <li>Primes: 2, 3, 5, 7, 11, \u2026 \u2014 there is no single formula generating only primes.</li>
        </ul>
        <div class="callout"><strong>Concept:</strong> a sequence is a <strong>function</strong> whose domain is <span class="tex" data-tex="\\mathbb{N} = \\{1, 2, 3, \\dots\\}">N = {1, 2, 3, \u2026}</span> (infinite sequence) or <span class="tex" data-tex="\\{1, 2, \\dots, k\\}">{1, 2, \u2026, k}</span> (finite sequence with k terms). <span class="tex" data-tex="a_n">a<sub>n</sub></span> is just "the output at input n".</div>
      </section>

      <!-- 2. Series -->
      <section id="series" class="fade-in">
        <h2>2. &#x2795; Series and \u03a3 notation \u2014 adding the list up</h2>
        <blockquote><strong>Series</strong> = the terms of a sequence joined by + signs: <span class="tex" data-tex="a_1 + a_2 + a_3 + \\dots">a<sub>1</sub> + a<sub>2</sub> + a<sub>3</sub> + \u2026</span> (+ \u2026).<br><strong>NCERT Remark (exam favourite):</strong> the <em>series</em> is the <strong>indicated sum</strong>; the <em>"sum of the series"</em> is the <strong>number</strong> you get after adding.</blockquote>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Sequence</th><th>Associated series</th></tr></thead>
            <tbody>
              <tr><td>2, 4, 6, \u2026, 2n</td><td>2 + 4 + 6 + \u2026 + 2n</td></tr>
              <tr><td>3, 5, 7, 9</td><td>3 + 5 + 7 + 9 (finite \u2014 adds to 24)</td></tr>
            </tbody>
          </table>
        </div>
        <h3>Sigma (\u03a3) notation \u2014 shorthand, not a formula</h3>
        <p><span class="tex" data-tex="a_1 + a_2 + \\dots + a_n">a<sub>1</sub> + a<sub>2</sub> + \u2026 + a<sub>n</sub></span> is abbreviated <span class="tex" data-tex="\\sum_{k=1}^{n} a_k"><strong>\u03a3(k=1 to n) a<sub>k</sub></strong></span>.</p>
        <ul>
          <li>Read it as: "start k at 1, write <span class="tex" data-tex="a_k">a<sub>k</sub></span> for each k, add everything up to n".</li>
          <li>Example: <span class="tex" data-tex="2 + 4 + 6 + \\dots + 2n = \\sum_{k=1}^{n} 2k">2 + 4 + 6 + \u2026 + 2n = <strong>\u03a3(k=1 to n) 2k</strong></span>.</li>
        </ul>
        <div class="callout">\u26a0\ufe0f <span class="tex" data-tex="\\sum">\u03a3</span> denotes the <strong>process of adding</strong>, not the answer.</div>
        <h3>Recurrence \u2192 series (worked)</h3>
        <p>Rule: <span class="tex" data-tex="a_1 = 3,\\quad a_n = a_{n-1} + 2">a<sub>1</sub> = 3, a<sub>n</sub> = a<sub>n\u22121</sub> + 2</span>.</p>
        <ul>
          <li>Terms: 3, <strong>5</strong>, <strong>7</strong>, <strong>9</strong> (each = previous + 2)</li>
          <li>Series: 3 + 5 + 7 + 9 (finite; its sum is 24 by direct adding)</li>
        </ul>
      </section>

      <!-- 3. GP -->
      <section id="gp" class="fade-in">
        <h2>3. &#x2716;&#xfe0f; Geometric Progression (GP) \u2014 multiply by the same number every step</h2>
        <blockquote><strong>GP definition:</strong> every term is <strong>non-zero</strong>, and the ratio of each term to the previous one is a <strong>constant <span class="tex" data-tex="r \\neq 0">r (\u2260 0)</span></strong>: <span class="tex" data-tex="\\frac{a_{k+1}}{a_k} = r \\quad (k \\geq 1)">a<sub>k+1</sub> / a<sub>k</sub> = r for all k \u2265 1</span>. First term <span class="tex" data-tex="a \\neq 0"><strong>a \u2260 0</strong></span>.</blockquote>
        <ul>
          <li>Standard finite form: <span class="tex" data-tex="a,\\ ar,\\ ar^2,\\ \\dots,\\ ar^{n-1}"><strong>a, ar, ar\u00b2, \u2026, ar\u207f\u207b\u00b9</strong></span> (n terms)</li>
          <li>Standard infinite form: <span class="tex" data-tex="a,\\ ar,\\ ar^2,\\ \\dots"><strong>a, ar, ar\u00b2, \u2026</strong></span></li>
        </ul>
        <div class="callout"><strong>Why the exponent is n\u22121:</strong> the 1st term must be <span class="tex" data-tex="a \\cdot r^0 = a">a \u00d7 r\u2070 = a</span> (anything to power 0 is 1), so the nth term carries <span class="tex" data-tex="r^{n-1}">r\u207f\u207b\u00b9</span>, not <span class="tex" data-tex="r^n">r\u207f</span>. This off-by-one is the chapter's most repeated silly mistake.</div>
        <h3>The general (nth) term</h3>
        <div class="tex tex-block" data-tex="a_n = a\\cdot r^{n-1}\\qquad (n \\geq 1)">a<sub>n</sub> = a \u00b7 r\u207f\u207b\u00b9, for n \u2265 1. (a = first term, r = common ratio)</div>
        <p><strong>Ratio test</strong> (is it a GP?): divide consecutive terms \u2014 2nd/1st, 3rd/2nd, \u2026 If every ratio is equal, it is a GP and that value is r.</p>
        <h3>Worked examples</h3>
        <ol>
          <li>2, 6, 18, \u2026 \u2192 <span class="tex" data-tex="r = \\frac{6}{2} = \\frac{18}{6} = 3">r = 6/2 = 18/6 = <strong>3</strong></span>. <span class="tex" data-tex="a_6 = 2\\cdot 3^5 = 2\\cdot 243 = 486">a<sub>6</sub> = 2 \u00d7 3<sup>5</sup> = 2 \u00d7 243 = <strong>486</strong></span>.</li>
          <li>First term 3, 4th term 24 \u2192 <span class="tex" data-tex="3r^3 = 24 \\Rightarrow r^3 = 8 \\Rightarrow r = 2">3\u00b7r\u00b3 = 24 \u2192 r\u00b3 = 8 \u2192 <strong>r = 2</strong></span>. Terms: 3, 6, 12, 24. \u2713</li>
          <li>NOT a GP: 2, 6, 12, \u2026 (<span class="tex" data-tex="\\frac{6}{2} = 3">6/2 = 3</span> but <span class="tex" data-tex="\\frac{12}{6} = 2">12/6 = 2</span> \u2014 ratios differ).</li>
        </ol>
        <h3>Retained GP properties (short list)</h3>
        <ul>
          <li>Multiplying or dividing <strong>every</strong> term by the same non-zero k gives another GP (same r).</li>
          <li>Reciprocals <span class="tex" data-tex="\\frac{1}{a_1},\\ \\frac{1}{a_2},\\ \\dots">1/a<sub>1</sub>, 1/a<sub>2</sub>, \u2026</span> form a GP.</li>
          <li>Term-by-term product or quotient of two GPs is a GP.</li>
          <li>Ends multiply equal: <span class="tex" data-tex="a_1\\cdot a_n = a_2\\cdot a_{n-1} = \\dots">a<sub>1</sub>\u00b7a<sub>n</sub> = a<sub>2</sub>\u00b7a<sub>n\u22121</sub> = \u2026</span> (mirror pairs).</li>
          <li>nth term from the last = <span class="tex" data-tex="\\dfrac{l}{r^{n-1}}">l / r\u207f\u207b\u00b9</span>, where l is the last term.</li>
        </ul>
      </section>

      <!-- 4. GP sum -->
      <section id="gp-sum" class="fade-in">
        <h2>4. &#x1f9ee; Sum of the first n terms of a GP</h2>
        <h3>The derivation (learn this once \u2014 it is the whole concept)</h3>
        <p>Let <span class="tex" data-tex="S_n = a + ar + ar^2 + \\dots + ar^{n-1}">S<sub>n</sub> = a + ar + ar\u00b2 + \u2026 + ar\u207f\u207b\u00b9</span>. Multiply everything by r:</p>
        <div class="tex tex-block" data-tex="r\\cdot S_n = ar + ar^2 + \\dots + ar^{n-1} + ar^n">r\u00b7S<sub>n</sub> = ar + ar\u00b2 + \u2026 + ar\u207f\u207b\u00b9 + ar\u207f.</div>
        <div class="tex tex-block" data-tex="S_n - r\\cdot S_n = a - ar^n">Subtract: S<sub>n</sub> \u2212 r\u00b7S<sub>n</sub> = a \u2212 ar\u207f (every middle term cancels \u2014 that is the magic).</div>
        <div class="tex tex-block" data-tex="(1 - r)\\cdot S_n = a(1 - r^n)">(1 \u2212 r)\u00b7S<sub>n</sub> = a(1 \u2212 r\u207f).</div>
        <h3>The formulas (both forms are identical algebra)</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Case</th><th>Formula</th><th>When to use</th></tr></thead>
            <tbody>
              <tr><td>r \u2260 1</td><td><span class="tex" data-tex="S_n = \\dfrac{a(1-r^n)}{1-r}"><strong>S<sub>n</sub> = a(1 \u2212 r\u207f) / (1 \u2212 r)</strong></span></td><td>Default form</td></tr>
              <tr><td>r \u2260 1</td><td><span class="tex" data-tex="S_n = \\dfrac{a(r^n-1)}{r-1}"><strong>S<sub>n</sub> = a(r\u207f \u2212 1) / (r \u2212 1)</strong></span></td><td>Same formula; use when r &gt; 1 so the denominator stays positive</td></tr>
              <tr><td>r = 1</td><td><span class="tex" data-tex="S_n = n\\cdot a"><strong>S<sub>n</sub> = n\u00b7a</strong></span></td><td>All terms equal a (the fraction forms would divide by zero!)</td></tr>
            </tbody>
          </table>
        </div>
        <h3>Worked examples</h3>
        <ol>
          <li>1 + 2 + 4 + \u2026 + 512 \u2192 a = 1, r = 2, and <span class="tex" data-tex="512 = 2^9">512 = 2<sup>9</sup></span> so n = 10.<br><span class="tex" data-tex="S_{10} = \\dfrac{2^{10}-1}{2-1} = 1024 - 1 = 1023">S<sub>10</sub> = (2<sup>10</sup> \u2212 1)/(2 \u2212 1) = 1024 \u2212 1 = <strong>1023</strong></span>.</li>
          <li>a = 3, r = 1/2, n = 4 \u2192 terms 3, 3/2, 3/4, 3/8.<br><span class="tex" data-tex="S_4 = \\dfrac{3\\left(1-(1/2)^4\\right)}{1-1/2} = \\dfrac{45}{8} = 5.625">S<sub>4</sub> = 3(1 \u2212 (1/2)<sup>4</sup>)/(1 \u2212 1/2) = 3(15/16)/(1/2) = <strong>45/8 = 5.625</strong></span>. Direct check: 3 + 1.5 + 0.75 + 0.375 = 5.625. \u2713</li>
          <li><strong>Application (depreciation):</strong> machine worth \u20b91250 loses 20% value yearly \u2192 values form a GP with r = 0.8.<br>After 5 years: <span class="tex" data-tex="1250 \\times 0.8^5 = 1250 \\times 0.32768 = 409.60">1250 \u00d7 0.8<sup>5</sup> = 1250 \u00d7 0.32768 = <strong>\u20b9409.60</strong></span>.</li>
        </ol>
      </section>

      <!-- 5. Infinite GP -->
      <section id="infinite-gp" class="fade-in">
        <h2>5. &#x267e;&#xfe0f; Infinite GP and its sum \u2014 the <span class="tex" data-tex="|r| < 1">|r| &lt; 1</span> rule</h2>
        <h3>The concept (why only some infinite lists add up to a number)</h3>
        <blockquote>If <span class="tex" data-tex="|r| < 1">|r| &lt; 1</span>, powers <strong>shrink to 0</strong>: <span class="tex" data-tex="(1/2)^{10} \\approx 0.001,\\quad (1/2)^{20} \\approx 0.000001">(1/2)<sup>10</sup> \u2248 0.001, (1/2)<sup>20</sup> \u2248 0.000001</span>, \u2026<br>So for large n, <span class="tex" data-tex="r^n \\approx 0">r\u207f \u2248 0</span> and the finite-sum formula <span class="tex" data-tex="S_n = \\dfrac{a(1-r^n)}{1-r}">S<sub>n</sub> = a(1 \u2212 r\u207f)/(1 \u2212 r)</span> settles down to <span class="tex" data-tex="\\dfrac{a}{1-r}"><strong>a/(1 \u2212 r)</strong></span>.<br>If <span class="tex" data-tex="|r| \\geq 1">|r| \u2265 1</span>, terms never die out \u2014 the infinite sum <strong>does not exist</strong> in this chapter. This condition is the examiner's favourite trap.</blockquote>
        <h3>The formula (with its strict condition)</h3>
        <div class="tex tex-block" data-tex="S_\\infty = \\dfrac{a}{1-r}\\qquad \\text{valid ONLY if } |r| < 1"><strong>S<sub>\u221e</sub> = a / (1 \u2212 r), valid ONLY if |r| &lt; 1.</strong></div>
        <p>Always verify <span class="tex" data-tex="|r| < 1">|r| &lt; 1</span> <strong>before</strong> using it.</p>
        <h3>Worked examples</h3>
        <ol>
          <li>1 + 1/2 + 1/4 + \u2026 \u2192 a = 1, r = 1/2 (|r| &lt; 1 \u2713). <span class="tex" data-tex="S_\\infty = \\dfrac{1}{1-1/2} = 2">S<sub>\u221e</sub> = 1/(1 \u2212 1/2) = <strong>2</strong></span>.</li>
          <li>3 + 1 + 1/3 + \u2026 \u2192 a = 3, r = 1/3 \u2713. <span class="tex" data-tex="S_\\infty = \\dfrac{3}{1-1/3} = \\dfrac{3}{2/3} = \\dfrac{9}{2}">S<sub>\u221e</sub> = 3/(1 \u2212 1/3) = 3/(2/3) = <strong>9/2</strong></span>.</li>
          <li>5 \u2212 5 + 5 \u2212 5 + \u2026 \u2192 <span class="tex" data-tex="r = -1 \\Rightarrow |r| = 1 \\geq 1 \\Rightarrow \\text{no sum}">r = \u22121, |r| = 1 \u2276 1 \u2192 <strong>no sum</strong></span> (terms just flip forever).</li>
        </ol>
      </section>

      <!-- 6. GM -->
      <section id="gm" class="fade-in">
        <h2>6. &#x1f4d0; Geometric Mean (GM)</h2>
        <h3>Single GM</h3>
        <div class="tex tex-block" data-tex="G^2 = ab,\\qquad G = +\\sqrt{ab}\\quad (a, b > 0)">If a, G, b are in GP with <strong>a, b &gt; 0</strong>, then G\u00b2 = ab and <strong>G = +\u221a(ab)</strong> (NCERT takes the positive root).</div>
        <ul>
          <li>Worked: GM of 4 and 16 = <span class="tex" data-tex="\\sqrt{4\\cdot 16} = \\sqrt{64} = 8">\u221a(4\u00d716) = \u221a64 = <strong>8</strong></span>. Check: 4, 8, 16 has ratio 2. \u2713</li>
        </ul>
        <h3>Inserting n GMs between a and b</h3>
        <p>Treat b as the (n+2)th term: <span class="tex" data-tex="b = a\\cdot r^{n+1}">b = a\u00b7r\u207f\u207a\u00b9</span>, so <span class="tex" data-tex="r = \\left(\\frac{b}{a}\\right)^{1/(n+1)}">r = (b/a)<sup>1/(n+1)</sup></span> (principal positive root; \u2212r is also real when n+1 is even) and <span class="tex" data-tex="G_k = a\\cdot r^k \\quad (k = 1\\dots n)">G<sub>k</sub> = a\u00b7r<sup>k</sup> for k = 1\u2026n</span>.</p>
        <ul>
          <li><strong>Worked (NCERT-type):</strong> insert 3 numbers between 1 and 256.<br><span class="tex" data-tex="r^4 = 256 \\Rightarrow r = +4 \\text{ or } -4">r<sup>4</sup> = 256 \u2192 <strong>r = +4 or \u22124</strong></span> (real roots) \u2192 <strong>4, 16, 64</strong> or <strong>\u22124, 16, \u221264</strong>.<br>(The single-GM positivity rule applies to <span class="tex" data-tex="G = \\sqrt{ab}">G = \u221a(ab)</span>, not to every insertion case \u2014 negative r is allowed here.)</li>
          <li><strong>Corollary:</strong> product of the n inserted GMs = <span class="tex" data-tex="(ab)^{n/2}">(ab)<sup>n/2</sup></span> (= <span class="tex" data-tex="G^n">G\u207f</span> where G is the single GM).</li>
        </ul>
      </section>

      <!-- 7. AM-GM -->
      <section id="am-gm" class="fade-in">
        <h2>7. &#x2696;&#xfe0f; Relationship between AM and GM</h2>
        <h3>Definitions</h3>
        <ul>
          <li><strong>Arithmetic Mean</strong> of a and b: <span class="tex" data-tex="A = \\frac{a+b}{2}"><strong>A = (a + b)/2</strong></span> (this is the "A.M." named in the syllabus).</li>
          <li><strong>Geometric Mean</strong> of a and b (positive): <span class="tex" data-tex="G = \\sqrt{ab}"><strong>G = \u221a(ab)</strong></span>.</li>
        </ul>
        <h3>The theorem + NCERT proof (learn the 3 lines)</h3>
        <div class="tex tex-block" data-tex="A \\geq G\\qquad \\text{for positive reals } a, b;\\quad A = G \\iff a = b">For positive real numbers a, b: <strong>A \u2265 G</strong>, with equality <strong>iff a = b</strong>.</div>
        <p>Proof: <span class="tex" data-tex="A - G = \\frac{a+b}{2} - \\sqrt{ab} = \\frac{a + b - 2\\sqrt{ab}}{2} = \\frac{(\\sqrt{a}-\\sqrt{b})^2}{2} \\geq 0">A \u2212 G = (a + b)/2 \u2212 \u221a(ab) = (a + b \u2212 2\u221a(ab))/2 = <strong>(\u221aa \u2212 \u221ab)\u00b2/2 \u2265 0</strong></span> (a square is never negative). It equals 0 exactly when <span class="tex" data-tex="\\sqrt{a} = \\sqrt{b}">\u221aa = \u221ab</span>, i.e. <span class="tex" data-tex="a = b"><strong>a = b</strong></span>. \u220e</p>
        <h3>Application (prove with AM \u2265 GM)</h3>
        <p>For positive x, y, z, show <span class="tex" data-tex="(x+y)(y+z)(z+x) \\geq 8xyz"><strong>(x+y)(y+z)(z+x) \u2265 8xyz</strong></span>:</p>
        <ul>
          <li><span class="tex" data-tex="x + y \\geq 2\\sqrt{xy},\\quad y + z \\geq 2\\sqrt{yz},\\quad z + x \\geq 2\\sqrt{zx}">x + y \u2265 2\u221a(xy), y + z \u2265 2\u221a(yz), z + x \u2265 2\u221a(zx)</span> (AM \u2265 GM on each pair).</li>
          <li>Multiply: <span class="tex" data-tex="\\text{LHS} \\geq 8\\sqrt{xy\\cdot yz\\cdot zx} = 8xyz">LHS \u2265 8\u221a(xy\u00b7yz\u00b7zx) = 8\u221a(x\u00b2y\u00b2z\u00b2) = <strong>8xyz</strong></span>. \u220e</li>
        </ul>
        <div class="callout"><strong>Boundary:</strong> the mean of n numbers <span class="tex" data-tex="\\frac{a_1+\\dots+a_n}{n}">(a<sub>1</sub>+\u2026+a<sub>n</sub>)/n</span> is just a definition here. The n-variable AM \u2265 GM inequality is <strong>not proved</strong> in the main Class 11 text \u2014 do not present it as an NCERT result.</div>
      </section>

      <!-- 8. Formula wall -->
      <section id="formula-wall" class="fade-in">
        <h2>8. &#x26a1; Formula Wall (board-required only)</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th><th>Result</th><th>Exact condition</th></tr></thead>
            <tbody>
              <tr><td>1</td><td>Series <span class="tex" data-tex="a_1+\\dots+a_n = \\sum_{k=1}^{n} a_k">a<sub>1</sub>+\u2026+a<sub>n</sub> = \u03a3(k=1 to n) a<sub>k</sub></span></td><td>Notation \u2014 always valid</td></tr>
              <tr><td>2</td><td>GP nth term: <span class="tex" data-tex="a_n = a\\cdot r^{n-1}">a<sub>n</sub> = a\u00b7r\u207f\u207b\u00b9</span></td><td>a \u2260 0, r \u2260 0, n \u2265 1</td></tr>
              <tr><td>3</td><td>GP sum: <span class="tex" data-tex="S_n = \\dfrac{a(1-r^n)}{1-r} = \\dfrac{a(r^n-1)}{r-1}">S<sub>n</sub> = a(1\u2212r\u207f)/(1\u2212r) = a(r\u207f\u22121)/(r\u22121)</span></td><td>r \u2260 1</td></tr>
              <tr><td>4</td><td>GP sum: <span class="tex" data-tex="S_n = n\\cdot a">S<sub>n</sub> = n\u00b7a</span></td><td>r = 1</td></tr>
              <tr><td>5</td><td>Infinite GP: <span class="tex" data-tex="S_\\infty = \\dfrac{a}{1-r}">S<sub>\u221e</sub> = a/(1\u2212r)</span></td><td><strong>|r| &lt; 1</strong> (strict)</td></tr>
              <tr><td>6</td><td>Single GM: <span class="tex" data-tex="G = \\sqrt{ab}">G = \u221a(ab)</span></td><td>a, b &gt; 0 (positive root)</td></tr>
              <tr><td>7</td><td>n GMs: <span class="tex" data-tex="r = \\left(\\frac{b}{a}\\right)^{1/(n+1)},\\ G_k = a\\cdot r^k">r = (b/a)<sup>1/(n+1)</sup> (also \u2212r when n+1 even), G<sub>k</sub> = a\u00b7r<sup>k</sup></span></td><td>a, b &gt; 0; k = 1\u2026n</td></tr>
              <tr><td>8</td><td>Single AM: <span class="tex" data-tex="A = \\frac{a+b}{2}">A = (a+b)/2</span></td><td>a, b any reals</td></tr>
              <tr><td>9</td><td><span class="tex" data-tex="A \\geq G">AM \u2265 GM</span>, equality iff a = b</td><td>a, b positive reals</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 9. Traps -->
      <section id="traps" class="fade-in">
        <h2>9. &#x1faa4; Ten Traps (night-before checklist)</h2>
        <ol>
          <li><strong>Series \u2260 sum.</strong> Series = the indicated sum (<span class="tex" data-tex="a_1+a_2+\\dots">a<sub>1</sub>+a<sub>2</sub>+\u2026</span>); "sum of the series" = the number. (NCERT Remark.)</li>
          <li><strong>Not every sequence has a formula.</strong> Primes have none; some sequences need recurrence or words.</li>
          <li><strong>GP needs non-zero everything:</strong> first term <span class="tex" data-tex="a \\neq 0">a \u2260 0</span> and ratio <span class="tex" data-tex="r \\neq 0">r \u2260 0</span>. r = 0 is not allowed.</li>
          <li><strong>nth term exponent is n\u22121</strong>, not n. (First term = <span class="tex" data-tex="a\\cdot r^0 = a">a\u00b7r\u2070 = a</span>.)</li>
          <li><strong>Never use the fraction sum formula when r = 1</strong> \u2014 division by zero. Use <span class="tex" data-tex="S_n = na">S<sub>n</sub> = na</span>.</li>
          <li><strong>Infinite GP needs <span class="tex" data-tex="|r| < 1">|r| &lt; 1</span> \u2014 always check first.</strong> r = 1, r = \u22121, r = 2\u2026 all have no infinite sum.</li>
          <li><strong>GM sign:</strong> for positive a, b, NCERT's GM is <span class="tex" data-tex="+\\sqrt{ab}"><strong>+\u221a(ab)</strong></span>. <span class="tex" data-tex="-\\sqrt{ab}">\u2212\u221a(ab)</span> squares correctly but is not the NCERT GM.</li>
          <li><strong>AM \u2265 GM needs positive numbers</strong>, and equality holds (<span class="tex" data-tex="A = G">A = G</span>) exactly when a = b \u2014 not strict &gt;.</li>
          <li><strong><span class="tex" data-tex="\\sum">\u03a3</span> is the adding process</strong>, not the answer.</li>
          <li><span class="tex" data-tex="\\sum n^3 = \\left(\\sum n\\right)^2 = \\left[\\frac{n(n+1)}{2}\\right]^2"><strong>\u03a3n\u00b3 = (\u03a3n)\u00b2</strong>, i.e. [n(n+1)/2]\u00b2</span> \u2014 one mirror site misprints it as <span class="tex" data-tex="\\left[\\frac{n(n+1)(2n+1)}{6}\\right]^2">[n(n+1)(2n+1)/6]\u00b2</span>, which is <strong>wrong</strong>. (The formula itself sits in Appendix R \u2014 deleted from boards.)</li>
        </ol>
      </section>

      <!-- 10. Exam types -->
      <section id="exam-types" class="fade-in">
        <h2>10. &#x1f3af; Standard Exam Question Types (and the method for each)</h2>
        <ul>
          <li><strong>Write first terms from a<sub>n</sub></strong> \u2014 substitute n = 1, 2, 3\u2026 directly.</li>
          <li><strong>Find an indicated term</strong> (e.g. <span class="tex" data-tex="a_n = (n-1)(2-n)(3+n)">a<sub>n</sub> = (n\u22121)(2\u2212n)(3+n)</span>) \u2014 careful bracket arithmetic.</li>
          <li><strong>Build a series from a recurrence</strong> \u2014 generate terms step by step, then join with +.</li>
          <li><strong>GP nth term / sum given a, r</strong> \u2014 identify a, r first; watch the n\u22121 exponent.</li>
          <li><strong>Depreciation / growth cascade</strong> (<span class="tex" data-tex="1250\\times 0.8^5">1250\u00d70.8<sup>5</sup></span> type; sides halving each step) \u2014 model as GP, then apply <span class="tex" data-tex="a_n">a<sub>n</sub></span> or <span class="tex" data-tex="S_n">S<sub>n</sub></span>.</li>
          <li><strong>Insert GMs between two numbers</strong> \u2014 <span class="tex" data-tex="b = a\\cdot r^{n+1}">b = a\u00b7r\u207f\u207a\u00b9</span> route; remember \u00b1 roots are both real answers.</li>
          <li><strong>Infinite GP: verify <span class="tex" data-tex="|r| < 1">|r| &lt; 1</span>, then <span class="tex" data-tex="\\dfrac{a}{1-r}">a/(1\u2212r)</span></strong> \u2014 or find a/r backwards from a given <span class="tex" data-tex="S_\\infty">S<sub>\u221e</sub></span>.</li>
          <li><strong>Prove AM \u2265 GM / deduce product inequalities</strong> \u2014 the <span class="tex" data-tex="(\\sqrt{a}-\\sqrt{b})^2">(\u221aa\u2212\u221ab)\u00b2</span> proof, then apply per-pair and multiply.</li>
          <li><strong>Sigma reading</strong> \u2014 expand <span class="tex" data-tex="\\sum">\u03a3</span> into terms or compress a listed sum into <span class="tex" data-tex="\\sum">\u03a3</span> (notation only).</li>
        </ul>
      </section>

      <!-- 11. Practice questions -->
      <section id="practice-questions" class="fade-in">
        <h2>11. &#x1f4aa; Practice Questions with Full Solutions</h2>
        <div class="callout">23 exam-style questions \u2014 one set per topic. Cover the solution, solve it yourself, then open the dropdown to match every step.</div>
        <h3>Sequences</h3>
        <details class="qa"><summary><strong>Q1.</strong> Write the first five terms of the sequence with <span class="tex" data-tex="a_n = n(n+2)">a<sub>n</sub> = n(n + 2)</span>.</summary><div class="sol">
          <p><strong>Solution.</strong> Substitute n = 1, 2, 3, 4, 5 directly:</p>
          <ul>
            <li>a<sub>1</sub> = 1 \u00d7 3 = <strong>3</strong></li>
            <li>a<sub>2</sub> = 2 \u00d7 4 = <strong>8</strong></li>
            <li>a<sub>3</sub> = 3 \u00d7 5 = <strong>15</strong></li>
            <li>a<sub>4</sub> = 4 \u00d7 6 = <strong>24</strong></li>
            <li>a<sub>5</sub> = 5 \u00d7 7 = <strong>35</strong></li>
          </ul>
          <p>\u2705 <strong>Sequence: 3, 8, 15, 24, 35.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q2.</strong> Find the 10th term of the sequence <span class="tex" data-tex="a_n = (-1)^{n-1}\\cdot 5^{n+1}">a<sub>n</sub> = (\u22121)\u207f\u207b\u00b9 \u00b7 5\u207f\u207a\u00b9</span>.</summary><div class="sol">
          <p><strong>Solution.</strong> Put n = 10:</p>
          <ul>
            <li>Sign: (\u22121)<sup>9</sup> = <strong>\u22121</strong> (odd exponent keeps the minus).</li>
            <li>Power: 5<sup>11</sup> = 5<sup>10</sup> \u00d7 5 = 9,765,625 \u00d7 5 = <strong>48,828,125</strong>.</li>
            <li>a<sub>10</sub> = \u22121 \u00d7 48,828,125.</li>
          </ul>
          <p>\u2705 <strong>a<sub>10</sub> = \u221248,828,125.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q3.</strong> Write the first five terms of the sequence defined by <span class="tex" data-tex="a_1 = 3,\\quad a_n = 3a_{n-1} + 2">a<sub>1</sub> = 3 and a<sub>n</sub> = 3a<sub>n\u22121</sub> + 2</span> for n &gt; 1.</summary><div class="sol">
          <p><strong>Solution.</strong> Build each term from the previous one:</p>
          <ul>
            <li>a<sub>1</sub> = <strong>3</strong> (given)</li>
            <li>a<sub>2</sub> = 3 \u00d7 3 + 2 = <strong>11</strong></li>
            <li>a<sub>3</sub> = 3 \u00d7 11 + 2 = <strong>35</strong></li>
            <li>a<sub>4</sub> = 3 \u00d7 35 + 2 = <strong>107</strong></li>
            <li>a<sub>5</sub> = 3 \u00d7 107 + 2 = <strong>323</strong></li>
          </ul>
          <p>\u2705 <strong>Sequence: 3, 11, 35, 107, 323.</strong></p>
        </div></details>
        <h3>Series and sigma notation</h3>
        <details class="qa"><summary><strong>Q4.</strong> For <span class="tex" data-tex="a_n = n^2 + 2n">a<sub>n</sub> = n\u00b2 + 2n</span>, write the first three terms and the corresponding series.</summary><div class="sol">
          <p><strong>Solution.</strong> Substitute n = 1, 2, 3:</p>
          <ul>
            <li>a<sub>1</sub> = 1 + 2 = <strong>3</strong></li>
            <li>a<sub>2</sub> = 4 + 4 = <strong>8</strong></li>
            <li>a<sub>3</sub> = 9 + 6 = <strong>15</strong></li>
          </ul>
          <p>\u2705 <strong>Series: 3 + 8 + 15.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q5.</strong> Expand <span class="tex" data-tex="\\sum_{k=1}^{10}(2k-1)">\u03a3(k=1 to 10)(2k \u2212 1)</span> and find its sum by pairing \u2014 no formula allowed.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 expand: k = 1\u202610 gives <strong>1, 3, 5, 7, 9, 11, 13, 15, 17, 19</strong>.</li>
            <li>Step 2 \u2014 pair first with last: (1 + 19) + (3 + 17) + (5 + 15) + (7 + 13) + (9 + 11).</li>
            <li>Step 3 \u2014 each pair = 20, and there are 5 pairs: 20 \u00d7 5 = <strong>100</strong>.</li>
          </ul>
          <p>\u2705 <strong>Sum = 100.</strong></p>
        </div></details>
        <h3>GP \u2014 general term</h3>
        <details class="qa"><summary><strong>Q6.</strong> Find the 10th term of the GP 5, 25, 125, \u2026</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 5, r = 25/5 = <strong>5</strong>.</li>
            <li>Step 2 \u2014 apply <span class="tex" data-tex="a_n = a\\cdot r^{n-1}">a<sub>n</sub> = a\u00b7r\u207f\u207b\u00b9</span>: <span class="tex" data-tex="a_{10} = 5\\cdot 5^9 = 5^{10}">a<sub>10</sub> = 5 \u00d7 5<sup>9</sup> = 5<sup>10</sup></span>.</li>
            <li>Step 3 \u2014 compute: 5<sup>9</sup> = 1,953,125, so 5<sup>10</sup> = 1,953,125 \u00d7 5 = <strong>9,765,625</strong>.</li>
          </ul>
          <p>\u2705 <strong>a<sub>10</sub> = 9,765,625.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q7.</strong> Which term of the GP <span class="tex" data-tex="2,\\ 2\\sqrt{2},\\ 4,\\ \\dots">2, 2\u221a2, 4, \u2026</span> is 128?</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 2, <span class="tex" data-tex="r = \\sqrt{2}">r = <strong>\u221a2</strong></span> (check: 4/(2\u221a2) = 2/\u221a2 = \u221a2 \u2713).</li>
            <li>Step 2 \u2014 set up: <span class="tex" data-tex="2\\cdot(\\sqrt{2})^{n-1} = 128">2\u00b7(\u221a2)\u207f\u207b\u00b9 = 128</span> \u2192 <span class="tex" data-tex="(\\sqrt{2})^{n-1} = 64">(\u221a2)\u207f\u207b\u00b9 = 64</span>.</li>
            <li>Step 3 \u2014 match powers of \u221a2: 64 = 2<sup>6</sup> = (\u221a2)<sup>12</sup>, so n \u2212 1 = 12 \u2192 <strong>n = 13</strong>.</li>
          </ul>
          <p>\u2705 <strong>128 is the 13th term.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q8.</strong> The 4th term of a GP is the square of its 2nd term, and the first term is \u22123. Find the 7th term.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 translate: <span class="tex" data-tex="a\\cdot r^3 = (a\\cdot r)^2 = a^2 r^2">a\u00b7r\u00b3 = (a\u00b7r)\u00b2 = a\u00b2r\u00b2</span>.</li>
            <li>Step 2 \u2014 substitute a = \u22123: <span class="tex" data-tex="-3r^3 = 9r^2">\u22123r\u00b3 = 9r\u00b2</span>. Since r \u2260 0, divide by 3r\u00b2: \u2212r = 3 \u2192 <strong>r = \u22123</strong>.</li>
            <li>Step 3 \u2014 verify: a<sub>4</sub> = \u22123 \u00d7 (\u221227) = 81; a<sub>2</sub> = \u22123 \u00d7 \u22123 = 9; 9\u00b2 = 81 \u2713.</li>
            <li>Step 4 \u2014 <span class="tex" data-tex="a_7 = a\\cdot r^6 = -3\\times(-3)^6 = -3\\times 729">a<sub>7</sub> = a\u00b7r<sup>6</sup> = \u22123 \u00d7 (\u22123)<sup>6</sup> = \u22123 \u00d7 729</span>.</li>
          </ul>
          <p>\u2705 <strong>a<sub>7</sub> = \u22122,187.</strong></p>
        </div></details>
        <h3>GP \u2014 sum of n terms</h3>
        <details class="qa"><summary><strong>Q9.</strong> Find the sum of 1 + 3 + 9 + \u2026 to 8 terms.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 1, r = 3, n = 8. Since r &gt; 1, use <span class="tex" data-tex="S_n = \\dfrac{a(r^n-1)}{r-1}">S<sub>n</sub> = a(r\u207f \u2212 1)/(r \u2212 1)</span>.</li>
            <li>Step 2 \u2014 powers: 3<sup>8</sup> = 6,561.</li>
            <li>Step 3 \u2014 <span class="tex" data-tex="S_8 = \\dfrac{6561-1}{2} = \\dfrac{6560}{2}">S<sub>8</sub> = (6,561 \u2212 1)/2 = 6,560/2</span>.</li>
          </ul>
          <p>\u2705 <strong>S<sub>8</sub> = 3,280.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q10.</strong> How many terms of the GP 3, 9, 27, \u2026 add up to 120?</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 3, r = 3. Equation: <span class="tex" data-tex="\\dfrac{3(3^n-1)}{3-1} = 120">3(3\u207f \u2212 1)/(3 \u2212 1) = 120</span>.</li>
            <li>Step 2 \u2014 simplify: 3(3\u207f \u2212 1)/2 = 120 \u2192 3\u207f \u2212 1 = 80 \u2192 3\u207f = 81 = 3<sup>4</sup> \u2192 <strong>n = 4</strong>.</li>
            <li>Step 3 \u2014 check: 3 + 9 + 27 + 81 = 120 \u2713.</li>
          </ul>
          <p>\u2705 <strong>4 terms.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q11.</strong> Find the sum to 20 terms of 0.15 + 0.015 + 0.0015 + \u2026</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 0.15, r = 0.015/0.15 = <strong>0.1</strong>.</li>
            <li>Step 2 \u2014 apply <span class="tex" data-tex="S_n = \\dfrac{a(1-r^n)}{1-r}">S<sub>n</sub> = a(1 \u2212 r\u207f)/(1 \u2212 r)</span>: <span class="tex" data-tex="S_{20} = \\dfrac{0.15(1-0.1^{20})}{0.9}">S<sub>20</sub> = 0.15(1 \u2212 0.1<sup>20</sup>)/0.9</span>.</li>
            <li>Step 3 \u2014 simplify: 0.15/0.9 = 15/90 = <strong>1/6</strong>.</li>
          </ul>
          <p>\u2705 <strong>S<sub>20</sub> = (1/6)(1 \u2212 10<sup>\u221220</sup>).</strong></p>
        </div></details>
        <h3>Infinite GP</h3>
        <details class="qa"><summary><strong>Q12.</strong> Find the sum to infinity of 0.5 + 0.05 + 0.005 + \u2026</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 0.5, r = 0.05/0.5 = <strong>0.1</strong>.</li>
            <li>Step 2 \u2014 check the condition: |0.1| &lt; 1 \u2713, so S<sub>\u221e</sub> exists.</li>
            <li>Step 3 \u2014 <span class="tex" data-tex="S_\\infty = \\dfrac{0.5}{1-0.1} = \\dfrac{0.5}{0.9} = \\dfrac{5}{9}">S<sub>\u221e</sub> = 0.5/(1 \u2212 0.1) = 0.5/0.9 = 5/9</span>.</li>
          </ul>
          <p>\u2705 <strong>S<sub>\u221e</sub> = 5/9.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q13.</strong> The sum to infinity of a GP is 15 and the common ratio is 2/3. Find the first term.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 write the equation: <span class="tex" data-tex="\\dfrac{a}{1-2/3} = 15">a/(1 \u2212 2/3) = 15</span>.</li>
            <li>Step 2 \u2014 simplify: a/(1/3) = 15 \u2192 3a = 15 \u2192 <strong>a = 5</strong>.</li>
            <li>Step 3 \u2014 sanity check: |2/3| &lt; 1 \u2713, and 5/(1/3) = 15 \u2713.</li>
          </ul>
          <p>\u2705 <strong>First term = 5.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q14 (trap demo).</strong> Can the sum to infinity of a GP (r \u2260 0) ever equal exactly half the first term?</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 set up: <span class="tex" data-tex="\\dfrac{a}{1-r} = \\dfrac{a}{2}">a/(1 \u2212 r) = a/2</span>. Since a \u2260 0, cancel a: <span class="tex" data-tex="\\dfrac{1}{1-r} = \\dfrac{1}{2}">1/(1 \u2212 r) = 1/2</span>.</li>
            <li>Step 2 \u2014 solve: 1 \u2212 r = 2 \u2192 <strong>r = \u22121</strong>.</li>
            <li>Step 3 \u2014 check the condition: |\u22121| = 1, which is NOT &lt; 1 \u2014 so no infinite sum exists for r = \u22121.</li>
          </ul>
          <p>\u2705 <strong>Impossible \u2014 this is exactly why you must verify |r| &lt; 1 first.</strong></p>
        </div></details>
        <h3>Geometric Mean</h3>
        <details class="qa"><summary><strong>Q15.</strong> Find the geometric mean of 0.04 and 0.09, and verify it sits in a GP.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 <span class="tex" data-tex="G = \\sqrt{0.04\\times 0.09} = \\sqrt{0.0036} = 0.06">G = \u221a(0.04 \u00d7 0.09) = \u221a0.0036 = <strong>0.06</strong></span> (positive root, per NCERT).</li>
            <li>Step 2 \u2014 verify: 0.06/0.04 = 1.5 and 0.09/0.06 = 1.5 \u2014 equal ratios \u2713.</li>
          </ul>
          <p>\u2705 <strong>GM = 0.06 (sequence 0.04, 0.06, 0.09).</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q16.</strong> Insert 4 geometric means between 2 and 64, then verify them with the product rule.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 64 is the 6th term: <span class="tex" data-tex="64 = 2\\cdot r^5 \\Rightarrow r^5 = 32 \\Rightarrow r = 2">64 = 2\u00b7r<sup>5</sup> \u2192 r<sup>5</sup> = 32 \u2192 <strong>r = 2</strong></span>.</li>
            <li>Step 2 \u2014 the means: 2\u00d72 = <strong>4</strong>, then <strong>8</strong>, <strong>16</strong>, <strong>32</strong> (check: 32 \u00d7 2 = 64 \u2713).</li>
            <li>Step 3 \u2014 product rule: 4 \u00d7 8 \u00d7 16 \u00d7 32 = 16,384; <span class="tex" data-tex="(ab)^{n/2} = (2\\times 64)^2 = 128^2 = 16384">(ab)\u207f\u207e\u00b2 = (2 \u00d7 64)\u00b2 = 128\u00b2 = 16,384</span> \u2713.</li>
          </ul>
          <p>\u2705 <strong>GMs: 4, 8, 16, 32.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q17.</strong> Three positive numbers x, 10, y are in GP and x + y = 52. Find x and y.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 GM condition: <span class="tex" data-tex="10^2 = xy \\Rightarrow xy = 100">10\u00b2 = xy \u2192 <strong>xy = 100</strong></span>.</li>
            <li>Step 2 \u2014 with x + y = 52, x and y are roots of <span class="tex" data-tex="t^2 - 52t + 100 = 0">t\u00b2 \u2212 52t + 100 = 0</span>.</li>
            <li>Step 3 \u2014 <span class="tex" data-tex="t = \\frac{52\\pm\\sqrt{2704-400}}{2} = \\frac{52\\pm 48}{2}">t = (52 \u00b1 \u221a(2,704 \u2212 400))/2 = (52 \u00b1 48)/2</span> \u2192 t = 50 or t = 2.</li>
          </ul>
          <p>\u2705 <strong>{x, y} = {50, 2}</strong> \u2014 i.e. 50, 10, 2 (r = 1/5) or 2, 10, 50 (r = 5).</p>
        </div></details>
        <h3>AM\u2013GM relation</h3>
        <details class="qa"><summary><strong>Q18.</strong> The AM and GM of two positive numbers are 10 and 8 respectively. Find the numbers.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 translate: <span class="tex" data-tex="\\frac{a+b}{2} = 10 \\Rightarrow a+b = 20">(a + b)/2 = 10 \u2192 <strong>a + b = 20</strong></span>; <span class="tex" data-tex="\\sqrt{ab} = 8 \\Rightarrow ab = 64">\u221a(ab) = 8 \u2192 <strong>ab = 64</strong></span>.</li>
            <li>Step 2 \u2014 a and b are roots of <span class="tex" data-tex="t^2 - 20t + 64 = 0">t\u00b2 \u2212 20t + 64 = 0</span>.</li>
            <li>Step 3 \u2014 <span class="tex" data-tex="t = \\frac{20\\pm\\sqrt{400-256}}{2} = \\frac{20\\pm 12}{2}">t = (20 \u00b1 \u221a(400 \u2212 256))/2 = (20 \u00b1 12)/2</span> \u2192 t = 16 or t = 4.</li>
          </ul>
          <p>\u2705 <strong>The numbers are 4 and 16</strong> (check: (4+16)/2 = 10 \u2713, \u221a(64) = 8 \u2713).</p>
        </div></details>
        <details class="qa"><summary><strong>Q19.</strong> For x &gt; 0, prove that <span class="tex" data-tex="x + \\frac{1}{x} \\geq 2">x + 1/x \u2265 2</span>, and state when equality holds.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 apply AM \u2265 GM to the two positive numbers x and 1/x: <span class="tex" data-tex="\\frac{x + 1/x}{2} \\geq \\sqrt{x\\cdot 1/x}">(x + 1/x)/2 \u2265 \u221a(x \u00b7 1/x)</span>.</li>
            <li>Step 2 \u2014 simplify: \u221a(1) = 1, so <span class="tex" data-tex="x + \\frac{1}{x} \\geq 2">x + 1/x \u2265 <strong>2</strong></span>.</li>
            <li>Step 3 \u2014 equality iff the two numbers are equal: <span class="tex" data-tex="x = \\frac{1}{x} \\Rightarrow x^2 = 1 \\Rightarrow x = 1">x = 1/x \u2192 x\u00b2 = 1 \u2192 <strong>x = 1</strong></span> (x &gt; 0).</li>
          </ul>
          <p>\u2705 <strong>Proved; equality at x = 1.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q20.</strong> Prove that <span class="tex" data-tex="a^2 + b^2 \\geq 2ab">a\u00b2 + b\u00b2 \u2265 2ab</span> for all real a, b, using AM \u2265 GM.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 easy case first: if ab \u2264 0, then 2ab \u2264 0 \u2264 a\u00b2 + b\u00b2 (a sum of squares is never negative) \u2014 done.</li>
            <li>Step 2 \u2014 now let ab &gt; 0, so a\u00b2 and b\u00b2 are both positive. Apply AM \u2265 GM to them: <span class="tex" data-tex="\\frac{a^2+b^2}{2} \\geq \\sqrt{a^2b^2} = |ab| = ab">(a\u00b2 + b\u00b2)/2 \u2265 \u221a(a\u00b2b\u00b2) = |ab| = ab</span> (since ab &gt; 0).</li>
            <li>Step 3 \u2014 multiply by 2: a\u00b2 + b\u00b2 \u2265 2ab. Equality iff a\u00b2 = b\u00b2, i.e. a = \u00b1b (with ab \u2265 0 this means a = b).</li>
          </ul>
          <p>\u2705 <strong>Proved for all real a, b.</strong></p>
        </div></details>
        <h3>Appendix R practice (removed from boards \u2014 reference only)</h3>
        <details class="qa"><summary><strong>Q21.</strong> Find the 20th term of the AP 10, 7, 4, \u2026</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 identify: a = 10, d = 7 \u2212 10 = <strong>\u22123</strong> (APs can decrease!).</li>
            <li>Step 2 \u2014 <span class="tex" data-tex="a_{20} = a + 19d = 10 + 19\\times(-3) = 10 - 57">a<sub>20</sub> = a + 19d = 10 + 19 \u00d7 (\u22123) = 10 \u2212 57</span>.</li>
          </ul>
          <p>\u2705 <strong>a<sub>20</sub> = \u221247.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q22.</strong> Find the sum of the first 15 multiples of 8.</summary><div class="sol">
          <ul>
            <li>Step 1 \u2014 the series is 8, 16, \u2026, 120 (15th term = 8 \u00d7 15 = 120).</li>
            <li>Step 2 \u2014 use <span class="tex" data-tex="S_n = \\frac{n}{2}\\cdot(a+l)">S<sub>n</sub> = n/2\u00b7(a + l)</span>: <span class="tex" data-tex="S_{15} = \\frac{15}{2}\\times(8+120) = 15\\times 64">S<sub>15</sub> = 15/2 \u00d7 (8 + 120) = 15 \u00d7 64</span>.</li>
          </ul>
          <p>\u2705 <strong>S<sub>15</sub> = 960.</strong></p>
        </div></details>
        <details class="qa"><summary><strong>Q23.</strong> Find <span class="tex" data-tex="1^2 + 2^2 + \\dots + 10^2">1\u00b2 + 2\u00b2 + \u2026 + 10\u00b2</span>.</summary><div class="sol">
          <ul>
            <li>Apply <span class="tex" data-tex="\\sum n^2 = \\frac{n(n+1)(2n+1)}{6}">\u03a3n\u00b2 = n(n+1)(2n+1)/6</span> with n = 10: <span class="tex" data-tex="\\frac{10\\times 11\\times 21}{6} = \\frac{2310}{6}">10 \u00d7 11 \u00d7 21/6 = 2,310/6</span>.</li>
          </ul>
          <p>\u2705 <strong>Sum = 385.</strong></p>
        </div></details>
      </section>

      <!-- R. Appendix -->
      <section id="appendix-r" class="fade-in">
        <h2>R. &#x1f4e6; Appendix R \u2014 Removed from rationalized NCERT (reference only)</h2>
        <div class="callout">Everything below was in the <strong>old</strong> Chapter 9 but was <strong>deleted in the 2023 rationalization</strong> (old \u00a79.4 AP theory, old \u00a79.7 special sums, with related examples/exercises). Revise it only if your school test follows the old book. Formulas here are still mathematically correct.</div>
        <h3>R1. Arithmetic Progression (AP) \u2014 essentials</h3>
        <ul>
          <li><strong>Definition:</strong> <span class="tex" data-tex="a_{n+1} = a_n + d">a<sub>n+1</sub> = a<sub>n</sub> + d</span>, constant difference d (any real \u2014 APs can decrease!). Form: <span class="tex" data-tex="a,\\ a+d,\\ a+2d,\\ \\dots">a, a+d, a+2d, \u2026</span></li>
          <li><strong>nth term:</strong> <span class="tex" data-tex="a_n = a + (n-1)d">a<sub>n</sub> = a + (n\u22121)d</span>. Last term <span class="tex" data-tex="l = a + (n-1)d">l = a + (n\u22121)d</span>.</li>
          <li><strong>Sum:</strong> <span class="tex" data-tex="S_n = \\frac{n}{2}\\cdot[2a+(n-1)d] = \\frac{n}{2}\\cdot(a+l)">S<sub>n</sub> = n/2\u00b7[2a + (n\u22121)d] = <strong>n/2\u00b7(a + l)</strong></span>.</li>
          <li><strong>Term from sum:</strong> <span class="tex" data-tex="a_n = S_n - S_{n-1}\\ \\ (n \\geq 2)">a<sub>n</sub> = S<sub>n</sub> \u2212 S<sub>n\u22121</sub> (n \u2265 2)</span>; <span class="tex" data-tex="a_1 = S_1">a<sub>1</sub> = S<sub>1</sub></span>. If <span class="tex" data-tex="S_n = pn + qn^2">S<sub>n</sub> = pn + qn\u00b2</span> then <span class="tex" data-tex="d = 2q">d = 2q</span>.</li>
          <li><strong>Single AM:</strong> a, A, b in AP \u2192 <span class="tex" data-tex="A = \\frac{a+b}{2}">A = (a+b)/2</span>.</li>
          <li><strong>n AMs between a and b:</strong> <span class="tex" data-tex="d = \\frac{b-a}{n+1}">d = (b\u2212a)/(n+1)</span>, <span class="tex" data-tex="A_k = a + k\\cdot d">A<sub>k</sub> = a + k\u00b7d</span>. Their sum = <span class="tex" data-tex="\\frac{n(a+b)}{2}">n(a+b)/2</span>.</li>
          <li><strong>Worked:</strong> 3, 7, 11, \u2026 (a = 3, d = 4): <span class="tex" data-tex="a_{10} = 3 + 9\\times 4 = 39">a<sub>10</sub> = 3 + 9\u00d74 = <strong>39</strong></span>; <span class="tex" data-tex="S_{10} = \\frac{10}{2}\\times(3+39) = 210">S<sub>10</sub> = 10/2\u00d7(3+39) = 5\u00d742 = <strong>210</strong></span>.</li>
          <li><strong>Worked:</strong> 3 AMs between 4 and 16: <span class="tex" data-tex="d = \\frac{12}{4} = 3">d = 12/4 = 3</span> \u2192 <strong>7, 10, 13</strong> (sum 30 = 3\u00d720/2 \u2713).</li>
        </ul>
        <h3>R2. Special sums (deleted from board assessment \u2014 practice only)</h3>
        <ul>
          <li><span class="tex" data-tex="\\sum n = \\frac{n(n+1)}{2}">\u03a3n = 1+2+\u2026+n = <strong>n(n+1)/2</strong></span></li>
          <li><span class="tex" data-tex="\\sum n^2 = \\frac{n(n+1)(2n+1)}{6}">\u03a3n\u00b2 = 1\u00b2+2\u00b2+\u2026+n\u00b2 = <strong>n(n+1)(2n+1)/6</strong></span></li>
          <li><span class="tex" data-tex="\\sum n^3 = \\left[\\frac{n(n+1)}{2}\\right]^2 = \\left(\\sum n\\right)^2">\u03a3n\u00b3 = 1\u00b3+2\u00b3+\u2026+n\u00b3 = <strong>[n(n+1)/2]\u00b2 = (\u03a3n)\u00b2</strong></span></li>
          <li>Check at n = 3: <span class="tex" data-tex="6 = \\frac{3\\times 4}{2}">6 = 3\u00d74/2</span> \u2713; <span class="tex" data-tex="14 = \\frac{3\\times 4\\times 7}{6}">1+4+9 = 14 = 3\u00d74\u00d77/6</span> \u2713; <span class="tex" data-tex="36 = 6^2">1+8+27 = 36 = 6\u00b2</span> \u2713.</li>
          <li>Method (old NCERT): if <span class="tex" data-tex="a_n">a<sub>n</sub></span> is a polynomial in n, split into <span class="tex" data-tex="\\sum n^3/\\sum n^2/\\sum n">\u03a3n\u00b3/\u03a3n\u00b2/\u03a3n</span>/constant pieces and sum each.</li>
        </ul>
        <h3>R3. Things the internet adds that were NEVER in this chapter</h3>
        <p>Harmonic Mean <span class="tex" data-tex="\\frac{2ab}{a+b}">2ab/(a+b)</span>, <span class="tex" data-tex="H<G<A">H&lt;G&lt;A</span> chains, <span class="tex" data-tex="G^2 = AH">G\u00b2 = AH</span>, arithmetico-geometric series, <span class="tex" data-tex="a-d,\\ a,\\ a+d">"a\u2212d, a, a+d"</span> selection templates, boxed odd/even sums \u2014 <strong>none of these are in NCERT Sequences and Series</strong>. Ignore them for boards.</p>
      </section>

      <hr>

      <!-- Key Terms -->
      <section id="key-terms" class="fade-in">
        <h2>&#x1f4dd; Key Terms to Remember</h2>
        <div class="terms-grid">
          __TERMS__
        </div>
      </section>

      <hr>

      <!-- Quick Recap -->
      <section id="quick-recap" class="fade-in">
        <h2>&#x1f504; Quick Recap (60-second self-test \u2014 answers in brackets)</h2>
        <ul>
          <li>Sequence vs series in one line? (List in order vs list joined by +.)</li>
          <li>GP general term + why n\u22121? (<span class="tex" data-tex="a_n = ar^{n-1}">a<sub>n</sub> = ar\u207f\u207b\u00b9</span>; first term needs <span class="tex" data-tex="r^0">r\u2070</span>.)</li>
          <li>Both GP sum forms + the r = 1 case? (Fractions for <span class="tex" data-tex="r \\neq 1">r \u2260 1</span>; <span class="tex" data-tex="S_n = na">S<sub>n</sub> = na</span> for r = 1.)</li>
          <li>Infinite GP condition + formula? (<span class="tex" data-tex="|r| < 1">|r| &lt; 1</span>, then <span class="tex" data-tex="\\dfrac{a}{1-r}">a/(1\u2212r)</span>.)</li>
          <li>Single GM + single AM? (<span class="tex" data-tex="\\sqrt{ab}">\u221a(ab)</span>; <span class="tex" data-tex="\\frac{a+b}{2}">(a+b)/2</span>.)</li>
          <li>AM \u2265 GM proof in 3 lines + equality case? (<span class="tex" data-tex="\\dfrac{(\\sqrt{a}-\\sqrt{b})^2}{2} \\geq 0">(\u221aa\u2212\u221ab)\u00b2/2 \u2265 0</span>; equality iff a = b.)</li>
          <li>Spot checks: <span class="tex" data-tex="S_\\infty">S<sub>\u221e</sub></span> of <span class="tex" data-tex="5 + \\frac{5}{3} + \\frac{5}{9} + \\dots\\ \\left[= \\frac{15}{2}\\right]">5 + 5/3 + 5/9 + \u2026 [= 15/2]</span>; one GM between 2 and 8 [= 4]; <span class="tex" data-tex="a_6">a<sub>6</sub></span> of 2, 6, 18, \u2026 [= 486].</li>
        </ul>
      </section>
"""


def build():
    ref = BST_REF.read_text(encoding="utf-8")
    style, inline_js = extract_shell(ref)

    terms_html = "".join(
        f'<div class="term"><strong>{t}</strong><span>{d}</span></div>'
        for t, d in KEY_TERMS
    )
    body = BODY.replace("__TERMS__", terms_html)

    # Every TOC link must land on a real section id.
    ids = set(re.findall(r'<section id="([^"]+)"', body))
    for anchor, _label, _cls in TOC:
        assert anchor in ids, f"TOC anchor #{anchor} has no matching section"

    # Every data-tex attribute must be present and parse-level sane.
    texs = re.findall(r'data-tex="([^"]+)"', body)
    assert texs, "no data-tex formulas found"
    for t in texs:
        assert t.count("{") == t.count("}"), f"unbalanced braces in: {t[:80]}"
        assert "\\u" not in t and "&#" not in t, f"bad escape in: {t[:80]}"

    key_terms_data = json.dumps(
        [{"term": t, "definition": d} for t, d in KEY_TERMS[:8]],
        ensure_ascii=False,
    )
    mindmap_json = json.dumps(MINDMAP_MD, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{PAGE_TITLE}</title>
  <meta name="description" content="{META_DESC}">
  <meta name="chapter-id" content="maths-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/study-os.css">
  {HEAD_EXTRA}
  {style}
  {TEX_CSS}
</head>
<body>

  <!-- Nav -->
  <nav class="top-nav">
    <a href="../index.html" class="logo">{NAV_LOGO}</a>
    <span class="meta">{NAV_META}</span>
    <button class="mindmap-toggle" aria-label="Open mind map" title="Mind Map"><span class="mm-icon">\U0001f5fa\ufe0f</span> Mind Map</button>
  </nav>

  <!-- Progress -->
  <div class="progress-bar"><div class="fill" id="progressFill"></div></div>

<!-- Mobile TOC Toggle -->
  <button class="toc-toggle" id="tocToggle" aria-label="Toggle table of contents">\u2630 Contents</button>

  <!-- Layout -->
  <div class="wrapper">

    <!-- Sidebar TOC -->
    <aside class="toc" id="toc">
      {toc_html()}
    </aside>

    <!-- Main Content -->
    <main class="content">

      <!-- Hero -->
      <header class="hero fade-in">
        <span class="chapter-badge">{BADGE}</span>
        <h1>{H1}</h1>
        <p class="subtitle">{SUBTITLE}</p>
      </header>

{body}
      <script>
        const KEY_TERMS_DATA = {key_terms_data};
      </script>

      <footer>
        <p>{FOOTER}</p>
      </footer>

    </main>
  </div>

  {inline_js}
  {RENDER_JS}

  <script id="chapter-mindmap-data" type="application/json">{mindmap_json}
  </script>

  <script src="../assets/study-os.js"></script>
<script src="../assets/toc-scrollspy.js"></script>
</body>
</html>"""

    ROOT.mkdir(parents=True, exist_ok=True)
    out = ROOT / "Chapter-8-Sequences-and-Series.html"
    out.write_text(html, encoding="utf-8")
    print(f"{out.name}: {len(TOC)} sections, {len(texs)} LaTeX formulas, {len(html)} chars")


build()
