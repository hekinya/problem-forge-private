#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<long long> a(n);
    long long sum = 0, maximum = 0;
    for (long long &x : a) {
        cin >> x;
        sum += x;
        maximum = max(maximum, x);
    }

    auto feasible = [&](long long limit) {
        int groups = 1;
        long long current = 0;
        for (long long x : a) {
            if (current + x > limit) {
                ++groups;
                current = x;
            } else {
                current += x;
            }
        }
        return groups == k;
    };

    long long low = maximum, high = sum;
    while (low < high) {
        long long mid = low + (high - low) / 2;
        if (feasible(mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    cout << low << '\n';
    return 0;
}
