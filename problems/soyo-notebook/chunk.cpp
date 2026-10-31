// 素世的笔记本 —— 分块做法（独立实现，用于中等规模对拍）
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 50005;
int n, m;
int a[MAXN];
vector<int> vals;

int B, nb;
int bl[MAXN];
vector<int> blk[256];

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 1; i <= n; ++i) {
        scanf("%d", &a[i]);
        vals.push_back(a[i]);
    }
    struct Op { int t; long long x, y, z; };
    vector<Op> ops(m);
    for (int i = 0; i < m; ++i) {
        if (scanf("%d %lld %lld", &ops[i].t, &ops[i].x, &ops[i].y) != 3) return 0;
        if (ops[i].t != 2) {
            if (scanf("%lld", &ops[i].z) != 1) return 0;
        } else {
            vals.push_back((int)ops[i].y);
        }
    }
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());

    B = max(1, (int)sqrt((double)n) + 1);
    nb = (n + B - 1) / B;
    for (int i = 1; i <= n; ++i) {
        bl[i] = (i - 1) / B;
        blk[bl[i]].push_back(a[i]);
    }
    for (int b = 0; b < nb; ++b) sort(blk[b].begin(), blk[b].end());

    auto rebuild = [&](int b) {
        blk[b].clear();
        for (int i = b * B + 1; i <= min(n, (b + 1) * B); ++i) blk[b].push_back(a[i]);
        sort(blk[b].begin(), blk[b].end());
    };

    auto countLE = [&](int l, int r, int x) {
        int res = 0;
        if (bl[l] == bl[r]) {
            for (int i = l; i <= r; ++i) res += (a[i] <= x);
            return res;
        }
        for (int i = l; i <= min(n, (bl[l] + 1) * B); ++i) res += (a[i] <= x);
        for (int i = bl[r] * B + 1; i <= r; ++i) res += (a[i] <= x);
        for (int b = bl[l] + 1; b <= bl[r] - 1; ++b)
            res += (int)(upper_bound(blk[b].begin(), blk[b].end(), x) - blk[b].begin());
        return res;
    };

    long long lst = 0;
    for (int i = 0; i < m; ++i) {
        int t = ops[i].t;
        if (t == 2) {
            int p = (int)((ops[i].x + lst - 1) % n) + 1;
            a[p] = (int)ops[i].y;
            rebuild(bl[p]);
        } else {
            int l = (int)((ops[i].x + lst - 1) % n) + 1;
            int r = (int)((ops[i].y + lst - 1) % n) + 1;
            if (l > r) swap(l, r);
            int len = r - l + 1;
            if (t == 3) {
                int ans = countLE(l, r, (int)ops[i].z);
                printf("%d\n", ans);
                lst = ans;
            } else {
                int k = (int)((ops[i].z + lst - 1) % len) + 1;
                int lo = 0, hi = (int)vals.size() - 1;
                while (lo < hi) {
                    int mid = (lo + hi) >> 1;
                    if (countLE(l, r, vals[mid]) >= k) hi = mid;
                    else lo = mid + 1;
                }
                printf("%d\n", vals[lo]);
                lst = vals[lo];
            }
        }
    }
    return 0;
}
