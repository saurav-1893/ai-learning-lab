import pandas as pd

df = pd.read_csv('data-cleansing.csv')

missing_value = df.isna()

missing_count_per_col = df.isna().sum()
missing_value_col = df.columns[missing_value.any()]

rows_with_missing = df[df.isna().any(axis=1)]


duplicate_vals = df.duplicated()
unique_city_names = df['city'].unique()
number_of_unique_cities = len(unique_city_names) # or I could use nununique method 
data_type_of_col = df.dtypes

'''
Challenge: Create a Cleaning Plan

For each issue, tell me what you would do and why.

1. Missing age

Would you:

delete the row?
fill it with the average age?
fill it with the city's average age?
leave it missing?

Why?

- For age I would prefer to have a mean average number assigned to the person as long as their salary column is > 0.

2. Missing salary

Same question.

What's your policy? - for missing salary , it either needs to be 0 or some string which notifies the user that this data needs verification. 

3. Inconsistent city names

How would you standardize them?

Would you use: The city column to be converted in either upper or lower case

all lowercase?
title case?
uppercase?

Why?

4. Impossible age (300)

Do you:

delete the row?
replace with 30?
replace with median age?
flag it for manual review?

What's the engineering trade-off?

5. Duplicate row

Always remove duplicates?

Or are there situations where duplicates are legitimate?

Think about airline bookings, purchases, or sensor readings.

'''


print(df)