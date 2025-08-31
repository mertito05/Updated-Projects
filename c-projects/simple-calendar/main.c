#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_EVENTS 100
#define MAX_DESCRIPTION 100
#define DATE_LENGTH 11 // YYYY-MM-DD format

typedef struct {
    int id;
    char date[DATE_LENGTH];
    char description[MAX_DESCRIPTION];
} Event;

Event events[MAX_EVENTS];
int event_count = 0;

void add_event() {
    if (event_count >= MAX_EVENTS) {
        printf("Event limit reached!\n");
        return;
    }
    
    Event new_event;
    new_event.id = event_count + 1;
    
    printf("Enter date (YYYY-MM-DD): ");
    scanf("%s", new_event.date);
    
    printf("Enter event description: ");
    scanf(" %[^\n]", new_event.description);
    
    events[event_count] = new_event;
    event_count++;
    printf("Event added successfully!\n");
}

void display_events() {
    if (event_count == 0) {
        printf("No events scheduled.\n");
        return;
    }
    
    printf("\n=== Scheduled Events ===\n");
    printf("ID\tDate\t\tDescription\n");
    printf("------------------------------------------------------------\n");
    
    for (int i = 0; i < event_count; i++) {
        printf("%d\t%s\t%s\n",
               events[i].id,
               events[i].date,
               events[i].description);
    }
}

void display_events_by_date() {
    if (event_count == 0) {
        printf("No events scheduled.\n");
        return;
    }
    
    char search_date[DATE_LENGTH];
    printf("Enter date to search (YYYY-MM-DD): ");
    scanf("%s", search_date);
    
    printf("\n=== Events on %s ===\n", search_date);
    printf("ID\tDescription\n");
    printf("----------------------------------------\n");
    
    int found = 0;
    for (int i = 0; i < event_count; i++) {
        if (strcmp(events[i].date, search_date) == 0) {
            printf("%d\t%s\n", events[i].id, events[i].description);
            found = 1;
        }
    }
    
    if (!found) {
        printf("No events found for this date.\n");
    }
}

int main() {
    int choice;
    
    printf("=== Simple Calendar Application ===\n");
    
    while (1) {
        printf("\nMenu:\n");
        printf("1. Add Event\n");
        printf("2. Display All Events\n");
        printf("3. Display Events by Date\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                add_event();
                break;
            case 2:
                display_events();
                break;
            case 3:
                display_events_by_date();
                break;
            case 4:
                printf("Goodbye! Have a great day!\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
    
    return 0;
}
