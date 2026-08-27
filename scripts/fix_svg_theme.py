#!/usr/bin/env python3
"""Normalize lesson SVGs for Quarto dark/light toggle.

External <img> SVGs cannot read data-bs-theme. Strategy:
1. Architecture: remove .fig-bg fill + prefers-color-scheme (transparent canvas).
2. Theory (and any ink-class SVGs): strip @media (prefers-color-scheme: dark)
   blocks so ink stays light-theme readable; CSS puts a light plate behind the image.

Site CSS (custom.scss) supplies the plate via var / forced light background in dark mode.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STYLE_MEDIA_RE = re.compile(
    r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{(?:[^{}]|\{[^{}]*\})*\}",
    re.S,
)
# Compact one-liner CDATA styles used by Architecture Models
CDATA_FIG_BG_RE = re.compile(
    r"<style><!\[CDATA\[\.fig-bg\s*\{[^}]*\}\s*"
    r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*\.fig-bg\s*\{[^}]*\}\s*\}\s*"
    r"\]\]></style>",
    re.S,
)
FIG_BG_RECT_RE = re.compile(
    r'<rect\s+class="fig-bg"[^>]*?/?>\s*',
    re.S,
)
INLINE_FIG_FILL_RE = re.compile(
    r'(<rect\s+class="fig-bg"[^>]*?\sfill=")#[0-9A-Fa-f]{3,8}(")',
    re.S,
)


def patch_svg(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    orig = text

    if CDATA_FIG_BG_RE.search(text):
        text = CDATA_FIG_BG_RE.sub("", text)
        notes.append("removed-cdata-fig-bg-style")

    if STYLE_MEDIA_RE.search(text):
        text = STYLE_MEDIA_RE.sub("", text)
        notes.append("stripped-prefers-dark")

    # Transparent / remove opaque fig-bg fill
    if 'class="fig-bg"' in text:
        text2, n = INLINE_FIG_FILL_RE.subn(r"\1none\2", text)
        if n:
            text = text2
            notes.append(f"fig-bg-fill-none:{n}")
        # also remove fill attribute duplicates on class fig-bg with fill= after class
        text3, n3 = re.subn(
            r'(<rect class="fig-bg"[^>]*?)(\sfill="[^"]*")',
            lambda m: m.group(1) if 'fill="none"' in m.group(0) else m.group(1) + ' fill="none"',
            text,
        )
        # Simpler: force fill="none" on fig-bg rects
        def _fig_rect(m: re.Match) -> str:
            tag = m.group(0)
            if re.search(r'\sfill="', tag):
                tag = re.sub(r'\sfill="[^"]*"', ' fill="none"', tag, count=1)
            else:
                tag = tag.replace("<rect", '<rect fill="none"', 1)
            return tag

        text, n4 = re.subn(r"<rect\b[^>]*class=\"fig-bg\"[^>]*/?>", _fig_rect, text)
        if n4:
            notes.append(f"fig-bg-transparent:{n4}")

    # Clean empty style tags left behind
    text = re.sub(r"<style>\s*</style>\s*", "", text)
    text = re.sub(r"<style><!\[CDATA\[\s*\]\]></style>\s*", "", text)

    if text != orig and not notes:
        notes.append("changed")
    return text, notes


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed = 0
    scanned = 0
    for path in sorted(ROOT.rglob("*.svg")):
        if any(x in path.parts for x in ("_site", ".quarto", "node_modules")):
            continue
        # keep brand assets as-is (already light/dark aware via page CSS)
        if path.as_posix().startswith("assets/img/"):
            continue
        scanned += 1
        raw = path.read_text(encoding="utf-8", errors="replace")
        # Skip binary-corrupted
        try:
            raw.encode("utf-8")
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print("skip-encoding", path)
            continue
        new, notes = patch_svg(text)
        if not notes:
            continue
        changed += 1
        if dry:
            print("would", path, notes)
        else:
            path.write_text(new, encoding="utf-8")
    print(f"scanned={scanned} changed={changed} dry={dry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
