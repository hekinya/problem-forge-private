#!/usr/bin/env python3
"""素世的笔记本 —— 生成并校验 data/tests。

流程：生成 -> validate.py 校验格式 -> solution.exe 出答案 -> 小规模再用
brute.exe 交叉验证。所有 .out 统一为 LF 换行。
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "data", "tests")
BUILD = os.path.join(HERE, ".build")

# (文件名, 模式, n, m, seed, 是否用暴力交叉验证)
SPECS = [
    ("01", "random",       1,      1,      101, True),   # 最小规模
    ("02", "random",       10,     10,     102, True),
    ("03", "range-small",  200,    200,    103, True),   # 极短区间
    ("04", "all-same",     1000,   1000,   104, True),   # 全部相同
    ("05", "dup",          2000,   2000,   105, True),   # 极少量不同值
    ("06", "sorted-inc",   5000,   5000,   106, False),
    ("07", "sorted-dec",   5000,   5000,   107, False),
    ("08", "extremes",     10000,  10000,  108, False),  # 只有 0 和 1e9
    ("09", "modify-heavy", 20000,  20000,  109, False),
    ("10", "random",       50000,  50000,  110, False),
    ("11", "query-heavy",  100000, 100000, 111, False),  # 时限压力
    ("12", "modify-heavy", 80000,  80000,  112, False),  # 内存/修改压力
    ("13", "extremes",     100000, 100000, 113, False),
    ("14", "random",       100000, 100000, 114, False),
]


def run(exe, inp, outp=None):
    with open(inp, "rb") as fi:
        if outp:
            with open(outp, "wb") as fo:
                r = subprocess.run([exe], stdin=fi, stdout=fo, stderr=subprocess.PIPE)
        else:
            r = subprocess.run([exe], stdin=fi, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r


def main():
    os.makedirs(TESTS, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    sol = os.path.join(HERE, "solution.exe")
    brute = os.path.join(HERE, "brute.exe")
    validator = os.path.join(HERE, "validate.py")
    gen = os.path.join(HERE, "generator.py")

    failures = 0
    for name, mode, n, m, seed, check in SPECS:
        inp = os.path.join(TESTS, f"{name}.in")
        out = os.path.join(TESTS, f"{name}.out")
        subprocess.run([sys.executable, gen, "--mode", mode, "--n", str(n),
                        "--m", str(m), "--seed", str(seed), "--out", inp], check=True)

        with open(inp, "rb") as fi:
            v = subprocess.run([sys.executable, validator], stdin=fi,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if v.returncode != 0:
            print(f"{name}: 校验失败 {v.stderr.decode('utf-8', 'replace')[:200]}")
            failures += 1
            continue

        run(sol, inp, out)
        with open(out, "rb") as f:
            data = f.read().replace(b"\r\n", b"\n")
        with open(out, "wb") as f:
            f.write(data)

        status = "ok"
        if check:
            bpath = os.path.join(BUILD, f"brute-{name}.txt")
            run(brute, inp, bpath)
            with open(bpath, "rb") as f:
                bdata = f.read().replace(b"\r\n", b"\n")
            if bdata != data:
                status = "与暴力不一致!"
                failures += 1
        print(f"{name}: n={n} m={m} mode={mode} -> {status}")
    print(f"失败 {failures} 个" if failures else "全部测试生成并校验通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
