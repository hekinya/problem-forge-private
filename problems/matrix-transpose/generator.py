"""Reproducible internal test generator: python generator.py TYPE SEED."""
import argparse
import random

MAX_N = 100
MAX_M = 100
MAX_VALUE = 1000


def build(kind, seed):
    rng = random.Random(seed)

    if kind == "min":
        return 1, 1, [[7]]
    if kind == "min-max":
        return 1, 1, [[MAX_VALUE]]
    if kind == "row":
        return 1, MAX_M, [[j + 1 for j in range(MAX_M)]]
    if kind == "col":
        return MAX_N, 1, [[i + 1] for i in range(MAX_N)]
    if kind == "max":
        return MAX_N, MAX_M, [
            [rng.randint(1, MAX_VALUE) for _ in range(MAX_M)]
            for _ in range(MAX_N)
        ]
    if kind == "max-values":
        return MAX_N, MAX_M, [[MAX_VALUE] * MAX_M for _ in range(MAX_N)]
    if kind == "equal":
        return MAX_N, MAX_M, [[42] * MAX_M for _ in range(MAX_N)]
    if kind == "increasing":
        return MAX_N, MAX_M, [
            [(i * MAX_M + j) % MAX_VALUE + 1 for j in range(MAX_M)]
            for i in range(MAX_N)
        ]
    if kind == "decreasing":
        return MAX_N, MAX_M, [
            [MAX_VALUE - ((i * MAX_M + j) % MAX_VALUE) for j in range(MAX_M)]
            for i in range(MAX_N)
        ]
    if kind == "symmetric":
        return MAX_N, MAX_M, [
            [min(MAX_VALUE, i + j + 1) for j in range(MAX_M)]
            for i in range(MAX_N)
        ]
    if kind == "random-tall":
        return MAX_N, 37, [
            [rng.randint(1, MAX_VALUE) for _ in range(37)]
            for _ in range(MAX_N)
        ]
    if kind == "random-wide":
        return 37, MAX_M, [
            [rng.randint(1, MAX_VALUE) for _ in range(MAX_M)]
            for _ in range(37)
        ]
    if kind == "random-small":
        return 5, 7, [
            [rng.randint(1, MAX_VALUE) for _ in range(7)]
            for _ in range(5)
        ]
    if kind == "random-medium":
        return 50, 73, [
            [rng.randint(1, MAX_VALUE) for _ in range(73)]
            for _ in range(50)
        ]
    if kind == "boundary":
        return MAX_N, MAX_M, [
            [1 if (i + j) % 2 == 0 else MAX_VALUE for j in range(MAX_M)]
            for i in range(MAX_N)
        ]

    raise ValueError(f"unknown test type: {kind}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=(
        "min", "min-max", "row", "col", "max", "max-values", "equal",
        "increasing", "decreasing", "symmetric", "random-tall",
        "random-wide", "random-small", "random-medium", "boundary",
    ))
    parser.add_argument("seed", type=int)
    args = parser.parse_args()

    n, m, a = build(args.type, args.seed)
    print(n, m)
    for row in a:
        print(*row)


if __name__ == "__main__":
    main()
