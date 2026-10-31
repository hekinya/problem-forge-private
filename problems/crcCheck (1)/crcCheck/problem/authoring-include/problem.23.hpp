#pragma once

#include <cstddef>
#include <cstdint>
#include <optional>
#include <ranges>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "cplib.hpp"

inline constexpr std::int32_t MAX_T = 1000;
inline constexpr std::size_t MAX_TOTAL_LEN = 5000;

struct TestCaseInput {
  std::string m, g;

  static auto read(cplib::var::Reader &in, std::int32_t tc_idx)
      -> TestCaseInput {
    std::string m, g;
    std::tie(m, std::ignore, g, std::ignore) =
        in(cplib::var::String("m", cplib::Pattern("[01]+")), cplib::var::space,
           cplib::var::String("g", cplib::Pattern("1[01]+")), cplib::var::eoln);
    if (in.get_trace_level() >= cplib::trace::Level::FULL) {
      in.attach_tag("hull/case", tc_idx);
    }
    return {.m = std::move(m), .g = std::move(g)};
  }
};

struct Input {
  std::vector<TestCaseInput> test_cases;

  static auto read(cplib::var::Reader &in) -> Input {
    std::int32_t t;
    std::tie(t, std::ignore) =
        in(cplib::var::i32("T", 1, MAX_T), cplib::var::eoln);
    auto test_cases = in.read(
        cplib::var::ExtVec<TestCaseInput>("test_cases", std::views::iota(0, t),
                                          cplib::var::Separator(std::nullopt)));

    std::size_t total_m = 0, total_g = 0;
    for (const auto &tc : test_cases) {
      total_m += tc.m.size();
      total_g += tc.g.size();
    }
    if (total_m > MAX_TOTAL_LEN) in.fail("Sum of |M| exceeds the limit");
    if (total_g > MAX_TOTAL_LEN) in.fail("Sum of |G| exceeds the limit");
    return {.test_cases = std::move(test_cases)};
  }
};

struct TestCaseOutput {
  std::string q, r;

  static auto read(cplib::var::Reader &in, std::int32_t) -> TestCaseOutput {
    auto [q, r] = in(cplib::var::String("q", cplib::Pattern("[01]+")),
                     cplib::var::String("r", cplib::Pattern("[01]+")));
    return {.q = std::move(q), .r = std::move(r)};
  }
};

struct Output {
  std::vector<TestCaseOutput> test_cases;

  static auto read(cplib::var::Reader &in, const Input &input) -> Output {
    auto t = static_cast<std::int32_t>(input.test_cases.size());
    auto test_cases = in.read(cplib::var::ExtVec<TestCaseOutput>(
        "test_cases", std::views::iota(0, t),
        cplib::var::Separator(std::nullopt)));
    return {.test_cases = std::move(test_cases)};
  }

  static auto evaluate(cplib::evaluate::Evaluator &ev, const Output &pans,
                       const Output &jans, const Input &)
      -> cplib::evaluate::Result {
    auto res = cplib::evaluate::Result::ac();
    for (std::size_t i = 0; i < jans.test_cases.size(); ++i) {
      res &= ev.eq("q", pans.test_cases[i].q, jans.test_cases[i].q);
      res &= ev.eq("r", pans.test_cases[i].r, jans.test_cases[i].r);
    }
    return res;
  }
};

inline auto traits(const Input &) -> std::vector<cplib::validator::Trait> {
  return {};
}
