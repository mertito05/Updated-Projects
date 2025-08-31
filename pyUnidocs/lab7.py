# Lab 7: Data Visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Task 1: Bar chart for monthly sales
print("Task 1: Bar Chart for Monthly Sales")
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales = [1000, 1200, 900, 1500, 1800, 1600]

plt.figure(figsize=(10, 6))
plt.bar(months, sales, color='skyblue')
plt.title('Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.show()

# Task 2: Line chart for temperature over time
print("\nTask 2: Line Chart for Temperature Over Time")
days = list(range(1, 31))
temperature = [20 + 5*np.sin(2*np.pi*i/30) + np.random.normal(0, 2) for i in days]

plt.figure(figsize=(10, 6))
plt.plot(days, temperature, marker='o', linestyle='-', color='red')
plt.title('Daily Temperature Over 30 Days')
plt.xlabel('Day')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()

# Task 3: Scatter plot for height vs weight
print("\nTask 3: Scatter Plot for Height vs Weight")
np.random.seed(42)
height = np.random.normal(170, 10, 100)
weight = 0.5 * height + np.random.normal(0, 5, 100)

plt.figure(figsize=(10, 6))
plt.scatter(height, weight, alpha=0.7, color='green')
plt.title('Height vs Weight')
plt.xlabel('Height (cm)')
plt.ylabel('Weight (kg)')
plt.show()

# Task 4: Pie chart for market share
print("\nTask 4: Pie Chart for Market Share")
companies = ['Company A', 'Company B', 'Company C', 'Company D']
market_share = [35, 25, 20, 20]

plt.figure(figsize=(8, 8))
plt.pie(market_share, labels=companies, autopct='%1.1f%%', startangle=90)
plt.title('Market Share Distribution')
plt.axis('equal')
plt.show()

# Task 5: Histogram for exam scores
print("\nTask 5: Histogram for Exam Scores")
np.random.seed(42)
scores = np.random.normal(75, 15, 200)

plt.figure(figsize=(10, 6))
plt.hist(scores, bins=20, edgecolor='black', alpha=0.7)
plt.title('Distribution of Exam Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.show()

# Task 6: Box plot for different groups
print("\nTask 6: Box Plot for Different Groups")
np.random.seed(42)
group1 = np.random.normal(70, 10, 50)
group2 = np.random.normal(75, 12, 50)
group3 = np.random.normal(80, 8, 50)

data = [group1, group2, group3]
labels = ['Group 1', 'Group 2', 'Group 3']

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=labels)
plt.title('Box Plot of Different Groups')
plt.ylabel('Values')
plt.show()

# Task 7: Heatmap for correlation matrix
print("\nTask 7: Heatmap for Correlation Matrix")
np.random.seed(42)
data = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100),
    'C': np.random.randn(100),
    'D': np.random.randn(100)
})

correlation_matrix = data.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix Heatmap')
plt.show()

# Task 8: Subplots
print("\nTask 8: Subplots")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Subplot 1: Bar chart
axes[0, 0].bar(months, sales, color='skyblue')
axes[0, 0].set_title('Monthly Sales')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Sales ($)')

# Subplot 2: Line chart
axes[0, 1].plot(days[:10], temperature[:10], marker='o', linestyle='-', color='red')
axes[0, 1].set_title('Temperature (First 10 Days)')
axes[0, 1].set_xlabel('Day')
axes[0, 1].set_ylabel('Temperature (°C)')
axes[0, 1].grid(True)

# Subplot 3: Scatter plot
axes[1, 0].scatter(height[:50], weight[:50], alpha=0.7, color='green')
axes[1, 0].set_title('Height vs Weight (Sample)')
axes[1, 0].set_xlabel('Height (cm)')
axes[1, 0].set_ylabel('Weight (kg)')

# Subplot 4: Histogram
axes[1, 1].hist(scores, bins=15, edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Exam Scores Distribution')
axes[1, 1].set_xlabel('Score')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
