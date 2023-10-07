import csv
import sys
import random

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python tournament.py FILENAME")

    database = []
    # TODO: Read databases into memory from file
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)

    #TODO: Read the length of each & each key itself
    keys = []
    for x in database[0]:
        keys.append(x)
    keys = keys[1:] #change to 1 later after debugging

    #dna = []
    counts = []
    counter = 0
    # TODO: Read DNA into memory from file (open the sequences file)
    with open(sys.argv[2]) as f:
        sequence = f.read()
        #TODO: splice it per the length of each key & compare to that key
        for z in keys:
            counter = 0
            #print(z)
            checker = z
            checker_len = len(z)
            #print(checker_len)

            #TODO: splice the DNA and get streaks
            streak = 1
            high_streak = 1
            for idx, i in enumerate(sequence):
                r = idx + checker_len
                element = sequence[idx:r]

                if element == sequence[r:r+checker_len] and element == z:
                    r = r + checker_len
                    streak = streak + 1

                    while True:
                        if element == sequence[r:r+checker_len] and element == z:
                            streak = streak + 1
                            r = r + checker_len

                        elif element != sequence[r:r+checker_len]:
                            if streak > high_streak:
                                high_streak = streak
                                streak = 1
                                break
                            else:
                                streak = 1
                                break

            counts.append(str(high_streak))

    #print(counts)

    omega = 0
    zeta = 0
    match = False
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        #next(reader)
        for row in reader:
            zeta = 0
            for x in keys:
                value = row[x]
                if value == counts[omega]:
                    zeta = zeta + 1

                omega = omega + 1

            if zeta == len(counts):
                print(row["name"])
                match = True
                break
            omega = 0

    if match == False:
        print("No match")
    #TODO: compare the counts with the database




                #print(element)
               # dna.append(element)

            #Check the sequence of DNA
            #for idz, y in enumerate(dna):

                #increment = idz+1
                #if idz == len(dna) - 1:
                    #counter = streak
                    #streak = 0
                    #break

                #elif y == dna[increment] and y == checker and dna[increment] == checker:
                    #streak = streak + 1


                #elif y != dna[increment] and y != checker and dna[increment] != checker:
                    #counter = streak
                    #streak = 0

            #Append to a counter array
            #counts.append(counter)




main()
# tasks:
# read the database thingies as a dict (complete)
# read the length of each key & each key (complete)
# open the sequences file (complete)
# splice it per the length of each key & compare to that key (complete)
# keep a counter (complete)
# compare to the original database (complete)
# return value if True else say not found (complete)

#use enumerate() for the indices