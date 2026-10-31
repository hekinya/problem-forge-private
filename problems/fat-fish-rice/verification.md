# 验题记录

- `forge.py check`：私有仓库 5 个题目目录（含新建的 `fat-fish-rice`）通过结构检查。
- 数据与答案：`data/samples` 1 对、`data/tests` 12 对，`.in` / `.out` 一一对应；全部输入通过范围校验（`0 ≤ a ≤ 10^4`、`0 ≤ b ≤ 9`），答案文件与独立计算 `⌊(10a+b)/19⌋` 逐例一致。定向用例覆盖 `a=b=0`、`a=0,b=9`、`(10a+b)` 恰为 19 的倍数（04、07、09）、差 1 不够一碗（05）、以及两个变量的上界（03、10）。
- 双解交叉验证：`solution.cpp`（C++20）与独立实现 `solution2.py` 在全部 13 个用例及 500 组随机数据上输出一致。
- 错误解验题：`wrong_ignore_b.cpp`（只数大礼包、漏掉散装 token）被 3 个用例拒绝；`wrong_round_up.cpp`（认为必须花光余额、向上取整）被 9 个用例拒绝，包括样例 `01.in`。
- 数据生成器：`generator.py` 六种类型（min / max / random / small / edge / multiple）各 4 个种子，生成的输入全部合法且与双解一致。
- 题面：`statement.pdf` 为单页；`render_preview.py` 校验页眉、`Problem` 编号、输入文件 / 输出文件 / 时间限制 / 内存限制四项、各小节标题与样例文本均可见。已目视检查：中文与英文正常、无英文单词跨行截断、无行首标点、样例表格边框与对齐正常、PDF 内不含题解。
- 排版脚本 `build_statement.py` 未沿用 reportlab `Paragraph`，改用自带 CJK 断行（禁则 + 拉丁词不拆行），因此晚些修改正文后仍需重新目视检查。
- 页眉与题序：按确认结果渲染为「2026 HHACM 招新赛」与 `Problem G`，命令为 `py -3 build_statement.py --contest "2026 HHACM 招新赛" --index 7`；`render_preview.py` 用相同参数校验页眉与题号。
- Hydro 导出包：按你的要求暂用题名作 pid（`G-大肥鱼买白饭.zip`），`problem.yaml` 的 `pid: 大肥鱼买白饭`、`problem_zh.md` 为 `@[pdf](file://statement.pdf)`、`additional_file/statement.pdf` 与内部原件字节一致；`testdata` 含 `sample01` 与 `case01–12`，`.in` / `.ans` 共 13 对一一对应，`config.yaml` 为 `type: default`、`time: 1s`、`memory: 125m`（读取自 `problem.json`）；压缩包 30 个条目与导出目录一致。
- pid 为占位：题名不是合法的 Hydro 题号格式，正式导入前需要换成比赛分配的题号后重跑 `py -3 pack_hydro.py <pid>`；本仓库 `statement.md` 沿用 A/B/C 题的 `##` 小节写法，若改用 `tools/build_xcpc.py`，需要先转成带 `{#input}` 等语义锚点和 `::: {.samples}` 容器的形式。
- 尚待在目标 Hydro 实例验证导入与 PDF 嵌入；当前不能声称压缩包已在该实例直接导入成功。
