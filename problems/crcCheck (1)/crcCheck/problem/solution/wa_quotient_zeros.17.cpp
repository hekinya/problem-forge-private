#include <iostream>
#include <string>

// Prints all |M| quotient bits without removing leading zeros.
auto main() -> int {
  int t;
  std::cin >> t;
  while (t--) {
    std::string m, g;
    std::cin >> m >> g;
    int n = m.size(), l = g.size(), r = l - 1;
    std::string x = m + std::string(r, '0'), q(n, '0');
    for (int i = 0; i < n; ++i) {
      q[i] = x[i];
      if (x[i] == '1') {
        for (int j = 0; j < l; ++j) x[i + j] ^= g[j] & 1;
      }
    }
    std::cout << q << ' ' << x.substr(n) << '\n';
  }
  return 0;
}
