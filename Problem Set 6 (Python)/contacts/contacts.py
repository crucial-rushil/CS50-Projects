import csv
import sys
import random

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    database = []
    # TODO: Read databases into memory from file
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)

    #TODO: Write into a new CSV file
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = ['email', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writecolumn({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
