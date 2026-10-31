"""Generate one test case for the fat-fish-rice problem: python generator.py <kind> <seed>."""
import random
import sys

MAX_A = 10 ** 4
MAX_B = 9
MAX_TOTAL = 10 * MAX_A + MAX_B
PRICE = 19
KINDS = ("min", "max", "random", "small", "edge", "multiple")


def generate(kind: str, seed: int) -> tuple[int, int]:
    """Return (a, b) with 10a + b tokens in the wallet."""
    rng = random.Random(seed * 1000003 + KINDS.index(kind))
    if kind == "min":
        return 0, 0
    if kind == "max":
        return MAX_A, MAX_B
    if kind == "small":
        return rng.randint(0, 3), rng.randint(0, 9)
    if kind == "multiple":
        # 10a + b 恰好是一碗价格 19 的整数倍。
        return divmod(PRICE * rng.randint(0, MAX_TOTAL // PRICE), 10)
    if kind == "edge":
        # 围绕 19 的倍数前后各偏移一点，卡住取整边界。
        total = PRICE * rng.randint(0, MAX_TOTAL // PRICE) + rng.choice((0, -1, 1, 18, 19))
        return divmod(max(0, min(MAX_TOTAL, total)), 10)
    return rng.randint(0, MAX_A), rng.randint(0, MAX_B)


def main() -> int:
    kind = sys.argv[1] if len(sys.argv) > 1 else "random"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if kind not in KINDS:
        raise SystemExit(f"unknown kind: {kind}")
    a, b = generate(kind, seed)
    print(a, b)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
