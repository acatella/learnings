#include <cs50.h>
#include <stdio.h>

int main(void)
{
    /* get input */
    long long cc;
    do
    {
        printf("Card number to verify: ");
        cc = get_long_long();
    }
    while (cc < 0);
    
    /* define variables */
    long long checker = cc;
    int checkSum = 0;
    int digit;
    
    /* starting w/ 2nd to last number, multiply every other # by two and add it to checksum */
    do
    {
        /* cut off one digit, grab last digit, multiply it by two */
        checker = checker / 10;
        /*printf("checker is: %lld\n",checker);*/
        digit = (checker % 10) * 2;
        
        /* if the digit is over two, add each of its digits to the checksum, otherwise add the digit to checksum */
        if (digit > 9)
        {
            do
            {
                int x = digit % 10;
                checkSum += x;
                digit = digit / 10;
            }
            while (digit > 0);
        }
        else
        {
            checkSum += digit;
        }
        
        /* cut off one number */
        checker = checker / 10;
        /*printf("checker now is: %lld\n",checker); */
    }
    while (checker >= 1);
    
    /* starting at last digit in cc, add up every other digit */
    checker = cc;
    do
    {
        digit = checker % 10;
        checkSum += digit;
        checker = checker / 100;
    }
    while (checker >= 1);
    
    /* if last digit in checksum is 0 and card # is long enough/recognized it's valid */
    if (checkSum % 10 == 0 && cc > 1000000000000)
    {
        
        /* get first and second digits of cc # */
        do
        {
            cc = cc / 10;
        }
        while (cc > 100);
        
        int second = cc % 10;
        int first = cc / 10;
        int sum = first + second;
        
        /* check if VISA */
        if (first == 4) {
            printf("VISA\n");
        }
        /* check if AMEX */
        else if (first == 3 && (sum == 7 || sum == 10))
        {
            printf("AMEX\n");
        }
        else if (first == 5 && ((5 < sum) && (sum < 11)))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");    
        }
    }
    else
    {
        printf("INVALID\n");
    }
}