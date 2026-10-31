"""Validate the private data and compare independent accepted solutions."""
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)

CORRECT = ("solution.cpp", "solution2.cpp")
WRONG = ("wrong_original.cpp", "wrong_reverse_rows.cpp")


def compile_source(name):
    exe = BUILD / (Path(name).stem + ".exe")
    subprocess.run(
        ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra",
         str(ROOT / name), "-o", str(exe)],
        check=True,
    )
    return exe


correct_exes = [compile_source(name) for name in CORRECT]
wrong_exes = {name: compile_source(name) for name in WRONG}


def run(exe, raw):
    return subprocess.check_output([str(exe)], input=raw).decode().split()


def parse(raw):
    values = list(map(int, raw.split()))
    assert len(values) >= 2
    n, m = values[0], values[1]
    flat = values[2:]
    assert 1 <= n <= 100 and 1 <= m <= 100
    assert len(flat) == n * m
    assert all(1 <= value <= 1000 for value in flat)
    return n, m, [flat[i * m:(i + 1) * m] for i in range(n)]


def reference(a):
    n = len(a)
    m = len(a[0])
    return [str(a[i][j]) for j in range(m) for i in range(n)]


checked = 0
for directory in (ROOT / "data" / "samples", ROOT / "data" / "tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}
    for inp in inputs:
        raw = inp.read_bytes()
        n, m, a = parse(raw)
        expected = reference(a)
        stored = inp.with_suffix(".out").read_text().split()
        assert stored == expected, inp.name
        for exe in correct_exes:
            actual = run(exe, raw)
            assert actual == expected, (inp.name, exe.name)
        checked += 1
    print(f"{directory.name}: {len(inputs)} cases passed")
print(f"all data: {checked} cases passed with both accepted solutions")

rng = random.Random(20261031)
for _ in range(200):
    n = rng.randint(1, 12)
    m = rng.randint(1, 12)
    a = [[rng.randint(1, 1000) for _ in range(m)] for _ in range(n)]
    raw = (f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in a) + "\n").encode()
    expected = reference(a)
    for exe in correct_exes:
        actual = run(exe, raw)
        assert actual == expected, (n, m, exe.name)
print("random matrices: 200 cases passed")

targets = {
    "wrong_original.cpp": ("11", "printing the original matrix"),
    "wrong_reverse_rows.cpp": ("11", "reversing each transposed row"),
}
for name, (stem, description) in targets.items():
    inp = ROOT / "data" / "tests" / f"{stem}.in"
    n, m, a = parse(inp.read_bytes())
    expected = reference(a)
    actual = run(wrong_exes[name], inp.read_bytes())
    assert actual != expected, (name, stem)
    print(f"{name}: rejected by case {stem} ({description})")

generator_cases = (
    ("01", "min"), ("02", "min-max"), ("03", "row"), ("04", "col"),
    ("05", "max"), ("06", "max-values"), ("07", "equal"),
    ("08", "increasing"), ("09", "decreasing"), ("10", "symmetric"),
    ("11", "random-tall"), ("12", "random-wide"), ("13", "random-small"),
    ("14", "random-medium"), ("15", "boundary"),
)
for stem, kind in generator_cases:
    assert (ROOT / "data" / "tests" / f"{stem}.in").is_file(), (stem, kind)
print("test set: all 15 generated cases present")

print("validation passed")
