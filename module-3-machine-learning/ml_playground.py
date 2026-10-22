import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import numpy as np

df = pd.read_csv('ml_playground_data.csv')

model = LinearRegression()

numeric_features = ['years_experience', 'performance_score']
categorical_features = ['department']

preprocessor = ColumnTransformer(
    transformers= [
        (
            'categorical', 
            OneHotEncoder(handle_unknown='ignore'), 
            categorical_features
            )
            ], 
            remainder='passthrough')

pipeline = Pipeline(
    steps=[
        ('preprocessor',preprocessor),
        ('model', model)
        ]
    )
# encoded = pd.get_dummies(df, columns= ['department'], dtype= int)
X = df[
    ['years_experience', 'performance_score', 'department']
]

y = df['salary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# T_X= preprocessor.fit_transform(X)

pipeline.fit(X_train, y_train)

# prediction = pipeline.predict(X_test)
# mae = mean_absolute_error(y_test, prediction)

feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

coefficients = pipeline.named_steps['model'].coef_
intercpet = pipeline.named_steps['model'].intercept_
test= np.array([1,0,0,5,8])

manual_prediction = np.sum(test*coefficients) + intercpet

new_employee = pd.DataFrame({
    'years_experience': [5],
    'performance_score': [8],
    'department': ['Engineering']
})

sklearn_prediction = pipeline.predict(new_employee)

# print(f'Actual: {y_test[1]}')
# print(f'Predicted: {prediction}')
# print(f'MAE: {mae}')
# print(encoded.shape)
# print(feature_names)
# print(coefficients)
# print(intercpet)
# print(manual_prediction)
# print(sklearn_prediction)



# more playground

df = pd.DataFrame({
    'close': [1.1200, 1.1250, 1.1300, 1.1350, 1.1400],
    'volume': [1000, 2000, 3000, 4000, 5000]
})

scaler = StandardScaler()

scaled_values = scaler.fit_transform(df)

scaled_df = pd.DataFrame(
    scaled_values,
    columns=df.columns
)

print("Original:")
print(df)
print("Scaled:")
print(scaled_df)