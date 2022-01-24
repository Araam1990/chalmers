/*
 * 	startup.c
 *
 */
__attribute__((naked)) __attribute__((section (".start_section")) )
void startup ( void )
{
__asm__ volatile(" LDR R0,=0x2001C000\n");		/* set stack */
__asm__ volatile(" MOV SP,R0\n");
__asm__ volatile(" BL main\n");					/* call main */
__asm__ volatile(".L1: B .L1\n");				/* never return */
}

#include <stdio.h> 
int main(void) 
{  
  int n = 15, first = 0, second = 1, next, c;  
  for ( c = 0 ; c < n ; c++ )  
  {  
    if ( c <= 1 )  
      next = c;  
    else  
    {  
      next = first + second;  
      first = second;  
      second = next;  
    }   
  } 
  return 0;  
} 

