from pathlib import Path
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

root = Path(__file__).resolve().parent
meta = json.loads((root / 'problem.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('SimHei', r'C:\Windows\Fonts\simhei.ttf'))
c = canvas.Canvas(str(root / 'statement.pdf'), pagesize=A4)
w, h = A4
left, right = 55, w - 55
y = h - 42
style = ParagraphStyle('body', fontName='SimHei', fontSize=11, leading=17)

def para(s, gap=6):
    global y
    p = Paragraph(s, style)
    _, height = p.wrap(right-left, 1000)
    p.drawOn(c, left, y-height)
    y -= height+gap

def heading(s):
    global y
    y -= 6
    c.setFont('SimHei', 15)
    c.drawString(left, y, s)
    y -= 12

c.setFont('SimHei', 11)
c.drawCentredString(w/2, y, '2026 HHACM 招新赛')
y -= 13
c.line(left, y, right, y)
y -= 28
c.setFont('SimHei', 19)
c.drawString(left, y, 'Problem B. Yes-Yes?')
y -= 25
c.setFont('SimHei', 10.5)
for label, value in [('输入文件', '标准输入'), ('输出文件', '标准输出'), ('时间限制', f"{meta['time_limit_ms']/1000:g} s"), ('内存限制', f"{meta['memory_limit_mb']} MB")]:
    c.drawString(left+20, y, label+'：')
    c.drawString(left+115, y, value)
    y -= 16
y -= 6
para('你问了 Chumeng 一堆问题，Chumeng 不喜欢浪费生命的问题，所以他只回答了一堆 Yes。但是因为电话信号不好，你只听到了回答的一个子串。也就是说，如果他回答了 YesYes，你可能只听到了 esYe，但你不会听到 esYs，因为它不是回答的子串。')
para('判断给定的一个字符串 s 是否是 YesYesYes... 的子串（... 表示 Yes 重复了很多次）。')
heading('输入格式')
para('第一行包括一个正整数 t（1 ≤ t ≤ 50）——测试用例的数量。接下来有 t 个测试用例。每个测试用例包括一个字符串 s（1 ≤ |s| ≤ 50）。')
heading('输出格式')
para('对于每个测试用例，如果对应的字符串是 YesYesYes... 的子串，则打印 "YES"，否则打印 "NO"。')
para('你可以以任意大小写形式打印每个字母。例如，字符串 "yEs"、"yes"、"Yes" 和 "YES" 都将被视为肯定回答。')
heading('样例')
inp=(root/'data/samples/01.in').read_text().splitlines()
out=(root/'data/samples/01.out').read_text().splitlines()
top=y
mid=w/2
row_h=15
height=25+row_h*max(len(inp),len(out))+6
c.setStrokeColor(colors.black)
c.rect(left,top-height,right-left,height)
c.line(mid,top,mid,top-height)
c.line(left,top-22,right,top-22)
c.setFont('SimHei',11)
c.drawCentredString((left+mid)/2,top-16,'标准输入')
c.drawCentredString((mid+right)/2,top-16,'标准输出')
c.setFont('Courier',9)
for i,s in enumerate(inp): c.drawString(left+8,top-36-row_h*i,s)
for i,s in enumerate(out): c.drawString(mid+8,top-36-row_h*i,s)
assert top-height > 35
c.showPage()
c.save()
