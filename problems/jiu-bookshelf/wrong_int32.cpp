#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    int sum = 0, maximum = 0;
    for (int &x : a) {
        cin >> x;
        sum += x;
        maximum = max(maximum, x);
    }

    auto feasible = [&](int limit) {
        int groups = 1;
        int current = 0;
        for (int x : a) {
            if (current + x > limit) {
                ++groups;
                current = x;
            } else {
                current += x;
            }
        }
        return groups <= k;
    };

    int low = maximum, high = sum;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (feasible(mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    cout << low << '\n';
    return 0;
}
