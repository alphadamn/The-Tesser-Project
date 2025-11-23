#include <bits/stdc++.h>

using namespace std;

int main () {
    int n,r;
    vector<int> time;
    vector<vector<int>> qs;
    cin >> n >> r;
    for (int i=0;i<r;i++) {
        int tmp=0;
        cin >> tmp;
        time.push_back(tmp);
    }
    sort(time.begin(), time.end());
    for (int j=0;j<r;j++) {
        qs.push_back(vector<int>());
    }

}