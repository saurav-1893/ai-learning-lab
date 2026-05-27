import sys
import os
import csv

if len(sys.argv) < 2:
    sys.exit('Please provide a CSV file')
    
elif not os.path.isfile(sys.argv[1]):
    sys.exit('File not found')

with open(sys.argv[1]) as file:
    reader = csv.reader(file)
    header = next(reader)

    missing = {}
    for i in header:
        missing[i] = 0

    count = 0

    for row in reader:
        count +=1
        for i, val in enumerate(row):
            if val == '':
                missing[header[i]] +=1
        # print(row)
    print(f'Number of columns : {len(header)}')
    print(f'Number of rows : {count}')
    print(missing)