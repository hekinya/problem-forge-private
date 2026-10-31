#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long jump;
    cin >> n >> jump;

    int count = 0;
    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (x <= jump) ++count;
    }

    cout << jump + count << '\n';
    return 0;
}
