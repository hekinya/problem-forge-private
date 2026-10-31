#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

// Tries every quotient Q in increasing order. The answer is the Q whose
// carry-less product with G matches X on every position above the last r bits.
auto main() -> int {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);
  int t;
  std::cin >> t;
  while (t--) {
    std::string m, g;
    std::cin >> m >> g;
    int n = m.size(), l = g.size(), r = l - 1;
    std::string x = m + std::string(r, '0');
    std::string q(n, '0');
    std::string rem;
    while (true) {
      std::vector<char> product(n + r, 0);
      for (int i = 0; i < n; ++i) {
        if (q[i] == '0') continue;
        for (int j = 0; j < l; ++j) product[i + j] ^= g[j] - '0';
      }
      bool ok = true;
      for (int i = 0; i < n; ++i) {
        if (product[i] != x[i] - '0') ok = false;
      }
      if (ok) {
        rem.assign(r, '0');
        for (int i = 0; i < r; ++i) {
          rem[i] = static_cast<char>('0' + (product[n + i] ^ (x[n + i] - '0')));
        }
        break;
      }
      int i = n - 1;
      while (q[i] == '1') q[i--] = '0';
      q[i] = '1';
    }
    int s = 0;
    while (s + 1 < n && q[s] == '0') ++s;
    std::cout << q.substr(s) << ' ' << rem << '\n';
  }
  return 0;
}
