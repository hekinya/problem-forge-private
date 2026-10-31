# 验题记录

## 结构检查

- 题目目录 `problems/matrix-transpose/`，pid/代号为 `ZXS2026`。
- 采用新版 XCPC Typst 流程：`statement.md` 为唯一正文源，`problem.json` 提供时限内存，样例来自 `data/samples/`。
- PDF 页眉为“2026 HHACM 招新赛”，标题为“矩阵转置”，不添加题号。

## 数据与约束

- 测试文件：样例 1 组，独立测试 15 组，共 16 组 `.in` / `.out` 成对。
- 所有输入均通过范围校验：$1\le n,m\le 100$，元素个数为 $nm$，$1\le A_{i,j}\le 1000$。
- 覆盖边界：$1\times1$、$1\times100$、$100\times1$、$100\times100$、最大元素、全相等、递增、递减、对称矩阵、随机非方阵、交替边界值。

## 正确性对拍

- `solution.cpp`：按列优先遍历原矩阵并输出，$O(nm)$。
- `solution2.cpp`：读入时直接写入转置数组，再按行输出；实现方式独立。
- 两个正确解在样例与全部 15 组测试上输出一致，且与答案文件一致。
- 另用 Python 独立转置对 200 组随机矩阵核对，结果全部一致。

## 错误解定向拒绝

- `wrong_original.cpp`（直接输出原矩阵）：被测试 `11` 拒绝。
- `wrong_reverse_rows.cpp`（转置后把每行倒序输出）：被测试 `11` 拒绝。

## 题面 PDF

- 使用 Typst 0.15.1 与固定 XCPC 模板生成 `statement.pdf`，并转为 140 dpi 图片检查。
- 页眉、标题、四项运行信息（标准输入、标准输出、1 s、128 MB）、公式和带边框的样例表均正常，单页显示。
- 题面按原题顺序为：题目描述 → 输入格式 → 输出格式 → 样例；约束写在输入格式中。样例表头使用模板默认的 `standard input` / `standard output`。

## Hydro 导出

- 已生成 `hydro/ZXS2026/` 与 `hydro/ZXS2026.zip`。
- 导出包包含 `problem.yaml`、`problem_zh.md`、`additional_file/statement.pdf`、`testdata/config.yaml` 及 16 对 `.in` / `.ans`。
- 已核对压缩包与导出目录一致、PDF 字节一致，16 组输入/答案一一对应。
- 尚待在目标 Hydro 实例复测导入与内嵌 PDF 引用；仅保存在本地，未提交或推送。
