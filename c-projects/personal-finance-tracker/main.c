#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TRANSACTIONS 100
#define MAX_DESCRIPTION 100

typedef struct {
    int id;
    char description[MAX_DESCRIPTION];
    float amount;
    int type; // 0 = expense, 1 = income
    char date[11]; // YYYY-MM-DD format
} Transaction;

Transaction transactions[MAX_TRANSACTIONS];
int transaction_count = 0;

void add_transaction() {
    if (transaction_count >= MAX_TRANSACTIONS) {
        printf("Transaction limit reached!\n");
        return;
    }
    
    Transaction new_transaction;
    new_transaction.id = transaction_count + 1;
    
    printf("Enter description: ");
    scanf(" %[^\n]", new_transaction.description);
    
    printf("Enter amount: ");
    scanf("%f", &new_transaction.amount);
    
    printf("Enter type (0 for expense, 1 for income): ");
    scanf("%d", &new_transaction.type);
    
    printf("Enter date (YYYY-MM-DD): ");
    scanf("%s", new_transaction.date);
    
    transactions[transaction_count] = new_transaction;
    transaction_count++;
    printf("Transaction added successfully!\n");
}

void display_summary() {
    if (transaction_count == 0) {
        printf("No transactions recorded.\n");
        return;
    }
    
    float total_income = 0;
    float total_expenses = 0;
    
    printf("\n=== Financial Summary ===\n");
    printf("ID\tDate\t\tType\t\tAmount\tDescription\n");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < transaction_count; i++) {
        printf("%d\t%s\t%s\t$%.2f\t%s\n",
               transactions[i].id,
               transactions[i].date,
               transactions[i].type ? "Income" : "Expense",
               transactions[i].amount,
               transactions[i].description);
        
        if (transactions[i].type) {
            total_income += transactions[i].amount;
        } else {
            total_expenses += transactions[i].amount;
        }
    }
    
    printf("\n=== Totals ===\n");
    printf("Total Income: $%.2f\n", total_income);
    printf("Total Expenses: $%.2f\n", total_expenses);
    printf("Net Balance: $%.2f\n", total_income - total_expenses);
}

void display_balance() {
    float total_income = 0;
    float total_expenses = 0;
    
    for (int i = 0; i < transaction_count; i++) {
        if (transactions[i].type) {
            total_income += transactions[i].amount;
        } else {
            total_expenses += transactions[i].amount;
        }
    }
    
    printf("\nCurrent Balance: $%.2f\n", total_income - total_expenses);
}

int main() {
    int choice;
    
    printf("=== Personal Finance Tracker ===\n");
    
    while (1) {
        printf("\nMenu:\n");
        printf("1. Add Transaction\n");
        printf("2. Display Summary\n");
        printf("3. Show Current Balance\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                add_transaction();
                break;
            case 2:
                display_summary();
                break;
            case 3:
                display_balance();
                break;
            case 4:
                printf("Goodbye! Keep tracking your finances!\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
