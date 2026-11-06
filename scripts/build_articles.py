#!/usr/bin/env python3
"""Build DOCX and PDF from canonical Markdown manuscripts in articles/."""
from __future__ import annotations
import argparse
import html
import json
import re
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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph

ROOT = Path(__file__).resolve().parents[1]
CJK_FONTS = [
    Path('/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf'),
    Path('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'),
    Path('/usr/share/fonts/truetype/arphic/uming.ttc'),
]

def manuscript(text: str):
    lines = text.replace('\r\n', '\n').strip().splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith('# ')), '未题')
    sections = re.split(r'\n\s*\n', '\n'.join(line for line in lines if not line.startswith('# ')).strip())
    return title, [re.sub(r'\s*\n\s*', '', s).strip() for s in sections if s.strip()]

def add_runs(paragraph, value):
    for piece in re.split(r'(\*\*.*?\*\*)', value):
        if not piece:
            continue
        is_bold = piece.startswith('**') and piece.endswith('**')
        run = paragraph.add_run(piece[2:-2] if is_bold else piece)
        run.bold = is_bold
        run.font.name = 'Noto Serif CJK SC'
        run._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Noto Serif CJK SC')
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
        run.font.name = 'Noto Serif CJK SC'
        run._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Noto Serif CJK SC')
        run.font.size = Pt(21)
    normal = doc.styles['Normal']
    normal.font.name = 'Noto Serif CJK SC'
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
    for path in CJK_FONTS:
        if path.is_file():
            pdfmetrics.registerFont(TTFont('YuHanCJK', str(path), subfontIndex=0))
            pdfmetrics.registerFontFamily('YuHanCJK', normal='YuHanCJK', bold='YuHanCJK')
            return 'YuHanCJK'
    raise RuntimeError('Missing CJK TrueType font. Install fonts-arphic-gbsn00lp on Linux.')

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
