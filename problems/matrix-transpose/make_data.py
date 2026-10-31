"""Generate the private test set and reference answers."""
from pathlib import Path

from generator import build

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "data" / "tests"

CASES = (
    ("01", "min", 1),
    ("02", "min-max", 2),
    ("03", "row", 3),
    ("04", "col", 4),
    ("05", "max", 5),
    ("06", "max-values", 6),
    ("07", "equal", 7),
    ("08", "increasing", 8),
    ("09", "decreasing", 9),
    ("10", "symmetric", 10),
    ("11", "random-tall", 11),
    ("12", "random-wide", 12),
    ("13", "random-small", 13),
    ("14", "random-medium", 14),
    ("15", "boundary", 15),
)


def reference(a):
    n = len(a)
    m = len(a[0])
    return [[a[i][j] for i in range(n)] for j in range(m)]


def main():
    TESTS.mkdir(parents=True, exist_ok=True)
    for stem, kind, seed in CASES:
        n, m, a = build(kind, seed)
        assert 1 <= n <= 100 and 1 <= m <= 100, (stem, n, m)
        assert len(a) == n and all(len(row) == m for row in a), stem
        assert all(1 <= value <= 1000 for row in a for value in row), stem

        transposed = reference(a)
        (TESTS / f"{stem}.in").write_text(
            f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in a) + "\n",
            encoding="utf-8",
        )
        (TESTS / f"{stem}.out").write_text(
            "\n".join(" ".join(map(str, row)) for row in transposed) + "\n",
            encoding="utf-8",
        )
        print(f"{stem}: {kind} n={n} m={m}")


if __name__ == "__main__":
    main()
