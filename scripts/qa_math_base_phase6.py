#!/usr/bin/env python3
"""Phase 6 QA gate for math-base integration (build-math-lesson.md)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
MATH = ROOT / "bai-hoc" / "math-base"
SNAP = ROOT / "_snapshots" / "math-base-phase0"
AUDIT = ROOT / "_snapshots" / "math-base-phase0-audit.json"

CHAPTERS = [
    ("01-probability", "1. Probability"),
    ("02-statistics", "2. Statistics"),
    ("03-linear-algebra", "3. Linear Algebra"),
    ("04-calculus", "4. Calculus"),
    ("05-optimization", "5. Optimization"),
    ("06-information-theory", "6. Information Theory"),
    ("07-graph-theory", "7. Graph Theory"),
]

HEAVY = [
    "01-probability/conditional-probability.html",
    "04-calculus/the-chain-rule.html",
    "03-linear-algebra/matrix-calculus.html",
    "04-calculus/partial-derivatives.html",
]


def ok(name: str, passed: bool, detail: str = "") -> bool:
    mark = "PASS" if passed else "FAIL"
    extra = f" — {detail}" if detail else ""
    print(f"[{mark}] {name}{extra}")
    return passed


def strip_fm_and_crosslink(text: str) -> str:
    if text.startswith("---"):
        text = text.split("---", 2)[2].lstrip("\n")
    # Phase 5 callouts appended after original body
    text = text.split("<!-- CROSSLINK_MATH_THEORY -->")[0]
    return text


def normalize_math_delimiters_for_compare(snap: str) -> str:
    """Apply same [ → $$ transform used in Phase 2 (line-only fences)."""
    lines = snap.splitlines(keepends=True)
    out = []
    i = 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if not in_fence and stripped == "[":
            nl = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
            out.append("$$" + nl)
            i += 1
            while i < len(lines):
                if lines[i].strip() == "]":
                    c = lines[i]
                    cnl = "\r\n" if c.endswith("\r\n") else ("\n" if c.endswith("\n") else "")
                    out.append("$$" + cnl)
                    i += 1
                    break
                out.append(lines[i])
                i += 1
            continue
        out.append(line)
        i += 1
    text = "".join(out)

    # Escape bare % inside $ / $$ (Phase 2)
    parts = []
    i = 0
    n = len(text)

    def esc(s: str) -> str:
        return re.sub(r"(?<!\\)%", r"\\%", s)

    while i < n:
        if text.startswith("```", i):
            end = text.find("```", i + 3)
            if end < 0:
                parts.append(text[i:])
                break
            parts.append(text[i : end + 3])
            i = end + 3
            continue
        if text.startswith("$$", i):
            end = text.find("$$", i + 2)
            if end < 0:
                parts.append(text[i:])
                break
            parts.append("$$" + esc(text[i + 2 : end]) + "$$")
            i = end + 2
            continue
        if text[i] == "$" and not text.startswith("$$", i):
            end = i + 1
            while end < n:
                if text[end] == "\\" and end + 1 < n:
                    end += 2
                    continue
                if text[end] == "$":
                    break
                end += 1
            if end < n and text[end] == "$":
                parts.append("$" + esc(text[i + 1 : end]) + "$")
                i = end + 1
                continue
        parts.append(text[i])
        i += 1
    return "".join(parts)


def main() -> int:
    results = []

    # 1) Render artifacts exist; whitelist exclusions
    math_html = list((SITE / "bai-hoc" / "math-base").rglob("*.html"))
    results.append(
        ok(
            "Render math-base HTML",
            len(math_html) >= 68,
            f"{len(math_html)} html under _site/bai-hoc/math-base",
        )
    )
    results.append(ok("No du-an in _site", not (SITE / "du-an").exists()))
    results.append(ok("No nghien-cuu in _site", not (SITE / "nghien-cuu").exists()))

    # 2) Sidebar no nested folder (sample lesson)
    sample = SITE / "bai-hoc/math-base/01-probability/conditional-probability.html"
    if sample.exists():
        html = sample.read_text(encoding="utf-8", errors="replace")
        texts = re.findall(r'class="menu-text">([^<]+)</span>', html)
        nested = [t for t in texts if re.match(r"^0\d[\s-]", t) or t in {"01 Probability", "01-probability"}]
        results.append(ok("Sidebar không lồng folder", not nested, f"bad={nested[:5]}"))
        sections = [t for t in texts if re.match(r"^\d+\. ", t)]
        # Unique section labels for math sidebar
        want = [c[1] for c in CHAPTERS]
        has_all = all(any(w == s for s in sections) for w in want)
        results.append(ok("Sidebar 7 chapter labels", has_all, f"found={sorted(set(sections))[:10]}…"))
        results.append(ok("Page navigation present", "page-navigation" in html))
    else:
        results.append(ok("Sidebar sample exists", False, str(sample)))

    # 3) Sample HTML ≥1/chapter + heavy formulas
    for chap, _ in CHAPTERS:
        files = list((SITE / "bai-hoc/math-base" / chap).glob("*.html"))
        results.append(ok(f"Sample chapter {chap}", len(files) >= 1, f"{len(files)} html"))
    for rel in HEAVY:
        p = SITE / "bai-hoc/math-base" / rel
        if not p.exists():
            results.append(ok(f"Heavy {rel}", False, "missing"))
            continue
        h = p.read_text(encoding="utf-8", errors="replace")
        displays = h.count('class="math display"')
        bare = len(re.findall(r"<p>\[</p>", h))
        results.append(
            ok(
                f"Heavy math {rel}",
                displays >= 5 and bare == 0,
                f"display≈{displays}, bare[={bare}",
            )
        )

    # 4) Listing / RSS
    bh = SITE / "bai-hoc/index.html"
    rss = SITE / "bai-hoc/index.xml"
    if bh.exists():
        t = bh.read_text(encoding="utf-8", errors="replace")
        results.append(ok("Listing có Math Base", "Math Base" in t and "math-base" in t))
    else:
        results.append(ok("Listing bai-hoc", False))
    if rss.exists():
        x = rss.read_text(encoding="utf-8", errors="replace")
        results.append(ok("RSS có math-base", "math-base" in x))
    else:
        results.append(ok("RSS index.xml exists", False))

    # 5) Mobile overflow CSS for math / tables
    scss = (ROOT / "assets/css/custom.scss").read_text(encoding="utf-8")
    has_table_overflow = "overflow-x: auto" in scss
    # Prefer dedicated math overflow rule (may be added in Phase 6)
    has_math_overflow = "math display" in scss or ".MathJax" in scss or "mjx-container" in scss
    results.append(
        ok(
            "Overflow CSS (tables/code or math)",
            has_table_overflow or has_math_overflow,
            f"table/code={has_table_overflow}, math={has_math_overflow}",
        )
    )

    # 6) Body vs snapshot (S2): allow FM + Phase2 delimiter + Phase5 callout
    if not AUDIT.exists() or not SNAP.exists():
        results.append(ok("Snapshot available", False))
    else:
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        fail = []
        for item in audit["lessons"]:
            snap_p = SNAP / item["source"]
            cur_p = MATH / item["target_dir"] / item["target_file"]
            if not snap_p.exists() or not cur_p.exists():
                fail.append(item["target_file"] + ":missing")
                continue
            snap = snap_p.read_text(encoding="utf-8")
            expected = normalize_math_delimiters_for_compare(snap)
            actual = strip_fm_and_crosslink(cur_p.read_text(encoding="utf-8"))
            if expected != actual:
                # tolerate trailing newline differences
                if expected.rstrip("\n") != actual.rstrip("\n"):
                    fail.append(item["target_file"])
        results.append(
            ok(
                "Body diff vs snapshot (S2)",
                len(fail) == 0,
                f"mismatches={len(fail)}" + (f" e.g. {fail[:3]}" if fail else ""),
            )
        )

    # 7) Homepage / about / README / JS 4 chuỗi
    idx = (SITE / "index.html").read_text(encoding="utf-8", errors="replace")
    about = (SITE / "about.html").read_text(encoding="utf-8", errors="replace")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cont = (ROOT / "assets/js/home-continue.html").read_text(encoding="utf-8")
    prog = (ROOT / "assets/js/lesson-progress.html").read_text(encoding="utf-8")
    results.append(ok("Homepage CTA Math Base", "Bắt đầu Math Base" in idx and "series-card--math" in idx))
    results.append(ok("Homepage 4 chuỗi", "Bốn chuỗi" in idx))
    results.append(ok("About Math trước Theory", about.find("Math Base") < about.find("Theory AI")))
    results.append(ok("README 4 chuỗi / Math", "Math Base" in readme and "Bốn chuỗi" in readme))
    results.append(ok("JS continue Math Base", "Math Base" in cont and "math-base" in cont))
    results.append(
        ok(
            "Completion Math → Theory",
            "message-passing-neural-networks" in prog and "hoàn thành chuỗi Math Base" in prog,
        )
    )
    results.append(ok("Narrative Math→Theory in JS", "Tiếp: Theory AI" in prog))

    # 8) Navbar order Math before Theory
    dd = re.findall(r'class="dropdown-text">([^<]+)</span>', idx)
    if "Math Base" in dd and "Theory AI" in dd:
        results.append(ok("Navbar Math trước Theory", dd.index("Math Base") < dd.index("Theory AI"), str(dd)))
    else:
        results.append(ok("Navbar Math/Theory present", False, str(dd)))

    # 9) Bracket blocks remaining in sources
    rem = 0
    for p in MATH.rglob("*.qmd"):
        lines = p.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == "[":
                rem += 1
                i += 1
                while i < len(lines) and lines[i].strip() != "]":
                    i += 1
                i += 1
            else:
                i += 1
    results.append(ok("No leftover [ math blocks", rem == 0, f"remaining={rem}"))

    failed = sum(1 for r in results if not r)
    print(f"\n=== Phase 6 QA: {len(results) - failed}/{len(results)} passed ===")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
