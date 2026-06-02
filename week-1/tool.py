import sys
import os
import csv

def summarize_csv(filepath):
    with open(filepath) as file:
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
    

        columns = len(header)
        rows = count
    
        return columns, rows, missing

def csv_file_check(args):
    if len(args) < 2:
        return sys.exit('Please provide a CSV file')
    
    validated_file = args[1]
    
    if not os.path.isfile(validated_file):
        return sys.exit('File not found')
    
    return validated_file



def command_check(args):
    if len(args) < 3:
        sys.exit('No command provided')

    if args[2] != '--summary':
        sys.exit('Invalid command')

filepath = csv_file_check(sys.argv)
command_check(sys.argv)

total_columns, total_rows, missing_values = summarize_csv(filepath)
print(f'Total columns are : {total_columns}')
print(f'Total rows are : {total_rows}')
print('\nMissing values are:')
for i, val in missing_values.items():
    print(f'{i}: {val}')