#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 100
#define MAX_NAME_LENGTH 50

typedef struct {
    int id;
    char name[MAX_NAME_LENGTH];
    int quantity;
    float price;
} Item;

Item inventory[MAX_ITEMS];
int item_count = 0;

void add_item() {
    if (item_count >= MAX_ITEMS) {
        printf("Inventory is full!\n");
        return;
    }
    
    Item new_item;
    new_item.id = item_count + 1;
    
    printf("Enter item name: ");
    scanf("%s", new_item.name);
    printf("Enter quantity: ");
    scanf("%d", &new_item.quantity);
    printf("Enter price: ");
    scanf("%f", &new_item.price);
    
    inventory[item_count] = new_item;
    item_count++;
    printf("Item added successfully!\n");
}

void display_items() {
    if (item_count == 0) {
        printf("No items in inventory.\n");
        return;
    }
    
    printf("\n=== Inventory ===\n");
    printf("ID\tName\t\tQuantity\tPrice\n");
    printf("--------------------------------------------\n");
    
    for (int i = 0; i < item_count; i++) {
        printf("%d\t%s\t\t%d\t\t$%.2f\n", 
               inventory[i].id, 
               inventory[i].name, 
               inventory[i].quantity, 
               inventory[i].price);
    }
}

void search_item() {
    char search_name[MAX_NAME_LENGTH];
    printf("Enter item name to search: ");
    scanf("%s", search_name);
    
    int found = 0;
    for (int i = 0; i < item_count; i++) {
        if (strcmp(inventory[i].name, search_name) == 0) {
            printf("Item found:\n");
            printf("ID: %d, Name: %s, Quantity: %d, Price: $%.2f\n",
                   inventory[i].id, inventory[i].name, 
                   inventory[i].quantity, inventory[i].price);
            found = 1;
            break;
        }
    }
    
    if (!found) {
        printf("Item not found.\n");
    }
}

void update_item() {
    int id;
    printf("Enter item ID to update: ");
    scanf("%d", &id);
    
    if (id < 1 || id > item_count) {
        printf("Invalid ID.\n");
        return;
    }
    
    printf("Enter new quantity: ");
    scanf("%d", &inventory[id-1].quantity);
    printf("Enter new price: ");
    scanf("%f", &inventory[id-1].price);
    
    printf("Item updated successfully!\n");
}

int main() {
    int choice;
    
    printf("=== Inventory Management System ===\n");
    
    while (1) {
        printf("\nMenu:\n");
        printf("1. Add Item\n");
        printf("2. Display Items\n");
        printf("3. Search Item\n");
        printf("4. Update Item\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                add_item();
                break;
            case 2:
                display_items();
                break;
            case 3:
                search_item();
                break;
            case 4:
                update_item();
                break;
            case 5:
                printf("Goodbye!\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
