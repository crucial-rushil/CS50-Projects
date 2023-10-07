#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Create boolean integer to use as toggle
    int run = 0;

    // Checks to make sure that the user only inputs ONE command-line arguement
    if (argc != 2)
    {
        run = 1;
    }

    // Checks to make sure that if the user only inputs ONE argument that it's all integers
    if (argc == 2)
    {
        string first = argv[1];
        int counter = 0;
        for (int i = 0; i < strlen(first); i++)
        {
            if (first[i] < 48 || first[i] > 57)
            {
                counter += 1;
            }
        }

        if (counter != 0)
        {
            run = 1;
        }
    }

    // Returns Exit Code 1 if no arguement given
    if (argc == 1)
    {
        return 1;
    }

    //If run is 0, then the user inputted a good key to use. The program can proceed
    if (run == 0)
    {
        int key = atoi(argv[1]);

        // Gets plaintext input from user
        string plaintext = get_string("plaintext: ");

        //Encrypt text
        int n = strlen(plaintext);
        for (int i = 0; i < n; i++)
        {
            if (isalpha(plaintext[i]))
            {
                if (isupper(plaintext[i]))
                {
                    plaintext[i] = 65 + (plaintext[i] - 65 + key) % 26;
                }

                else if (islower(plaintext[i]))
                {
                    plaintext[i] = 97 + (plaintext[i] - 97 + key) % 26;
                }
            }
        }

        //Print ciphertext
        printf("ciphertext: %s\n", plaintext);

    }

    //If the command line arguement was a bad input, print the below message to the user.
    if (run == 1)
    {
        printf("Usage: ./caesar key\n");
    }
}