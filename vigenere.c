#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    
string keyword = argv[1];

// make sure there is exactly one cmd line argument and it's a non-null string
if (argc != 2 || strlen(keyword) < 1)
{
    // if not, return an error
    printf("Please enter a secret key\n");
    return 1;
}

// define length of key and helper variables
int keyLen = strlen(keyword);
int key;
int j;
int iter = 0;

// ensure keyword is composed of only alphabet chars
for (int k = 0; k < keyLen; k++) {
    int c = (int)keyword[k];
    if(c < 65 || c > 122 || (c > 90 && c < 97))
    {
        // if not, return an error
        printf("Please enter a secret key\n");
        return 1;
    }
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
    
    // determine which letter of key to use
    if (iter >= keyLen)
    {
      j = iter % keyLen;
    }
    else
    {
        j = iter;
    }
    
    // convert key letter to uppercase then to ascii int then subtract 65 to make it usable key
    key = (int)toupper(keyword[j]);
    key = key - 65;
    
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
        
        iter++;
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
        
        iter++;
    }
    // if char is not an ascii letter, print it
    else
    {
        printf("%c",plaintext[i]);
    }
}           
printf("\n");

}            
