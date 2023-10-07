#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)

{

    float change;
    int counter = 0;

    //Get input
    do
    {
     change = get_float("Change owed: ");
    }
    while (change < 0);
    int cents = round(change * 100);

    //Check how many quarters
    do
    {
        if(cents-25 >= 0)
        {
            cents = cents - 25;
            counter = counter + 1;
        }
    }
    while(cents-25 >= 0);

    //Check how many dimes
    do
    {
        if(cents-10 >= 0)
        {
            cents = cents - 10;
            counter = counter + 1;
        }
    }
    while (cents - 10 >= 0);

    //Check how many nickels
    do
    {
        if(cents-5 >= 0)
        {
            cents = cents - 5;
            counter = counter + 1;
        }
    }
    while(cents-5 >= 0);

    //check how many pennies
    do
    {
        if(cents-1 >= 0)
        {
            cents = cents - 1;
            counter = counter + 1;
        }
    }
    while(cents-1 >= 0);

    //Print total count
    printf("%i\n", counter);

}