#!/usr/bin/env python3
"""Append a short self-check block to Theory AI lessons that lack <details>.

Generates 1–2 questions from title, description, definition heading, and first formula.
Skips files that already contain <details>.
Marker: <!-- auto-self-check -->
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEORY = ROOT / "bai-hoc" / "theory-ai"
MARKER = "<!-- auto-self-check -->"


def parse_yaml(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip("\"'")
    return out


def first_sentence(text: str, max_len: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    for sep in (". ", "。", "? ", "! "):
        if sep in text:
            text = text.split(sep, 1)[0] + ("." if sep.startswith(".") else "")
            break
    if len(text) > max_len:
        text = text[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return text


def extract_definition(body: str) -> str:
    # Prefer "## … là gì" style sections
    m = re.search(
        r"^##[^\n]*(?:là gì|định nghĩa|overview)[^\n]*\n+(.*?)(?=\n## |\Z)",
        body,
        re.S | re.I | re.M,
    )
    if not m:
        m = re.search(r"^## [^\n]+\n+(.*?)(?=\n## |\Z)", body, re.S | re.M)
    if not m:
        return ""
    para = m.group(1).strip()
    para = re.sub(r"```.*?```", " ", para, flags=re.S)
    para = re.sub(r"\$\$.*?\$\$", " ", para, flags=re.S)
    para = re.sub(r"!\[.*?\]\(.*?\)", " ", para)
    para = re.sub(r":::.*?:::", " ", para, flags=re.S)
    return first_sentence(para, 260)


def extract_formula(body: str) -> str:
    m = re.search(r"\$\$(.*?)\$\$", body, re.S)
    if not m:
        return ""
    formula = m.group(1).strip()
    # keep compact
    formula = re.sub(r"\s+", " ", formula)
    if len(formula) > 180:
        formula = formula[:177] + "…"
    return formula


def build_block(title: str, description: str, body: str) -> str:
    desc = first_sentence(description.replace("…", "").strip(), 200)
    definition = extract_definition(body)
    formula = extract_formula(body)

    q1_ans = definition or desc or f"Xem lại phần mở đầu bài «{title}»."
    items = [
        (
            f"Ý chính của bài «{title}» là gì?",
            q1_ans,
        )
    ]
    if formula:
        items.append(
            (
                "Công thức / quan hệ cốt lõi trong bài là gì?",
                f"$${formula}$$",
            )
        )
    else:
        items.append(
            (
                f"Khi nào nên nhớ / áp dụng «{title}»?",
                desc
                or definition
                or "Khi gặp đúng ngữ cảnh mà phần mở đầu và ví dụ số trong bài mô tả.",
            )
        )

    lines = [
        "",
        MARKER,
        "",
        "::: {.callout-note}",
        "## Kiểm tra nhanh",
    ]
    for summary, answer in items[:2]:
        lines.append("<details>")
        lines.append(f"<summary>{summary}</summary>")
        lines.append(answer)
        lines.append("</details>")
    lines.append(":::")
    lines.append("")
    return "\n".join(lines)


def process(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    if "<details>" in text or MARKER in text:
        return "skip"
    meta = parse_yaml(text)
    title = meta.get("title") or path.stem.replace("-", " ").title()
    description = meta.get("description") or ""
    body = re.sub(r"^---\n.*?---\n", "", text, count=1, flags=re.S)
    block = build_block(title, description, body)
    if dry_run:
        return "would-add"
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
    return "added"


def main() -> int:
    dry = "--dry-run" in sys.argv
    added = skip = 0
    for path in sorted(THEORY.rglob("*.qmd")):
        if path.name == "index.qmd" or path.name.startswith("_"):
            continue
        status = process(path, dry_run=dry)
        if status == "added" or status == "would-add":
            added += 1
        else:
            skip += 1
    print(f"{'would add' if dry else 'added'}={added} skip={skip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
