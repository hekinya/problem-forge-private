#include <bits/stdc++.h>
// Wrong: 忘记把散装 token 算进去，只数大礼包。
int main() {
    long long a, b;
    if (!(std::cin >> a >> b)) return 0;
    std::cout << a * 10 / 19 << '\n';
    return 0;
}
