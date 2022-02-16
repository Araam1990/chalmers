#define GPIO_D 0x40020C00
#define GPIO_MODER ((volatile unsigned int *)(GPIO_D))
#define GPIO_OTYPER ((volatile unsigned short *)(GPIO_D + 0x4))
#define GPIO_PUPDR ((volatile unsigned int *)(GPIO_D + 0xC))
#define GPIO_IDR_LOW ((volatile unsigned char *)(GPIO_D + 0x10))
#define GPIO_IDR_HIGH ((volatile unsigned char *)(GPIO_D + 0x11))
#define GPIO_ODR_LOW ((volatile unsigned char *)(GPIO_D + 0x14))
#define GPIO_ODR_HIGH ((volatile unsigned char *)(GPIO_D + 0x15))

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

#define MAX_POINTS 30
typedef struct
{
    int numpoints;
    int sizex, sizey;
    POINT px[MAX_POINTS];
} GEOMETRY, *PGEOMETRY;

typedef struct tObj
{
    PGEOMETRY geo;
    int dirx, diry;
    int posx, posy;
    void (*draw)(struct tObj *);
    void (*clear)(struct tObj *);
    void (*move)(struct tObj *);
    void (*set_speed)(struct tObj *, int, int);
} OBJECT, *POBJECT;

void init_app(void)
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
    default:
        *GPIO_ODR_HIGH = 0x00;
        break;
    }
}

unsigned char read_column()
{
    unsigned char c;
    c = *GPIO_IDR_HIGH;
    if (c & 0x8)
        return 4;
    if (c & 0x4)
        return 3;
    if (c & 0x2)
        return 2;
    if (c & 0x1)
        return 1;
    return 0;
}

unsigned char keyb(void)
{
    unsigned char col;
    unsigned char keys[] = {0x1, 0x2, 0x3, 0xA, 0x4, 0x5, 0x6, 0xB, 0x7, 0x8, 0x9, 0xC, 0xE, 0x0, 0xF, 0xD};
    for (int row = 1; row <= 4; row++)
    {
        activate_row(row);
        col = read_column();
        if (col)
        {
            return (unsigned char)keys[(row - 1) * 4 + (col - 1)];
        }
    }
    return 0xFF;
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

void draw_object(POBJECT o)
{
    for (char i = 0; i < o->geo->numpoints; i++)
    {
        graphic_pixel_set(o->posx + o->geo->px[i].x, o->posy + o->geo->px[i].y);
    }
}

void clear_object(POBJECT o)
{
    for (char i = 0; i < o->geo->numpoints; i++)
    {
        graphic_pixel_clear(o->posx + o->geo->px[i].x, o->posy + o->geo->px[i].y);
    }
}

void move_ballobject(POBJECT o)
{
    o->clear(o);

    o->posx += o->dirx;
    o->posy += o->diry;

    if (o->posx < 1)
        o->dirx = 4;
    else if ((o->posx + o->geo->sizex) > 128)
        o->dirx = -4;
    else if (o->posy < 1)
        o->diry = 1;
    else if ((o->posy + o->geo->sizey) > 64)
        o->diry = -1;

    o->draw(o);
}

void move_spiderobject(POBJECT o)
{
    o->clear(o);

    o->posx += o->dirx;
    o->posy += o->diry;

    o->draw(o);
}

void set_object_speed(POBJECT o, int speedx, int speedy)
{
    o->dirx = speedx;
    o->diry = speedy;
}

int overlapping(POBJECT o1, POBJECT o2)
{
    return ((o1->posy + o1->geo->sizey) >= o2->posy && o1->posy <= (o2->posy + o2->geo->sizey) && (o1->posx + o1->geo->sizex) >= o2->posx && o1->posx <= (o2->posx + o2->geo->sizex));
}

GEOMETRY ball_geometry = {
    12,
    4,
    4,
    {{0, 1},
     {0, 2},
     {1, 0},
     {1, 1},
     {1, 2},
     {1, 3},
     {2, 0},
     {2, 1},
     {2, 2},
     {2, 3},
     {3, 1},
     {3, 2}}};

static OBJECT ball = {&ball_geometry, 0, 0, 1, 1, draw_object, clear_object, move_ballobject, set_object_speed};

GEOMETRY spider_geometry = {
    22,
    6,
    8,
    {
        {2, 0},
        {3, 0},
        {1, 1},
        {4, 1},
        {0, 2},
        {1, 2},
        {2, 2},
        {3, 2},
        {4, 2},
        {5, 2},
        {0, 3},
        {2, 3},
        {3, 3},
        {5, 3},
        {1, 4},
        {4, 4},
        {2, 5},
        {3, 5},
        {1, 6},
        {4, 6},
        {0, 7},
        {5, 7},
    }};

static OBJECT spider = {&spider_geometry, 0, 0, 61, 28, draw_object, clear_object, move_spiderobject, set_object_speed};

void main(void)
{
    char c;
    POBJECT b = &ball;
    POBJECT s = &spider;
    init_app();
    graphic_initialize();
    graphic_clear_screen();

    b->set_speed(b, 4, 1);

    while (1)
    {
        b->move(b);
        s->move(s);
        c = keyb();
        switch (c)
        {
        case 6:
            s->set_speed(s, 2, 0);
            break;
        case 4:
            s->set_speed(s, -2, 0);
            break;
        case 5:
            s->set_speed(s, 0, 0);
            break;
        case 2:
            s->set_speed(s, 0, -2);
            break;
        case 8:
            s->set_speed(s, 0, 2);
            break;
        default:
            s->set_speed(s, 0, 0);
            break;
        }
        if (overlapping(b, s) || (s->posx + s->geo->sizex) < 1 || s->posx > 128 || (s->posy + s->geo->sizey) < 1 || s->posy > 64)
            break;
        delay_mikro(10);
    }
}