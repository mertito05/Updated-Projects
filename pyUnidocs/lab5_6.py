# Lab 5 & 6: Multiple Linear Regression, Polynomial Regression, Logistic Regression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

# Task 2: Multiple Linear Regression for Tourist Expenses
print("Task 2: Multiple Linear Regression for Tourist Expenses")
tourist_data = pd.DataFrame({
    'Accommodation': [600, 450, 650, 400, 550, 450, 500, 550, 700, 500],
    'Food': [500, 550, 650, 450, 450, 600, 700, 550, 800, 780],
    'Services': [300, 470, 400, 300, 350, 420, 370, 450, 500, 440],
    'Total': [1420, 1500, 1720, 1170, 1380, 1480, 1600, 1570, 2000, 1730]
})

X_tourist = tourist_data[['Accommodation', 'Food', 'Services']]
y_tourist = tourist_data['Total']

model_tourist = LinearRegression()
model_tourist.fit(X_tourist, y_tourist)

print(f'Coefficients: {model_tourist.coef_}')
print(f'Intercept: {model_tourist.intercept_:.2f}')
print(f'R-squared: {model_tourist.score(X_tourist, y_tourist):.2f}')

# Regression equation
print(f'Regression equation: Total = {model_tourist.intercept_:.2f} + {model_tourist.coef_[0]:.2f}*Accommodation + {model_tourist.coef_[1]:.2f}*Food + {model_tourist.coef_[2]:.2f}*Services')

# Task 3: Multiple Linear Regression for Box Prices
print("\nTask 3: Multiple Linear Regression for Box Prices")
box_data = pd.DataFrame({
    'Length': [7, 10, 8, 9, 10],
    'Width': [5, 4, 5, 5, 6],
    'Height': [5, 5, 5, 5, 5],
    'Price': [6.5, 6.55, 6.31, 5.51, 4.44]
})

X_box = box_data[['Length', 'Width', 'Height']]
y_box = box_data['Price']

model_box = LinearRegression()
model_box.fit(X_box, y_box)

print(f'Coefficients: {model_box.coef_}')
print(f'Intercept: {model_box.intercept_:.2f}')
print(f'R-squared: {model_box.score(X_box, y_box):.2f}')

# Prediction for 7x6x5 box
pred_box = model_box.predict(np.array([[7, 6, 5]]))
print(f'Predicted price for 7x6x5 box: ${pred_box[0]:.2f}')

# Task 4: Polynomial Regression for Advertising Costs and Sales
print("\nTask 4: Polynomial Regression for Advertising Costs and Sales")
ad_data = pd.DataFrame({
    'Cost': [2, 3, 4, 5, 6, 7],
    'Sales': [10, 29, 66, 127, 218, 345]
})

X_ad = ad_data[['Cost']]
y_ad = ad_data['Sales']

# Polynomial features (degree 3 for cubic relationship)
poly = PolynomialFeatures(degree=3)
X_ad_poly = poly.fit_transform(X_ad)

model_ad = LinearRegression()
model_ad.fit(X_ad_poly, y_ad)

print(f'Coefficients: {model_ad.coef_}')
print(f'Intercept: {model_ad.intercept_:.2f}')
print(f'R-squared: {model_ad.score(X_ad_poly, y_ad):.2f}')

# Plot
plt.scatter(X_ad, y_ad, color='blue')
X_plot = np.linspace(2, 7, 100).reshape(-1, 1)
X_plot_poly = poly.transform(X_plot)
plt.plot(X_plot, model_ad.predict(X_plot_poly), color='red')
plt.title('Advertising Cost vs Sales')
plt.xlabel('Cost (€)')
plt.ylabel('Sales (units)')
plt.show()

# Predictions for costs 8, 9, 10
pred_costs = model_ad.predict(poly.transform(np.array([[8], [9], [10]])))
print(f'Predicted sales for €8: {pred_costs[0]:.0f} units')
print(f'Predicted sales for €9: {pred_costs[1]:.0f} units')
print(f'Predicted sales for €10: {pred_costs[2]:.0f} units')

# Task 5: Logistic Regression for Spam Emails
print("\nTask 5: Logistic Regression for Spam Emails")
spam_data = pd.DataFrame({
    'Day': [1, 2, 3, 4, 5, 6, 7],
    'Spam': [2, 4, 4, 5, 6, 7, 8]
})

# Fit logistic curve
from scipy.optimize import curve_fit

def logistic_function(x, A, k, x0):
    return A / (1 + np.exp(-k*(x-x0)))

x_spam = np.array(spam_data['Day'])
y_spam = np.array(spam_data['Spam'])

popt, pcov = curve_fit(logistic_function, x_spam, y_spam)
print(f'Logistic parameters: A={popt[0]:.2f}, k={popt[1]:.2f}, x0={popt[2]:.2f}')

# Plot
plt.scatter(x_spam, y_spam, color='blue')
x_plot = np.linspace(1, 10, 100)
plt.plot(x_plot, logistic_function(x_plot, *popt), color='red')
plt.title('Spam Emails Over Days')
plt.xlabel('Day')
plt.ylabel('Spam Count')
plt.show()

# Prediction for day 10
pred_day10 = logistic_function(10, *popt)
print(f'Predicted spam on day 10: {int(pred_day10)}')

# Task 6: Logistic Regression for Email Classification
print("\nTask 6: Logistic Regression for Email Classification")
email_data = pd.DataFrame({
    'Sender': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'Length': [248, 180, 120, 200, 75, 320, 150, 280, 90],
    'Frequency': [2, 3, 1, 4, 1, 5, 2, 3, 1],
    'Size': [22, 16, 8, 20, 6, 30, 12, 24, 5],
    'Category': ['spam', 'spam', 'non-spam', 'spam', 'non-spam', 'spam', 'non-spam', 'spam', 'non-spam']
})

# Split data
train_data, test_data = train_test_split(email_data, test_size=0.3, random_state=42)

# Train model
X_train = train_data[['Length', 'Frequency', 'Size']]
y_train = train_data['Category']
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Test model
X_test = test_data[['Length', 'Frequency', 'Size']]
y_test = test_data['Category']
y_pred = log_reg.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Predict for new email
new_email = pd.DataFrame({
    'Length': [150],
    'Frequency': [2],
    'Size': [12]
})
pred_category = log_reg.predict(new_email)
print(f'Predicted category for new email: {pred_category[0]}')
