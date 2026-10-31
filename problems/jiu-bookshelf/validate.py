"""Validate the private data and compare independent accepted solutions."""
from itertools import combinations
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)

CORRECT = ("solution.cpp", "solution2.cpp")
WRONG = ("wrong_avg.cpp", "wrong_exact.cpp", "wrong_int32.cpp")


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
    n, k = values[0], values[1]
    a = values[2:]
    assert 1 <= k <= n <= 200000
    assert len(a) == n
    assert all(1 <= value <= 10**9 for value in a)
    return n, k, a


def brute(n, k, a):
    best = 10**30
    for cuts in combinations(range(1, n), k - 1):
        previous = 0
        largest = 0
        for cut in cuts + (n,):
            largest = max(largest, sum(a[previous:cut]))
            previous = cut
        best = min(best, largest)
    return best


checked = 0
for directory in (ROOT / "data" / "samples", ROOT / "data" / "tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}
    for inp in inputs:
        raw = inp.read_bytes()
        n, k, a = parse(raw)
        expected = int(inp.with_suffix(".out").read_text().strip())
        assert max(a) <= expected <= sum(a)
        if k == 1:
            assert expected == sum(a), inp.name
        if k == n:
            assert expected == max(a), inp.name
        for exe in correct_exes:
            actual = run(exe, raw)
            assert actual == expected, (inp.name, exe.name, actual, expected)
        checked += 1
    print(f"{directory.name}: {len(inputs)} cases passed")
print(f"all data: {checked} cases passed with both accepted solutions")

rng = random.Random(20261030)
for _ in range(300):
    n = rng.randint(1, 8)
    k = rng.randint(1, n)
    a = [rng.randint(1, 9) for _ in range(n)]
    raw = (f"{n} {k}\n" + " ".join(map(str, a)) + "\n").encode()
    expected = brute(n, k, a)
    for exe in correct_exes:
        actual = run(exe, raw)
        assert actual == expected, (n, k, a, exe.name, actual, expected)
print("brute force: 300 random small cases passed")

targets = {
    "wrong_avg.cpp": ("05", "average-based greedy"),
    "wrong_exact.cpp": ("06", "requiring exactly K greedy groups"),
    "wrong_int32.cpp": ("07", "32-bit sum overflow"),
}
for name, (stem, description) in targets.items():
    inp = ROOT / "data" / "tests" / f"{stem}.in"
    expected = int(inp.with_suffix(".out").read_text().strip())
    actual = run(wrong_exes[name], inp.read_bytes())
    assert actual != expected, (name, stem, actual, expected)
    print(f"{name}: rejected by case {stem} ({description})")

generator_cases = (
    ("01", "min"), ("02", "single-max"), ("03", "two-k1"), ("04", "two-kn"),
    ("05", "avg-fail"), ("06", "exact-k-fail"), ("07", "int32-overflow"),
    ("08", "overflow-k1"), ("09", "max-kn"), ("10", "equal"),
    ("11", "equal-large"), ("12", "increasing-large"), ("13", "staircase-large"),
    ("14", "random-small"), ("15", "random-medium"), ("16", "random-large"),
    ("17", "random-large-k1"), ("18", "random-large-kn"),
)
for stem, kind in generator_cases:
    assert (ROOT / "data" / "tests" / f"{stem}.in").is_file(), (stem, kind)
print("test set: all 18 generated cases present")

print("validation passed")
