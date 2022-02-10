/*
 * 	startup.c
 *
 */
__attribute__((naked)) __attribute__((section(".start_section"))) void startup(void)
{
    __asm__ volatile(" LDR R0,=0x2001C000\n"); /* set stack */
    __asm__ volatile(" MOV SP,R0\n");
    __asm__ volatile(" BL main\n");   /* call main */
    __asm__ volatile(".L1: B .L1\n"); /* never return */

#define GPIO_D 0x40020C00
#define GPIO_MODER ((volatile unsigned int *)(GPIO_D))
#define GPIO_OTYPER ((volatile unsigned short *)(GPIO_D + 0x4))
#define GPIO_PUPDR ((volatile unsigned int *)(GPIO_D + 0xC))
#define GPIO_IDR_LOW ((volatile unsigned char *)(GPIO_D + 0x10))
#define GPIO_IDR_HIGH ((volatile unsigned char *)(GPIO_D + 0x11))
#define GPIO_ODR_LOW ((volatile unsigned char *)(GPIO_D + 0x14))
#define GPIO_ODR_HIGH ((volatile unsigned char *)(GPIO_D + 0x15))
}

void app_init(void)
{
    *GPIO_MODER = 0x55005555;

    *GPIO_PUPDR &= 0x0000FFFF;
    *GPIO_PUPDR |= 0x00AA0000;

    *GPIO_OTYPER &= 0x0FFF;
}

void activate_row(row)
{
    switch (row)
    {
    case 1:
        *GPIO_ODR_HIGH = 0x10;
        break;
    case 2:
        *GPIO_ODR_HIGH = 0x20;
        break;
    case 3:
        *GPIO_ODR_HIGH = 0x40;
        break;
    case 4:
        *GPIO_ODR_HIGH = 0x80;
        break;
    case 5:
        *GPIO_ODR_HIGH = 0xF0;
        break;
    default:
        *GPIO_ODR_HIGH = 0x00;
        break;
    }
}

unsigned short keyb_alt_ctrl(void)
{
    unsigned short bitmask = 0x0000;
    for (int row = 1; row <= 4; row++)
    {
        bitmask *= 0x10;
        activate_row(row);
        bitmask += *GPIO_IDR_HIGH;
    }
    return bitmask;
}

unsigned char is_numeric(keyb_status)
{
    unsigned short masks[10] = {0x0002, 0x1000, 0x2000, 0x4000, 0x0100, 0x0200, 0x0400, 0x0010, 0x0020, 0x0040};
    for (unsigned char i = 0; i < 10; i++)
    {
        if (keyb_status & masks[i])
            return i;
    }
    return 0xFF;
}

void out7seg(unsigned char c)
{
    unsigned char segcodes[16] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x67, 0x77, 0x7A, 0x39, 0x5E, 0x79, 0x71};
    *GPIO_ODR_LOW = segcodes[c];
}

void main(void)
{
    unsigned short keyb_status;
    unsigned char c;
    app_init();

    while (1)
    {
        keyb_status = keyb_alt_ctrl();
        c = is_numeric(keyb_status);
        if (c != 0xFF)
            out7seg(c);
    }
}