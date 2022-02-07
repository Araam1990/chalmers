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

#define GPIO_D          0x40020C00
#define GPIO_MODER      ((volatile unsigned int *)      (GPIO_D))
#define GPIO_OTYPER     ((volatile unsigned short *)    (GPIO_D+0x4))
#define GPIO_PUPDR      ((volatile unsigned int *)      (GPIO_D+0xC))
#define GPIO_IDR_LOW    ((volatile unsigned char *)     (GPIO_D+0x10))
#define GPIO_IDR_HIGH   ((volatile unsigned char *)     (GPIO_D+0x11))
#define GPIO_ODR_LOW    ((volatile unsigned char *)     (GPIO_D+0x14))
#define GPIO_ODR_HIGH   ((volatile unsigned char *)     (GPIO_D+0x15))
}

unsigned char wait = 0;

void app_init(void)
{
    *GPIO_MODER = 0x55005555;
    
    *GPIO_PUPDR &= 0x0000FFFF;
    *GPIO_PUPDR |= 0x00AA0000;
    
    *GPIO_OTYPER &= 0x0FFF
}


void activate_row(row)
{
    switch(row)
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

unsigned char read_column()
{
    unsigned char c;
    c = *GPIO_IDR_HIGH;
    if ( c & 0x8 ) return 4;
    if ( c & 0x4 ) return 3;
    if ( c & 0x2 ) return 2;
    if ( c & 0x1 ) return 1;
    return 0;
}

unsigned char wait_for_me(void)
{
    activate_row(5);
    unsigned char col = read_column();
    if (!col){
        wait = 0;
    }
    return 0xFF;
}

unsigned char keyb(void)
{
    unsigned char col;
    unsigned char keys[] = {0x1,0x2,0x3,0xA,0x4,0x5,0x6,0xB,0x7,0x8,0x9,0xC,0xE,0x0,0xF,0xD};
    for(int row = 1; row <= 4; row++){
        activate_row(row);
        col = read_column();
        if(col){
            wait = 1;
            return (unsigned char) keys[(row-1)*4+(col-1)];
        }
    }
    return 0xFF;
}


unsigned char keyb_enhanced(void)
{
    if (wait)
        return wait_for_me();
    
    else
        return keyb();
}

void out7seg(unsigned char c)
{
    unsigned char segcodes[]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67,0x77,0x7A,0x39,0x5E,0x79,0x71};
    *GPIO_ODR_LOW = segcodes[c];
}

void main(void)
{
    unsigned char c;
    app_init();
    while(1){
        c = keyb_enhanced();
        if (c != 0xFF)
            out7seg(c);
    }
}