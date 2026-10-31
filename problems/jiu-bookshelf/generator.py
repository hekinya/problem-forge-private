"""Reproducible internal test generator: python generator.py TYPE SEED."""
import argparse
import random

MAX_N = 200000
MAX_V = 10**9


def build(kind, seed):
    rng = random.Random(seed)

    if kind == "min":
        return 1, 1, [1]
    if kind == "single-max":
        return 1, 1, [MAX_V]
    if kind == "two-k1":
        return 2, 1, [MAX_V, MAX_V]
    if kind == "two-kn":
        return 2, 2, [MAX_V, MAX_V]
    if kind == "avg-fail":
        return 4, 3, [4, 3, 3, 4]
    if kind == "exact-k-fail":
        return 4, 3, [1, 1, 1, 1]
    if kind == "int32-overflow":
        return 5, 2, [MAX_V] * 5
    if kind == "overflow-k1":
        return MAX_N, 1, [MAX_V] * MAX_N
    if kind == "max-kn":
        return MAX_N, MAX_N, [MAX_V] * MAX_N
    if kind == "equal":
        return 100, 37, [5] * 100
    if kind == "equal-large":
        return MAX_N, 99999, [123456789] * MAX_N

    if kind == "increasing-large":
        n = MAX_N
        k = 100000
        return n, k, [1 + 4999 * i for i in range(n)]

    if kind == "staircase-large":
        n = MAX_N
        k = 77777
        half = n // 2
        return n, k, [1 + (i if i <= half else n - i) for i in range(n)]

    if kind == "random-small":
        n = rng.randint(1, 60)
        k = rng.randint(1, n)
        return n, k, [rng.randint(1, 20) for _ in range(n)]

    if kind == "random-medium":
        n = 2000
        k = rng.randint(1, n)
        return n, k, [rng.randint(1, 10**6) for _ in range(n)]

    if kind == "random-large":
        n = MAX_N
        k = rng.randint(1, n)
        return n, k, [rng.randint(1, MAX_V) for _ in range(n)]

    if kind == "random-large-k1":
        n = MAX_N
        return n, 1, [rng.randint(1, MAX_V) for _ in range(n)]

    if kind == "random-large-kn":
        n = MAX_N
        return n, n, [rng.randint(1, MAX_V) for _ in range(n)]

    raise ValueError(f"unknown test type: {kind}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=(
        "min", "single-max", "two-k1", "two-kn", "avg-fail", "exact-k-fail",
        "int32-overflow", "overflow-k1", "max-kn", "equal", "equal-large",
        "increasing-large", "staircase-large", "random-small", "random-medium",
        "random-large", "random-large-k1", "random-large-kn",
    ))
    parser.add_argument("seed", type=int)
    args = parser.parse_args()

    n, k, a = build(args.type, args.seed)
    print(n, k)
    print(*a)


if __name__ == "__main__":
    main()
