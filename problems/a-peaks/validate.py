"""Validate A problem data and compare two independent accepted solutions."""
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)
SOURCES = ("solution.cpp", "solution2.cpp")
executables = []
for source in SOURCES:
    exe = BUILD / (Path(source).stem + ".exe")
    subprocess.run(["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / source), "-o", str(exe)], check=True)
    executables.append(exe)

def check(raw: bytes, expected: int | None = None):
    values = list(map(int, raw.split()))
    assert values
    n, a = values[0], values[1:]
    assert 1 <= n <= 200000 and len(a) == n
    assert all(-10**9 <= value <= 10**9 for value in a)
    oracle = sum(a[i] > a[i - 1] and a[i] > a[i + 1] for i in range(1, n - 1))
    if expected is not None:
        assert expected == oracle
    for exe in executables:
        actual = int(subprocess.check_output([str(exe)], input=raw).strip())
        assert actual == oracle, (exe, actual, oracle)
    return oracle

for directory in (ROOT / "data/samples", ROOT / "data/tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}
    for inp in inputs:
        check(inp.read_bytes(), int(inp.with_suffix(".out").read_text()))
    print(f"{directory.name}: {len(inputs)} cases passed")

rng = random.Random(20261028)
for _ in range(500):
    n = rng.randint(1, 100)
    a = [rng.randint(-3, 3) for _ in range(n)]
    check((str(n) + "\n" + " ".join(map(str, a)) + "\n").encode())
print("random: 500 cases passed")

wrong = BUILD / "wrong_equal.exe"
subprocess.run(["g++", "-std=gnu++20", "-O2", str(ROOT / "wrong_equal.cpp"), "-o", str(wrong)], check=True)
equal_case = (ROOT / "data/tests/05.in").read_bytes()
assert int(subprocess.check_output([str(wrong)], input=equal_case).strip()) != check(equal_case)
print("wrong_equal: rejected by case 05")

for kind in ("min", "max", "random-small", "random-large", "equal"):
    raw = subprocess.check_output(["python", str(ROOT / "generator.py"), kind, "20261028"])
    check(raw)
print("generator: all 5 types passed")
