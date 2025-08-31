#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 100
#define MAX_NAME_LENGTH 50
#define MAX_EMAIL_LENGTH 100

typedef struct {
    int id;
    char name[MAX_NAME_LENGTH];
    int age;
    char email[MAX_EMAIL_LENGTH];
} Record;

Record records[MAX_RECORDS];
int record_count = 0;

void add_record() {
    if (record_count >= MAX_RECORDS) {
        printf("Database is full! Cannot add more records.\n");
        return;
    }
    
    Record new_record;
    new_record.id = record_count + 1;
    
    printf("Enter name: ");
    scanf(" %[^\n]", new_record.name);
    
    printf("Enter age: ");
    scanf("%d", &new_record.age);
    
    printf("Enter email: ");
    scanf(" %[^\n]", new_record.email);
    
    records[record_count] = new_record;
    record_count++;
    printf("Record added successfully!\n");
}

void view_records() {
    if (record_count == 0) {
        printf("No records in the database.\n");
        return;
    }
    
    printf("\n=== Database Records ===\n");
    printf("ID\tName\t\tAge\tEmail\n");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < record_count; i++) {
        printf("%d\t%s\t%d\t%s\n", 
               records[i].id, 
               records[i].name, 
               records[i].age, 
               records[i].email);
    }
}

void update_record() {
    if (record_count == 0) {
        printf("No records to update.\n");
        return;
    }
    
    int id;
    printf("Enter record ID to update: ");
    scanf("%d", &id);
    
    if (id < 1 || id > record_count) {
        printf("Invalid ID!\n");
        return;
    }
    
    printf("Updating record %d:\n", id);
    printf("Enter new name: ");
    scanf(" %[^\n]", records[id-1].name);
    
    printf("Enter new age: ");
    scanf("%d", &records[id-1].age);
    
    printf("Enter new email: ");
    scanf(" %[^\n]", records[id-1].email);
    
    printf("Record updated successfully!\n");
}

void delete_record() {
    if (record_count == 0) {
        printf("No records to delete.\n");
        return;
    }
    
    int id;
    printf("Enter record ID to delete: ");
    scanf("%d", &id);
    
    if (id < 1 || id > record_count) {
        printf("Invalid ID!\n");
        return;
    }
    
    // Shift records to fill the gap
    for (int i = id - 1; i < record_count - 1; i++) {
        records[i] = records[i + 1];
        records[i].id = i + 1;
    }
    
    record_count--;
    printf("Record deleted successfully!\n");
}

int main() {
    int choice;
    
    printf("=== Simple Database Management System ===\n");
    
    while (1) {
        printf("\nMenu:\n");
        printf("1. Add Record\n");
        printf("2. View Records\n");
        printf("3. Update Record\n");
        printf("4. Delete Record\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                add_record();
                break;
            case 2:
                view_records();
                break;
            case 3:
                update_record();
                break;
            case 4:
                delete_record();
                break;
            case 5:
                printf("Goodbye! Database system closed.\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
