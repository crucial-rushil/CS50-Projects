#include <cs50.h>
#include <stdio.h>

int main(void){

    int height;

    do
    {
     height = get_int("Height: ");
    }
    while (height<1 || height > 8);

    for (int a = 1; a <= height; a++)
    {
         for(int x=0; x < height-a; x++)
         {
             printf(" ");
         }

         for (int b = 0; b < a; b++)
          {
              printf("#");
          }

          printf("\n");
    }
}