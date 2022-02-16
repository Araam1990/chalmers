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

__attribute__((naked)) void graphic_initialize(void)
{
    __asm__ volatile(" .HWORD 0xDFF0\n");
    __asm__ volatile(" BX LR\n");
}

__attribute__((naked)) void graphic_clear_screen(void)
{
    __asm__ volatile(" .HWORD 0xDFF1\n");
    __asm__ volatile(" BX LR\n");
}

__attribute__((naked)) void graphic_pixel_set(int x, int y)
{
    __asm__ volatile(" .HWORD 0xDFF2\n");
    __asm__ volatile(" BX LR\n");
}

__attribute__((naked)) void graphic_pixel_clear(int x, int y)
{
    __asm__ volatile(" .HWORD 0xDFF3\n");
    __asm__ volatile(" BX LR\n");
}

typedef struct
{
    char x, y;
} POINT, *PPOINT;

typedef struct
{
    POINT p0, p1;
} LINE, *PLINE;

typedef struct
{
    POINT p;
    char x, y;
} RECT, *PRECT;

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

void swap(char *xp, char *yp)
{
    char temp = *xp;
    *xp = *yp;
    *yp = temp;
}

int draw_line(PLINE l)
{
    if (l->p0.x > 128 || l->p0.x < 1 || l->p1.x > 128 || l->p1.x < 1 || l->p0.y > 64 || l->p0.y < 1 || l->p1.y > 64 || l->p1.y < 1)
        return 0;
    char steep;
    steep = (abs(l->p1.y - l->p0.y) > abs(l->p1.x - l->p0.x));
    if (steep)
    {
        swap(&l->p0.x, &l->p0.y);
        swap(&l->p1.x, &l->p1.y);
    }
    if (l->p0.x > l->p1.x)
    {
        swap(&l->p0.x, &l->p1.x);
        swap(&l->p0.y, &l->p1.y);
    }
    char deltax = l->p1.x - l->p0.x;
    char deltay = abs(l->p1.y - l->p0.y);
    signed char error = 0;
    char y = l->p0.y;
    char ystep;
    if (l->p0.y < l->p1.y)
        ystep = 1;
    else
        ystep = -1;
    for (char x = l->p0.x; x <= l->p1.x; x++)
    {
        if (steep)
            graphic_pixel_set(y, x);
        else
            graphic_pixel_set(x, y);
        error += deltay;
        if (2 * error >= deltax)
        {
            y += ystep;
            error -= deltax;
        }
    }
    return 1;
}

void draw_rect(PRECT r)
{
    POINT p = {r->p.x, r->p.y};
    char x = r->x, y=r->y;
    LINE lines[] = {
        {p, p.x+x,p.y},
        {p.x+x,p.y, p.x+x,p.y+y},
        {p.x+x,p.y+y, p.x,p.y+y},
        {p.x,p.y+y, p},
    };
    for(char i = 0; i < 4; i++)
    {
        draw_line(&lines[i]);
    }
}

void main(void)
{
    char i;
    graphic_initialize();
    graphic_clear_screen();

    while (1)
    {
        RECT rects[] = {
            {10, 10, 20, 10},
            {25, 25, 10, 20},
            {40, 30, 70, 20},
            {60, 35, 10, 10},
            {70, 10, 5, 5},
        };
        for (i = 0; i < sizeof(rects) / sizeof(RECT); i++)
        {
            draw_rect(&rects[i]);
            delay_mikro(200);
        }
        graphic_clear_screen();
    }
}
