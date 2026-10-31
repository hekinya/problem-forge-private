#!/usr/bin/env python3
"""千奈的甜点日历 —— 生成并校验 data/tests。

流程：生成 -> validate.py 校验 -> solution.exe 出答案 -> 与矩阵快速幂
(solution2.py) 交叉验证 -> n 较小时再与递归暴力比对。.out 统一 LF。
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "data", "tests")
BUILD = os.path.join(HERE, ".build")
PY = sys.executable

# (文件, 模式, m, seed, 是否用递归暴力复核)
SPECS = [
    ("01", "min",        1,      101, True),
    ("02", "small",      10,     102, True),
    ("03", "boundary",   50,     103, False),
    ("04", "jump",       1000,   104, False),
    ("05", "tiny-range", 100000, 105, True),   # 暴力可覆盖（记忆化后总工作量 O(maxn)）
    ("06", "random",     1000,   106, False),
    ("07", "random",     100000, 107, False),
    ("08", "max",        100000, 108, False),
    ("09", "boundary",   100000, 109, False),
    ("10", "jump",       100000, 110, False),
]


def run(cmd, inp, outp):
    with open(inp, "rb") as fi, open(outp, "wb") as fo:
        r = subprocess.run(cmd, stdin=fi, stdout=fo, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} 退出码 {r.returncode}: {r.stderr.decode('utf-8', 'replace')[:300]}")
    with open(outp, "rb") as f:
        data = f.read().replace(b"\r\n", b"\n")
    with open(outp, "wb") as f:
        f.write(data)
    return data


def main():
    os.makedirs(TESTS, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    sol = os.path.join(HERE, "solution.exe")
    brute = os.path.join(HERE, "brute.exe")
    mat = os.path.join(HERE, "solution2.py")
    validator = os.path.join(HERE, "validate.py")
    gen = os.path.join(HERE, "generator.py")

    failures = 0
    for name, mode, m, seed, check_brute in SPECS:
        inp = os.path.join(TESTS, f"{name}.in")
        out = os.path.join(TESTS, f"{name}.out")
        subprocess.run([PY, gen, "--mode", mode, "--m", str(m), "--seed", str(seed),
                        "--out", inp], check=True)

        with open(inp, "rb") as fi:
            v = subprocess.run([PY, validator], stdin=fi,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if v.returncode != 0:
            print(f"{name}: 校验失败 {v.stderr.decode('utf-8', 'replace')[:200]}")
            failures += 1
            continue

        data = run([sol], inp, out)

        # 矩阵快速幂独立复核
        mout = os.path.join(BUILD, f"mat-{name}.txt")
        mdata = run([PY, mat], inp, mout)
        status = "ok"
        if mdata != data:
            status = "与矩阵解不一致!"
            failures += 1
        elif check_brute:
            bout = os.path.join(BUILD, f"brute-{name}.txt")
            bdata = run([brute], inp, bout)
            if bdata != data:
                status = "与暴力不一致!"
                failures += 1
            else:
                status = "ok（矩阵解 + 暴力均一致）"
        else:
            status = "ok（矩阵解一致）"
        print(f"{name}: mode={mode} m={m} -> {status}")

    print(f"失败 {failures} 个" if failures else "全部测试生成并校验通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
