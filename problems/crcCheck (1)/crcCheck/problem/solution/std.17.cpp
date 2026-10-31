#include <cstdio>
#include <cstring>

constexpr int MAX_LEN = 5000;

static char m[MAX_LEN + 2], g[MAX_LEN + 2], x[MAX_LEN * 2 + 2], q[MAX_LEN + 2];

auto main() -> int {
  int t;
  std::scanf("%d", &t);
  while (t--) {
    std::scanf("%s%s", m, g);
    int n = std::strlen(m), l = std::strlen(g), r = l - 1;
    std::memcpy(x, m, n);
    std::memset(x + n, '0', r);
    x[n + r] = '\0';
    for (int i = 0; i < n; ++i) {
      q[i] = x[i];
      if (x[i] == '1') {
        for (int j = 0; j < l; ++j) x[i + j] ^= g[j] & 1;
      }
    }
    q[n] = '\0';
    int s = 0;
    while (s + 1 < n && q[s] == '0') ++s;
    std::printf("%s %s\n", q + s, x + n);
  }
  return 0;
}
