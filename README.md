# Problem Forge Private

未发布题目的私有工作区。通用模板和检查工具保存在公开仓库 [problem-forge](https://github.com/hekinya/problem-forge)。不要在公开仓库提交这里的题面、数据或标程。

## 新建与检查

将两个仓库下载在同一个父目录下，然后运行：

```bash
python ../problem-forge/tools/forge.py new example --root problems
python ../problem-forge/tools/forge.py check --root problems
```

每道题位于 `problems/<题目代号>/`。填写 `problem.json`、`statement.md` 和样例；数据生成器、标程及其他验题材料也放在该题目目录。模板和文件约定见公开仓库的 [WORKFLOW.md](https://github.com/hekinya/problem-forge/blob/main/WORKFLOW.md)。
