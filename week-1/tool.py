import sys
import os
import csv

if len(sys.argv) < 2:
    sys.exit('Please provide a CSV file')
    
elif not os.path.isfile(sys.argv[1]):
    sys.exit('File not found')

if len(sys.argv) < 3:
    sys.exit('No command provided')

if sys.argv[2] != '--summary':
    sys.exit('Invalid command')

else:
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
    

        print(f'Number of columns : {len(header)}')
        print(f'Number of rows : {count}')
    
        print('Missing values are:')
        for i, val in missing.items():
            print(f'{i} : {val}')