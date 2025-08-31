import json
import os
import getpass
from cryptography.fernet import Fernet

PASSWORD_FILE = "passwords.json"
KEY_FILE = "secret.key"

def generate_key():
    """Generate a key for encryption"""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    return generate_key()

def encrypt_password(password, key):
    """Encrypt a password"""
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    """Decrypt a password"""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()

def load_passwords(key):
    """Load passwords from JSON file"""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    return []

def save_passwords(passwords):
    """Save passwords to JSON file"""
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file, indent=2)

def add_password(passwords, key, service, username, password):
    """Add a new password entry"""
    encrypted_password = encrypt_password(password, key)
    entry = {
        "id": len(passwords) + 1,
        "service": service,
        "username": username,
        "password": encrypted_password
    }
    passwords.append(entry)
    save_passwords(passwords)
    print(f"Password for {service} added successfully!")

def view_passwords(passwords, key):
    """View all password entries (without showing actual passwords)"""
    if not passwords:
        print("No passwords stored!")
        return
    
    print("\nYour Password Manager:")
    print("-" * 60)
    for entry in passwords:
        print(f"Entry #{entry['id']}: {entry['service']}")
        print(f"Username: {entry['username']}")
        print(f"Password: [ENCRYPTED]")
        print("-" * 60)

def get_password(passwords, key, service):
    """Get a specific password (decrypted)"""
    for entry in passwords:
        if entry['service'].lower() == service.lower():
            decrypted_password = decrypt_password(entry['password'], key)
            print(f"\nService: {entry['service']}")
            print(f"Username: {entry['username']}")
            print(f"Password: {decrypted_password}")
            return
    
    print(f"No password found for {service}")

def delete_password(passwords, service):
    """Delete a password entry"""
    for i, entry in enumerate(passwords):
        if entry['service'].lower() == service.lower():
            removed = passwords.pop(i)
            # Reindex remaining entries
            for j, remaining_entry in enumerate(passwords[i:], i):
                remaining_entry['id'] = j + 1
            save_passwords(passwords)
            print(f"Password for {service} deleted successfully!")
            return
    
    print(f"No password found for {service}")

def main():
    key = load_key()
    passwords = load_passwords(key)
    
    print("Password Manager Application")
    print("============================")
    print("🔒 Your passwords are encrypted for security")
    
    while True:
        print("\nOptions:")
        print("1. Add new password")
        print("2. View all services")
        print("3. Get specific password")
        print("4. Delete password")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            service = input("Enter service name: ").strip()
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            add_password(passwords, key, service, username, password)
        
        elif choice == "2":
            view_passwords(passwords, key)
        
        elif choice == "3":
            service = input("Enter service name: ").strip()
            get_password(passwords, key, service)
        
        elif choice == "4":
            service = input("Enter service name to delete: ").strip()
            delete_password(passwords, service)
        
        elif choice == "5":
            print("Goodbye! Your passwords are securely stored.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
