#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float current_Red = image[i][j].rgbtRed;
            float current_Green = image[i][j].rgbtGreen;
            float current_Blue = image[i][j].rgbtBlue;

            float mean_RGB = round((current_Red + current_Green + current_Blue) / 3);

            image[i][j].rgbtRed = mean_RGB;
            image[i][j].rgbtGreen = mean_RGB;
            image[i][j].rgbtBlue = mean_RGB;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float current_Red = image[i][j].rgbtRed;
            float current_Green = image[i][j].rgbtGreen;
            float current_Blue = image[i][j].rgbtBlue;

            float sepia_Red = round((0.393 * current_Red) + (0.769 * current_Green) + (0.189 * current_Blue));
            float sepia_Green = round((0.349 * current_Red) + (0.686 * current_Green) + (0.168 * current_Blue));
            float sepia_Blue = round((0.272 * current_Red) + (0.534 * current_Green) + (0.131 * current_Blue));

            if (sepia_Red > 255)
            {
                sepia_Red = 255;
            }

            if (sepia_Green > 255)
            {
                sepia_Green = 255;
            }

            if (sepia_Blue > 255)
            {
                sepia_Blue = 255;
            }

            //assign values
            image[i][j].rgbtRed = sepia_Red;
            image[i][j].rgbtGreen = sepia_Green;
            image[i][j].rgbtBlue = sepia_Blue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //make a copy of the image
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    //assign the image the values of the copy in reverse order
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int x = width - 1 - j;
            image[i][j] = copy[i][x];
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    //make a copy to store changes
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red_total = 0;
            float green_total = 0;
            float blue_total = 0;
            float counter = 0;

            //top row left
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red_total += image[i - 1][j - 1].rgbtRed;
                green_total += image[i - 1][j - 1].rgbtGreen;
                blue_total += image[i - 1][j - 1 ].rgbtBlue;
                counter += 1;
            }

            //top row center
            if (i - 1 >= 0)
            {
                red_total += image[i - 1][j].rgbtRed;
                green_total += image[i - 1][j].rgbtGreen;
                blue_total += image[i - 1][j].rgbtBlue;
                counter += 1;
            }

            //top row right
            if (i - 1 >= 0 && j + 1 < width)
            {
                red_total += image[i - 1][j + 1].rgbtRed;
                green_total += image[i - 1][j + 1].rgbtGreen;
                blue_total += image[i - 1][j + 1].rgbtBlue;
                counter += 1;
            }

            //one to the left
            if (j - 1 >= 0)
            {
                red_total += image[i][j - 1].rgbtRed;
                green_total += image[i][j - 1].rgbtGreen;
                blue_total += image[i][j - 1].rgbtBlue;
                counter += 1;
            }

            //CENTER
            red_total += image[i][j].rgbtRed;
            green_total += image[i][j].rgbtGreen;
            blue_total += image[i][j].rgbtBlue;
            counter += 1;

            //one to the right
            if (j + 1 < width)
            {
                red_total += image[i][j + 1].rgbtRed;
                green_total += image[i][j + 1].rgbtGreen;
                blue_total += image[i][j + 1].rgbtBlue;
                counter += 1;
            }

            //bottom row left
            if (i + 1 < height && j - 1 >= 0)
            {
                red_total += image[i + 1][j - 1].rgbtRed;
                green_total += image[i + 1][j - 1].rgbtGreen;
                blue_total += image[i + 1][j - 1].rgbtBlue;
                counter += 1;
            }

            //bottom row center
            if (i + 1 < height)
            {
                red_total += image[i + 1][j].rgbtRed;
                green_total += image[i + 1][j].rgbtGreen;
                blue_total += image[i + 1][j].rgbtBlue;
                counter += 1;
            }


            //bottom row right
            if (i + 1 < height && j + 1 < width)
            {
                red_total += image[i + 1][j + 1].rgbtRed;
                green_total += image[i + 1][j + 1].rgbtGreen;
                blue_total += image[i + 1][j + 1].rgbtBlue;
                counter += 1;
            }


            //computer averages
            float red_average = round(red_total / counter);
            float green_average = round(green_total / counter);
            float blue_average = round(blue_total / counter);


            copy[i][j].rgbtRed = red_average;
            copy[i][j].rgbtGreen = green_average;
            copy[i][j].rgbtBlue = blue_average;

            red_total = 0;
            green_total = 0;
            blue_total = 0;
            counter = 0;
        }
    }

    //assign values from copy to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
}