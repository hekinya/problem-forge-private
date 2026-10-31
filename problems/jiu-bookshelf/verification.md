# 验题记录

## 结构检查

- `forge.py check --root problems`：通过，4 个题目目录均无结构错误。
- 题目目录 `problems/jiu-bookshelf/`，pid 为 `ZXS2026D`；题面标题显示“D. 鸠的书架”。

## 数据与约束

- 测试文件：样例 2 组，独立测试 18 组，共 20 组 `.in` / `.out` 成对。
- 所有输入均通过范围校验：$1\le K\le N\le 2\times10^5$，$1\le a_i\le 10^9$，元素个数与 $N$ 一致。
- 覆盖边界：$N=1$、$K=1$、$K=N$、全相等、递增、先增后减、随机小/中/大、总和超过 $2^{31}$、总和达到 $2\times10^{14}$。
- 对每组数据核对答案下界 $\max a_i$ 与上界 $\sum a_i$；$K=1$ 时答案等于总和，$K=N$ 时答案等于最大单本价值。

## 正确性对拍

- `solution.cpp`：二分答案 + 从左向右贪心，$O(N\log\sum a_i)$。
- `solution2.cpp`：二分答案 + 从右向左贪心，实现方向独立。
- 两个正确解在样例与全部 18 组测试上输出完全一致，且与答案文件一致。
- 另以 Python 暴力枚举所有划分，对 300 组随机小数据（$N\le 8$，$a_i\le 9$）核对，结果全部一致。
- 由于 $a_i>0$，“不超过 $K$ 段”和“恰好 $K$ 段”等价：若贪心得到少于 $K$ 段，总可以继续拆分区间直到恰好 $K$ 段，且最大值不会增大。

## 错误解定向拒绝

- `wrong_avg.cpp`（只取 $\max(\max a_i,\lceil\sum a_i/K\rceil)$）：被测试 `05` 拒绝，正确答案 $6$，该解输出 $5$。
- `wrong_exact.cpp`（判定时要求贪心段数恰好为 $K$）：被测试 `06` 拒绝，正确答案 $2$。
- `wrong_int32.cpp`（用 32 位整数累计总和）：被测试 `07` 拒绝，正确答案 $3000000000$。

## 性能

- 时限 1000 ms，内存 256 MB。
- C++ 标程在本机对 5 组 $N=2\times10^5$ 的数据实测约 0.015–0.016 s，远低于时限；未通过异常短时限卡正确解。

## 题面 PDF

- 已生成 `statement.pdf`，并转为 140 dpi 图片逐页目视检查。
- 页头、标题、粗体小节、数据范围、带边框的样例输入输出表格均正常。
- 输入文件、输出文件、时间限制、内存限制四项均可见：标准输入、标准输出、1 s、256 MB。
- 题面标题前显示“D.”；不含题解或内部验证信息；两组样例与答案文件一致。

## Hydro 导出

- pid 已确认为 `ZXS2026D`，已生成 `hydro/ZXS2026D/` 与 `hydro/ZXS2026D.zip`。
- 导出包共 44 个文件：`problem.yaml`、`problem_zh.md`、`additional_file/statement.pdf`、`testdata/config.yaml` 及 20 对 `.in` / `.ans`。
- 压缩包文件列表与导出目录一致；导出 PDF 与内部 `statement.pdf` 字节一致；`config.yaml` 中 20 组输入/答案一一对应。
- `problem_zh.md` 使用 `@[pdf](file://statement.pdf)`；`config.yaml` 为 `type: default`、`time: 1s`、`memory: 256m`。
- 尚待在目标 Hydro 实例验证导入及内嵌 PDF 的 `file://` 引用。
