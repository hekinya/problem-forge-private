#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;

    int answer = 0;
    for (int i = 1; i + 1 < n; ++i) {
        if (a[i] > a[i - 1] && a[i] > a[i + 1]) ++answer;
    }
    cout << answer << '\n';
}
