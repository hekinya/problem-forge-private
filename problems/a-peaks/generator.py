"""Reproducible internal test generator: python generator.py TYPE SEED."""
import argparse
import random

p = argparse.ArgumentParser()
p.add_argument("type", choices=("min", "max", "random-small", "random-large", "equal"))
p.add_argument("seed", type=int)
args = p.parse_args()
rng = random.Random(args.seed)
if args.type == "min":
    a = [rng.randint(-10**9, 10**9)]
elif args.type == "max":
    a = [10**9 if i % 2 else -10**9 for i in range(200000)]
elif args.type == "equal":
    a = [0] * 100
else:
    n = rng.randint(3, 100) if args.type == "random-small" else 200000
    a = [rng.randint(-10**9, 10**9) for _ in range(n)]
print(len(a))
print(*a)
