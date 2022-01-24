#include <stdio.h>

int is_prime(int n)
{
    if(n < 2)
        return 0;
    int i;
    for(i = 2; i < n; i++)
        if(n % i == 0)
            return 0;
    return 1;
}

int goldbach(int start, int sum)
{
    while(start >= 0) {
        if(is_prime(start) && is_prime(sum - start))
            return start;
        start--;
    }
    return 0;
}

int main(int argc, char** argv)
{
    int x, cur;
    printf("Goldbachs conjecture\n");
    while(1) {
        printf("Enter number:");
        scanf("%d", &x);
        if(x < 2 || x % 2 == 1)
            continue;
        cur = x / 2;
        while(cur >= 0) {
            cur = goldbach(cur, x);
            if(cur)
                printf("%d + %d\n", cur, x - cur);
            cur--;
        }
    }
    return 0;
}
