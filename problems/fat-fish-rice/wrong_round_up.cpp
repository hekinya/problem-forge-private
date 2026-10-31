#include <bits/stdc++.h>
// Wrong: 以为余额要花光，向上取整。
int main() {
    long long a, b;
    if (!(std::cin >> a >> b)) return 0;
    long long total = a * 10 + b;
    std::cout << (total + 18) / 19 << '\n';
    return 0;
}
