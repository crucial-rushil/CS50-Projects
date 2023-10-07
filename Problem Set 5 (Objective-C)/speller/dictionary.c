// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = -1; //was changed; original value: 1

unsigned int counter = 0;

// Hash table
node *table[N];
node *head = NULL;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int indexC = hash(word);
    if (table[indexC] != NULL)
    {
       if (strcasecmp(word,table[indexC]->word) == 0)
        {
            return true;
        }
    }

    /*for (node *checker = table[indexC]; checker != NULL; checker = checker->next)
    {
        if (strcasecmp(word,checker->word) == 0)
        {
            return true;
        }
    }*/

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO:

    //Hash Algorithm: DBJ2;
    //Credit: Daniel J. Bernstein (author of original hash function made in 1991)
    //Code Source: http://www.cse.yorku.ca/~oz/hash.html

    unsigned long hash = 5381;
        int c;

        while ((c = *word++))
        {
            hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
        }

    return hash;
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO:

    //open file
    //printf("N = %u",N);
    FILE *file = fopen(dictionary, "r");

    //check to see if file can be opened
    if (!file)
    {
        return false;
    }

    //create a buffer to read words into
    char word1[LENGTH+1];

    node *tail = NULL;
    //read ze words
    while (fscanf(file,"%s",word1) != EOF)
    {
        //allocates memory for new node
        node *n = malloc(sizeof(node));
        n->next = NULL;

        //checks to see if there is enough memory
        if (n == NULL)
        {
            return false;
        }

        //copies from buffer array into node
        strcpy(n->word,word1);

        //finds index where to insert in linked list
        unsigned int index = hash(n->word);
        table[index] = n;
        if (tail == NULL)
        {
            tail = n;
            head = n;
        }

        else
        {
            tail->next = n;
            tail = n;
        }
        //assigns the nodes pointer to the first element in the linked list in the hash table
        //n->next = table[index];

        //assigns the first element in the linked list in the hash table to the node
        //table[index]->next = n;

        counter += 1;
        //printf("Counter = %i",counter);
    }
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *p = head;
    while (p != NULL)
    {
        node *temp = p;
        p = p->next;
        free(temp);
    }
    /*for (int i = 0; i < N; i++)
    {
        int counter1 = 0;
        for (node *liberate = table[i], *tmp = table[i]; liberate != NULL; liberate = liberate->next)
        {
            if (counter1 == 0)
            {
                liberate = liberate->next;
            }
            free(tmp);
            tmp = liberate;
            counter += 1;
        }
    }*/
    return true;
}
