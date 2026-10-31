#include <algorithm>
#include <cstddef>
#include <print>
#include <string>
#include <vector>

#include "cplib.hpp"

CPLIB_REGISTER_GENERATOR(gen, args,                               //
                         t = Var<cplib::var::i32>("t", 1, 1000),  //
                         n = Var<cplib::var::i32>("n", 1, 5000),  //
                         g = Var<cplib::var::i32>("g", 2, 5000),  //
                         head_n = Var<cplib::var::i32>("head-n", 1, 5000),
                         head_g = Var<cplib::var::i32>("head-g", 2, 5000),
                         m_kind = Var<cplib::var::String>("m-kind"),
                         density = Var<cplib::var::i32>("density", 0, 100),
                         zeros = Var<cplib::var::i32>("zeros", 0, 5000),
                         rem_bits = Var<cplib::var::i32>("rem-bits", 0, 5000),
                         g_kind = Var<cplib::var::String>("g-kind"),
                         g_density = Var<cplib::var::i32>("g-density", 0, 100),
                         g_odd = Flag("g-odd"),
                         salt = Var<cplib::var::String>("salt"));

auto random_bits(std::size_t len, int percent) -> std::string {
  std::string s(len, '0');
  for (auto &c : s) {
    if (gen.rnd.next(0, 99) < percent) c = '1';
  }
  return s;
}

auto make_g(int len) -> std::string {
  if (args::g_kind == "crc8") return "100000111";
  if (args::g_kind == "crc16") return "11000000000000101";
  if (args::g_kind == "crc32") return "100000100110000010001110110110111";
  if (args::g_kind != "random") cplib::panic("Unknown g-kind");
  auto s = random_bits(len, args::g_density);
  s.front() = '1';
  if (args::g_odd) s.back() = '1';
  return s;
}

// Builds M such that (M followed by r zeros) mod G has exactly rem-bits
// significant bits. X is a multiple of G xor a short remainder, so the
// low r bits of the multiple must equal that remainder.
auto make_tail_m(std::size_t len, const std::string &g) -> std::string {
  auto r = g.size() - 1;
  if (g.back() != '1') cplib::panic("m-kind=tail requires an odd G");
  if (len < r) cplib::panic("m-kind=tail requires |M| >= |G| - 1");
  if (static_cast<std::size_t>(args::rem_bits) > r) {
    cplib::panic("rem-bits must be at most |G| - 1");
  }

  // Bits below are indexed from the lowest position.
  std::vector<char> target(len + r, 0);
  for (std::size_t i = 0; i < static_cast<std::size_t>(args::rem_bits); ++i) {
    target[i] = gen.rnd.next(0, 1);
  }
  if (args::rem_bits > 0) target[args::rem_bits - 1] = 1;
  auto bit_of_g = [&](std::size_t i) { return g[r - i] == '1'; };

  std::vector<char> product(len + r, 0);
  for (std::size_t i = 0; i < len; ++i) {
    bool k =
        i < r ? product[i] != target[i] : gen.rnd.next(0, 99) < args::density;
    if (i + 1 == len) k = true;
    if (!k) continue;
    for (std::size_t j = 0; j <= r && i + j < len + r; ++j) {
      product[i + j] ^= static_cast<char>(bit_of_g(j));
    }
  }

  std::string m(len, '0');
  for (std::size_t i = 0; i < len; ++i) {
    if (product[r + i] != 0) m[len - 1 - i] = '1';
  }
  return m;
}

auto make_m(int len, const std::string &g) -> std::string {
  std::string s;
  if (args::m_kind == "random") {
    s = random_bits(len, args::density);
  } else if (args::m_kind == "alternating") {
    s.resize(len);
    for (int i = 0; i < len; ++i) s[i] = i % 2 == 0 ? '1' : '0';
  } else if (args::m_kind == "tail") {
    return make_tail_m(len, g);
  } else {
    cplib::panic("Unknown m-kind");
  }
  std::fill_n(s.begin(), std::min(args::zeros, len), '0');
  return s;
}

void generator_main() {
  std::println("{}", args::t);
  for (int i = 0; i < args::t; ++i) {
    auto g = make_g(i == 0 ? args::head_g : args::g);
    auto m = make_m(i == 0 ? args::head_n : args::n, g);
    std::println("{} {}", m, g);
  }
  gen.quit_ok();
}
