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

void main(void) {

  char a = 11;

  char b = 7;

  char c = 238;

  a = b - c;

  c = b ^ a;

  a = c - b;

  c = b - a;

  c = a - b;

  b = a | c;

  b = a * c;

  b = a + c;

  a = b + c;

  a = c + b;

  a += b;

  a += c;

  char result = (char)(a & 0xFF);

}

