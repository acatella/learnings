#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
// get string from user
string name = "";
do
{
    name = get_string();
}
while (!name);

// print uppercase of first index
printf("%c",toupper(name[0]));

// get length of name string
int n = strlen(name);

// loop through full string starting at [1]
for (int i = 1; i < n; i++)
{
    // if char before letter == a space, print uppercase of letter
    if (name[i-1] == ' ')
    {
        printf("%c",toupper(name[i]));
    }
}

printf("\n");
}
