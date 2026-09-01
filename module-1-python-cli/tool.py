import sys
import os
import csv
import numpy as np

def load_csv(filepath):
    with open(filepath) as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)
    return header, rows

def summarize_csv(header, rows):

        missing = {i : 0 for i in header}

        for row in rows:
            for i, val in enumerate(row):
                if val == '':
                    missing[header[i]] +=1
    

        columns = len(header)
        number_of_rows = len(rows)
    
        return columns, number_of_rows, missing

def csv_file_check(args):
    if len(args) < 2:
        return sys.exit('Please provide a CSV file')
    
    validated_file = args[1]
    
    if not os.path.isfile(validated_file):
        return sys.exit('File not found')
    
    return validated_file

def get_command(args):
    if len(args) < 3:
        sys.exit('No command provided')
    if args[2] == '--summary':
        return '--summary'
    if args[2] == '--stats':
        return '--stats'
    if args[2] == '--columns':
        return '--columns'
    if args[2] == '--filter':
        if len(args) < 5:
            sys.exit('Filter metrics not provided')
        return '--filter'
    sys.exit('Invalid command')

def get_stats(header, rows): 
        
        numeric_data = {i : [] for i in header}

        for row in rows:            
            for i, val in enumerate(row):
                try:
                    numeric_data[header[i]].append(float(val))
                    
                except ValueError:
                    pass
        pure_numeric_data = {}    
        for column, value in numeric_data.items():
            if value != []:
                pure_numeric_data[column] = value

        final_stats = {}
        for column , value in pure_numeric_data.items():
            arr = np.array(value, dtype=float)
            final_stats[column] = {
                'count' : len(arr),
                'min' : np.min(arr),
                'max': np.max(arr),
                'mean': np.mean(arr),
                'median': np.median(arr),
                'std' : np.std(arr, ddof=1)
                }
                

        return final_stats

def print_stats(header, rows):
    for column_name , stats in get_stats(header, rows).items():
        print(f'{column_name}')
        for stat_name, stat_value in stats.items():
            print(f'{stat_name} : {stat_value}')

def print_columns(header):
    for i in range(len(header)):
        print(f'{i+1}. {header[i]}')

def get_filter_matches(header, rows, col_name, target_value):
    if col_name not in header:
        return None
        

    col_index = header.index(col_name)
    return [row for row in rows if row[col_index] ==target_value]


def main():
    filepath = csv_file_check(sys.argv)
    command = get_command(sys.argv)
    header, rows = load_csv(filepath)

    if command == '--summary':
        total_columns, total_rows, missing_values = summarize_csv(header, rows)
        print(f'Total columns are : {total_columns}')
        print(f'Total rows are : {total_rows}') 
        print('\nMissing values are:')
        for column_name, missing_count in missing_values.items():
            print(f'{column_name}: {missing_count}')
    
    elif command == '--stats':
        print(f'Stats:')
        print_stats(header, rows)
    elif command == '--columns':
        print(f'Columns:')
        print_columns(header)
    elif command == '--filter':
        matches = get_filter_matches(header, rows, sys.argv[3], sys.argv[4])

        if matches is None:
            print(f'Column: {sys.argv[3]} not found in the dataset')
        elif not matches:
            print('No match found')
        else:
            for match in matches:
                print(match)



if __name__ == '__main__':
    main()       