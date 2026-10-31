#!/usr/bin/env python3
"""素世的笔记本 —— 数据生成器

用法:
    python generator.py --mode random --n 1000 --m 1000 --seed 1 --out 02.in

注意：本题强制在线，操作中的 l、r、k 都是"编码前"的值。解码后
下标一定落在 [1, n]，k 一定落在 [1, len]，所以生成器只需要保证
1 <= l, r, k, p <= n 即可，不需要知道 lst 的取值。
"""

import argparse
import random

MAXV = 10**9

# 每个模式的操作配比 (操作1, 操作2, 操作3)
MIX = {
    "random": (0.45, 0.25, 0.30),
    "all-same": (0.40, 0.20, 0.40),
    "dup": (0.45, 0.25, 0.30),
    "extremes": (0.45, 0.25, 0.30),
    "sorted-inc": (0.50, 0.20, 0.30),
    "sorted-dec": (0.50, 0.20, 0.30),
    "modify-heavy": (0.25, 0.55, 0.20),
    "range-small": (0.50, 0.20, 0.30),
    "query-heavy": (0.90, 0.05, 0.05),
}


def make_values(mode, n, rnd):
    if mode == "all-same":
        v = rnd.choice([0, 1, 12345, MAXV])
        return [v] * n, (lambda: v)
    if mode == "dup":
        pool = [0, 1, 2, 7, MAXV // 2, MAXV - 1, MAXV]
        return [rnd.choice(pool) for _ in range(n)], (lambda: rnd.choice(pool))
    if mode == "extremes":
        return [rnd.choice([0, MAXV]) for _ in range(n)], (lambda: rnd.choice([0, MAXV]))
    if mode == "sorted-inc":
        return sorted(rnd.randint(0, MAXV) for _ in range(n)), (lambda: rnd.randint(0, MAXV))
    if mode == "sorted-dec":
        return sorted((rnd.randint(0, MAXV) for _ in range(n)), reverse=True), (lambda: rnd.randint(0, MAXV))
    if mode == "range-small":
        return [rnd.randint(0, 10**6) for _ in range(n)], (lambda: rnd.randint(0, 10**6))
    return [rnd.randint(0, MAXV) for _ in range(n)], (lambda: rnd.randint(0, MAXV))


def gen(mode, n, m, seed):
    rnd = random.Random(seed)
    if mode not in MIX:
        raise SystemExit(f"未知模式: {mode}")
    base, pick = make_values(mode, n, rnd)
    p1, p2, _p3 = MIX[mode]

    lines = [f"{n} {m}", " ".join(map(str, base))]
    for _ in range(m):
        r = rnd.random()
        if r < p2:
            lines.append(f"2 {rnd.randint(1, n)} {pick()}")
            continue
        if mode == "range-small":
            l = rnd.randint(1, n)
            r2 = min(n, l + rnd.randint(0, 3))
        else:
            l = rnd.randint(1, n)
            r2 = rnd.randint(1, n)
        if r < p2 + p1:
            lines.append(f"1 {l} {r2} {rnd.randint(1, n)}")
        else:
            lines.append(f"3 {l} {r2} {pick()}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="random", choices=sorted(MIX))
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = gen(args.mode, args.n, args.m, args.seed)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)


if __name__ == "__main__":
    main()
