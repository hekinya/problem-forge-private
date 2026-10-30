"""Build the Hydro import archive after the contest PID is confirmed."""
import argparse
from pathlib import Path
import re
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("pid", help="Confirmed Hydro problem ID, such as T1001")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,20}", args.pid):
    parser.error("invalid Hydro PID")

name = f"A-{args.pid}"
target = ROOT / "hydro" / name
(target / "testdata").mkdir(parents=True, exist_ok=True)
(target / "additional_file").mkdir(exist_ok=True)
(target / "problem.yaml").write_text(
    f"pid: {args.pid}\nowner: 1\ntitle: 数列中的山峰\ntag: []\nnSubmit: 0\nnAccept: 0\n",
    encoding="utf-8",
)
(target / "problem_zh.md").write_text(
    "![题面第 1 页](file://statement-01.png)\n", encoding="utf-8"
)
old_image = target / "additional_file" / "statement-01.png"
if old_image.exists():
    old_image.unlink()
shutil.copy2(ROOT / "statement-v2.png", target / "additional_file" / "statement-01.png")

data = ROOT / "data"
cases = []
for folder, prefix in ((data / "samples", "sample"), (data / "tests", "case")):
    for inp in sorted(folder.glob("*.in")):
        stem = f"{prefix}{inp.stem}"
        out = inp.with_suffix(".out")
        if not out.is_file():
            raise SystemExit(f"Missing answer: {out}")
        shutil.copy2(inp, target / "testdata" / f"{stem}.in")
        shutil.copy2(out, target / "testdata" / f"{stem}.ans")
        cases.append(stem)

config = "type: default\nchecker_type: default\ntime: 1s\nmemory: 256m\ncases:\n"
for stem in cases:
    config += f"  - input: {stem}.in\n    output: {stem}.ans\n"
(target / "testdata" / "config.yaml").write_text(config, encoding="utf-8")

archive = ROOT / "hydro" / f"{name}.zip"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for path in sorted(target.rglob("*")):
        if path.is_file():
            z.write(path, Path(name) / path.relative_to(target))
print(archive)
