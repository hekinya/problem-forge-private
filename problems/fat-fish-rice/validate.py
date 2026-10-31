"""Validate fat-fish-rice data, cross-check two accepted solutions and reject wrong solutions."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)
MAX_A, MAX_B = 10 ** 4, 9
PRICE = 19


def build(source: str) -> Path:
    exe = BUILD / (Path(source).stem + ".exe")
    subprocess.run(
        ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / source), "-o", str(exe)],
        check=True,
    )
    return exe


def expected(a: int, b: int) -> int:
    return (10 * a + b) // PRICE


def run(exe: Path, raw: bytes) -> int:
    return int(subprocess.check_output([str(exe)], input=raw).strip())


def check(raw: bytes) -> tuple[int, int, int]:
    values = list(map(int, raw.split()))
    assert len(values) == 2, f"期望两个整数，实际为 {values}"
    a, b = values
    assert 0 <= a <= MAX_A and 0 <= b <= MAX_B, f"越界输入：{a} {b}"
    answer = expected(a, b)
    for exe in (accepted_cpp,):
        got = run(exe, raw)
        assert got == answer, f"{exe.name}：{a} {b} 输出 {got}，应为 {answer}"
    got = int(subprocess.check_output([sys.executable, str(ROOT / "solution2.py")], input=raw).strip())
    assert got == answer, f"solution2.py：{a} {b} 输出 {got}，应为 {answer}"
    return a, b, answer


accepted_cpp = build("solution.cpp")
wrong_ignore_b = build("wrong_ignore_b.cpp")
wrong_round_up = build("wrong_round_up.cpp")

all_inputs: list[Path] = []
for directory in (ROOT / "data/samples", ROOT / "data/tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs, f"{directory} 中没有测试数据"
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}, f"{directory} 中 .in / .out 未成对"
    for inp in inputs:
        answer = int(inp.with_suffix(".out").read_text(encoding="utf-8").strip())
        _, _, oracle = check(inp.read_bytes())
        assert answer == oracle, f"{inp.name} 的答案文件 {answer} 与独立计算 {oracle} 不一致"
        all_inputs.append(inp)
    print(f"{directory.name}: {len(inputs)} 个用例通过")

statement = (ROOT / "statement.md").read_text(encoding="utf-8")
sample_in = (ROOT / "data/samples/01.in").read_text(encoding="utf-8").strip()
sample_out = (ROOT / "data/samples/01.out").read_text(encoding="utf-8").strip()
assert f"```text\n{sample_in}\n```" in statement, "题面样例输入与 data/samples/01.in 不一致"
assert f"```text\n{sample_out}\n```" in statement, "题面样例输出与 data/samples/01.out 不一致"
print("statement: 样例与 data/samples 一致")

rng = random.Random(20261031)
for _ in range(500):
    check(f"{rng.randint(0, MAX_A)} {rng.randint(0, MAX_B)}\n".encode())
print("random: 500 个用例通过")

for name, exe in (("wrong_ignore_b", wrong_ignore_b), ("wrong_round_up", wrong_round_up)):
    rejected = []
    for inp in all_inputs:
        raw = inp.read_bytes()
        a, b = map(int, raw.split())
        if run(exe, raw) != expected(a, b):
            rejected.append(inp.name)
    assert rejected, f"{name} 没有被任何用例拒绝"
    print(f"{name}: 被 {len(rejected)} 个用例拒绝（例如 {rejected[0]}）")

sys.path.insert(0, str(ROOT))
from generator import KINDS, generate  # noqa: E402

for kind in KINDS:
    for seed in (1, 2, 3, 20261031):
        a, b = generate(kind, seed)
        assert 0 <= a <= MAX_A and 0 <= b <= MAX_B, f"generator {kind}/{seed} 越界：{a} {b}"
        check(f"{a} {b}\n".encode())
print(f"generator: {len(KINDS)} 种类型 × 4 个种子通过")
print("全部检查通过")
