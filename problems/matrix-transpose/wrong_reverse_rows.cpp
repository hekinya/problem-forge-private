#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<int>> a(n, vector<int>(m));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> a[i][j];
        }
    }

    for (int j = 0; j < m; ++j) {
        for (int i = n - 1; i >= 0; --i) {
            if (i != n - 1) cout << ' ';
            cout << a[i][j];
        }
        cout << '\n';
    }
    return 0;
}
