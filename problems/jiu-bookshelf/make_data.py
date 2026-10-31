"""Generate the private test set and reference answers."""
from pathlib import Path

from generator import build

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "data" / "tests"

CASES = (
    ("01", "min", 1),
    ("02", "single-max", 2),
    ("03", "two-k1", 3),
    ("04", "two-kn", 4),
    ("05", "avg-fail", 5),
    ("06", "exact-k-fail", 6),
    ("07", "int32-overflow", 7),
    ("08", "overflow-k1", 8),
    ("09", "max-kn", 9),
    ("10", "equal", 10),
    ("11", "equal-large", 11),
    ("12", "increasing-large", 12),
    ("13", "staircase-large", 13),
    ("14", "random-small", 14),
    ("15", "random-medium", 15),
    ("16", "random-large", 16),
    ("17", "random-large-k1", 17),
    ("18", "random-large-kn", 18),
)


def reference(n, k, a):
    low, high = max(a), sum(a)
    while low < high:
        limit = low + (high - low) // 2
        groups = 1
        current = 0
        for i in range(n - 1, -1, -1):
            value = a[i]
            if current + value > limit:
                groups += 1
                current = value
            else:
                current += value
        if groups <= k:
            high = limit
        else:
            low = limit + 1
    return low


def main():
    TESTS.mkdir(parents=True, exist_ok=True)
    for stem, kind, seed in CASES:
        n, k, a = build(kind, seed)
        assert 1 <= k <= n <= 200000, (stem, n, k)
        assert len(a) == n
        assert all(1 <= value <= 10**9 for value in a), stem

        answer = reference(n, k, a)
        assert answer >= max(a) and answer <= sum(a)
        if k == 1:
            assert answer == sum(a), stem
        if k == n:
            assert answer == max(a), stem

        (TESTS / f"{stem}.in").write_text(
            f"{n} {k}\n" + " ".join(map(str, a)) + "\n", encoding="utf-8"
        )
        (TESTS / f"{stem}.out").write_text(f"{answer}\n", encoding="utf-8")
        print(f"{stem}: {kind} n={n} k={k} answer={answer}")


if __name__ == "__main__":
    main()
