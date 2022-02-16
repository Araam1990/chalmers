#define SYSTICK 0xE000E010
#define STK_CTRL ((volatile unsigned int *)(SYSTICK))
#define STK_LOAD ((volatile unsigned int *)(SYSTICK + 0x4))
#define STK_VAL ((volatile unsigned int *)(SYSTICK + 0x8))
#define STK_CALIB ((volatile unsigned int *)(SYSTICK + 0xC))

__attribute__((naked)) __attribute__((section (".start_section")) )
void startup ( void )
{
__asm__ volatile(" LDR R0,=0x2001C000\n");		/* set stack */
__asm__ volatile(" MOV SP,R0\n");
__asm__ volatile(" BL main\n");					/* call main */
__asm__ volatile(".L1: B .L1\n");				/* never return */
}

__attribute__((naked))
void graphic_initialize(void)
{
    __asm__ volatile (" .HWORD 0xDFF0\n");
    __asm__ volatile (" BX LR\n");
}

__attribute__((naked))
void graphic_clear_screen(void)
{
    __asm__ volatile (" .HWORD 0xDFF1\n");
    __asm__ volatile (" BX LR\n");
}

__attribute__((naked))
void graphic_pixel_set(int x, int y)
{
    __asm__ volatile (" .HWORD 0xDFF2\n");
    __asm__ volatile (" BX LR\n");
}

__attribute__((naked))
void graphic_pixel_clear(int x, int y)
{
    __asm__ volatile (" .HWORD 0xDFF3\n");
    __asm__ volatile (" BX LR\n");
}

void delay_250ns(void)
{
    *STK_CTRL = 0;
    *STK_LOAD = 41;
    *STK_VAL = 0;
    *STK_CTRL = 5;
    while (!(0x10000 & *STK_CTRL))
        ;
    *STK_CTRL = 0;
}

void delay_mikro(unsigned int us)
{
    for (unsigned int i = 0; i < us * 4; i++)
        delay_250ns();
}

void delay_milli(unsigned int ms)
{
    for (unsigned int i = 0; i < ms * 4000; i++)
        delay_250ns();
}

void main(void)
{
    int i;
    graphic_initialize();
    graphic_clear_screen();
    for (i = 1; i <= 128; i++){
        graphic_pixel_set(i,10);
    }
    for (i = 1; i <= 64; i++){
        graphic_pixel_set(10,i);
    }
    delay_milli(1);
    for (i = 1; i <= 128; i++){
        graphic_pixel_clear(i,10);
    }
    for (i = 1; i <= 64; i++){
        graphic_pixel_clear(10,i);
    }
}

