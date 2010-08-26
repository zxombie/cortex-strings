#include <stddef.h>

int spawniis(int (*fun)(int, int, size_t), int runs, int a, int b, size_t c)
{
    int result;
    int i;

    for (i = 0; i != runs; i++)
    {
        result = fun(a, b, c);
    }

    return result;
}
