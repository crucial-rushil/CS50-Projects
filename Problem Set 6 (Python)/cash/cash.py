from cs50 import get_float

counter = 0
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

change = round(change*100,2)

while True:
    if change-25 >= 0:
        change = change - 25
        counter = counter + 1

    else:
        break

while True:
    if change-10 >= 0:
        change = change - 10
        counter = counter + 1

    else:
        break

while True:
    if change-5 >= 0:
        change = change - 5
        counter = counter + 1

    else:
        break

while True:
    if change-1 >= 0:
        change = change - 1
        counter = counter + 1

    else:
        break

print(counter)