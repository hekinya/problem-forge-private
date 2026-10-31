#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long jump;
    if (!(cin >> n >> jump)) return 0;

    vector<int> height(n);
    for (int &x : height) cin >> x;

    sort(height.begin(), height.end());
    for (int x : height) {
        if (x <= jump) {
            ++jump;
        } else {
            break;
        }
    }

    cout << jump << '\n';
    return 0;
}
