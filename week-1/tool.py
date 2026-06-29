import sys
import os
import csv

def load_csv(filepath):
    with open(filepath) as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)
    return header, rows

def summarize_csv(filepath):
        header, rows = load_csv(filepath)

        missing = {}
        for i in header:
            missing[i] = 0

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
    sys.exit('Invalid command')

def get_stats(filepath):
        header, rows = load_csv(filepath)
 
        numeric_data = {}
        for i in header:
            numeric_data[i] = []

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
            x = {'count': len(value), 'min': min(value), 'max': max(value), 'mean': sum(value)/len(value)}
            final_stats[column] = x
                

        return final_stats

def print_stats(filepath):
    for column_name , stats in get_stats(filepath).items():
        print(f'{column_name}')
        for stat_name, stat_value in stats.items():
            print(f'{stat_name} : {stat_value}')

def print_columns(filepath):
    header, _ = load_csv(filepath)
    for i in range(len(header)):
        print(f'{i+1}. {header[i]}')






def main():
    filepath = csv_file_check(sys.argv)
    command = get_command(sys.argv)

    if command == '--summary':
        total_columns, total_rows, missing_values = summarize_csv(filepath)
        print(f'Total columns are : {total_columns}')
        print(f'Total rows are : {total_rows}') 
        print('\nMissing values are:')
        for column_name, missing_count in missing_values.items():
            print(f'{column_name}: {missing_count}')
    
    elif command == '--stats':
        print(f'Stats:')
        print_stats(filepath)
    elif command == '--columns':
        print(f'Columns:')
        print_columns(filepath)


if __name__ == '__main__':
    main()       