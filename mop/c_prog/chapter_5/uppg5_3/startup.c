#define GPIO_E 0x40021000
#define GPIO_MODER ((volatile unsigned int *)(GPIO_E))
#define BARGRAPH ((volatile unsigned char *)(GPIO_E + 0x14))

#define SYSTICK 0xE000E010
#define STK_CTRL ((volatile unsigned int *)(SYSTICK))
#define STK_LOAD ((volatile unsigned int *)(SYSTICK + 0x4))
#define STK_VAL ((volatile unsigned int *)(SYSTICK + 0x8))
#define STK_CALIB ((volatile unsigned int *)(SYSTICK + 0xC))

__attribute__((naked)) __attribute__((section(".start_section"))) void startup(void)
{
    __asm__ volatile(" LDR R0,=0x2001C000\n"); /* set stack */
    __asm__ volatile(" MOV SP,R0\n");
    __asm__ volatile(" BL main\n");   /* call main */
    __asm__ volatile(".L1: B .L1\n"); /* never return */
}

void app_init(void)
{
    *GPIO_MODER = 0x5555;
}

void delay_250ns(void)
{
    *STK_CTRL = 0;
    *STK_LOAD = 41;
    *STK_VAL = 0;
    *STK_CTRL = 5;
    while (!(0x10000 & *STK_CTRL));
    *STK_CTRL = 0;
}

void delay_mikro(unsigned int us)
{
    for (unsigned int i = 0; i < us * 4; i++)
    {
        delay_250ns();
    }
}

void delay_milli(unsigned int ms)
{
    for (unsigned int i = 0; i < ms * 4000; i++)
    {
        delay_250ns();
    }
}

void main(void)
{
    app_init();
    while (1)
    {
        *BARGRAPH = 0;
        delay_milli(1);
        *BARGRAPH = 0xFF;
        delay_milli(2);
    }
}
