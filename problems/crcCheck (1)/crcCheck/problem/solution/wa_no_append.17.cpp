#include <iostream>
#include <string>

// Divides M itself and forgets to append r zeros.
auto main() -> int {
  int t;
  std::cin >> t;
  while (t--) {
    std::string x, g;
    std::cin >> x >> g;
    int n = x.size(), l = g.size(), r = l - 1;
    std::string q;
    for (int i = 0; i + r < n; ++i) {
      q += x[i];
      if (x[i] == '1') {
        for (int j = 0; j < l; ++j) x[i + j] ^= g[j] & 1;
      }
    }
    std::string rem = n >= r ? x.substr(n - r) : std::string(r - n, '0') + x;
    auto s = q.find('1');
    std::cout << (s == std::string::npos ? "0" : q.substr(s)) << ' ' << rem
              << '\n';
  }
  return 0;
}
