import json
import os
from datetime import datetime

DIARY_FILE = "diary_entries.json"

def load_entries():
    """Load diary entries from JSON file"""
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_entries(entries):
    """Save diary entries to JSON file"""
    with open(DIARY_FILE, 'w') as file:
        json.dump(entries, file, indent=2)

def add_entry(entries, content):
    """Add a new diary entry"""
    entry = {
        "id": len(entries) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": content
    }
    entries.append(entry)
    save_entries(entries)
    print(f"Entry #{entry['id']} added successfully!")

def view_entries(entries):
    """View all diary entries"""
    if not entries:
        print("No diary entries found!")
        return
    
    print("\nYour Diary Entries:")
    print("-" * 50)
    for entry in entries:
        print(f"Entry #{entry['id']} - {entry['date']}")
        print(f"Content: {entry['content']}")
        print("-" * 50)

def search_entries(entries, keyword):
    """Search entries containing a keyword"""
    results = []
    for entry in entries:
        if keyword.lower() in entry['content'].lower():
            results.append(entry)
    
    if not results:
        print(f"No entries found containing '{keyword}'")
        return
    
    print(f"\nEntries containing '{keyword}':")
    print("-" * 50)
    for entry in results:
        print(f"Entry #{entry['id']} - {entry['date']}")
        print(f"Content: {entry['content']}")
        print("-" * 50)

def delete_entry(entries, entry_id):
    """Delete a specific diary entry"""
    for i, entry in enumerate(entries):
        if entry['id'] == entry_id:
            removed = entries.pop(i)
            # Reindex remaining entries
            for j, remaining_entry in enumerate(entries[i:], i):
                remaining_entry['id'] = j + 1
            save_entries(entries)
            print(f"Entry #{entry_id} deleted successfully!")
            return
    
    print(f"Entry #{entry_id} not found!")

def main():
    entries = load_entries()
    
    print("Personal Diary Application")
    print("==========================")
    
    while True:
        print("\nOptions:")
        print("1. Add new entry")
        print("2. View all entries")
        print("3. Search entries")
        print("4. Delete entry")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            content = input("Enter your diary entry: ").strip()
            if content:
                add_entry(entries, content)
            else:
                print("Entry cannot be empty!")
        
        elif choice == "2":
            view_entries(entries)
        
        elif choice == "3":
            keyword = input("Enter keyword to search: ").strip()
            if keyword:
                search_entries(entries, keyword)
            else:
                print("Please enter a keyword!")
        
        elif choice == "4":
            view_entries(entries)
            try:
                entry_id = int(input("Enter entry number to delete: ").strip())
                delete_entry(entries, entry_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "5":
            print("Goodbye! Your diary has been saved.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
