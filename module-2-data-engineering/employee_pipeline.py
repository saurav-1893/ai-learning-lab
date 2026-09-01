import pandas as pd
import sys
import os

#  LOAD DATA

def csv_file_check(args):
    if len(args) < 2:
        sys.exit('No CSV provided')

    validated_file = args[1]

    if not os.path.isfile(validated_file):
        sys.exit('File not found')

    return validated_file

def get_command(args):
    if len(args) < 3:
        sys.exit('No command provided.')
    given_command = args[2]

    acceptable_commands = ('quality_report', 'cleaned_data', 'summary', 'export_data')

    if given_command not in acceptable_commands:
        sys.exit('Command not recognized')

    return given_command

def get_metric(args):
    if len(args) < 4:
        sys.exit('No Quality Metric Provided')
    
    return args[3]    

def load_csv_file(filepath):
    df = pd.read_csv(filepath)

    return df

#  INSPECT DATA

def inspect_data(df):
    # data_shape = df.shape
    # data_head = df.head()
    # info_data = df.info()

    number_of_rows = len(df.index) #also found df.shape[0]
    number_of_columns = len(df.columns)#also found df.shape[1]
    
    missing_value_mask = df.isna()
    null_count_by_column = missing_value_mask.sum()
    total_null_values = null_count_by_column.sum()

    
    duplicated_rows = df[df.duplicated()]
    duplicate_employee_ids = df[df['employee_id'].duplicated(keep = False)]
    data_types = df.dtypes
    
    numeric_columns = df.select_dtypes(include='number')

#  QUALITY REPORT

    quality_report = {
        "rows": int(number_of_rows),
        "columns": int(number_of_columns),
        "missing_by_column": null_count_by_column.to_dict(),
        "total_missing": int(total_null_values),
        "duplicate_rows": int(len(duplicated_rows)),
        "duplicate_employee_ids" : duplicate_employee_ids.sort_values('employee_id') ,
        "dtypes": data_types.astype(str).to_dict(),
        "unique_departments": df['department'].dropna().unique().tolist(),
        "unique_cities": df['city'].dropna().unique().tolist(),
        "numeric_columns": numeric_columns.columns.tolist()
    }

    return quality_report

def get_quality_metric(quality_metric, quality_report):

    if quality_metric not in quality_report:
        sys.exit('Quality Metric Invalid')

    return quality_report[quality_metric]

#  CLEANING DATA

def clean_data(df):
    cleaned_df = df.copy()
    cleaned_df['city'] = cleaned_df['city'].astype('string').str.strip().str.upper()
    cleaned_df['department'] = cleaned_df['department'].astype('string').str.strip().str.lower()
    cleaned_df['salary'] = pd.to_numeric(cleaned_df['salary'], errors='coerce')
    cleaned_df['start_date'] = pd.to_datetime(cleaned_df['start_date'], errors= 'coerce')


    valid_age_mask = (cleaned_df['age'].between(18,100)) & (cleaned_df['age'].notna())
    
    invalid_age_mask= (~valid_age_mask)
    
    median_age = cleaned_df.loc[valid_age_mask, 'age'].median()
    cleaned_df.loc[invalid_age_mask, 'age'] = median_age


    cleaned_df['start_flag'] = 'OK'
    cleaned_df.loc[cleaned_df['start_date'].isna(), 'start_flag'] = 'Need Reviewing'

    salary_missing_mask = cleaned_df['salary'].isna()
    salary_negative_mask = cleaned_df['salary'] < 0
    invalid_salary_mask = (salary_missing_mask) | (salary_negative_mask)
    valid_salary_mask = ~invalid_salary_mask
    
    cleaned_df['salary_flag'] = 'OK'
    cleaned_df.loc[(salary_missing_mask) | (salary_negative_mask), 'salary_flag'] = 'Need Reviewing'
    
    invalid_department_mask = cleaned_df['department'].isna()
    
    cleaned_df['department_flag'] = 'OK'
    cleaned_df.loc[invalid_department_mask, 'department_flag'] = 'Needs Reviewing'


    cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df


# SUMMARY

def summarize_data(cleaned_df):

    average_salary_by_department = cleaned_df.groupby('department')['salary'].mean().sort_values(ascending=False)
    employee_count_by_department = cleaned_df.groupby('department')['employee_id'].count()
    average_age_by_city = cleaned_df.groupby('city')['age'].mean()
    highest_salary_by_department = cleaned_df.groupby('department')['salary'].max()
    highest_paying_department = highest_salary_by_department.idxmax()

    summary_of_dataset ={
        'average_salary_by_department' : average_salary_by_department,
        'employee_count_by_department' : employee_count_by_department,
        'average_age_by_city' : average_age_by_city,
        'highest_salary_by_department' : highest_salary_by_department,
        'highest_paying_department' : highest_paying_department
        }
    
    return summary_of_dataset

#  SAVE CLEANED DATASET / EXPORT

def export_data(cleaned_df):
    new_filepath = 'clean_employee_data.csv'
    cleaned_df.to_csv(new_filepath, index = False)

    return new_filepath

# MAIN

def main():

    filepath = csv_file_check(sys.argv)
    df = load_csv_file(filepath)
    user_command = get_command(sys.argv)

    if user_command == 'quality_report':
        quality_metric_requested = get_metric(sys.argv)
        quality_report = inspect_data(df)
        print(get_quality_metric(quality_metric_requested,quality_report))
    elif user_command == 'cleaned_data':
        cleaned_data = clean_data(df)
        print(cleaned_data)
    elif user_command == 'summary':
        cleaned_data = clean_data(df)
        print(summarize_data(cleaned_data))
    elif user_command == 'export_data':
        cleaned_data = clean_data(df)
        new_filepath = export_data(cleaned_data)
        print(f'Cleaned dataset exported to {new_filepath}')
    

if __name__ == '__main__':
    main()