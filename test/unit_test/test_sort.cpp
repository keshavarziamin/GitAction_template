#include "insertion.hpp"
#include "gtest/gtest.h"

class TEST_SORT : public ::testing::TestWithParam<std::pair<std::string, std::vector<int>>>
{
public:
    Sort sort;

protected:
};

std::vector<std::pair<std::string, std::vector<int>>> unsorted_list_vector = {
    {"empty", {}},
    {"one", {20}},
    {"mirror", {-10, -5, 0, 5, 10}},
    {"random", {1, 7, 8, 3, 2, 9, 4, 14, 60, 23, 20}}};

INSTANTIATE_TEST_SUITE_P(TEST_SORT_LIST_CASE, TEST_SORT,
                         ::testing::ValuesIn(unsorted_list_vector),
                         [](const ::testing::TestParamInfo<TEST_SORT::ParamType> &info)
                         { return info.param.first; });

TEST_P(TEST_SORT, INSERTION)
{
    auto list = GetParam().second;
    auto sorted_list = list;
    std::sort(sorted_list.begin(), sorted_list.end());

    sort.sort(list);
    EXPECT_EQ(list,sorted_list);
}