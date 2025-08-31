# Inventory Management System

A simple inventory management system implemented in C that allows users to manage product inventory with basic CRUD operations.

## Features

- Add new items to inventory
- Display all items in inventory
- Search for items by name
- Update item quantity and price
- Simple console-based interface

## Usage

1. Compile the program:
   ```bash
   gcc main.c -o inventory
   ```

2. Run the executable:
   ```bash
   ./inventory
   ```

3. Follow the menu options to manage your inventory.

## Menu Options

1. **Add Item**: Add a new item with name, quantity, and price
2. **Display Items**: Show all items in the inventory
3. **Search Item**: Find an item by name
4. **Update Item**: Modify quantity and price of an existing item
5. **Exit**: Quit the program

## Data Structure

The system uses a simple array-based storage with the following structure:
```c
typedef struct {
    int id;
    char name[50];
    int quantity;
    float price;
} Item;
```

## Limitations

- Maximum of 100 items
- Data is not persisted between sessions
- Simple console interface

## Future Enhancements

- File I/O for data persistence
- Delete item functionality
- More advanced search options
- GUI interface
