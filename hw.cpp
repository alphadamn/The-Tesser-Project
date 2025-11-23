#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

bool isSubsequence(const string& s, const string& p) {
    int i = 0, j = 0;
    int n = s.length(), m = p.length();
    
    while (i < n && j < m) {
        if (s[i] == p[j]) {
            j++;
        }
        i++;
    }
    
    return j == m;
}

string addThousandSeparator(const string& num) {
    string result;
    int count = 0;
    
    for (int i = num.length() - 1; i >= 0; i--) {
        result.push_back(num[i]);
        count++;
        
        if (count % 3 == 0 && i != 0) {
            result.push_back(',');
        }
    }
    
    reverse(result.begin(), result.end());
    return result;
}

int main() {
    int choice;
    cout << "请选择题目 (1-子序列判断, 2-千位分隔符): ";
    cin >> choice;
    
    if (choice == 1) {
        string s, p;
        cout << "请输入字符串 s: ";
        cin >> s;
        cout << "请输入字符串 p: ";
        cin >> p;
        
        if (isSubsequence(s, p)) {
            cout << "YES" << endl;
        } else {
            cout << "NO" << endl;
        }
        
    } else if (choice == 2) {
        string num;
        cout << "请输入正整数: ";
        cin >> num;
        
        string result = addThousandSeparator(num);
        cout << result << endl;
        
    } else {
        cout << "无效的选择!" << endl;
    }
    
    return 0;
}