#include <cstdio>

int main() {
    int n;
    if (std::scanf("%d", &n) != 1) return 0;
    long long left, middle, right;
    std::scanf("%lld", &left);
    if (n == 1) { std::puts("0"); return 0; }
    std::scanf("%lld", &middle);
    int count = 0;
    for (int i = 2; i < n; ++i) {
        std::scanf("%lld", &right);
        if (middle > left && middle > right) ++count;
        left = middle;
        middle = right;
    }
    std::printf("%d\n", count);
}
