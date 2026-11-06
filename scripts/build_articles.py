#!/usr/bin/env python3
"""Build DOCX and PDF from canonical Markdown manuscripts in articles/."""
from __future__ import annotations
import argparse
import html
import json
import os
import re
import warnings
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph

ROOT = Path(__file__).resolve().parents[1]
# Optional font candidates for embedding. Paths vary by OS/distribution.
# See docs/fonts.md. Never rely on these being installed.
CJK_FONTS = [
    ROOT / 'fonts' / 'CJK.ttf',  # private local asset (not tracked by Git)
    Path('/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf'),
    Path('/usr/share/fonts/truetype/arphic-gkai00mp/gkai00mp.ttf'),
    Path('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'),
    Path('/usr/share/fonts/truetype/arphic/uming.ttc'),
    Path('C:/Windows/Fonts/simsun.ttc'),
    Path('C:/Windows/Fonts/simhei.ttf'),
]
DOCX_FONT = os.getenv('YUHAN_DOCX_FONT', 'Noto Serif CJK SC')

def manuscript(text: str):
    """Read a Markdown essay, preserving its endnotes in printable form."""
    lines = text.replace('\r\n', '\n').strip().splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith('# ')), '未题')
    raw = '\n'.join(line for line in lines if not line.startswith('# ')).strip()
    parts = re.split(r'\n\s*---\s*\n', raw, maxsplit=1)
    body = parts[0].strip()
    sections = re.split(r'\n\s*\n', body)
    paragraphs = [
        re.sub(r'\[\^(\d+)\]', r'〔\1〕', re.sub(r'\s*\n\s*', '', s)).strip()
        for s in sections if s.strip()
    ]
    if len(parts) > 1:
        notes = re.findall(r'^\[\^(\d+)\]:\s*(.+)$', parts[1], flags=re.M)
        if notes:
            paragraphs.append('**史料与法规依据**')
            for number, note in notes:
                note = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
                              r'\1：\2', note)
                paragraphs.append(f'〔{number}〕{note}')
    return title, paragraphs

def add_runs(paragraph, value):
    for piece in re.split(r'(\*\*.*?\*\*)', value):
        if not piece:
            continue
        is_bold = piece.startswith('**') and piece.endswith('**')
        run = paragraph.add_run(piece[2:-2] if is_bold else piece)
        run.bold = is_bold
        run.font.name = DOCX_FONT
        run._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), DOCX_FONT)
        run.font.size = Pt(11.5)

def build_docx(title, sections, target):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    sec.top_margin, sec.bottom_margin = Cm(2.55), Cm(2.2)
    sec.left_margin, sec.right_margin = Cm(2.65), Cm(2.65)
    h = doc.add_heading(title, level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h.paragraph_format.space_after = Pt(24)
    for run in h.runs:
        run.font.name = DOCX_FONT
        run._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), DOCX_FONT)
        run.font.size = Pt(21)
    normal = doc.styles['Normal']
    normal.font.name = DOCX_FONT
    normal.font.size = Pt(11.5)
    for val in sections:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Pt(23)
        p.paragraph_format.line_spacing = 1.65
        p.paragraph_format.space_after = Pt(8)
        add_runs(p, val)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    doc.core_properties.title = title
    doc.core_properties.subject = '韩愈式古文论说文'
    doc.save(target)

def pick_font():
    """Select an embeddable local TrueType font, or use ReportLab CJK CID fallback.

    YUHAN_CJK_FONT is an explicit override: invalid paths/fonts fail clearly.
    Without an override, optional system fonts are tried in order and a built-in
    non-embedded CID font is used if no compatible font is available.
    """
    override = os.getenv('YUHAN_CJK_FONT', '').strip()
    candidates = [Path(override).expanduser()] if override else CJK_FONTS
    errors = []
    for path in candidates:
        if not path.is_file():
            if override:
                raise FileNotFoundError(
                    f'YUHAN_CJK_FONT points to a missing file: {path}'
                )
            continue
        try:
            pdfmetrics.registerFont(
                TTFont('YuHanCJK', str(path), subfontIndex=0)
            )
            pdfmetrics.registerFontFamily(
                'YuHanCJK', normal='YuHanCJK', bold='YuHanCJK',
                italic='YuHanCJK', boldItalic='YuHanCJK'
            )
            return 'YuHanCJK'
        except Exception as exc:
            # Some .ttc/.otf fonts contain PostScript outlines ReportLab
            # cannot embed; don't abandon the whole publication.
            errors.append(f'{path}: {exc}')
            if override:
                raise RuntimeError(
                    f'YUHAN_CJK_FONT cannot be embedded by ReportLab: {path}. '
                    'Use a TrueType-outlines .ttf/.ttc font.'
                ) from exc

    warnings.warn(
        'No embeddable CJK TrueType font found; using STSong-Light CID '
        'fallback. The PDF will not embed its font and some readers may '
        'require CJK font substitution. For portable PDFs, install a '
        'compatible CJK TTF or set YUHAN_CJK_FONT. '
        + ('Rejected candidates: ' + '; '.join(errors) if errors else ''),
        RuntimeWarning,
        stacklevel=2,
    )
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    pdfmetrics.registerFontFamily(
        'STSong-Light', normal='STSong-Light', bold='STSong-Light',
        italic='STSong-Light', boldItalic='STSong-Light',
    )
    return 'STSong-Light'

def pdf_markup(s):
    escaped = html.escape(s)
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped)

def build_pdf(title, sections, target):
    font = pick_font()
    content = []
    doc = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=57, leftMargin=57,
                            topMargin=74, bottomMargin=60, title=title, author='YuHan Articles')
    hstyle = ParagraphStyle('YuHanTitle', fontName=font, fontSize=22, leading=36,
                            alignment=TA_CENTER, spaceAfter=23, wordWrap='CJK')
    pstyle = ParagraphStyle('YuHanBody', fontName=font, fontSize=11.3, leading=21.5,
                            alignment=TA_JUSTIFY, firstLineIndent=23, spaceAfter=11, wordWrap='CJK',
                            textColor=colors.HexColor('#242424'))
    content.append(Paragraph(html.escape(title), hstyle))
    for paragraph in sections:
        content.append(Paragraph(pdf_markup(paragraph), pstyle))
    def on_page(canvas, document):
        canvas.saveState()
        canvas.setFont(font, 8.4)
        canvas.setFillColor(colors.HexColor('#777777'))
        w, _ = A4
        canvas.drawCentredString(w/2, 38, str(document.page))
        canvas.restoreState()
    doc.build(content, onFirstPage=on_page, onLaterPages=on_page)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--articles-root', type=Path, default=ROOT/'articles')
    args = parser.parse_args()
    built = 0
    for config in sorted(args.articles_root.rglob('article.json')):
        if '_templates' in config.relative_to(args.articles_root).parts:
            continue
        folder = config.parent
        meta = json.loads(config.read_text(encoding='utf-8'))
        source = folder / meta['manuscript']
        if not source.exists():
            raise FileNotFoundError(source)
        title, sections = manuscript(source.read_text(encoding='utf-8'))
        if not title or not sections:
            raise ValueError(f'Empty article: {source}')
        target_docx = source.with_suffix('.docx')
        target_pdf = source.with_suffix('.pdf')
        build_docx(title, sections, target_docx)
        build_pdf(title, sections, target_pdf)
        print(f'{source.relative_to(args.articles_root)} -> {target_docx.name}, {target_pdf.name}')
        built += 1
    print(f'Built {built} article(s).')

if __name__ == '__main__':
    main()
