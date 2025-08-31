# Lab 4: Linear Regression

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Task 3: Linear regression for shopping data
print("Task 3: Linear Regression for Shopping Data")
shopping_data = pd.DataFrame({
    'x': [5, 7, 10, 15, 20, 25],  # time in minutes
    'y': [8, 10, 13, 18, 22, 25]  # money spent
})

X = shopping_data[['x']]
y = shopping_data['y']

model = LinearRegression()
model.fit(X, y)

print(f'Coefficient: {model.coef_[0]:.2f}')
print(f'Intercept: {model.intercept_:.2f}')
print(f'R-squared: {model.score(X, y):.2f}')

# Plot
plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(X), color='red')
plt.title('Shopping Time vs Money Spent')
plt.xlabel('Time (minutes)')
plt.ylabel('Money Spent ($)')
plt.show()

# Prediction for 12 minutes
import numpy as np

pred_12 = model.predict(np.array([[12]]))
print(f'Predicted spending for 12 minutes: ${pred_12[0]:.2f}')

# Task 4: Linear regression for house prices (DataFrame version)
print("\nTask 4a: Linear Regression for House Prices (DataFrame)")
house_data = pd.DataFrame({
    'Area': [45, 60, 65, 70, 80, 100],
    'Price': [50000, 80000, 92000, 99000, 110000, 160000]
})

X_house = house_data[['Area']]
y_house = house_data['Price']

model_house = LinearRegression()
model_house.fit(X_house, y_house)

print(f'Coefficient: {model_house.coef_[0]:.2f}')
print(f'Intercept: {model_house.intercept_:.2f}')
print(f'R-squared: {model_house.score(X_house, y_house):.2f}')

# Plot
plt.scatter(X_house, y_house, color='blue')
plt.plot(X_house, model_house.predict(X_house), color='red')
plt.title('House Area vs Price')
plt.xlabel('Area (sq m)')
plt.ylabel('Price (€)')
plt.show()

# Prediction for 75 sq m
pred_75 = model_house.predict(np.array([[75]]))
print(f'Predicted price for 75 sq m: €{pred_75[0]:.2f}')

# Task 4b: CSV version (simulated)
print("\nTask 4b: Linear Regression for House Prices (CSV simulation)")
# In real scenario, you would read from CSV
# house_data_csv = pd.read_csv('houses_prices.csv', sep=';')
# But since we don't have the file, we'll use the same data
X_house_csv = house_data[['Area']]
y_house_csv = house_data['Price']

model_house_csv = LinearRegression()
model_house_csv.fit(X_house_csv, y_house_csv)

print(f'Coefficient: {model_house_csv.coef_[0]:.2f}')
print(f'Intercept: {model_house_csv.intercept_:.2f}')
print(f'R-squared: {model_house_csv.score(X_house_csv, y_house_csv):.2f}')

pred_75_csv = model_house_csv.predict(np.array([[75]]))
print(f'Predicted price for 75 sq m: €{pred_75_csv[0]:.2f}')
