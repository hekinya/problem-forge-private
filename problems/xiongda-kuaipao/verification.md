# 验题记录

## 结构检查

- 题目目录 `problems/xiongda-kuaipao/`，pid 为 `ZXS2026E`。
- 题面页头为“2026 HHACM 招新赛”，标题显示“Problem E. 熊大快跑”；四项运行信息完整。

## 数据与约束

- 测试文件：样例 2 组，独立测试 20 组，共 22 组 `.in` / `.out` 成对。
- 所有输入均通过范围校验：$1\le N\le 1000$，$1\le L\le 10000$，$1\le h_i\le 10000$，元素个数与 $N$ 一致。
- 覆盖边界：$N=1$、全部可摘、全部不可摘、全相等、递增、递减、乱序、部分不可达、$L$ 与 $h_i$ 相等、$L=9999$ 且 $h_i=10000$、随机小/中/大。
- 答案始终满足 $L\le \text{ans}\le L+N$；样例结果与原题一致。

## 正确性对拍

- `solution.cpp`：将高度升序排序后依次贪心摘取，$O(N\log N)$。
- `solution2.cpp`：用最小堆每次取出当前最低果实并提升弹跳高度，实现方式独立。
- 两个正确解在样例与全部 20 组测试上输出完全一致，且与答案文件一致。
- 另用状态压缩枚举所有可达的果实集合，对 300 组随机小数据（$N\le 10$）核对，结果全部一致。

## 错误解定向拒绝

- `wrong_single_pass.cpp`（不排序，只按输入顺序扫描一次）：被测试 `10` 拒绝，正确答案为 $6$。
- `wrong_strict.cpp`（用严格大于代替“不超过”）：被测试 `11` 拒绝，正确答案为 $6$。
- `wrong_initial.cpp`（只统计初始弹跳高度够得到的果实）：被测试 `12` 拒绝，正确答案为 $8$。

## 题面 PDF

- 已生成 `statement.pdf`，并转为 140 dpi 图片逐页目视检查。
- 页头、标题“Problem E. 熊大快跑”、粗体小节、数据范围、带边框的样例输入输出表格均正常，单页显示。
- 输入文件、输出文件、时间限制、内存限制四项均可见：标准输入、标准输出、1 s、256 MB。
- 题面使用“熊大快跑”背景，第一段开头已加入“穷玩车，富玩表，顶富就玩熊大快跑”；保留原题两组样例与数据范围，不含题解或内部验证信息。

## Hydro 导出

- pid 为 `ZXS2026E`，已生成 `hydro/ZXS2026E/` 与 `hydro/ZXS2026E.zip`。
- 导出包共 48 个文件：`problem.yaml`、`problem_zh.md`、`additional_file/statement.pdf`、`testdata/config.yaml` 及 22 对 `.in` / `.ans`。
- 压缩包文件列表与导出目录一致；导出 PDF 与内部 `statement.pdf` 字节一致；`config.yaml` 中 22 组输入/答案一一对应。
- `problem_zh.md` 使用 `@[pdf](file://statement.pdf)`；`config.yaml` 为 `type: default`、`time: 1s`、`memory: 256m`。
- 尚待在目标 Hydro 实例验证导入及内嵌 PDF 的 `file://` 引用。
