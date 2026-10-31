#!/usr/bin/env python3
"""千奈的甜点日历 —— 数据生成器

用法:
    python generator.py --mode random --m 100 --seed 1 --out 01.in
"""

import argparse
import random

MAXN = 10**6


def gen(mode, m, seed):
    rnd = random.Random(seed)

    if mode == "min":
        ns = [1] * m
    elif mode == "small":
        ns = [rnd.randint(1, 10) for _ in range(m)]
    elif mode == "boundary":
        # 特训日（3 的倍数）及其左右两侧
        ns = []
        for _ in range(m):
            k = rnd.randint(1, MAXN // 3)
            d = rnd.choice([-1, 0, 0, 1])
            ns.append(min(MAXN, max(1, 3 * k + d)))
    elif mode == "max":
        ns = [MAXN] * m
    elif mode == "tiny-range":
        ns = [rnd.randint(1, 5000) for _ in range(m)]
    elif mode == "jump":
        # 相邻询问跨度很大，检验预处理与边界
        ns = []
        for _ in range(m):
            ns.append(rnd.choice([1, 2, 3, 4, MAXN, MAXN - 1, MAXN // 2]))
    else:
        ns = [rnd.randint(1, MAXN) for _ in range(m)]

    lines = [str(m)] + [str(v) for v in ns]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="random",
                    choices=["random", "min", "small", "boundary", "max", "tiny-range", "jump"])
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = gen(args.mode, args.m, args.seed)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)


if __name__ == "__main__":
    main()
