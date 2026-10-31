#import "/figures.typ": flow, ladder, lead, xor-figure
#import "@preview/mannot:0.4.0": annot, markul

== #text(size: 15pt)[题目背景]

数据在传输过程中可能受到干扰，导致某些位出错．循环冗余校验（Cyclic Redundancy Check，CRC）是一种常用的检错方法，以太网和 ZIP 压缩文件都使用它．

发送方在信息后面接一段校验码，再一起发出．接收方对收到的内容再做一次除法：余数全为 `0` 时未发现错误，否则说明传输出错：

#flow("101001", "1101", 3)

== #text(size: 15pt)[题目描述]

现在由你担任发送方．给定两个 01 串：信息串 $M$ 和生成串 $G$．请在 $M$ 末尾添加 $r$ 个 `0` 得到 $X$，再用模 2 除法计算 $X$ 除以 $G$ 的商 $Q$ 和余数 $R$．余数 $R$ 就是校验码，它的位数 $r$ 为：

$
  r = markul(|G| - 1, #<len>) #annot(<len>, pos: right, dx: 1em, annot-text-props: (size: 0.85em, font: "FZShuSong-Z01"))[生成串的长度减 1]
$

#lead[01 串]只含 `0` 和 `1` 的字符串称为 01 串，$|S|$ 表示字符串 $S$ 的长度．

#lead[异或]两位相同得 `0`，不同得 `1`．两个等长的 01 串异或，就是逐位异或．

#xor-figure

#lead[模 2 除法]步骤如下：

1. 从左到右依次看 $X$ 的前 $|M|$ 位．如果当前位是 `1`，商写 `1`，并把 $G$ 的第一位对齐当前位，用 $G$ 与 $X$ 中对齐的 $|G|$ 位逐位异或，结果写回 $X$．如果当前位是 `0`，商写 `0`，$X$ 不变．
2. 写下的 $|M|$ 个商位连起来是商 $Q$．此时 $X$ 的最后 $r$ 位是余数 $R$．

#block(breakable: false, width: 100%)[
  #lead[例子]当 $M =$ `101001`，$G =$ `1101` 时，$r = 3$，除法竖式如下：

  #ladder("101001", "1101")
]

#pagebreak(weak: true)
