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
CONTEST = "2026 HHACM 招新赛"
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
y = height - 54
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


if CONTEST:
    c.setFont("CJKBody", 11)
    c.drawCentredString(width / 2, y, CONTEST)
    y -= 17
    c.setStrokeColor(colors.HexColor("#555555"))
    c.line(left, y, width - right, y)
    y -= 28

c.setFont("CJKBody", 19)
c.drawString(left, y, "Problem E. 熊大快跑")
c.drawString(left + 0.35, y, "Problem E. 熊大快跑")
y -= 30
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 3

paragraph("穷玩车，富玩表，顶富就玩熊大快跑。熊大报名参加了森林里的“熊大快跑”比赛。"
          "为了在赛道上越过越来越高的障碍，他决定先到训练场进行弹跳训练。")
paragraph("训练场上共有 <i>N</i> 个能量果实，第 <i>i</i> 个果实悬挂在离地 "
          "<i>h</i><sub>i</sub> 的高度。熊大的初始弹跳高度为 <i>L</i>。")
paragraph("熊大可以摘取高度不超过自己当前弹跳高度的果实，并将其吃下。每吃下一个能量果实，"
          "熊大的弹跳高度就会增加 1。熊大可以自由选择摘取果实的顺序。")
paragraph("请问训练结束后，熊大的弹跳高度最大可能是多少？")

heading("输入格式")
paragraph("第一行包含两个整数 <i>N</i> 和 <i>L</i>。第二行包含 <i>N</i> 个整数 "
          "<i>h</i><sub>1</sub>, <i>h</i><sub>2</sub>, …, <i>h</i><sub>N</sub>。")

heading("输出格式")
paragraph("输出一个整数，表示熊大最终能达到的最大弹跳高度。")

heading("数据范围")
paragraph("1 ≤ <i>N</i> ≤ 1000；1 ≤ <i>L</i> ≤ 10000；"
          "1 ≤ <i>h</i><sub>i</sub> ≤ 10000。")

sample_table(1, ["3 10", "10 11 13"], ["12"],
             "熊大先摘高度为 10 的果实，弹跳高度变为 11；再摘高度为 11 的果实，变为 12；"
             "高度为 13 的果实无法摘到，最终为 12。")
sample_table(2, ["9 1", "9 5 8 1 3 2 7 6 4"], ["10"],
             "熊大从高度为 1 的果实开始，按高度从小到大依次摘取全部 9 个果实，"
             "弹跳高度从 1 增加到 10。")

assert y > 40, f"Statement overflows page: {y}"
c.showPage()
c.save()
print(ROOT / "statement.pdf")
print(f"font: {font_path}")
