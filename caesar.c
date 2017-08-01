#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
// make sure there is exactly one cmd line argument
if (argc != 2)
{
    // if not, return an error
    printf("Please enter a secret key\n");
    return 1;
}

int key = atoi(argv[1]);
// set int cipher # as the argument % 26
if (key > 26)
{
    key = key % 26;
}

// prompt user for plaintext: input
string plaintext;
do
{
    printf("plaintext: ");
    plaintext = get_string();
}
while (!plaintext);

int n = strlen(plaintext);
printf("ciphertext: ");
// loop through full input
for (int i = 0; i < n; i++)
{
    int asciiCode = (int)plaintext[i];
    int newCode = asciiCode + key;
    // if letter is lowercase:
    if (asciiCode > 96 && asciiCode < 123)
    {
        // if letter ascii code + cipher# > 122
        if (newCode > 122)
        {
            // print letter of ascii code equal to 96 + letter ascii code + cipher# less 122
            newCode = newCode - 122 + 96;
            printf("%c",(char)newCode);
        }
        else {
            // otherwise print new character
            printf("%c",(char)newCode);
        }
    }
    // else if it's uppercase
    else if (asciiCode > 64 && asciiCode < 91)
    {
        if (newCode > 90 )
        {
            // print letter of ascii code equal to 64 + letter ascii code + cipher# less 122
            newCode = newCode - 90 + 64;
            printf("%c",(char)newCode);
        }
        else
        {
            printf("%c",(char)newCode);
        }
    }
    // if char is not an ascii letter, print it
    else
    {
        printf("%c",plaintext[i]);
    }
}           
printf("\n");

}            