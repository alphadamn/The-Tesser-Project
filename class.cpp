#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>

using namespace std;

struct cpile {
    int m,v;
    double unit_v;
};

template<typename T>
vector<T> greedyAlgorithm(
    const vector<T>& cpiles,
    function<bool(const T&, const T&)> comparator,
    function<bool(const T&, const vector<T>&)> selector) {
    
    vector<T> result;
    vector<T> sortedcpiles = cpiles;
    
    sort(sortedcpiles.begin(), sortedcpiles.end(), 
              [&comparator](const T& a, const T& b) {
                  return comparator(a, b);
              });
    
    for (const auto& cpile : sortedcpiles) {
        if (selector(cpile, result)) {
            result.push_back(cpile);
        }
    }
    
    return result;
}

int main() {
    int n,i;
    double t;
    cin >> n >> t;
    vector<cpile> piles;
    cpile pile;
    for (i=0;i<n;i++) {
        cin >> pile.m >> pile.v;
        pile.unit_v = (double)pile.v / pile.m;
        piles.push_back(pile);
    }
    
    auto valueDensityComparator = [](const cpile& a, const cpile& b) {
        return (a.v / a.m) > (b.v / b.m);
    };
    
    auto canSelect = [t](const cpile& pilec, const vector<cpile>& selected) {
        double totalWeight = 0;
        for (const auto& selectedcpile : selected) {
            totalWeight += selectedcpile.m;
        }
        return totalWeight + pilec.m <= t;
    };
    
    vector<cpile> result = greedyAlgorithm<cpile>(piles, valueDensityComparator, canSelect);
    
    cout << "选择的物品：" << endl;
    double totalValue = 0;
    double totalWeight = 0;
    
    for (const auto& cpile : result) {
        cout << " - 价值: " << cpile.v
                  << ", 重量: " << cpile.m << endl;
        totalValue += cpile.v;
        totalWeight += cpile.m;
    }
    
    cout << "总价值: " << totalValue << ", 总重量: " << totalWeight << endl;
    
    return 0;
}