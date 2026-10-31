#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;

    vector<long long> a(n);
    long long total = 0, largest = 0;
    for (int i = 0; i < n; ++i) {
        if (scanf("%lld", &a[i]) != 1) return 0;
        total += a[i];
        if (a[i] > largest) largest = a[i];
    }

    long long low = largest, high = total;
    while (low < high) {
        long long limit = low + (high - low) / 2;
        int groups = 1;
        long long current = 0;
        for (int i = n - 1; i >= 0; --i) {
            if (current + a[i] > limit) {
                ++groups;
                current = a[i];
            } else {
                current += a[i];
            }
        }
        if (groups <= k) {
            high = limit;
        } else {
            low = limit + 1;
        }
    }

    printf("%lld\n", low);
    return 0;
}
