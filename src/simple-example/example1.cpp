#include <iostream>
#include <iterator>
#include <vector>
#include "insertion.hpp"

void printVector( std::string const &str,std::vector<int> &list)
{
    std::cout<<str<<std::endl;
    std::copy(list.begin(), list.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout<<std::endl;
}

int main(int argc, char const *argv[])
{
    std::cout << "Hello CICD Github Action" << std::endl;
    std::vector<int> list = {20, 30, 10, 5, 9, 60};
    printVector("unsorted list:",list);

    Sort sort;
    sort.sort(list);
    printVector("sorted list:",list);
    
    return 0;
}
