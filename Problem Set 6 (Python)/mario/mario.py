from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(1,height+1,1):

    for z in range(0,height-i,1):
        print(" ", end ="")

    for x in range(0,i,1):
        print("#", end ="")

    print("\n",end="")