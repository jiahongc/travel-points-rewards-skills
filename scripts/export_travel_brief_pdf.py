#!/usr/bin/env python3
"""
Render a travel briefing markdown/plain-text file into a styled PDF.

Usage:
  python scripts/export_travel_brief_pdf.py input.md output.pdf
  python scripts/export_travel_brief_pdf.py input.md output.pdf --title "Sydney in August"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        ListFlowable,
        ListItem,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
    )
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: reportlab\n"
        "Install it with: python -m pip install reportlab"
    ) from exc


SECTION_RE = re.compile(r"^##\s+(.+)$")
NUMBERED_RE = re.compile(r"^\d+\.\s+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export travel brief to PDF.")
    parser.add_argument("input", type=Path, help="Input markdown/plain-text file")
    parser.add_argument("output", type=Path, help="Output PDF path")
    parser.add_argument("--title", help="Override title shown on the cover page")
    parser.add_argument(
        "--subtitle",
        help="Optional subtitle shown under the title",
        default="AI travel briefing",
    )
    return parser.parse_args()


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def infer_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    for line in text.splitlines():
        if line.startswith("## "):
            return line[3:].strip()
    return "Travel Briefing"


def normalize_inline(text: str) -> str:
    text = escape(text.strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = text.replace(" — ", "&#160;&#160;—&#160;&#160;")
    return text


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#123B4A"),
            alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#5C6B73"),
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "section": ParagraphStyle(
            "SectionCustom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=21,
            textColor=colors.white,
            backColor=colors.HexColor("#123B4A"),
            borderPadding=(7, 10, 7),
            spaceBefore=12,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#1E2A2F"),
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "MetaCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#6E7C85"),
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
    }


def add_cover(story: list, title: str, subtitle: str, styles: dict) -> None:
    story.append(Spacer(1, 2.2 * inch))
    story.append(Paragraph(normalize_inline(title), styles["title"]))
    story.append(Paragraph(normalize_inline(subtitle), styles["subtitle"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            "Formatted for print and sharing",
            styles["meta"],
        )
    )
    story.append(PageBreak())


def flush_paragraph(paragraph_lines: list[str], story: list, styles: dict) -> None:
    if not paragraph_lines:
        return
    text = " ".join(line.strip() for line in paragraph_lines if line.strip())
    if text:
        story.append(Paragraph(normalize_inline(text), styles["body"]))
    paragraph_lines.clear()


def make_list(items: list[str], bullet_type: str, styles: dict) -> ListFlowable:
    flow_items = [
        ListItem(Paragraph(normalize_inline(item), styles["body"])) for item in items
    ]
    return ListFlowable(
        flow_items,
        bulletType=bullet_type,
        start="1" if bullet_type == "1" else None,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=9,
        leftIndent=18,
    )


def build_story(text: str, title: str, subtitle: str) -> list:
    styles = build_styles()
    story: list = []
    add_cover(story, title, subtitle, styles)

    paragraph_lines: list[str] = []
    bullet_items: list[str] = []
    numbered_items: list[str] = []

    def flush_lists() -> None:
        nonlocal bullet_items, numbered_items
        if bullet_items:
            story.append(make_list(bullet_items, "bullet", styles))
            story.append(Spacer(1, 4))
            bullet_items = []
        if numbered_items:
            story.append(make_list(numbered_items, "1", styles))
            story.append(Spacer(1, 4))
            numbered_items = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        section_match = SECTION_RE.match(stripped)
        if section_match:
            flush_paragraph(paragraph_lines, story, styles)
            flush_lists()
            story.append(Paragraph(normalize_inline(section_match.group(1)), styles["section"]))
            continue

        if not stripped:
            flush_paragraph(paragraph_lines, story, styles)
            flush_lists()
            continue

        if stripped.startswith("- "):
            flush_paragraph(paragraph_lines, story, styles)
            numbered_items and flush_lists()
            bullet_items.append(stripped[2:].strip())
            continue

        if NUMBERED_RE.match(stripped):
            flush_paragraph(paragraph_lines, story, styles)
            bullet_items and flush_lists()
            numbered_items.append(NUMBERED_RE.sub("", stripped, count=1).strip())
            continue

        paragraph_lines.append(stripped)

    flush_paragraph(paragraph_lines, story, styles)
    flush_lists()
    return story


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = LETTER
    canvas.setFillColor(colors.HexColor("#123B4A"))
    canvas.rect(0, height - 18, width, 18, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#6E7C85"))
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(doc.leftMargin, 20, "travel-city PDF export")
    canvas.drawRightString(width - doc.rightMargin, 20, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build_pdf(input_text: str, output_path: Path, title: str, subtitle: str) -> None:
    doc = BaseDocTemplate(
        str(output_path),
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.55 * inch,
        title=title,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_page)])
    doc.build(build_story(input_text, title, subtitle))


def main() -> int:
    args = parse_args()
    input_path: Path = args.input
    output_path: Path = args.output

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    input_text = input_path.read_text(encoding="utf-8")
    title = args.title or infer_title(input_text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(input_text, output_path, title, args.subtitle)
    print(f"Created PDF: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
