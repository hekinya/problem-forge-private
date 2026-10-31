// 千奈的甜点日历 —— 暴力（递归 + 记忆化，用于小数据对拍）
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 1000000007;
static const int LIM = 5005;

long long memo[LIM];
bool vis[LIM];

long long calc(int n) {
    if (n <= 2) return 1;
    if (vis[n]) return memo[n];
    long long s = calc(n - 1) + calc(n - 2);
    if (n % 3 == 0) s *= 2;
    vis[n] = true;
    return memo[n] = s % MOD;
}

int main() {
    int m;
    if (scanf("%d", &m) != 1) return 0;
    while (m--) {
        int n;
        if (scanf("%d", &n) != 1) return 0;
        printf("%lld\n", calc(n));
    }
    return 0;
}
