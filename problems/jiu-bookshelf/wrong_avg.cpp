#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    long long sum = 0, maximum = 0;
    for (int i = 0; i < n; ++i) {
        long long x;
        cin >> x;
        sum += x;
        maximum = max(maximum, x);
    }

    long long average = (sum + k - 1) / k;
    cout << max(maximum, average) << '\n';
    return 0;
}
