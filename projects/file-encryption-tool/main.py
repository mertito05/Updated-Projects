import os
import hashlib
from cryptography.fernet import Fernet
import base64
import getpass

def generate_key_from_password(password, salt=None):
    """Generate encryption key from password using PBKDF2"""
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = base64.urlsafe_b64decode(salt)
    
    # Use PBKDF2 to derive key from password
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,  # Number of iterations
        32  # Desired key length
    )
    
    # Convert to Fernet-compatible key
    fernet_key = base64.urlsafe_b64encode(key)
    return fernet_key, base64.urlsafe_b64encode(salt).decode('utf-8')

def encrypt_file(input_file, output_file, password):
    """Encrypt a file using password-based encryption"""
    try:
        # Generate key from password
        key, salt = generate_key_from_password(password)
        fernet = Fernet(key)
        
        # Read file content
        with open(input_file, 'rb') as file:
            file_data = file.read()
        
        # Encrypt data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write encrypted data with salt prefix
        with open(output_file, 'wb') as file:
            file.write(salt.encode('utf-8') + b':' + encrypted_data)
        
        print(f"File encrypted successfully: {output_file}")
        return True
        
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False

def decrypt_file(input_file, output_file, password):
    """Decrypt a file using password-based encryption"""
    try:
        # Read encrypted file
        with open(input_file, 'rb') as file:
            data = file.read()
        
        # Extract salt and encrypted data
        if b':' not in data:
            print("Invalid encrypted file format")
            return False
            
        salt_b64, encrypted_data = data.split(b':', 1)
        salt = salt_b64.decode('utf-8')
        
        # Generate key from password and salt
        key, _ = generate_key_from_password(password, salt)
        fernet = Fernet(key)
        
        # Decrypt data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write decrypted data
        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
        
        print(f"File decrypted successfully: {output_file}")
        return True
        
    except Exception as e:
        print(f"Decryption failed: {e}")
        return False

def get_password(prompt="Enter password: "):
    """Get password securely"""
    return getpass.getpass(prompt)

def main():
    """Main function"""
    print("File Encryption Tool")
    print("===================")
    
    while True:
        print("\nOptions:")
        print("1. Encrypt file")
        print("2. Decrypt file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            input_file = input("Enter file to encrypt: ").strip()
            if not os.path.exists(input_file):
                print("File not found!")
                continue
                
            output_file = input("Enter output filename: ").strip()
            if not output_file:
                output_file = input_file + ".encrypted"
            
            password = get_password()
            confirm_password = get_password("Confirm password: ")
            
            if password != confirm_password:
                print("Passwords do not match!")
                continue
                
            encrypt_file(input_file, output_file, password)
        
        elif choice == "2":
            input_file = input("Enter file to decrypt: ").strip()
            if not os.path.exists(input_file):
                print("File not found!")
                continue
                
            output_file = input("Enter output filename: ").strip()
            if not output_file:
                if input_file.endswith('.encrypted'):
                    output_file = input_file[:-10]
                else:
                    output_file = input_file + ".decrypted"
            
            password = get_password()
            decrypt_file(input_file, output_file, password)
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

def generate_key_file():
    """Generate a new encryption key file"""
    key = Fernet.generate_key()
    key_file = "encryption_key.key"
    
    with open(key_file, 'wb') as file:
        file.write(key)
    
    print(f"New encryption key generated: {key_file}")
    print("⚠️  Keep this key safe! Without it, encrypted files cannot be decrypted.")
    return key_file

def encrypt_with_key_file(input_file, output_file, key_file):
    """Encrypt file using key from file"""
    try:
        with open(key_file, 'rb') as file:
            key = file.read()
        
        fernet = Fernet(key)
        
        with open(input_file, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = fernet.encrypt(file_data)
        
        with open(output_file, 'wb') as file:
            file.write(encrypted_data)
        
        print(f"File encrypted successfully: {output_file}")
        return True
        
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False

def decrypt_with_key_file(input_file, output_file, key_file):
    """Decrypt file using key from file"""
    try:
        with open(key_file, 'rb') as file:
            key = file.read()
        
        fernet = Fernet(key)
        
        with open(input_file, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
        
        print(f"File decrypted successfully: {output_file}")
        return True
        
    except Exception as e:
        print(f"Decryption failed: {e}")
        return False

if __name__ == "__main__":
    main()
