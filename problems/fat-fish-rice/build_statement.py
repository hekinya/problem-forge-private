"""Render the approved statement with the contest header, run info and sample table.

Body text uses a small CJK-aware line breaker instead of reportlab Paragraph:
Chinese text must not start a line with closing punctuation, and Latin words or
numbers must never be split across lines.
"""
import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
TITLE = "大肥鱼买白饭"
FONT = "SimHei"
BODY_SIZE = 11
LEADING = 19.5
NO_START = set("！？，。、；：）」』】》〉…—·")
NO_END = set("（「『【《〈")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--contest", default="比赛名称待确认", help="页眉里的比赛名称")
parser.add_argument("--index", type=int, default=1, help="比赛题序：A=1、B=2……")
args = parser.parse_args()
if not 1 <= args.index <= 26:
    parser.error("--index 必须是 1 到 26")
LETTER = chr(64 + args.index)

config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
assert config["time_limit_ms"] > 0 and config["memory_limit_mb"] > 0
pdfmetrics.registerFont(TTFont(FONT, r"C:\Windows\Fonts\simhei.ttf"))
c = canvas.Canvas(str(ROOT / "statement.pdf"), pagesize=A4)
width, height = A4
left, right = 58, 58
TEXT_WIDTH = width - left - right
y = height - 48

Char = tuple[str, bool]
Unit = list[Char]


def char_width(ch: str, sup: bool) -> float:
    return pdfmetrics.stringWidth(ch, FONT, BODY_SIZE * 0.7 if sup else BODY_SIZE)


def unit_width(unit: Unit) -> float:
    return sum(char_width(ch, sup) for ch, sup in unit)


def rich(text: str) -> Unit:
    """Parse `10^{4}` into characters, marking superscript digits."""
    chars: Unit = []
    i = 0
    while i < len(text):
        if text.startswith("^{", i):
            end = text.index("}", i)
            chars.extend((ch, True) for ch in text[i + 2 : end])
            i = end + 1
        else:
            chars.append((text[i], False))
            i += 1
    return chars


def split_units(chars: Unit) -> list[Unit]:
    """Latin words and numbers stay whole; CJK characters are single units."""
    units: list[Unit] = []
    current: Unit = []
    for ch, sup in chars:
        if ch.isascii() and not ch.isspace():
            current.append((ch, sup))
            continue
        if current:
            units.append(current)
            current = []
        units.append([(ch, sup)])
    if current:
        units.append(current)
    return units


def wrap(units: list[Unit], limit: float) -> list[list[Unit]]:
    lines: list[list[Unit]] = []
    current: list[Unit] = []
    used = 0.0
    for unit in units:
        w = unit_width(unit)
        if used + w <= limit or not current:
            current.append(unit)
            used += w
            continue
        previous = current[-1]
        single_char = len(unit) == 1 and len(previous) == 1
        if single_char and unit[0][0] in NO_START and len(current) > 1:
            current.pop()
            lines.append(current)
            current = [previous, unit]
            used = unit_width(previous) + w
        elif len(previous) == 1 and previous[0][0] in NO_END:
            current.pop()
            lines.append(current)
            current = [previous, unit]
            used = unit_width(previous) + w
        else:
            lines.append(current)
            current = [unit]
            used = w
    if current:
        lines.append(current)
    return lines


def paragraph(text: str, after: float = 8):
    global y
    for line in wrap(split_units(rich(text)), TEXT_WIDTH):
        x = left
        for unit in line:
            for ch, sup in unit:
                c.setFont(FONT, BODY_SIZE * 0.7 if sup else BODY_SIZE)
                c.drawString(x, y + (3.5 if sup else 0), ch)
                x += char_width(ch, sup)
        y -= LEADING
    y -= after


def heading(text, size=15, before=16, after=23):
    global y
    y -= before
    c.setFont(FONT, size)
    c.drawString(left, y, text)
    y -= after


def info_row(label, value):
    global y
    c.setFont(FONT, 10.5)
    c.drawString(left + 25, y, label)
    c.drawString(left + 108, y, value)
    y -= 17


def sample_table(number, input_lines, output_lines, note):
    global y
    heading(f"样例 {number}", before=16, after=23)
    top = y
    mid = left + TEXT_WIDTH / 2
    rows = max(len(input_lines), len(output_lines))
    table_h = 24 + rows * 16 + 10
    c.setStrokeColor(colors.HexColor("#555555"))
    c.rect(left, top - table_h, TEXT_WIDTH, table_h, fill=0, stroke=1)
    c.line(mid, top, mid, top - table_h)
    c.line(left, top - 24, width - right, top - 24)
    c.setFont(FONT, 10.5)
    c.drawCentredString((left + mid) / 2, top - 17, "标准输入")
    c.drawCentredString((mid + width - right) / 2, top - 17, "标准输出")
    c.setFont("Courier", 10)
    for i, line in enumerate(input_lines):
        c.drawString(left + 8, top - 40 - 16 * i, line)
    for i, line in enumerate(output_lines):
        c.drawString(mid + 8, top - 40 - 16 * i, line)
    y = top - table_h - 20
    paragraph(note, after=2)


c.setFont(FONT, 11)
c.drawCentredString(width / 2, y, args.contest)
y -= 17
c.setStrokeColor(colors.HexColor("#555555"))
c.line(left, y, width - right, y)
y -= 28
c.setFont(FONT, 19)
c.drawString(left, y, f"Problem {LETTER}. {TITLE}")
y -= 34
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 14
paragraph("在很深很深的数据海底，住着一条蓝色大肥鱼：deepseek。")
paragraph(
    "deepseek 的工作，是把整片语料海里的文字一口吞下去，再一句一句吐出来。"
    "它吐出的每一段文字都会被换算成 token，记进它的钱包。"
    "所以对 deepseek 来说，token 既是工资，也是饭钱。"
)
paragraph(
    "最近，深海食堂新开了一个「白饭档口」：一碗热气腾腾的大白饭，标价 19 token。"
    "档口生意很好，队伍排得很长，deepseek 每次都挤不过那些小虾米，只好在旁边等自己的鱼鳍够长。"
)
paragraph(
    "今天 deepseek 终于攒够了勇气，也攒下了一些 token。它的钱包分成两格："
    "上面一格装着「10 token 大礼包」，每个礼包里有 10 个 token，一共有 a 个；"
    "下面一格装着零散的 token，散 token 要用鱼鳍一个一个抓，一共只有 b 个。"
)
paragraph("档口只卖整碗，不卖半碗，也不许赊账。deepseek 想知道：凭钱包里现有的这些 token，它最多能买到几碗大白饭？")
heading("输入格式")
paragraph("一行两个整数 a 和 b，分别表示「10 token 大礼包」的个数和散装 token 的个数。")
heading("输出格式")
paragraph("输出一行一个整数，表示 deepseek 最多能买到的白饭碗数。")
heading("数据范围")
paragraph("对于全部测试点，0 ≤ a ≤ 10^{4}，0 ≤ b ≤ 9。")
sample_table(
    1,
    ["10 3"],
    ["5"],
    "10 个大礼包共 10 × 10 = 100 个 token，再加 3 个散装 token，共 103 个 token。"
    "一碗白饭 19 token，买 5 碗花掉 95 个 token，还剩 8 个，不够再买一碗，所以最多买 5 碗。",
)
assert y > 40, f"题面超出一页：y={y}"
c.showPage()
c.save()
print(ROOT / "statement.pdf")
