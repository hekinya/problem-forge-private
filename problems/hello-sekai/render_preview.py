"""Render statement.pdf to an image and verify the required content is visible."""
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "statement.pdf"
doc = fitz.open(PDF)
assert doc.page_count == 1, f"expected a single page, got {doc.page_count}"
page = doc[0]
text = page.get_text()
for needle in (
    "2026 HHACM 招新赛",
    "Problem C. Hello sekai",
    "输入文件",
    "输出文件",
    "时间限制",
    "内存限制",
    "本题没有输入",
    "Hello sekai",
):
    assert needle in text, f"missing on page: {needle}"
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
preview = ROOT / "statement-preview.png"
pix.save(preview)
print(preview)
