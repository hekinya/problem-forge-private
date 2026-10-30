"""Render the approved statement as a single-page PDF."""
from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
assert config["time_limit_ms"] > 0 and config["memory_limit_mb"] > 0
pdfmetrics.registerFont(TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf"))
c = canvas.Canvas(str(ROOT / "statement.pdf"), pagesize=A4)
width, height = A4
left, right = 58, 58
y = height - 54
body = ParagraphStyle("body", fontName="SimHei", fontSize=11.5, leading=22, textColor=colors.black)


def heading(text, size=15, before=16, after=13):
    global y
    y -= before
    c.setFont("SimHei", size)
    c.drawString(left, y, text)
    c.drawString(left + 0.35, y, text)
    y -= after


def info_row(label, value):
    global y
    c.setFont("SimHei", 10.5)
    c.drawString(left + 25, y, label)
    c.drawString(left + 108, y, value)
    y -= 17


def paragraph(text, after=8):
    global y
    item = Paragraph(text, body)
    _, h = item.wrap(width - left - right, 1000)
    item.drawOn(c, left, y - h)
    y -= h + after


def sample_table(number, input_lines, output_lines, note):
    global y
    heading(f"样例 {number}", before=12, after=10)
    top = y
    mid = left + (width - left - right) / 2
    rows = max(len(input_lines), len(output_lines))
    table_h = 24 + rows * 16 + 10
    c.setStrokeColor(colors.HexColor("#555555"))
    c.rect(left, top - table_h, width - left - right, table_h, fill=0, stroke=1)
    c.line(mid, top, mid, top - table_h)
    c.line(left, top - 24, width - right, top - 24)
    c.setFont("SimHei", 10.5)
    c.drawCentredString((left + mid) / 2, top - 17, "标准输入")
    c.drawCentredString((mid + width - right) / 2, top - 17, "标准输出")
    c.setFont("Courier", 10)
    for i, line in enumerate(input_lines):
        c.drawString(left + 8, top - 40 - 16 * i, line)
    for i, line in enumerate(output_lines):
        c.drawString(mid + 8, top - 40 - 16 * i, line)
    y = top - table_h - 8
    paragraph(note, after=2)


c.setFont("SimHei", 11)
c.drawCentredString(width / 2, y, "2026 HHACM 招新赛")
y -= 17
c.setStrokeColor(colors.HexColor("#555555"))
c.line(left, y, width - right, y)
y -= 28
c.setFont("SimHei", 19)
c.drawString(left, y, "Problem C. Hello World")
y -= 30
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 3
paragraph("这是一道签到题。")
paragraph('请编写一个程序，向标准输出打印一行文本：<font face="Courier">Hello World</font>。')
heading("输入格式")
paragraph("本题没有输入。")
heading("输出格式")
paragraph(
    '输出一行文本 <font face="Courier">Hello World</font>。两个单词之间的空格、每个字母的大小写都必须与要求完全一致，'
    "不要输出额外的空行或其他内容。"
)
sample_table(1, [], ["Hello World"], "程序直接输出这一行文本即可。")
assert y > 40, f"Statement overflows page: {y}"
c.showPage()
c.save()
print(ROOT / "statement.pdf")
