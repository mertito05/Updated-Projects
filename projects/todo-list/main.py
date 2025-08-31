import json
import os

TODO_FILE = "todos.json"

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=2)

def add_todo(todos, task):
    todos.append({"task": task, "completed": False})
    save_todos(todos)
    print(f"Added: {task}")

def view_todos(todos):
    if not todos:
        print("No todos found!")
        return
    
    print("\nYour To-Do List:")
    for i, todo in enumerate(todos, 1):
        status = "✓" if todo["completed"] else " "
        print(f"{i}. [{status}] {todo['task']}")

def complete_todo(todos, index):
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        save_todos(todos)
        print(f"Completed: {todos[index]['task']}")
    else:
        print("Invalid todo number!")

def delete_todo(todos, index):
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        save_todos(todos)
        print(f"Deleted: {removed['task']}")
    else:
        print("Invalid todo number!")

def main():
    todos = load_todos()
    
    while True:
        print("\nTo-Do List Menu:")
        print("1. View todos")
        print("2. Add todo")
        print("3. Complete todo")
        print("4. Delete todo")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            view_todos(todos)
        elif choice == "2":
            task = input("Enter the task: ")
            add_todo(todos, task)
        elif choice == "3":
            view_todos(todos)
            try:
                index = int(input("Enter todo number to complete: ")) - 1
                complete_todo(todos, index)
            except ValueError:
                print("Please enter a valid number!")
        elif choice == "4":
            view_todos(todos)
            try:
                index = int(input("Enter todo number to delete: ")) - 1
                delete_todo(todos, index)
            except ValueError:
                print("Please enter a valid number!")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
