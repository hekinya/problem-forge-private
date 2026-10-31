#include <iostream>
#include <string>

using ull = unsigned long long;

auto to_binary(ull v, int width) -> std::string {
  std::string s;
  for (; v != 0; v >>= 1) s.insert(s.begin(), static_cast<char>('0' + (v & 1)));
  if (static_cast<int>(s.size()) < width) s.insert(0, width - s.size(), '0');
  return s;
}

auto main() -> int {
  int t;
  std::cin >> t;
  while (t--) {
    std::string m, g;
    std::cin >> m >> g;
    int l = g.size(), r = l - 1;
    ull y = 0, top = r < 64 ? 1ULL << r : 0, cur = 0, q = 0;
    for (char c : g) y = y << 1 | (c - '0');
    std::string x = m + std::string(r, '0');
    for (char c : x) {
      cur = cur << 1 | (c - '0');
      q <<= 1;
      if ((cur & top) != 0) {
        q |= 1;
        cur ^= y;
      }
    }
    std::cout << to_binary(q, 1) << ' ' << to_binary(cur, r) << '\n';
  }
  return 0;
}
