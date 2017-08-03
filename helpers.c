/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
 

bool search(int value, int values[], int n)
{
    // define first last and middle indexes
    int first = 0;
    int last = n - 1;
    int mid = (first + last) / 2;
    
    // check against middle number while range is valid
    do
    {
        // printf("first index: %i\nlast index: %i\n mid index: %i\n",first,last,mid);
        // return true if middle number is equal to value
        if (values[mid] == value)
        {
            return true;
        }
        
        // if mid number is greater than value, move last index to middle - 1 to search left half
        else if (values[mid] > value)
        {
            last = mid - 1;
        }
        
        // if mid number is less than value, move first index to middle + 1 to search right half
        else 
        {
            first = mid + 1;
        }
        
        // update middle number
        mid = (first + last) / 2;
    }
    while (first <= last);
    
    // if do-while loop concludes without finding target value, we know it's not in the array
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    
    int min, minIndex, val;
    
    // loop through array up until penultimate index
    for (int i = 0; i < n - 1; i++)
    {
        // initial min value
        min = values[i];
        minIndex = i;
        
        // loop through array to find smallest value
        for (int j = i; j < n; j++)
        {
            // if the value is less than the minimum, update the min and remember the index
            if (values[j] < min)
            {
                min = values[j];
                minIndex = j;
            }
        }
        
        if (i == minIndex) {
            continue;
        }
        
        val = values[i];
        values[i] = min;
        values[minIndex] = val;
    }
    
    return;
}
