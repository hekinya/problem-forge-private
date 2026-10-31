---
title: "矩阵转置"
language: chinese
input-file: 标准输入
output-file: 标准输出
show-metadata: true
contest:
  name: 2026 HHACM 招新赛
---

输入一个 $n$ 行 $m$ 列的矩阵 $A$，输出它的转置 $A^T$。

$A^T$ 可以通过将 $A$ 的行与列互换得到，即

$$
A^T_{i,j}=A_{j,i}
$$

# 输入格式 {#input}

第一行包含两个整数 $n$ 和 $m$，表示矩阵 $A$ 的行数和列数。$1 \le n \le 100$，$1 \le m \le 100$。

接下来 $n$ 行，每行 $m$ 个整数，表示矩阵 $A$ 的元素。相邻两个整数之间用单个空格隔开，每个元素均在 $1 \sim 1000$ 之间。

# 输出格式 {#output}

输出 $m$ 行，每行 $n$ 个整数，为矩阵 $A$ 的转置。相邻两个整数之间用单个空格隔开。

::: {.samples}
``` {.input}
3 3
1 2 3
4 5 6
7 8 9
```

``` {.output}
1 4 7
2 5 8
3 6 9
```
:::
