# 循环冗余校验（crcCheck）

一道面向大一新生的 ICPC 风格题目，以 CRC 校验为背景，考察模 2 除法。使用 [Hull](https://hull.aberter0x3f.top/) 构建。

## 题意

给定 $T$ 组信息串 $M$ 和生成串 $G$。在 $M$ 后补 $|G| - 1$ 个 `0`，做模 2 除法，输出商 $Q$（去掉前导零）和校验码 $R$（恰好 $|G| - 1$ 位）。

- $1 \le T \le 1000$，$|M| \ge 1$，$|G| \ge 2$，$G$ 以 `1` 开头。
- $|M|$ 与 $|G|$ 的总和各不超过 $5000$。
- 标准解法按位模拟，时间复杂度 $O(|M| \cdot |G|)$。

## 目录

| 路径 | 内容 |
| --- | --- |
| `problem.nix` | 题目配置：限制、测试点、解法预测、文档、target |
| `authoring-include/problem.23.hpp` | 输入输出模型和数据范围，validator 与 checker 共用 |
| `validator.23.cpp`、`checker.23.cpp` | validator 和 checker 入口 |
| `generator/rand.23.cpp` | 多模式数据生成器 |
| `generator/exhaustive.23.cpp` | 穷举小数据生成器 |
| `solution/` | 标程、暴力、慢速正解和错解 |
| `document/statement/` | 题面：`main.typ` 接入 olymp-in-typst 模板，`figures.typ` 绘制图示，`zh/` 存放文字 |
| `document/editorial/` | 题解 |
| `data/` | 手写样例输入 |

## 解法

| 文件 | 说明 | 预期结果 |
| --- | --- | --- |
| `std.17.cpp` | 标程 | 通过 |
| `slow_string.17.cpp` | 写法笨重的正解，用于确认时限足够宽松 | 通过 |
| `bf.17.cpp` | 枚举商，用于独立对照 | 通过或超时 |
| `wa_ull.17.cpp` | 用 `unsigned long long` 存储 | 答案错误 |
| `wa_no_append.17.cpp` | 不补零 | 答案错误 |
| `wa_no_pad.17.cpp` | 余数丢失前导零 | 答案错误 |
| `wa_quotient_zeros.17.cpp` | 商保留前导零 | 答案错误 |
| `wa_ordinary_div.17.cpp` | 使用普通带借位除法 | 答案错误 |

## 构建

以下命令都在 `nix develop` 中执行。

```bash
hull build                           # 构建 default target，并运行组件测试和解法预测
hull build -t hydro -o result-hydro  # 构建 Hydro 题包
hull judge solution/std.17.cpp       # 评测单个解法
```

`default` target 的产物在 `result/`，包含数据、各解法的评测结果、`document/statement.zh.pdf` 和 `document/editorial.zh.pdf`。它包含标程和题解，不要发给选手。

## Hydro

`result-hydro` 是指向 zip 文件的符号链接。题包使用 Hydro 原生判题，时限 1000 ms，内存 1024 MB，满分 100。题解和解法不在包内。

导入前请确认：

- 实例已启用 `cc.cc20o2`，checker 和 validator 使用这个语言编译。
- g++ 支持 `<format>`，一般需要 13 或更高版本。

题包尚未在真实的 Hydro 实例上导入测试，目前只在本地按 syzoj checker 协议模拟验证过。

## 题面依赖

题面的图示由 `figures.typ` 按算法实时计算，不是手写的。修改示例时只需改传入的 `M` 和 `G`。

以下依赖都在 `problem.nix` 中固定了版本和哈希，构建时自动下载：

- 模板：[olymp-in-typst](https://github.com/lihaoze123/olymp-in-typst)。
- Typst 包：longops 0.2.1（竖式的下拉箭头，它依赖 CeTZ 0.4.2 和 zero 0.7.0）、mannot 0.4.0（公式标注）、pinit 0.2.2（输入输出字段标注）。longops 的 `division` 只做普通带借位除法，所以竖式由 `figures.typ` 按模 2 除法计算并用 grid 排版，只取它的 `pull-down`。longops 0.2.1 需要 Typst 0.15，所以 `flake.nix` 使用 nixos-unstable。
- 字体：方正书宋、方正黑体等从方正官方 CDN 下载，并嵌入 PDF。公开分发前请确认字体授权范围。

新增文件后，要先让 git 看到它（`git add -N <文件>` 或提交），否则 Nix 构建时找不到。
