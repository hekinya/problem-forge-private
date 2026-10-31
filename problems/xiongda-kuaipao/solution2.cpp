#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long jump;
    cin >> n >> jump;

    priority_queue<int, vector<int>, greater<int>> fruits;
    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        fruits.push(x);
    }

    while (!fruits.empty() && fruits.top() <= jump) {
        fruits.pop();
        ++jump;
    }

    cout << jump << '\n';
    return 0;
}
