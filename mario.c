#include <cs50.h>
#include <stdio.h>

int main(void)
{
    
    int height;
    do
    {
        /* prompt for input from user */
        printf("Height: ");    
        
        /* define variable for row and height */
        height = get_int();    
    }
    while (height > 23 || height < 0);

    /* loop while row <= height */
    for (int n = 0; n <= height - 1; n++)
    {
        /* define diff as height less row */
        int diff = height - 1 - n;
        
        /* loop through diff printing spaces each time */
        for (int i = diff; i > 0; i--)
        {
            printf(" ");
        }
        
        /* loop through row adding # each time */
        for (int j = n + 1; j > 0; j--)
        {
            printf("#");
        }
        
        /* add two spaces */
        printf("  ");
        
        /* loop through row adding # each time */
        for (int k = n + 1; k > 0; k--)
        {
            printf("#");
        }        
        
        printf("\n");
    }
    
    
}
