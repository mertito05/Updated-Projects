# Password Manager

A secure command-line password manager that encrypts your passwords using strong cryptography.

## Features
- Secure encryption using Fernet (AES-128-CBC)
- Master password protection
- PBKDF2 key derivation with 100,000 iterations
- Add, view, and search password entries
- Encrypted storage of sensitive data

## Security Features
- Passwords are encrypted before storage
- Uses cryptographically secure random salt
- Master password is never stored
- Uses industry-standard encryption algorithms

## Prerequisites
- Python 3.x
- cryptography library

## Installation
```bash
pip install cryptography
```

## How to Run
```bash
python main.py
```

## Usage
1. **First Run**: Create a master password to initialize the vault
2. **Subsequent Runs**: Enter your master password to unlock the vault
3. **Add Password**: Store service, username, and password
4. **View Passwords**: See all stored passwords
5. **Search**: Find passwords by service name

## File Structure
- `passwords.encrypted` - Encrypted password database
- `salt.bin` - Cryptographic salt for key derivation

## Security Notes
- The master password is used to derive the encryption key
- Never share your master password
- Keep the salt.bin file secure along with the encrypted database
- This is a basic implementation - consider using established password managers for critical use

## Warning
This is an educational project. For production use, consider established password managers like Bitwarden, LastPass, or 1Password.
