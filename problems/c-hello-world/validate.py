"""Validate the sign-in problem data and cross-check both accepted solutions."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)
TMP = BUILD / "tmp"
TMP.mkdir(exist_ok=True)
os.environ["TMP"] = os.environ["TEMP"] = os.environ["TMPDIR"] = str(TMP)

metadata = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
assert metadata["title"] == "Hello World", metadata["title"]
assert metadata["time_limit_ms"] > 0 and metadata["memory_limit_mb"] > 0

statement = (ROOT / "statement.md").read_text(encoding="utf-8")
assert "# Hello World" in statement and "请填写" not in statement
assert "本题没有输入" in statement and "Hello World" in statement

expected = b"Hello World\n"


def normalize(raw: bytes) -> bytes:
    """Windows text-mode stdout emits CRLF; compare with LF-normalized bytes."""
    return raw.replace(b"\r\n", b"\n")


for folder in ("data/samples", "data/tests"):
    directory = ROOT / folder
    if not directory.is_dir():
        continue
    inputs = sorted(directory.glob("*.in"))
    assert inputs, f"{folder} has no input"
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}, folder
    for inp in inputs:
        assert inp.read_bytes() == b"", f"{inp} must be empty (no input)"
        out = inp.with_suffix(".out")
        assert out.read_bytes() == expected, (out, out.read_bytes())
        print(f"{inp.relative_to(ROOT)}: empty input, exact answer passed")

exe = BUILD / "solution.exe"
subprocess.run(
    ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / "solution.cpp"), "-o", str(exe)],
    check=True,
)
wrong = BUILD / "wrong_hello_world.exe"
subprocess.run(
    ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / "wrong_hello_world.cpp"), "-o", str(wrong)],
    check=True,
)

for inp in sorted((ROOT / "data").rglob("*.in")):
    raw = inp.read_bytes()
    cpp = normalize(subprocess.check_output([str(exe)], input=raw))
    python = normalize(subprocess.check_output([sys.executable, str(ROOT / "solution2.py")], input=raw))
    assert cpp == python == expected, (inp, cpp, python)
    rejected = normalize(subprocess.check_output([str(wrong)], input=raw))
    assert rejected != expected, (inp, rejected)
    print(f"{inp.relative_to(ROOT)}: two accepted solutions match, wrong solution rejected")

print("All checks passed")
