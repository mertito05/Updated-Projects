#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_ENTITIES 100

typedef struct {
    int id;
    char name[50];
    bool active;
} Entity;

Entity entities[MAX_ENTITIES];
int entity_count = 0;

void add_entity(const char *name) {
    if (entity_count >= MAX_ENTITIES) {
        printf("Entity limit reached!\n");
        return;
    }
    
    entities[entity_count].id = entity_count + 1;
    snprintf(entities[entity_count].name, sizeof(entities[entity_count].name), "%s", name);
    entities[entity_count].active = true;
    entity_count++;
    printf("Entity '%s' added successfully!\n", name);
}

void update_entities() {
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].active) {
            printf("Updating entity: %s\n", entities[i].name);
            // Update logic here
        }
    }
}

void render_entities() {
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].active) {
            printf("Rendering entity: %s\n", entities[i].name);
            // Render logic here
        }
    }
}

int main() {
    char command[50];
    
    printf("=== Basic Game Engine ===\n");
    
    while (true) {
        printf("\nEnter command (add <name>, update, render, exit): ");
        scanf(" %[^\n]", command);
        
        if (strncmp(command, "add ", 4) == 0) {
            add_entity(command + 4);
        } else if (strcmp(command, "update") == 0) {
            update_entities();
        } else if (strcmp(command, "render") == 0) {
            render_entities();
        } else if (strcmp(command, "exit") == 0) {
            printf("Exiting game engine.\n");
            break;
        } else {
            printf("Unknown command: %s\n", command);
        }
    }
    
    return 0;
}
