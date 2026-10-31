"""Validate the private data and compare independent accepted solutions."""
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)

CORRECT = ("solution.cpp", "solution2.cpp")
WRONG = ("wrong_single_pass.cpp", "wrong_strict.cpp", "wrong_initial.cpp")


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
    return int(subprocess.check_output([str(exe)], input=raw).strip())


def parse(raw):
    values = list(map(int, raw.split()))
    assert len(values) >= 2
    n, jump = values[0], values[1]
    height = values[2:]
    assert 1 <= n <= 1000
    assert 1 <= jump <= 10000
    assert len(height) == n
    assert all(1 <= value <= 10000 for value in height)
    return n, jump, height


def brute(n, jump, height):
    full = 1 << n
    reachable = [False] * full
    reachable[0] = True
    best = 0
    for mask in range(full):
        if not reachable[mask]:
            continue
        eaten = mask.bit_count()
        best = max(best, eaten)
        current = jump + eaten
        for i in range(n):
            if not (mask >> i) & 1 and height[i] <= current:
                reachable[mask | (1 << i)] = True
    return jump + best


checked = 0
for directory in (ROOT / "data" / "samples", ROOT / "data" / "tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}
    for inp in inputs:
        raw = inp.read_bytes()
        n, jump, height = parse(raw)
        expected = int(inp.with_suffix(".out").read_text().strip())
        assert jump <= expected <= jump + n
        for exe in correct_exes:
            actual = run(exe, raw)
            assert actual == expected, (inp.name, exe.name, actual, expected)
        checked += 1
    print(f"{directory.name}: {len(inputs)} cases passed")
print(f"all data: {checked} cases passed with both accepted solutions")

rng = random.Random(20261030)
for _ in range(300):
    n = rng.randint(1, 10)
    jump = rng.randint(1, 8)
    height = [rng.randint(1, 15) for _ in range(n)]
    raw = (f"{n} {jump}\n" + " ".join(map(str, height)) + "\n").encode()
    expected = brute(n, jump, height)
    for exe in correct_exes:
        actual = run(exe, raw)
        assert actual == expected, (n, jump, height, exe.name, actual, expected)
print("brute force: 300 random small cases passed")

targets = {
    "wrong_single_pass.cpp": ("10", "single pass in input order"),
    "wrong_strict.cpp": ("11", "strict comparison instead of not-greater"),
    "wrong_initial.cpp": ("12", "counting only initially reachable fruits"),
}
for name, (stem, description) in targets.items():
    inp = ROOT / "data" / "tests" / f"{stem}.in"
    expected = int(inp.with_suffix(".out").read_text().strip())
    actual = run(wrong_exes[name], inp.read_bytes())
    assert actual != expected, (name, stem, actual, expected)
    print(f"{name}: rejected by case {stem} ({description})")

generator_cases = (
    ("01", "min-reach"), ("02", "min-unreach"), ("03", "max-all-reach"),
    ("04", "max-unreach"), ("05", "all-one"), ("06", "equal-mid"),
    ("07", "increasing"), ("08", "decreasing"), ("09", "gap"),
    ("10", "unordered"), ("11", "equality"), ("12", "initial-only"),
    ("13", "boundary-L"), ("14", "random-small"), ("15", "random-medium"),
    ("16", "random-large"), ("17", "random-large-L"),
    ("18", "random-all-unreach"), ("19", "random-large-mid"),
    ("20", "random-small2"),
)
for stem, kind in generator_cases:
    assert (ROOT / "data" / "tests" / f"{stem}.in").is_file(), (stem, kind)
print("test set: all 20 generated cases present")

print("validation passed")
