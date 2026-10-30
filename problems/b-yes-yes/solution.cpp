#include <iostream>
#include <string>
using namespace std;
int main() {
    int t; cin >> t;
    const string pattern = "Yes";
    while (t--) {
        string s; cin >> s;
        bool good = false;
        for (int start = 0; start < 3; ++start) {
            bool match = true;
            for (int i = 0; i < (int)s.size(); ++i) {
                if (s[i] != pattern[(start + i) % 3]) { match = false; break; }
            }
            good |= match;
        }
        cout << (good ? "YES" : "NO") << '\n';
    }
}
