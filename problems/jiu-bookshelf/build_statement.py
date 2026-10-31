"""Render the approved statement as a single-page PDF."""
from pathlib import Path
import glob
import json
import subprocess

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


def find_cjk_font():
    patterns = (
        r"C:\Windows\Fonts\simhei.ttf",
        "/nix/store/*foundertype-fonts*/share/fonts/truetype/foundertype/FZXH1K.TTF",
        "/nix/store/*lxgw-wenkai*/share/fonts/truetype/LXGWWenKai-Regular.ttf",
        "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    )
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            try:
                pdfmetrics.registerFont(TTFont("CJKBody", path, subfontIndex=0))
                return path
            except Exception:
                continue
    try:
        path = subprocess.check_output(
            ["fc-match", "-f", "%{file}", "sans-serif:lang=zh-cn"], text=True
        ).strip()
        if path:
            pdfmetrics.registerFont(TTFont("CJKBody", path, subfontIndex=0))
            return path
    except Exception:
        pass
    raise SystemExit("No CJK font found")


font_path = find_cjk_font()
c = canvas.Canvas(str(ROOT / "statement.pdf"), pagesize=A4)
width, height = A4
left, right = 58, 58
y = height - 48
body = ParagraphStyle("body", fontName="CJKBody", fontSize=11, leading=19,
                      textColor=colors.black)


def heading(text, size=15, before=13, after=11):
    global y
    y -= before
    c.setFont("CJKBody", size)
    c.drawString(left, y, text)
    c.drawString(left + 0.35, y, text)
    y -= after


def info_row(label, value):
    global y
    c.setFont("CJKBody", 10.5)
    c.drawString(left + 25, y, label)
    c.drawString(left + 108, y, value)
    y -= 17


def paragraph(text, after=6):
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
    table_h = 22 + rows * 15 + 8
    c.setStrokeColor(colors.HexColor("#555555"))
    c.rect(left, top - table_h, width - left - right, table_h, fill=0, stroke=1)
    c.line(mid, top, mid, top - table_h)
    c.line(left, top - 22, width - right, top - 22)
    c.setFont("CJKBody", 10.5)
    c.drawCentredString((left + mid) / 2, top - 16, "标准输入")
    c.drawCentredString((mid + width - right) / 2, top - 16, "标准输出")
    c.drawCentredString((left + mid) / 2 + 0.3, top - 16, "标准输入")
    c.drawCentredString((mid + width - right) / 2 + 0.3, top - 16, "标准输出")
    c.setFont("Courier", 10)
    for i, line in enumerate(input_lines):
        c.drawString(left + 8, top - 37 - 15 * i, line)
    for i, line in enumerate(output_lines):
        c.drawString(mid + 8, top - 37 - 15 * i, line)
    y = top - table_h - 8
    paragraph(note, after=2)


c.setFont("CJKBody", 11)
c.drawCentredString(width / 2, y, "2026 HHACM 招新赛")
y -= 17
c.setStrokeColor(colors.HexColor("#555555"))
c.line(left, y, width - right, y)
y -= 28
c.setFont("CJKBody", 19)
c.drawString(left, y, "D. 鸠的书架")
c.drawString(left + 0.35, y, "D. 鸠的书架")
y -= 30
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 3

paragraph("鸠是一位热爱阅读的学生，他有一个收藏书籍的计划。")
paragraph("某天，鸠得到了一批珍贵的书籍，一共有 <i>N</i> 本。每本书都有一个对应的收藏价值，"
          "第 <i>i</i> 本书的收藏价值为 <i>a</i><sub>i</sub>。")
paragraph("鸠准备将这些书按照原来的顺序摆放在书架上，并将它们分成恰好 <i>K</i> 个连续的区间，"
          "每个区间交给一个书架存放。")
paragraph("为了保证书籍能够安全保存，鸠希望每个书架存放的书籍总价值尽可能均衡。因此，他想知道："
          "在最优分配方案下，所有书架中，收藏价值总和最大的那个书架，其总价值最小可能是多少？")

heading("输入格式")
paragraph("第一行包含两个整数 <i>N</i> 和 <i>K</i>。第二行包含 <i>N</i> 个整数 "
          "<i>a</i><sub>1</sub>, <i>a</i><sub>2</sub>, …, <i>a</i><sub>N</sub>。")

heading("输出格式")
paragraph("输出一个整数，表示在最优分配方案下，所有书架中价值总和的最大值的最小可能值。")

heading("数据范围")
paragraph("1 ≤ <i>K</i> ≤ <i>N</i> ≤ 2 × 10<super>5</super>；"
          "1 ≤ <i>a</i><sub>i</sub> ≤ 10<super>9</super>。")

sample_table(1, ["6 3", "4 2 7 1 5 3"], ["8"],
             "最优划分为 [4,2] | [7,1] | [5,3]，三个书架的价值分别为 6, 8, 8，最大值为 8。")
sample_table(2, ["5 1", "3 1 4 1 5"], ["14"],
             "只有一个书架，所有书都放在一起，总价值为 14。")

assert y > 40, f"Statement overflows page: {y}"
c.showPage()
c.save()
print(ROOT / "statement.pdf")
print(f"font: {font_path}")
