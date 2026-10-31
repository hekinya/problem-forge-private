"""Build the Hydro import archive after the contest PID is confirmed."""
import argparse
from pathlib import Path
import json
import re
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))

parser = argparse.ArgumentParser()
parser.add_argument("pid", help="Confirmed Hydro problem ID, such as T1001")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,20}", args.pid):
    parser.error("invalid Hydro PID")

name = args.pid
target = ROOT / "hydro" / name
if target.exists():
    shutil.rmtree(target)
(target / "testdata").mkdir(parents=True)
(target / "additional_file").mkdir()

(target / "problem.yaml").write_text(
    f"pid: {args.pid}\nowner: 1\ntitle: {config['title']}\n"
    "tag: []\nnSubmit: 0\nnAccept: 0\n",
    encoding="utf-8",
)
(target / "problem_zh.md").write_text(
    "@[pdf](file://statement.pdf)\n", encoding="utf-8"
)
shutil.copy2(ROOT / "statement.pdf", target / "additional_file" / "statement.pdf")

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

time_limit = config["time_limit_ms"] / 1000
config_text = (
    "type: default\n"
    "checker_type: default\n"
    f"time: {time_limit:g}s\n"
    f"memory: {config['memory_limit_mb']}m\n"
    "cases:\n"
)
for stem in cases:
    config_text += f"  - input: {stem}.in\n    output: {stem}.ans\n"
(target / "testdata" / "config.yaml").write_text(config_text, encoding="utf-8")

archive = ROOT / "hydro" / f"{name}.zip"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for path in sorted(target.rglob("*")):
        if path.is_file():
            z.write(path, Path(name) / path.relative_to(target))
print(archive)
