#include "sort.hpp"

namespace Sort
{
    class Insertion : public Sort
    {
    private:
        /* data */
    public:
        Insertion(/* args */){};
        ~Insertion(){};

        void sort(std::vector<int> &list) override;
    };
    

} // namespace Sort
