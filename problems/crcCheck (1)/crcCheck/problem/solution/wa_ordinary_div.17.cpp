#include <algorithm>
#include <iostream>
#include <string>

// Uses ordinary binary long division with borrows instead of xor.
auto main() -> int {
  int t;
  std::cin >> t;
  while (t--) {
    std::string m, g;
    std::cin >> m >> g;
    int l = g.size(), r = l - 1;
    std::string x = m + std::string(r, '0'), q;
    std::string d = "0" + g;
    std::string cur(l + 1, '0');
    for (char c : x) {
      std::rotate(cur.begin(), cur.begin() + 1, cur.end());
      cur.back() = c;
      if (cur >= d) {
        int borrow = 0;
        for (int i = l; i >= 0; --i) {
          int v = (cur[i] - '0') - (d[i] - '0') - borrow;
          borrow = v < 0;
          cur[i] = static_cast<char>('0' + (v + 2) % 2);
        }
        q += '1';
      } else {
        q += '0';
      }
    }
    auto s = q.find('1');
    std::cout << (s == std::string::npos ? "0" : q.substr(s)) << ' '
              << cur.substr(l + 1 - r) << '\n';
  }
  return 0;
}
