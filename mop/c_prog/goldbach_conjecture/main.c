#include <stdio.h>

int is_prime(int n)
{
    int i;
    for (i = 2; i < n; i++)
    {
        if (n % i == 0)
        {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char **argv) 
{ 
  int x; 
  printf("Is prime test\n"); 
  while(1) 
  { 
    printf("Enter number to check:");  
    scanf("%d",&x);  
    if( x < 2 )
    {
        printf("Please enter a number higher than 1\n");
        continue;
    }
    if( is_prime( x ) ) 
      printf("%d is a prime number\n", x);  
    else 
      printf("Nop, %d is NOT a prime number\n", x);  
  } 
  return 0; 
} 
