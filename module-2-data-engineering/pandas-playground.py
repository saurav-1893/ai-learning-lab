import pandas as pd

df = pd.read_csv('pandas-data.csv')

# print(df)
# print(df['name'])
# print(df[['name', 'age']])

# print(df['city'] =='Oxford')
# grouped = df[(df['city'] == 'Oxford') & (df['age'] ==30)]
# print(grouped[['name', 'city']])

# print((df['city']).value_counts())

mean_age_by_city = df.groupby('city')['age'].mean()
avg_salary_by_city = df.groupby('city')['salary'].mean()

highest_avg_salary = avg_salary_by_city.max()
city_with_highest_avg_salary = avg_salary_by_city.idxmax()
residents_of_city = df.groupby('city')['name'].count()
city_counts = df.groupby('city')['name'].size()
city_over_2_residents = residents_of_city[residents_of_city > 2]


# print(city_counts)
print(city_over_2_residents)