#!/usr/bin/env python3
"""Normalize theory-ai lessons per Pha 2 of theory-ai-integration-plan.md.

Reads bai-hoc/theory-ai/_inventory.csv and, for each row:
  1. Converts HTML <figure>…</figure> → Quarto figure div
  2. Inserts YAML front-matter if missing (never overwrites existing title:)
  3. Renames .md → slug.qmd (inventory path_new)
  4. Applies known content fixes (broken img src)

Default is dry-run (no writes). Use --apply to mutate files.
Phase 2 gate: do not --apply on the live tree until Phase 3 pilot;
use --fixture to validate on a copy first.

Examples:
  python3 scripts/normalize_theory_ai.py
  python3 scripts/normalize_theory_ai.py --chapter 01-probability
  python3 scripts/normalize_theory_ai.py --fixture /tmp/theory-ai-fixture
  python3 scripts/normalize_theory_ai.py --fixture /tmp/theory-ai-fixture --apply
  python3 scripts/normalize_theory_ai.py --chapter 01-probability --apply
  python3 scripts/normalize_theory_ai.py --strip-hr              # dry-run
  python3 scripts/normalize_theory_ai.py --strip-hr --apply      # all inventory lessons
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THEORY = ROOT / "bai-hoc" / "theory-ai"
INVENTORY_NAME = "_inventory.csv"

FIGURE_BLOCK_RE = re.compile(r"<figure>\s*(.*?)\s*</figure>", re.IGNORECASE | re.DOTALL)
IMG_RE = re.compile(
    r'<img\b[^>]*?\bsrc\s*=\s*["\']([^"\']+)["\'][^>]*?\balt\s*=\s*["\']([^"\']*)["\'][^>]*/?>'
    r'|'
    r'<img\b[^>]*?\balt\s*=\s*["\']([^"\']*)["\'][^>]*?\bsrc\s*=\s*["\']([^"\']+)["\'][^>]*/?>',
    re.IGNORECASE | re.DOTALL,
)
CAPTION_RE = re.compile(r"<figcaption>\s*(.*?)\s*</figcaption>", re.IGNORECASE | re.DOTALL)
YAML_TITLE_RE = re.compile(r"(?m)^title\s*:")
BARE_IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
CODE_FENCE_RE = re.compile(r"(```.*?```)", re.DOTALL)

# Corrupted paste: figures/![x](figures/x)x  →  figures/x
BROKEN_SRC_RE = re.compile(
    r"figures/!\[[^\]]*\]\(figures/([^)]+)\)\1"
)


@dataclass
class Row:
    chapter: str
    order: int
    path_old: str
    slug: str
    path_new: str
    title: str
    group: str
    source_id: str
    notes: str = ""


@dataclass
class Report:
    renames: list[str] = field(default_factory=list)
    yaml_added: list[str] = field(default_factory=list)
    figures_converted: list[str] = field(default_factory=list)
    content_fixes: list[str] = field(default_factory=list)
    skipped_existing_yaml: list[str] = field(default_factory=list)
    missing_src: list[str] = field(default_factory=list)
    remaining_html_figure: list[str] = field(default_factory=list)
    remaining_bare_img: list[str] = field(default_factory=list)
    missing_file: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def load_inventory(inventory: Path, chapter: str | None) -> list[Row]:
    rows: list[Row] = []
    with inventory.open(encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            if chapter and raw["chapter"] != chapter:
                continue
            rows.append(
                Row(
                    chapter=raw["chapter"],
                    order=int(raw["order"]),
                    path_old=raw["path_old"],
                    slug=raw["slug"],
                    path_new=raw["path_new"],
                    title=raw["title"],
                    group=raw["group"],
                    source_id=raw.get("source_id", ""),
                    notes=raw.get("notes", ""),
                )
            )
    return rows


def yaml_quote(value: str) -> str:
    """Double-quote YAML scalar; escape internal quotes."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_yaml(row: Row, description: str) -> str:
    cats = f"[theory-ai, {row.group}]"
    lines = [
        "---",
        f"title: {yaml_quote(row.title)}",
        "date: 2026-08-26",
        f"order: {row.order}",
        f"categories: {cats}",
        "series: theory-ai",
        f"group: {row.group}",
        f"description: {yaml_quote(description)}",
    ]
    if row.source_id:
        lines.append(f"source-id: {yaml_quote(str(row.source_id))}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def first_paragraph_description(body: str, fallback: str, limit: int = 140) -> str:
    """Take first non-heading prose line as description."""
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(":::") or s.startswith("```"):
            continue
        if s.startswith("---"):
            continue
        s = re.sub(r"[*_`]", "", s)
        if len(s) > limit:
            s = s[: limit - 1].rstrip() + "…"
        return s
    return fallback


def fig_id_from_src(src: str, slug: str, index: int) -> str:
    name = Path(src).stem
    # prefer svg stem; fallback slug-n
    safe = re.sub(r"[^a-zA-Z0-9\-]+", "-", name).strip("-").lower()
    if not safe:
        safe = f"{slug}-{index}"
    return f"fig-{safe}"


def normalize_src(src: str) -> str:
    src = src.strip()
    m = BROKEN_SRC_RE.fullmatch(src) or BROKEN_SRC_RE.search(src)
    if m:
        return f"figures/{m.group(1)}"
    # also handle partial broken forms
    if "![" in src and "figures/" in src:
        m2 = re.search(r"figures/([A-Za-z0-9._\-]+\.svg)", src)
        if m2:
            return f"figures/{m2.group(1)}"
    return src


def convert_figure_block(block: str, slug: str, index: int) -> tuple[str, str | None]:
    """Return (replacement_markdown, src_or_None_if_failed)."""
    img = IMG_RE.search(block)
    if not img:
        return block, None
    if img.group(1) is not None:
        src, alt = img.group(1), img.group(2) or ""
    else:
        alt, src = img.group(3) or "", img.group(4)
    src = normalize_src(src)
    cap_m = CAPTION_RE.search(block)
    caption = re.sub(r"\s+", " ", cap_m.group(1)).strip() if cap_m else alt.strip()
    # escape quotes in attributes for Quarto
    caption_esc = caption.replace('"', "'")
    alt_esc = alt.strip().replace('"', "'")
    fig_id = fig_id_from_src(src, slug, index)
    md = (
        f'::: {{#{fig_id} fig-cap="{caption_esc}" fig-alt="{alt_esc}"}}\n'
        f"![]({src}){{fig-align=\"center\"}}\n"
        f":::"
    )
    return md, src


def protect_code_fences(text: str) -> tuple[str, list[str]]:
    chunks: list[str] = []

    def repl(m: re.Match[str]) -> str:
        chunks.append(m.group(1))
        return f"\0CODE{len(chunks) - 1}\0"

    return CODE_FENCE_RE.sub(repl, text), chunks


def restore_code_fences(text: str, chunks: list[str]) -> str:
    for i, chunk in enumerate(chunks):
        text = text.replace(f"\0CODE{i}\0", chunk)
    return text


def strip_horizontal_rules(text: str) -> tuple[str, int]:
    """Remove Markdown thematic breaks (lines that are only ---).

    Preserves YAML by operating on body only when caller splits first.
    Protects fenced code so --- inside ``` blocks is kept.
    Returns (new_text, removed_count).
    """
    text, fences = protect_code_fences(text)
    removed = 0
    out_lines: list[str] = []
    for line in text.splitlines():
        if line.strip() == "---":
            removed += 1
            continue
        out_lines.append(line)
    text = "\n".join(out_lines)
    text = restore_code_fences(text, fences)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if text and not text.endswith("\n"):
        text += "\n"
    return text, removed


def transform_body(text: str, slug: str, report: Report, label: str) -> str:
    text, fences = protect_code_fences(text)

    # Fix known broken src strings anywhere (inside figures before convert)
    def fix_broken(m: re.Match[str]) -> str:
        report.content_fixes.append(f"{label}: broken-src → figures/{m.group(1)}")
        return f"figures/{m.group(1)}"

    text2 = BROKEN_SRC_RE.sub(fix_broken, text)
    if text2 != text:
        text = text2

    fig_index = 0

    def repl_figure(m: re.Match[str]) -> str:
        nonlocal fig_index
        fig_index += 1
        md, src = convert_figure_block(m.group(0), slug, fig_index)
        if src is None:
            report.errors.append(f"{label}: could not parse <figure>")
            return m.group(0)
        report.figures_converted.append(f"{label}: {src}")
        return md

    text = FIGURE_BLOCK_RE.sub(repl_figure, text)

    # Remove leftover bare <img> (e.g. duplicate after broken figure in t-test)
    bare_left: list[str] = []

    def repl_bare(m: re.Match[str]) -> str:
        raw = m.group(0)
        img = IMG_RE.search(raw)
        if not img:
            bare_left.append(raw[:80])
            return raw
        src = normalize_src(img.group(1) or img.group(4) or "")
        alt = (img.group(2) if img.group(1) is not None else img.group(3)) or ""
        fig_index_local = fig_index + 1 + len(bare_left)
        # If this duplicates an already-converted figure src, drop it.
        if any(src in item for item in report.figures_converted if item.startswith(label)):
            report.content_fixes.append(f"{label}: drop duplicate bare <img> {src}")
            return ""
        caption_esc = alt.strip().replace('"', "'")
        fig_id = fig_id_from_src(src, slug, fig_index_local)
        report.figures_converted.append(f"{label}: bare→ {src}")
        report.content_fixes.append(f"{label}: convert bare <img> {src}")
        return (
            f'::: {{#{fig_id} fig-cap="{caption_esc}" fig-alt="{caption_esc}"}}\n'
            f"![]({src}){{fig-align=\"center\"}}\n"
            f":::"
        )

    text = BARE_IMG_RE.sub(repl_bare, text)
    text = restore_code_fences(text, fences)

    # Drop section HRs (---) — theory-ai uses ## headings; HR is visual noise
    text, n_hr = strip_horizontal_rules(text)
    if n_hr:
        report.content_fixes.append(f"{label}: removed {n_hr} horizontal rules")

    # tidy excessive blank lines from removals
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def has_yaml_title(text: str) -> bool:
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    header = text[3:end]
    return bool(YAML_TITLE_RE.search(header))


def strip_leading_h1_duplicate(body: str, title: str) -> str:
    """Keep H1 — plan says keep original H1. No-op."""
    return body


def process_row(
    theory_root: Path,
    row: Row,
    *,
    apply: bool,
    report: Report,
) -> None:
    src = theory_root / row.path_old
    # Already converted?
    dest = theory_root / row.path_new
    if not src.exists():
        if dest.exists():
            # idempotent path: work on existing .qmd
            src = dest
        else:
            report.missing_file.append(row.path_old)
            return

    original = src.read_text(encoding="utf-8")
    label = row.path_old

    body = original
    if has_yaml_title(original):
        report.skipped_existing_yaml.append(label)
        # still convert figures if needed
        # split yaml
        end = original.find("\n---", 3)
        yaml_part = original[: end + 4]
        body = original[end + 4 :].lstrip("\n")
        body = transform_body(body, row.slug, report, label)
        new_text = yaml_part + "\n" + body if not body.startswith("\n") else yaml_part + body
        if not new_text.endswith("\n"):
            new_text += "\n"
    else:
        body = transform_body(original, row.slug, report, label)
        desc = first_paragraph_description(body, row.title)
        yaml = build_yaml(row, desc)
        report.yaml_added.append(label)
        new_text = yaml + body
        if not new_text.endswith("\n"):
            new_text += "\n"

    # Validate figure paths exist
    for m in re.finditer(r"!\[\]\((figures/[^)]+)\)", new_text):
        fig_path = (src.parent / m.group(1)).resolve()
        if not fig_path.exists():
            report.missing_src.append(f"{label}: missing {m.group(1)}")

    renamed = src.resolve() != dest.resolve()
    if renamed:
        report.renames.append(f"{row.path_old} → {row.path_new}")

    if not apply:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")
    if renamed and src.exists() and src.resolve() != dest.resolve():
        src.unlink()


def post_scan(theory_root: Path, rows: list[Row], report: Report) -> None:
    """Scan resulting .qmd (or still-.md) for leftover HTML figures."""
    for row in rows:
        for candidate in (theory_root / row.path_new, theory_root / row.path_old):
            if not candidate.exists():
                continue
            text = candidate.read_text(encoding="utf-8")
            if FIGURE_BLOCK_RE.search(text):
                report.remaining_html_figure.append(str(candidate.relative_to(theory_root)))
            # bare img outside code
            protected, _ = protect_code_fences(text)
            if BARE_IMG_RE.search(protected):
                report.remaining_bare_img.append(str(candidate.relative_to(theory_root)))
            if not has_yaml_title(text) and candidate.suffix == ".qmd":
                report.errors.append(f"{candidate.name}: .qmd missing title YAML")
            break


def print_report(report: Report, *, apply: bool) -> None:
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== normalize_theory_ai [{mode}] ===")
    print(f"renames:            {len(report.renames)}")
    print(f"yaml_added:         {len(report.yaml_added)}")
    print(f"figures_converted:  {len(report.figures_converted)}")
    print(f"content_fixes:      {len(report.content_fixes)}")
    print(f"skipped_yaml:       {len(report.skipped_existing_yaml)}")
    print(f"missing_file:       {len(report.missing_file)}")
    print(f"missing_src:        {len(report.missing_src)}")
    print(f"remaining_<figure>: {len(report.remaining_html_figure)}")
    print(f"remaining_bare_img: {len(report.remaining_bare_img)}")
    print(f"errors:             {len(report.errors)}")

    def dump(title: str, items: list[str], limit: int = 30) -> None:
        if not items:
            return
        print(f"\n-- {title} ({len(items)}) --")
        for item in items[:limit]:
            print(f"  {item}")
        if len(items) > limit:
            print(f"  … {len(items) - limit} more")

    dump("renames", report.renames, 20)
    dump("content_fixes", report.content_fixes)
    dump("missing_file", report.missing_file)
    dump("missing_src", report.missing_src)
    dump("remaining_<figure>", report.remaining_html_figure)
    dump("remaining_bare_img", report.remaining_bare_img)
    dump("errors", report.errors)


def setup_fixture(live: Path, fixture: Path, chapter: str | None) -> None:
    if fixture.exists():
        shutil.rmtree(fixture)
    fixture.mkdir(parents=True)
    # always copy inventory
    shutil.copy2(live / INVENTORY_NAME, fixture / INVENTORY_NAME)
    chapters = [chapter] if chapter else [
        p.name for p in sorted(live.iterdir()) if p.is_dir() and re.match(r"^\d{2}-", p.name)
    ]
    for ch in chapters:
        src = live / ch
        if not src.exists():
            raise SystemExit(f"chapter not found: {ch}")
        shutil.copytree(src, fixture / ch)
    print(f"Fixture ready: {fixture} (chapters: {', '.join(chapters)})")


def body_without_yaml_and_figures(text: str) -> str:
    """Extract comparable body: drop YAML and Quarto/HTML figures for near-byte check."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    text = FIGURE_BLOCK_RE.sub("", text)
    text = re.sub(
        r"::: \{#fig-[^}]+\}.*?:::",
        "",
        text,
        flags=re.DOTALL,
    )
    text = BARE_IMG_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def fixture_diff_check(before_path: Path, after_path: Path) -> None:
    before = before_path.read_text(encoding="utf-8")
    after = after_path.read_text(encoding="utf-8")
    b = body_without_yaml_and_figures(before)
    a = body_without_yaml_and_figures(after)
    if a == b:
        print(f"FIXTURE BODY OK (prose/code unchanged): {after_path.name}")
    else:
        # show small context
        print(f"FIXTURE BODY DRIFT: {after_path.name}")
        import difflib

        diff = list(difflib.unified_diff(b.splitlines(), a.splitlines(), lineterm="", n=2))
        for line in diff[:40]:
            print(line)
        if len(diff) > 40:
            print(f"… {len(diff) - 40} diff lines")


def split_yaml_body(text: str) -> tuple[str | None, str]:
    """Return (yaml_block_including_delimiters_or_None, body)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    # require closing --- to look like front matter (has at least one key)
    header = text[3:end]
    if not re.search(r"(?m)^[a-zA-Z0-9_-]+\s*:", header):
        return None, text
    yaml_block = text[: end + 4]
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    return yaml_block, body


def run_strip_hr(theory_root: Path, rows: list[Row], *, apply: bool) -> int:
    """Strip body --- from existing .qmd/.md without rename/YAML/figure work."""
    mode = "APPLY" if apply else "DRY-RUN"
    total_files = 0
    total_hr = 0
    missing = 0
    changed_files = 0
    print(f"=== strip-hr [{mode}] ===")
    for row in rows:
        candidates = [theory_root / row.path_new, theory_root / row.path_old]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            missing += 1
            print(f"  MISSING {row.path_old}")
            continue
        total_files += 1
        original = path.read_text(encoding="utf-8")
        yaml_block, body = split_yaml_body(original)
        new_body, n = strip_horizontal_rules(body)
        if n == 0:
            continue
        changed_files += 1
        total_hr += n
        print(f"  {path.relative_to(theory_root)}: -{n} HR")
        if apply:
            if yaml_block is not None:
                out = yaml_block + "\n" + new_body.lstrip("\n")
            else:
                out = new_body
            if not out.endswith("\n"):
                out += "\n"
            path.write_text(out, encoding="utf-8")
    print(f"files_scanned={total_files} files_changed={changed_files} hr_removed={total_hr} missing={missing}")
    return 1 if missing else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--theory-root", type=Path, default=DEFAULT_THEORY)
    parser.add_argument("--inventory", type=Path, default=None, help="Defaults to <theory-root>/_inventory.csv")
    parser.add_argument("--chapter", type=str, default=None, help="Only this chapter folder, e.g. 01-probability")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=None,
        help="Copy selected chapters here first; operate on the copy (Phase 2 verify)",
    )
    parser.add_argument(
        "--check-body",
        action="store_true",
        help="With --fixture --apply: compare prose/code body before vs after on first file",
    )
    parser.add_argument(
        "--strip-hr",
        action="store_true",
        help="Only remove body horizontal rules (---) from inventory lessons; keep YAML. "
        "Use before Phase 4 so sources are clean. Respects --apply / dry-run.",
    )
    args = parser.parse_args(argv)

    live_root: Path = args.theory_root
    inventory = args.inventory or (live_root / INVENTORY_NAME)
    if not inventory.exists():
        print(f"Missing inventory: {inventory}", file=sys.stderr)
        return 2

    theory_root = live_root
    before_sample: Path | None = None
    sample_rel: str | None = None

    if args.fixture is not None:
        setup_fixture(live_root, args.fixture, args.chapter)
        theory_root = args.fixture
        inventory = theory_root / INVENTORY_NAME

    rows = load_inventory(inventory, args.chapter)
    if not rows:
        print("No inventory rows matched.", file=sys.stderr)
        return 2

    if args.strip_hr:
        return run_strip_hr(theory_root, rows, apply=args.apply)

    if args.check_body:
        sample_rel = rows[0].path_old
        before_sample = theory_root / sample_rel
        if not before_sample.exists():
            print(f"Cannot --check-body; missing {before_sample}", file=sys.stderr)
            return 2
        # keep a copy of original bytes
        before_text_path = theory_root / ".fixture-before-sample.md"
        before_text_path.write_text(before_sample.read_text(encoding="utf-8"), encoding="utf-8")
        before_sample = before_text_path

    report = Report()
    for row in rows:
        try:
            process_row(theory_root, row, apply=args.apply, report=report)
        except Exception as exc:  # noqa: BLE001 — collect and continue
            report.errors.append(f"{row.path_old}: {exc}")

    if args.apply:
        post_scan(theory_root, rows, report)
    else:
        # dry-run: simulate remaining by transforming in memory already tracked;
        # still flag inventory source files that would leave HTML if convert failed
        for row in rows:
            src = theory_root / row.path_old
            if not src.exists():
                continue
            # quick: if transform would leave figure — run transform on copy in memory
            text = src.read_text(encoding="utf-8")
            probe = Report()
            if has_yaml_title(text):
                end = text.find("\n---", 3)
                body = text[end + 4 :]
                body = transform_body(body, row.slug, probe, row.path_old)
                out = text[: end + 4] + "\n" + body.lstrip("\n")
            else:
                body = transform_body(text, row.slug, probe, row.path_old)
                out = build_yaml(row, row.title) + body
            if FIGURE_BLOCK_RE.search(out):
                report.remaining_html_figure.append(row.path_old)
            protected, _ = protect_code_fences(out)
            if BARE_IMG_RE.search(protected):
                report.remaining_bare_img.append(row.path_old)
            for m in re.finditer(r"!\[\]\((figures/[^)]+)\)", out):
                if not (src.parent / m.group(1)).exists():
                    report.missing_src.append(f"{row.path_old}: missing {m.group(1)}")

    print_report(report, apply=args.apply)

    if args.check_body and args.apply and before_sample and sample_rel:
        after = theory_root / rows[0].path_new
        if after.exists():
            fixture_diff_check(before_sample, after)

    # Non-zero if hard failures
    if report.missing_file or report.errors:
        return 1
    if args.apply and (report.remaining_html_figure or report.remaining_bare_img or report.missing_src):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
