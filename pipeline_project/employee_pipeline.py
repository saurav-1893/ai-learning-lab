import pandas as pd

df = pd.read_csv('employee_data.csv')


# info_data = df.info()

null_count = df - [df.notnull().sum()]

number_of_rows = len(df.index)
number_of_columns = len(df.columns)

missing_value_mask = df.isna()
rows_with_missing_values = df[missing_value_mask.any(axis=1)]
columns_with_missing_values = df.columns[missing_value_mask.any()]

duplicated_rows = df[df.duplicated()]

data_types = df.dtypes

unique_departments = df['department'].unique()
unique_cities = df['city'].unique()

# numeric_columns = df.columns.
print(null_count)
#print(df)