#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    //OpenDaFile
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Failed to open.\n");
        return 1;
    }

    //create buffer & pointer
    int pic_count = 0;
    BYTE buffer[512];
    char filename[8];
    FILE *img = 0;

    //read the file into buffer
    while (fread(&buffer, sizeof(BYTE), 512, file))
    {

        //if the first pic
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && pic_count == 0)
        {
            sprintf(filename, "%03i.jpg", pic_count);
            img = fopen(filename, "w");
            fwrite(&buffer, sizeof(BYTE), 512, img);
            pic_count += 1;
        }

        //for any other pic
        else if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && pic_count != 0)
        {
            fclose(img);
            sprintf(filename, "%03i.jpg", pic_count);
            img = fopen(filename, "w");
            fwrite(&buffer, sizeof(BYTE), 512, img);
            pic_count += 1;
        }

        //checks to see if blocks still from same img
        else if (img != 0)
        {
            fwrite(&buffer, sizeof(BYTE), 512, img);
        }
    }

    //close file
    fclose(file);
    return 0;

}