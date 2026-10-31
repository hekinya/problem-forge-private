#include <iostream>
#include <string>

// Correct, but rebuilds the remainder string with appends on every step.
auto main() -> int {
  int t;
  std::cin >> t;
  while (t--) {
    std::string m, g;
    std::cin >> m >> g;
    int l = g.size(), r = l - 1;
    std::string x = m + std::string(r, '0');
    std::string cur = x.substr(0, r), q;
    for (std::size_t i = r; i < x.size(); ++i) {
      cur += x[i];
      std::string next;
      if (cur[0] == '1') {
        q += '1';
        for (int j = 1; j < l; ++j) next += cur[j] == g[j] ? '0' : '1';
      } else {
        q += '0';
        next = cur.substr(1);
      }
      cur = next;
    }
    auto s = q.find('1');
    std::cout << (s == std::string::npos ? "0" : q.substr(s)) << ' ' << cur
              << '\n';
  }
  return 0;
}
