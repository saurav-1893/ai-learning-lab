import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np


model = LinearRegression()

# Load File

df = pd.read_csv('salary_data.csv')

# Create Model- Define X/y

X = df[['years_experience']]
y = df['salary']

# Split

X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.2, random_state= 3)

#Train - Fit on training data

model.fit(X_train, y_train)

# Predict Training data

# predictions = model.predict(X)

# How well it performs on the training employees

train_predictions = model.predict(X_train)

# How well it performs on the Unseen employees

test_predictions = model.predict(X_test)

# Predict on test data

train_mae = mean_absolute_error(y_train, train_predictions)
test_mae = mean_absolute_error(y_test, test_predictions)

# Split and Evaluate
cv_scores = cross_val_score(
    model,
    X,
    y,
    cv= 5,
    scoring='neg_mean_absolute_error' 
)

normalised_cv_scores = abs(cv_scores)
mean_cv_mae = (normalised_cv_scores).mean()

variation = np.std(normalised_cv_scores)

# Evaluate Both

# print(f'Slope: {model.coef_[0]}')
# print(f'Intercept: {model.intercept_}')

# print(f'Train Mae : {train_mae}')
# print(f'Test Mae : {test_mae}')
print(f'Fold MAEs: {normalised_cv_scores}')
print(f'Mean CV MAE: {mean_cv_mae}')
print(f'Standard deviation: {variation}')