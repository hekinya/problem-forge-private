# Yes-Yes?

你问了 Chumeng 一堆问题，Chumeng 不喜欢浪费生命的问题，所以他只回答了一堆 Yes。但是因为电话信号不好，你只听到了回答的一个子串。也就是说，如果他回答了 YesYes，你可能只听到了 esYe，但你不会听到 esYs，因为它不是回答的子串。

判断给定的一个字符串 `s` 是否是 `YesYesYes...` 的子串（`...` 表示 Yes 重复了很多次）。

## 输入格式

第一行包括一个正整数 `t`（`1 ≤ t ≤ 50`）——测试用例的数量。接下来有 `t` 个测试用例。每个测试用例包括一个字符串 `s`（`1 ≤ |s| ≤ 50`）。

## 输出格式

对于每个测试用例，如果对应的字符串是 `YesYesYes...` 的子串，则打印 `YES`，否则打印 `NO`。

你可以以任意大小写形式打印每个字母。例如，字符串 `yEs`、`yes`、`Yes` 和 `YES` 都将被视为肯定回答。

## 样例

输入：

```text
12
YES
esYes
no
es
se
YesY
esYesYesYesYesYesYe
seY
Yess
sY
o
Yes
```

输出：

```text
NO
YES
NO
YES
NO
YES
YES
NO
NO
YES
NO
YES
```
