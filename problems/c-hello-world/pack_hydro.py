"""Build the Hydro import package and archive after the PID is confirmed."""
import argparse
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("pid", help="Confirmed Hydro problem ID, such as ZXS2026C")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,20}", args.pid):
    parser.error("invalid Hydro PID")

meta = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
name = f"C-{args.pid}"
target = ROOT / "hydro" / name
if target.exists():
    shutil.rmtree(target)
(target / "testdata").mkdir(parents=True)
(target / "additional_file").mkdir()

(target / "problem.yaml").write_text(
    f"pid: {args.pid}\nowner: 1\ntitle: {meta['title']}\ntag: []\nnSubmit: 0\nnAccept: 0\n",
    encoding="utf-8",
)
(target / "problem_zh.md").write_text("@[pdf](file://statement.pdf)\n", encoding="utf-8")
shutil.copy2(ROOT / "statement.pdf", target / "additional_file" / "statement.pdf")

cases = []
for folder, prefix in ((ROOT / "data" / "samples", "sample"), (ROOT / "data" / "tests", "case")):
    if not folder.is_dir():
        continue
    for inp in sorted(folder.glob("*.in")):
        stem = f"{prefix}{inp.stem}"
        out = inp.with_suffix(".out")
        if not out.is_file():
            raise SystemExit(f"Missing answer: {out}")
        shutil.copy2(inp, target / "testdata" / f"{stem}.in")
        shutil.copy2(out, target / "testdata" / f"{stem}.ans")
        cases.append(stem)
if not cases:
    raise SystemExit("No test cases found")
if not any((ROOT / "data" / "samples").glob("*.in")):
    raise SystemExit("Sample data is required")

config = (
    "type: default\n"
    "checker_type: default\n"
    f"time: {meta['time_limit_ms'] / 1000:g}s\n"
    f"memory: {meta['memory_limit_mb']}m\n"
    "cases:\n"
)
for stem in cases:
    config += f"  - input: {stem}.in\n    output: {stem}.ans\n"
(target / "testdata" / "config.yaml").write_text(config, encoding="utf-8")

archive = ROOT / "hydro" / f"{name}.zip"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for path in sorted(target.rglob("*")):
        if path.is_file():
            z.write(path, Path(name) / path.relative_to(target))
print(archive)
