# 验题记录

- `forge.py check`：A、B、C 三个题目目录通过结构检查。
- 数据与答案：`data/samples/01.*` 与 `data/tests/01.*` 的输入均为空（0 字节），答案严格为 `Hello World\n`，与题面「本题没有输入」一致。
- 双解交叉验证：C++ `solution.cpp` 与独立 Python `solution2.py` 在空输入下输出（归一化换行后）一致，均为 `Hello World\n`。
- 错误解验题：`wrong_hello_world.cpp` 输出 `Hello, World!`，被判定为与答案不一致。
- 题面 PDF：`statement.pdf` 为单页；`render_preview.py` 校验页头、标题、输入文件 / 输出文件 / 时间限制 / 内存限制四项、输入格式、输出格式与样例文本均可见。`statement-preview.png` 已目视检查：中文与英文正常、样例输入输出表格边框与对齐正常、无题解内容。
- Hydro 导出包：`C-ZXS2026C`，`problem.yaml` 的 pid 为比赛确认的 `ZXS2026C`；`testdata` 含 `sample01.*` 与 `case01.*` 各一对，`.in` / `.ans` 一一对应；`config.yaml` 为 `type: default`、`time: 1s`、`memory: 256m`；`additional_file/statement.pdf` 与内部原件字节一致；`problem_zh.md` 使用 `@[pdf](file://statement.pdf)`；压缩包内容与导出目录一致。
- 无输入题目的数据特殊性：本题只有一个可能的输入（空），因此样例与测试内容相同，保留 sample / case 两套文件仅为沿用 A、B 的目录约定；不存在可构造的 min / max 或边界数据，验题改为逐字节核对答案与题面输出完全一致。
- 尚待在目标 Hydro 实例验证导入与 PDF 嵌入；当前不能声称压缩包已在该实例直接导入成功。
