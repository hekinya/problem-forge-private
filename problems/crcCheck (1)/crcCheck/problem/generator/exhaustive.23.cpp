#include <print>
#include <string>

#include "cplib.hpp"

CPLIB_REGISTER_GENERATOR(gen, args,  //
                         max_m = Var<cplib::var::i32>("max-m", 1, 4),
                         max_g = Var<cplib::var::i32>("max-g", 2, 5));

auto to_bits(int value, int len) -> std::string {
  std::string s(len, '0');
  for (int i = 0; i < len; ++i) {
    if ((value >> (len - 1 - i) & 1) != 0) s[i] = '1';
  }
  return s;
}

void generator_main() {
  int t = ((1 << (args::max_m + 1)) - 2) * ((1 << args::max_g) - 2);
  std::println("{}", t);
  for (int lm = 1; lm <= args::max_m; ++lm) {
    for (int m = 0; m < (1 << lm); ++m) {
      for (int lg = 2; lg <= args::max_g; ++lg) {
        for (int g = 1 << (lg - 1); g < (1 << lg); ++g) {
          std::println("{} {}", to_bits(m, lm), to_bits(g, lg));
        }
      }
    }
  }
  gen.quit_ok();
}
