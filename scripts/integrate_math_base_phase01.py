#!/usr/bin/env python3
"""Phase 0 audit + Phase 1 normalize math-base per build-math-lesson.md."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "bai-hoc" / "math-base"
SNAPSHOT = ROOT / "_snapshots" / "math-base-phase0"
AUDIT_JSON = ROOT / "_snapshots" / "math-base-phase0-audit.json"

CHAPTER_MAP = {
    "Probability": ("01-probability", "probability"),
    "Statistic": ("02-statistics", "statistics"),
    "Linear_Algebra": ("03-linear-algebra", "linear-algebra"),
    "Calculus": ("04-calculus", "calculus"),
    "Optimization": ("05-optimization", "optimization"),
    "Information_Theory": ("06-information-theory", "information-theory"),
    "Graph_Theory": ("07-graph-theory", "graph-theory"),
}

DUAL_CONTENT_MARKERS = re.compile(r"^----+\s*$", re.MULTILINE)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
ORDER_RE = re.compile(r"^(\d+)[-_]")
BRACKET_MATH_OPEN = re.compile(r"^\[$", re.MULTILINE)


def english_from_stem(stem: str) -> str:
    """Derive English title from filename stem (after order prefix)."""
    m = ORDER_RE.match(stem)
    rest = stem[m.end() :] if m else stem
    rest = rest.strip().rstrip()
    rest = rest.replace("_", " ")
    rest = re.sub(r"\s+", " ", rest)
    # hyphenated words: Conditional-Probability -> Conditional Probability
    rest = rest.replace("-", " ")
    rest = re.sub(r"\s+", " ", rest).strip()
    # Preserve (MLE) etc.
    return rest


def to_kebab(stem: str) -> str:
    m = ORDER_RE.match(stem)
    rest = stem[m.end() :] if m else stem
    rest = rest.strip().rstrip()
    rest = rest.lower()
    rest = rest.replace("_", "-")
    rest = rest.replace(" ", "-")
    rest = re.sub(r"-+", "-", rest)
    rest = rest.strip("-")
    # simplify (mle) -> mle
    rest = rest.replace("(", "").replace(")", "")
    rest = re.sub(r"-+", "-", rest)
    return rest


def parse_h1(text: str) -> str | None:
    m = H1_RE.search(text)
    return m.group(1).strip() if m else None


def build_title(h1: str | None, english: str) -> str:
    if not h1:
        return english
    # Already Việt (English)?
    if re.search(r"\([^)]+\)\s*$", h1):
        return h1
    return f"{h1} ({english})"


def extract_description(text: str) -> str:
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#"):
            continue
        if line.startswith("!["):
            continue
        if line.startswith(">"):
            desc = line.lstrip("> ").strip()
            if desc:
                return truncate_desc(desc)
            continue
        if line.startswith("---") or line.startswith("***"):
            continue
        if line.startswith("```"):
            continue
        # paragraph start
        para = line
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
            if lines[i].startswith("```"):
                break
            para += " " + lines[i].strip()
            i += 1
        para = re.sub(r"\*\*([^*]+)\*\*", r"\1", para)
        para = re.sub(r"\*([^*]+)\*", r"\1", para)
        para = re.sub(r"`([^`]+)`", r"\1", para)
        para = re.sub(r"\$[^$]+\$", "", para)
        para = re.sub(r"\s+", " ", para).strip()
        if len(para) > 20:
            return truncate_desc(para)
    return "Nền tảng toán cho học máy và AI."


def truncate_desc(s: str, max_len: int = 200) -> str:
    s = s.strip()
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 1].rsplit(" ", 1)[0]
    return cut + "…"


def yaml_escape(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return s


def count_bracket_blocks(text: str) -> int:
    count = 0
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "[":
            count += 1
            i += 1
            while i < len(lines) and lines[i].strip() != "]":
                i += 1
            i += 1
        else:
            i += 1
    return count


def has_dual_content(text: str) -> bool:
    if not DUAL_CONTENT_MARKERS.search(text):
        return False
    after = DUAL_CONTENT_MARKERS.split(text, maxsplit=1)
    if len(after) < 2:
        return False
    return bool(re.search(r"^#\s+1\.", after[1], re.MULTILINE))


def bad_filename(name: str) -> list[str]:
    issues = []
    if name.endswith(" .md") or name.endswith(" "):
        issues.append("trailing_space")
    if " '" in name or name.startswith("'"):
        issues.append("apostrophe")
    if "(" in name or ")" in name:
        issues.append("parens")
    if " _" in name or "_ " in name:
        issues.append("space_underscore")
    if re.search(r"\d_", name):
        issues.append("digit_underscore")
    return issues


@dataclass
class LessonAudit:
    source: str
    chapter: str
    target_dir: str
    target_file: str
    order: int
    title: str
    bracket_blocks: int
    dual_content: bool
    filename_issues: list[str]
    h1: str | None


def collect_lessons() -> list[Path]:
    files = sorted(SRC_ROOT.rglob("*.md"))
    return [f for f in files if f.is_file()]


def run_phase0() -> dict:
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    if SNAPSHOT.exists():
        shutil.rmtree(SNAPSHOT)
    shutil.copytree(SRC_ROOT, SNAPSHOT)

    lessons: list[LessonAudit] = []
    for path in collect_lessons():
        rel = path.relative_to(SRC_ROOT)
        chapter = rel.parts[0]
        if chapter not in CHAPTER_MAP:
            continue
        text = path.read_text(encoding="utf-8")
        stem = path.stem
        m = ORDER_RE.match(stem)
        order = int(m.group(1)) if m else 0
        english = english_from_stem(stem)
        h1 = parse_h1(text)
        title = build_title(h1, english)
        target_dir, slug = CHAPTER_MAP[chapter]
        kebab = to_kebab(stem)
        lessons.append(
            LessonAudit(
                source=str(rel),
                chapter=chapter,
                target_dir=target_dir,
                target_file=f"{kebab}.qmd",
                order=order,
                title=title,
                bracket_blocks=count_bracket_blocks(text),
                dual_content=has_dual_content(text),
                filename_issues=bad_filename(path.name),
                h1=h1,
            )
        )

    audit = {
        "date": date.today().isoformat(),
        "snapshot": str(SNAPSHOT.relative_to(ROOT)),
        "lesson_count": len(lessons),
        "total_bracket_blocks": sum(x.bracket_blocks for x in lessons),
        "dual_content_files": [x.source for x in lessons if x.dual_content],
        "bad_filename_files": [
            {"file": x.source, "issues": x.filename_issues}
            for x in lessons
            if x.filename_issues
        ],
        "bracket_heavy": [
            {"file": x.source, "blocks": x.bracket_blocks}
            for x in lessons
            if x.bracket_blocks > 0
        ],
        "lessons": [asdict(x) for x in lessons],
    }
    AUDIT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit


def run_phase1(audit: dict) -> None:
    # Move img.png alongside statistics lessons first
    img_src = SRC_ROOT / "Statistic" / "img.png"
    img_kept = img_src.exists()

    for item in audit["lessons"]:
        src = SRC_ROOT / item["source"]
        if not src.exists():
            raise FileNotFoundError(f"Missing source: {src}")
        body = src.read_text(encoding="utf-8")
        target_dir = SRC_ROOT / item["target_dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / item["target_file"]

        desc = extract_description(body)
        fm = (
            "---\n"
            f'title: "{yaml_escape(item["title"])}"\n'
            f'order: {item["order"]}\n'
            f'date: {date.today().isoformat()}\n'
            f'description: "{yaml_escape(desc)}"\n'
            "series: math-base\n"
            f'categories: [math-base, {item["target_dir"].split("-", 1)[1]}]\n'
            f'group: {item["target_dir"].split("-", 1)[1]}\n'
            "---\n"
        )
        # Fix group slug - use from CHAPTER_MAP
        chapter_old = item["chapter"]
        _, group_slug = CHAPTER_MAP[chapter_old]
        fm = (
            "---\n"
            f'title: "{yaml_escape(item["title"])}"\n'
            f'order: {item["order"]}\n'
            f'date: {date.today().isoformat()}\n'
            f'description: "{yaml_escape(desc)}"\n'
            "series: math-base\n"
            f"categories: [math-base, {group_slug}]\n"
            f"group: {group_slug}\n"
            "---\n"
        )
        target.write_text(fm + body, encoding="utf-8")

    # Copy img.png to new statistics folder
    if img_kept:
        dst = SRC_ROOT / "02-statistics" / "img.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(img_src, dst)

    # Remove old chapter dirs and stray files
    for old_name in CHAPTER_MAP:
        old_dir = SRC_ROOT / old_name
        if old_dir.exists():
            shutil.rmtree(old_dir)

    # Remove any leftover .md at root
    for md in SRC_ROOT.glob("*.md"):
        md.unlink()


def verify_phase1(audit: dict) -> dict:
    qmd_files = sorted(SRC_ROOT.rglob("*.qmd"))
    md_files = list(SRC_ROOT.rglob("*.md"))
    snapshot_lessons = [x["source"] for x in audit["lessons"]]

    body_ok = 0
    body_fail: list[str] = []
    for item in audit["lessons"]:
        snap = SNAPSHOT / item["source"]
        target = SRC_ROOT / item["target_dir"] / item["target_file"]
        if not target.exists():
            body_fail.append(f"missing: {target}")
            continue
        snap_body = snap.read_text(encoding="utf-8")
        new_text = target.read_text(encoding="utf-8")
        if new_text.startswith("---"):
            new_body = new_text.split("---", 2)[2].lstrip("\n")
        else:
            new_body = new_text
        if snap_body == new_body:
            body_ok += 1
        else:
            body_fail.append(item["target_file"])

    orders: dict[str, list[int]] = {}
    for q in qmd_files:
        rel_dir = q.parent.name
        text = q.read_text(encoding="utf-8")
        m = re.search(r"^order:\s*(\d+)", text, re.MULTILINE)
        if m:
            orders.setdefault(rel_dir, []).append(int(m.group(1)))

    order_issues = {}
    for d, ords in orders.items():
        expected = list(range(1, len(ords) + 1))
        if sorted(ords) != expected:
            order_issues[d] = {"got": sorted(ords), "expected": expected}

    return {
        "qmd_count": len(qmd_files),
        "expected_count": len(snapshot_lessons),
        "md_remaining": len(md_files),
        "body_match": body_ok,
        "body_fail": body_fail[:10],
        "body_fail_count": len(body_fail),
        "order_issues": order_issues,
    }


def main() -> None:
    print("Phase 0: snapshot + audit...")
    audit = run_phase0()
    print(f"  lessons: {audit['lesson_count']}")
    print(f"  bracket blocks: {audit['total_bracket_blocks']}")
    print(f"  dual-content: {len(audit['dual_content_files'])}")
    print(f"  bad filenames: {len(audit['bad_filename_files'])}")

    print("Phase 1: rename + .qmd + frontmatter...")
    run_phase1(audit)

    print("Verify...")
    v = verify_phase1(audit)
    print(json.dumps(v, indent=2, ensure_ascii=False))
    if v["qmd_count"] != v["expected_count"] or v["body_fail_count"] > 0:
        raise SystemExit(1)
    print("Done.")


if __name__ == "__main__":
    main()
