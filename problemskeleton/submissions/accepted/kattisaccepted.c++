#include <bits/stdc++.h>                           // ignore error, this will work on kattis
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> bad;
    int n;
    cin >> n;

    for (int k = 0; k < n; k++) {                   // Same logic as other languages, limited to 18 digit numbers due to limit of long long type
        string s;                                   // Must decide if switch to big-integer or limit problem size to 18 digits to allow val to work
        cin >> s;

        long long val = 0;
        bool ok = true;

        for (int i = 1; i <= (int)s.size(); i++) {
            int digit = s[i - 1] - '0';
            val = val * 10 + digit;

            if (val % i != 0) {
                ok = false;
                break;
            }
        }

        if (!ok)
            bad.push_back(s);
    }

    if (bad.empty()) {
        cout << "Firewall is secure!\n";
    } else {
        cout << "Vulnerabilities detected:\n";
        for (auto &x : bad) cout << x << "\n";
    }

    return 0;
}