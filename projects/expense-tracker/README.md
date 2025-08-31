# Expense Tracker

A command-line expense tracking application that helps you monitor your spending habits.

## Features
- Add expenses with amount, category, and optional description
- View all expenses with timestamps
- View expenses grouped by category
- Generate comprehensive expense reports
- Persistent storage using JSON file

## How to Run
```bash
python main.py
```

## Usage
1. **Add Expense**: Enter amount, category, and optional description
2. **View All Expenses**: See all expenses with dates and totals
3. **View by Category**: See spending breakdown by category
4. **Generate Report**: Get a comprehensive report with percentages and totals

## Data Storage
Expenses are stored in `expenses.json` with the following structure:
- Date and time of expense
- Amount spent
- Category (e.g., Food, Transportation, Entertainment)
- Optional description

## Report Features
- Total expenses
- Breakdown by category with percentages
- Number of expenses recorded

## Note
This application can be extended with features like:
- Monthly/yearly reports
- Budget setting and alerts
- Data visualization
- Export to CSV/Excel
