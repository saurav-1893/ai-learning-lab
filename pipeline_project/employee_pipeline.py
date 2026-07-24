import pandas as pd

df = pd.read_csv('employee_data.csv')

# Inspect data
data_shape = df.shape
data_head = df.head()
# info_data = df.info()

number_of_rows = len(df.index) #also found df.shape[0]
number_of_columns = len(df.columns)#also found df.shape[1]

non_null = df.notnull().sum()

missing_value_mask = df.isna()
null_count_by_column = missing_value_mask.sum()
total_null_values = null_count_by_column.sum()
rows_with_missing_values = df[missing_value_mask.any(axis=1)]
columns_with_missing_values = df.columns[missing_value_mask.any()]

duplicated_rows = df[df.duplicated()]

data_types = df.dtypes

unique_departments = df['department'].unique()
unique_cities = df['city'].unique()

numeric_columns = df.select_dtypes(include='number')

#invalid_values = # Iam yet to decide on policy to start defining In valid values

#Quality Report

quality_report = {
    "rows": number_of_rows,
    "columns": number_of_columns,
    "missing_by_column": null_count_by_column,
    "total_missing": total_null_values,
    "duplicate_rows": duplicated_rows,
    "dtypes": data_types,
    "unique_departments": unique_departments,
    "unique_cities": unique_cities,
    "numeric_columns": numeric_columns.columns.tolist()
}

#Cleaning data 

df['city'] = df['city'].astype(str).str.rstrip().str.capitalize()
df['department'] = df['department'].astype(str).str.rstrip().str.lower()
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
df['start_date'] = pd.to_datetime(df['start_date'], errors= 'coerce')


rows_by_invalid_age = df[(df['age'] < 18) | (df['age'].isna()) | (df['age'] > 100)]
employee_id_by_invalid_age = rows_by_invalid_age['employee_id']

valid_ages = df[df['age'].between(18,100) & df['age'].notna()]
print(quality_report['numeric_columns'])
# print(valid_ages)