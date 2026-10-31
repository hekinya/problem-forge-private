"""Generate the private test set and reference answers."""
from pathlib import Path

from generator import build

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "data" / "tests"

CASES = (
    ("01", "min-reach", 1),
    ("02", "min-unreach", 2),
    ("03", "max-all-reach", 3),
    ("04", "max-unreach", 4),
    ("05", "all-one", 5),
    ("06", "equal-mid", 6),
    ("07", "increasing", 7),
    ("08", "decreasing", 8),
    ("09", "gap", 9),
    ("10", "unordered", 10),
    ("11", "equality", 11),
    ("12", "initial-only", 12),
    ("13", "boundary-L", 13),
    ("14", "random-small", 14),
    ("15", "random-medium", 15),
    ("16", "random-large", 16),
    ("17", "random-large-L", 17),
    ("18", "random-all-unreach", 18),
    ("19", "random-large-mid", 19),
    ("20", "random-small2", 20),
)


def reference(n, jump, height):
    for value in sorted(height):
        if value <= jump:
            jump += 1
        else:
            break
    return jump


def main():
    TESTS.mkdir(parents=True, exist_ok=True)
    for stem, kind, seed in CASES:
        n, jump, height = build(kind, seed)
        assert 1 <= n <= 1000, (stem, n)
        assert 1 <= jump <= 10000, (stem, jump)
        assert len(height) == n
        assert all(1 <= value <= 10000 for value in height), stem

        answer = reference(n, jump, height)
        assert jump <= answer <= jump + n
        if kind == "min-reach":
            assert answer == 2
        if kind == "min-unreach":
            assert answer == 1
        if kind == "unordered":
            assert answer == 6
        if kind == "initial-only":
            assert answer == 8

        (TESTS / f"{stem}.in").write_text(
            f"{n} {jump}\n" + " ".join(map(str, height)) + "\n", encoding="utf-8"
        )
        (TESTS / f"{stem}.out").write_text(f"{answer}\n", encoding="utf-8")
        print(f"{stem}: {kind} n={n} L={jump} answer={answer}")


if __name__ == "__main__":
    main()
