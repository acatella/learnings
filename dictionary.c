/**
 * Implements a dictionary's functionality.
 */

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <cs50.h>
#include <ctype.h>


/**
 * Returns true if word is in dictionary else false using hash table.
 */

// Global variables
unsigned int entries = 0;

// Create node struct

typedef struct node {
    char word[LENGTH+1];
    struct node *next;
}
node;

// Create hashing function and hash table 
node *table[ITEMS];

// hash djb2 courtesty of Dan Bernstein
unsigned long
getHash(char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    
    hash = hash % ITEMS;
    return hash;
}



bool check(const char *word)
{
    int len = strlen(word);
    // Convert word to lowecase
    char check[LENGTH + 1];
    bool wordEnded = false;
    for (int i = 0; i < LENGTH + 1; i++) {
        if (word[i] == '\0' || wordEnded) {
            check[i] = '\0';
            wordEnded = true;
            continue;
        }
        char lwr = tolower(word[i]);
        check[i] = lwr;
    }
    
    check[len] = '\0';
    
    // Check position in hash table
    int ix = getHash(check);
    node *checker = table[ix];
    
    if (checker == NULL) {
        return false;
    }
    // If not empty, search for word
    else {
        while (checker != NULL) {
            if(strcmp(check, checker -> word ) == 0) {
                return true;
            }
            checker = checker -> next;
        }
    }
    
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE* dict = fopen(dictionary,"r");
    if (dict == NULL) {
        printf("Couldn't open provided dictionary :(");
        return false;
    }
    
    char entry[LENGTH + 1];
    
    // Adds all the words in dictionary to hash table
    while (fscanf(dict, "%s\n", entry) != EOF) {
        
        // Create node pointer and memory for entry and place it in the table
        node *newEntry = malloc(sizeof(node));
        
        int len = 0;
        for (int k = 0; k < LENGTH; k++) {
            if (entry[k] == '\0') {
                break;
            }
            len++;
        }
        // Make string lowercase before adding it
        char *newWord = malloc((len + 1) * sizeof(char));
        for (int i = 0; i < strlen(entry); i++) {
            char lwr = tolower(entry[i]);
            newWord[i] = lwr;
        }
        
        newWord[len] = '\0';
        
        strcpy(newEntry -> word, newWord);
        int i = getHash(newWord);
        
        if (table[i] != NULL) {
            newEntry -> next = table[i];
            table[i] = newEntry;
        }
        else {
            table[i] = newEntry;
            newEntry -> next = NULL;
        }
        
        entries++;
        free(newWord);
    }
    
    fclose(dict);
    
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return entries;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // free data in hash table
    for (int i = 0; i < ITEMS; i++) {
        while (table[i] != NULL) {
            node *current = table[i];
            table[i] = current -> next;
            free(current);
        }
    }
    return true;
}
