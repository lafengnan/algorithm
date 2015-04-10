/*************************************************************************
	> File Name: pop.c
	> Author: lafengnan
	> Mail: panzhongbin@gmail.com 
	> Created Time: 五  3/13 20:32:08 2015
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>

#define MAX 100

#define SWAP(a, b) (a) ^= (b) ^= (a) ^= (b)

void swap(int*, int*);
void swap2(int*, int*);
static int count = 0;
static int a[] = {6, 3, 2, 1, -1, 5, 6, 7, -20, 10, 9, 8, 30};

void debug(int *a, const int len)
{
    for (int i = 0; i < len; ++i)
        printf("anan: a[%d] = %d\n\n", i, a[i]);
}

int* pop(int *a, int len)
{
    for(int j = len; j > 0; j--)
    for(int i = 0; i < j; i++) 
    {
        debug(a, len);
        if (a[i] > a[i+1]){
            count++;
            swap2(&a[i], &a[i+1]);
        }
    }
    return a;
}

int* pop2(int *a, int len, int stop)
{
    debug(a, stop);
    for(int i = 0; i < len && len > 0; ++i)
    {
        if (a[i] >= a[i+1])
        {
            count++;
            //swap2(&a[i], &a[i+1]);
            SWAP(a[i], a[i+1]);
        }
    }
    return (len == 1)?a:pop2(a, --len, stop);
}

int* insert_sort(int *a, int len)
{
    debug(a, len);
    for(int i = 1; i < len; ++i)
    {
        for(int j = i; j > 0; --j)
        {
            if(a[j] <= a[j-1])
            {
                count++;
                SWAP(a[j], a[j-1]);
            }
        }
    }

    return a;
}



int* insert_sort2(int *a, int len, int const stop)
{
    debug(a, stop);

    for(int i = len; i > 0; --i)
    {
        if (a[i] <= a[i-1])
        {
            count++;
            printf("swap %d and %d\n", i, i -1);
            SWAP(a[i], a[i-1]);
        }
    }
    return (len == stop - 1)?a:insert_sort2(a, ++len, stop);
}

//int* biinsert_sort(int *a, int len)
//{
//    debug(a, len);
//    int m = 0;
//    for (int i = 1 ; i < len; ++i)
//    {
//        int low = 0;
//        int high = i;
//        while(low <= high)
//        {
//            m = (low + high)/2;
//            if (a[m] <= a[i])
//                low = m + 1;
//            else if (a[m] > a[i])
//                high = m - 1;
//        }
//        for (int j = i; j > high; --j)
//        {
//            SWAP(a[j], a[j-1]);
//        }
//    }
//    return a;
//}

void swap(int *a, int *b)
{
    int tmp = 0;
    *a = tmp;
    tmp = *b;
    *a = tmp;
}

void swap2(int *a, int *b)
{
    *a ^= *b ^= *a ^= *b;
}

void init_array(int *a, int len)
{
    for (int i = 0; i < len; ++i)
       a[i] = 0x7ffffffff;
}

int main(int argc, char **argv)
{
    
    int len = sizeof(a)/sizeof(a[0]);
    int *d = insert_sort2(a, 1, len);
    for (int i = 0; i < len; i++) 
    {
        printf("a[%d] = %d\n", i, d[i]);
    }

    printf("swap %d times\n", count);
}
