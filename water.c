#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("Minutes: ");
    int showerLength = get_int();
    int waterUsed = showerLength * 1.5 * 128 / 16;
    printf("Bottles: %i\n",waterUsed);
}
