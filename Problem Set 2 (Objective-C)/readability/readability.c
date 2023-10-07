#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int lexicon(string texty);

int main(void)
{
    // Get text input
    string text = get_string("Text: ");
    int level = lexicon(text);

    //Print out reading grade level
    if (level < 16 && level > 1)
    {
        printf("Grade %i\n", level);
    }

    if (level >= 16)
    {
        printf("Grade 16+\n");
    }

    if (level <= 1)
    {
        printf("Before Grade 1\n");
    }

}

//Write function lexicon that will return reading grade level
int lexicon(string texty)
{
    int n = strlen(texty);

    // TODO: Find word count
    int word_count = 1;
    for (int x = 0; x < n; x++)
    {
        if (texty[x] == ' ')
        {
            word_count += 1;
        }
    }

    //TODO: Find letter count
    int letter_count = 0;
    for (int i = 0; i < n; i++)
    {
        if ((int)texty[i] <= 90 && (int)texty[i] >= 65)
        {
            letter_count += 1;
        }

        else if ((int)texty[i] <= 122 && (int)texty[i] >= 97)
        {
            letter_count += 1;
        }

    }

    //TODO: Find sentence count
    int sentence_count = 0;
    for (int y = 0; y < n; y++)
    {
        if (texty[y] == '.')
        {
            sentence_count += 1;
        }

        if (texty[y] == '!')
        {
            sentence_count += 1;
        }

        if (texty[y] == '?')
        {
            sentence_count += 1;
        }
    }

    //TODO: Find index value and return it
    float L = ((float)letter_count / (float)word_count) * 100;
    float S = ((float)sentence_count / (float)word_count) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int indices = round(index);

    //Return Index from function
    return indices;

}