// 素世的笔记本 —— 暴力（用于对拍，复杂度 O(n) 每次询问）
#include <bits/stdc++.h>
using namespace std;

int n, m;
int a[50005];
int tmp[50005];

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 1; i <= n; ++i) scanf("%d", &a[i]);
    long long lst = 0;
    for (int i = 0; i < m; ++i) {
        int t;
        scanf("%d", &t);
        long long x, y, z;
        scanf("%lld %lld", &x, &y);
        if (t == 2) {
            int p = (int)((x + lst - 1) % n) + 1;
            a[p] = (int)y;
        } else {
            scanf("%lld", &z);
            int l = (int)((x + lst - 1) % n) + 1;
            int r = (int)((y + lst - 1) % n) + 1;
            if (l > r) swap(l, r);
            int len = r - l + 1;
            if (t == 3) {
                int cnt = 0;
                for (int j = l; j <= r; ++j)
                    if (a[j] <= (int)z) ++cnt;
                printf("%d\n", cnt);
                lst = cnt;
            } else {
                int k = (int)((z + lst - 1) % len) + 1;
                for (int j = 0; j < len; ++j) tmp[j] = a[l + j];
                nth_element(tmp, tmp + k - 1, tmp + len);
                int ans = tmp[k - 1];
                printf("%d\n", ans);
                lst = ans;
            }
        }
    }
    return 0;
}
