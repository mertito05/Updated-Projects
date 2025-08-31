import json
import os

EXPENSE_FILE = "expenses.json"

def load_expenses():
    """Load expenses from JSON file"""
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file, indent=2)

def add_expense(expenses, amount, category, description):
    """Add a new expense"""
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense #{expense['id']} added successfully!")

def view_expenses(expenses):
    """View all expenses"""
    if not expenses:
        print("No expenses found!")
        return
    
    print("\nYour Expenses:")
    print("-" * 50)
    for expense in expenses:
        print(f"Expense #{expense['id']}: ${expense['amount']} - {expense['category']}")
        print(f"Description: {expense['description']}")
        print("-" * 50)

def delete_expense(expenses, expense_id):
    """Delete a specific expense"""
    for i, expense in enumerate(expenses):
        if expense['id'] == expense_id:
            removed = expenses.pop(i)
            # Reindex remaining expenses
            for j, remaining_expense in enumerate(expenses[i:], i):
                remaining_expense['id'] = j + 1
            save_expenses(expenses)
            print(f"Expense #{expense_id} deleted successfully!")
            return
    
    print(f"Expense #{expense_id} not found!")

def main():
    expenses = load_expenses()
    
    print("Expense Tracker Application")
    print("==========================")
    
    while True:
        print("\nOptions:")
        print("1. Add new expense")
        print("2. View all expenses")
        print("3. Delete expense")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            try:
                amount = float(input("Enter expense amount: "))
                category = input("Enter expense category: ").strip()
                description = input("Enter expense description: ").strip()
                add_expense(expenses, amount, category, description)
            except ValueError:
                print("Please enter a valid amount!")
        
        elif choice == "2":
            view_expenses(expenses)
        
        elif choice == "3":
            view_expenses(expenses)
            try:
                expense_id = int(input("Enter expense number to delete: ").strip())
                delete_expense(expenses, expense_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "4":
            print("Goodbye! Your expenses have been saved.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
