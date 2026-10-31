#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long jump;
    cin >> n >> jump;

    vector<int> height(n);
    for (int &x : height) cin >> x;
    sort(height.begin(), height.end());

    for (int x : height) {
        if (jump > x) {
            ++jump;
        } else {
            break;
        }
    }

    cout << jump << '\n';
    return 0;
}
