#define PORT_BASE (int)0x40021000

#define PORT_MODER ((volatile unsigned int *)(PORT_BASE))
#define PORT_OTYPER ((volatile unsigned int *)(PORT_BASE + 0x04))
#define PORT_OSPEEDR ((volatile unsigned int *)(PORT_BASE + 0x08))
#define PORT_PUPDR ((volatile unsigned int *)(PORT_BASE + 0x0C))

#define PORT_IDR_LOW ((volatile unsigned char *)(PORT_BASE + 0x10))
#define PORT_IDR_HIGH ((volatile unsigned char *)(PORT_BASE + 0x11))
#define PORT_ODR_LOW ((volatile unsigned char *)(PORT_BASE + 0x14))
#define PORT_ODR_HIGH ((volatile unsigned char *)(PORT_BASE + 0x15))

#define CONTROLLER PORT_ODR_LOW
#define WRITE_DATA PORT_ODR_HIGH
#define READ_DATA PORT_IDR_HIGH

#define B_E (unsigned char)0x40
#define B_SELECT (unsigned char)0x04
#define B_RW (unsigned char)0x02
#define B_RS (unsigned char)0x01

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

void init_app(void)
{
    *PORT_MODER = 0x55555555;
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

void ascii_ctrl_bit_set(unsigned char bits)
{
    *CONTROLLER |= bits;
}

void ascii_ctrl_bit_clear(unsigned char bits)
{
    *CONTROLLER &= ~bits;
}

void ascii_write_controller(unsigned char command)
{
    ascii_ctrl_bit_set(B_E);
    *WRITE_DATA = command;
    delay_250ns();
    ascii_ctrl_bit_clear(B_E);
}

void ascii_write_cmd(unsigned char command)
{
    ascii_ctrl_bit_clear(B_RS + B_RW);
    ascii_write_controller(command);
}

void ascii_write_data(unsigned char data)
{
    ascii_ctrl_bit_set(B_RS);
    ascii_ctrl_bit_clear(B_RW);
    ascii_write_controller(data);
}

unsigned char ascii_read_controller(void)
{
    ascii_ctrl_bit_set(B_E);
    delay_250ns();
    delay_250ns();
    unsigned char rv = *READ_DATA;
    ascii_ctrl_bit_clear(B_E);
    return rv;
}

unsigned char ascii_read_status(void)
{
    *PORT_MODER &= 0x0000FFFF;
    ascii_ctrl_bit_clear(B_RS);
    ascii_ctrl_bit_set(B_RW);
    unsigned char rv = ascii_read_controller();
    *PORT_MODER |= 0x55550000;
    return rv;
}

unsigned char ascii_read_data(void)
{
    *PORT_MODER &= 0x0000FFFF;
    ascii_ctrl_bit_set(B_RW + B_RS);
    unsigned char rv = ascii_read_controller();
    *PORT_MODER |= 0x55550000;
    return rv;
}

void ascii_command(unsigned char command)
{
    while (ascii_read_status() & 0x0080)
        ;
    delay_mikro(8);
    ascii_write_cmd(command);
}

void function_set(void)
{
    ascii_command(0x38);
    delay_mikro(39);
}

void display_control(void)
{
    ascii_command(0x0E);
    delay_mikro(39);
}

void clear_display(void)
{
    ascii_command(1);
    delay_milli(2);
}

void entry_mode_set(void)
{
    ascii_command(0x06);
    delay_mikro(39);
}

void ascii_init(void)
{
    ascii_ctrl_bit_set(B_SELECT);
    function_set();
    display_control();
    clear_display();
    entry_mode_set();
}

void ascii_write_char(unsigned char c)
{
    while (ascii_read_status() & 0x0080)
        ;
    delay_mikro(8);
    ascii_write_data(c);
    delay_mikro(43);
}

void ascii_gotoxy(unsigned char row, unsigned char col)
{
    unsigned char address = row - 1;
    if (col == 2){
        address += 0x40;
    }
    ascii_command(0x80 | address);
    delay_mikro(39);
}

int main(void)
{
    char *s;
    char test1[] = "Alfanumerisk ";
    char test2[] = "Display - test";

    init_app();
    ascii_init();
    ascii_gotoxy(1,1);
    s = test1;
    while(*s)
        ascii_write_char(*s++);
    ascii_gotoxy(1,2);
    s=test2;
    while(*s)
        ascii_write_char(*s++);
    return 0;
}