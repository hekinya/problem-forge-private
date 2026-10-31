"""Reproducible internal test generator: python generator.py TYPE SEED."""
import argparse
import random

MAX_N = 1000
MAX_VALUE = 10000


def build(kind, seed):
    rng = random.Random(seed)

    if kind == "min-reach":
        return 1, 1, [1]
    if kind == "min-unreach":
        return 1, 1, [2]
    if kind == "max-all-reach":
        return MAX_N, MAX_VALUE, [MAX_VALUE] * MAX_N
    if kind == "max-unreach":
        return MAX_N, 1, [MAX_VALUE] * MAX_N
    if kind == "all-one":
        return MAX_N, 1, [1] * MAX_N
    if kind == "equal-mid":
        return MAX_N, 5000, [5000] * MAX_N
    if kind == "increasing":
        return MAX_N, 1, [i + 1 for i in range(MAX_N)]
    if kind == "decreasing":
        return MAX_N, 1, [MAX_N - i for i in range(MAX_N)]
    if kind == "gap":
        return 10, 5, [5, 5, 5, 100, 100, 100, 1, 2, 3, 4]
    if kind == "unordered":
        return 3, 3, [5, 3, 4]
    if kind == "equality":
        return 1, 5, [5]
    if kind == "initial-only":
        return 3, 5, [5, 6, 7]
    if kind == "boundary-L":
        return MAX_N, 9999, [MAX_VALUE] * MAX_N

    if kind == "random-small":
        n = 20
        jump = 5
        return n, jump, [rng.randint(1, 100) for _ in range(n)]
    if kind == "random-medium":
        n = 200
        jump = 100
        return n, jump, [rng.randint(1, MAX_VALUE) for _ in range(n)]
    if kind == "random-large":
        n = MAX_N
        jump = 1
        return n, jump, [rng.randint(1, MAX_VALUE) for _ in range(n)]
    if kind == "random-large-L":
        n = MAX_N
        jump = MAX_VALUE
        return n, jump, [rng.randint(1, MAX_VALUE) for _ in range(n)]
    if kind == "random-all-unreach":
        n = MAX_N
        jump = 1
        return n, jump, [rng.randint(2, MAX_VALUE) for _ in range(n)]
    if kind == "random-large-mid":
        n = MAX_N
        jump = 5000
        return n, jump, [rng.randint(1, MAX_VALUE) for _ in range(n)]
    if kind == "random-small2":
        n = 50
        jump = 10
        return n, jump, [rng.randint(1, 50) for _ in range(n)]

    raise ValueError(f"unknown test type: {kind}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=(
        "min-reach", "min-unreach", "max-all-reach", "max-unreach",
        "all-one", "equal-mid", "increasing", "decreasing", "gap",
        "unordered", "equality", "initial-only", "boundary-L",
        "random-small", "random-medium", "random-large", "random-large-L",
        "random-all-unreach", "random-large-mid", "random-small2",
    ))
    parser.add_argument("seed", type=int)
    args = parser.parse_args()

    n, jump, height = build(args.type, args.seed)
    print(n, jump)
    print(*height)


if __name__ == "__main__":
    main()
