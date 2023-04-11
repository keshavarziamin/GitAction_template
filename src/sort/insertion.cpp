#include "insertion.hpp"

static void inserion(std::vector<int> &list, int temp);

void Sort::Insertion::sort(std::vector<int> &list)
{
    if (list.size() <= 1)
        return;

    auto temp = list[list.size() - 1];
    list.pop_back();
    sort(list);
    insertion(list, temp);
}

static void insertion(std::vector<int> &list, int temp)
{
    if (list.size() == 0 || list[list.size() - 1] <= temp)
    {
        list.push_back(temp);
        return;
    }
    int x = list[list.size() - 1];
    list.pop_back();
    insertion(list, temp);
    list.push_back(x);
}