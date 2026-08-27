#!/usr/bin/env python3
"""Phase 2: normalize math delimiters in math-base (build-math-lesson.md).

- Convert block [ ... ] (lines that are only [ / ]) to $$ ... $$
- Escape bare % inside math to \\% for MathJax
- Do not rewrite LaTeX content; skip fenced code blocks
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH_ROOT = ROOT / "bai-hoc" / "math-base"

# Priority files from plan (Matrix Calculus already uses $$; still run % escape)
PRIORITY = [
    MATH_ROOT / "01-probability" / "conditional-probability.qmd",
    MATH_ROOT / "04-calculus" / "the-chain-rule.qmd",
    MATH_ROOT / "03-linear-algebra" / "matrix-calculus.qmd",
    MATH_ROOT / "04-calculus" / "partial-derivatives.qmd",
]


def count_bracket_blocks(text: str) -> int:
    n = 0
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "[":
            n += 1
            i += 1
            while i < len(lines) and lines[i].strip() != "]":
                i += 1
            i += 1
        else:
            i += 1
    return n


def convert_bracket_blocks(text: str) -> tuple[str, int]:
    """Replace line-only [ / ] math fences with $$. Skip fenced code."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    converted = 0
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
            # Collect until closing ]
            nl = "\n" if line.endswith("\n") else ""
            # preserve original newline style from opening line
            if line.endswith("\r\n"):
                nl = "\r\n"
            elif line.endswith("\n"):
                nl = "\n"
            else:
                nl = ""

            out.append("$$" + nl)
            i += 1
            while i < len(lines):
                if lines[i].strip() == "]":
                    closing = lines[i]
                    if closing.endswith("\r\n"):
                        cnl = "\r\n"
                    elif closing.endswith("\n"):
                        cnl = "\n"
                    else:
                        cnl = ""
                    out.append("$$" + cnl)
                    i += 1
                    converted += 1
                    break
                out.append(lines[i])  # formula lines unchanged
                i += 1
            else:
                # Unclosed — restore opening as-is (should not happen)
                raise ValueError("Unclosed [ math block")
            continue

        out.append(line)
        i += 1

    return "".join(out), converted


def escape_percent_in_math(text: str) -> tuple[str, int]:
    """Escape bare % inside $…$ and $$…$$; skip code fences."""
    escapes = 0
    parts: list[str] = []
    i = 0
    n = len(text)

    def escape_inner(s: str) -> str:
        nonlocal escapes
        out = []
        j = 0
        while j < len(s):
            if s[j] == "%" and (j == 0 or s[j - 1] != "\\"):
                out.append("\\%")
                escapes += 1
            else:
                out.append(s[j])
            j += 1
        return "".join(out)

    while i < n:
        # fenced code
        if text.startswith("```", i):
            end = text.find("```", i + 3)
            if end == -1:
                parts.append(text[i:])
                break
            parts.append(text[i : end + 3])
            i = end + 3
            continue

        # display math $$
        if text.startswith("$$", i):
            end = text.find("$$", i + 2)
            if end == -1:
                parts.append(text[i:])
                break
            inner = text[i + 2 : end]
            parts.append("$$" + escape_inner(inner) + "$$")
            i = end + 2
            continue

        # inline math $…$ (not $$)
        if text[i] == "$" and not text.startswith("$$", i):
            end = i + 1
            while end < n:
                if text[end] == "\\" and end + 1 < n:
                    end += 2
                    continue
                if text[end] == "$":
                    break
                end += 1
            if end >= n or text[end] != "$":
                parts.append(text[i])
                i += 1
                continue
            inner = text[i + 1 : end]
            parts.append("$" + escape_inner(inner) + "$")
            i = end + 1
            continue

        parts.append(text[i])
        i += 1

    return "".join(parts), escapes


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    before_brackets = count_bracket_blocks(original)

    text, converted = convert_bracket_blocks(original)
    text, pct_escapes = escape_percent_in_math(text)

    after_brackets = count_bracket_blocks(text)
    changed = text != original
    if changed:
        path.write_text(text, encoding="utf-8")

    return {
        "file": str(path.relative_to(MATH_ROOT)),
        "bracket_before": before_brackets,
        "converted": converted,
        "bracket_after": after_brackets,
        "percent_escapes": pct_escapes,
        "changed": changed,
    }


def main() -> None:
    results = []
    # All qmd under math-base (bracket convert only hits 2 files; % may hit more)
    for path in sorted(MATH_ROOT.rglob("*.qmd")):
        results.append(process_file(path))

    converted_files = [r for r in results if r["converted"] > 0]
    pct_files = [r for r in results if r["percent_escapes"] > 0]
    total_conv = sum(r["converted"] for r in results)
    total_pct = sum(r["percent_escapes"] for r in results)
    remaining = sum(r["bracket_after"] for r in results)

    print("=== Phase 2 normalize math ===")
    print(f"Files touched (any change): {sum(1 for r in results if r['changed'])}")
    print(f"Bracket blocks converted: {total_conv}")
    print(f"Bracket blocks remaining: {remaining}")
    print(f"% escapes in math: {total_pct}")
    print("\nBracket conversions:")
    for r in converted_files:
        print(f"  {r['converted']:4d}  {r['file']}")
    print("\n% escapes:")
    for r in pct_files:
        print(f"  {r['percent_escapes']:4d}  {r['file']}")

    if remaining != 0:
        raise SystemExit(f"FAIL: {remaining} bracket blocks remain")
    if total_conv != 279:
        print(f"WARN: expected 279 conversions, got {total_conv}")
    else:
        print("\nOK: 279 bracket blocks → $$")


if __name__ == "__main__":
    main()
