"""Render the approved statement with math typography and sample blocks."""
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
OUT = ROOT / "statement.pdf"
config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
assert config["time_limit_ms"] > 0 and config["memory_limit_mb"] > 0
pdfmetrics.registerFont(TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf"))
c = canvas.Canvas(str(OUT), pagesize=A4)
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
    c.drawCentredString((left + mid) / 2 + 0.3, top - 17, "标准输入")
    c.drawCentredString((mid + width - right) / 2 + 0.3, top - 17, "标准输出")
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
c.drawString(left, y, "Problem A. 数列中的山峰")
y -= 30
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 3
paragraph("给定一个长度为 <i>n</i> 的整数数列 <i>a</i><sub>1</sub>, <i>a</i><sub>2</sub>, …, <i>a</i><sub>n</sub>。")
paragraph("若位置 <i>i</i> 同时满足 2 ≤ <i>i</i> ≤ <i>n</i> - 1、"
          "<i>a</i><sub>i</sub> &gt; <i>a</i><sub>i-1</sub> 且 "
          "<i>a</i><sub>i</sub> &gt; <i>a</i><sub>i+1</sub>，则称位置 <i>i</i> 为一个“山峰”。")
paragraph("请统计数列中山峰的个数。首尾位置不可能成为山峰；相等的相邻元素不满足严格大于。")
heading("输入格式")
paragraph("第一行包含一个整数 <i>n</i>。第二行包含 <i>n</i> 个整数 "
          "<i>a</i><sub>1</sub>, <i>a</i><sub>2</sub>, …, <i>a</i><sub>n</sub>。")
heading("输出格式")
paragraph("输出一个整数，表示山峰的个数。")
heading("数据范围")
paragraph("1 ≤ <i>n</i> ≤ 2 × 10<super>5</super>；-10<super>9</super> ≤ "
          "<i>a</i><sub>i</sub> ≤ 10<super>9</super>。")
sample_table(1, ["7", "1 3 2 4 4 5 1"], ["2"], "山峰位于位置 2 和位置 6。")
sample_table(2, ["5", "2 5 1 4 2"], ["2"], "山峰位于位置 2 和位置 4。")
assert y > 40, f"Statement overflows page: {y}"
c.showPage()
c.save()
print(OUT)
