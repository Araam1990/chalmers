#include <stdio.h>

int main(int argc, char **argv)
{
	* ( (unsigned int *) 0x40020C00) &= 0x0000FFFF;
    * ( (unsigned int *) 0x40020C00) |= 0x55000000;
    
    * ( (unsigned int *) 0x40020C04) &= 0xFFFF00FF;
    * ( (unsigned int *) 0x40020C04) |= 0x0000F000;
    
    * ( (unsigned int *) 0x40020C0C) &= 0x0000FFFF;
    * ( (unsigned int *) 0x40020C0C) |= 0x00AA0000;
    
    
    return 0;
}
