// Internal wrong answer: equal neighbors are incorrectly accepted as peaks.
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int answer = 0;
    for (int i = 1; i + 1 < n; ++i)
        answer += a[i] >= a[i - 1] && a[i] >= a[i + 1];
    cout << answer << '\n';
}
