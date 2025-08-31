# File Encryption Tool

A secure file encryption and decryption tool that uses strong cryptographic algorithms to protect your files. This application supports both password-based encryption and key file-based encryption.

## Features
- **Password-Based Encryption**: Encrypt files using a user-provided password
- **Key File Encryption**: Generate and use encryption key files for added security
- **Strong Cryptography**: Uses Fernet symmetric encryption with AES-128-CBC
- **Password Hashing**: PBKDF2 with SHA256 and 100,000 iterations for key derivation
- **Secure Password Input**: Uses getpass for hidden password entry
- **File Integrity**: Encrypted files include salt for proper key derivation
- **Cross-Platform**: Works on Windows, macOS, and Linux

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

### Password-Based Encryption
1. **Encrypt a file**:
   - Choose option 1 from the menu
   - Enter the input file path
   - Specify output filename (optional)
   - Enter and confirm your password
   - The file will be encrypted with `.encrypted` extension

2. **Decrypt a file**:
   - Choose option 2 from the menu
   - Enter the encrypted file path
   - Specify output filename (optional)
   - Enter the password used for encryption
   - The file will be decrypted to its original form

### Key File-Based Encryption
The tool also supports encryption using key files:
- Use `generate_key_file()` to create a new encryption key
- Use `encrypt_with_key_file()` and `decrypt_with_key_file()` functions

## Security Features
- **Salt**: Each encryption uses a random salt to prevent rainbow table attacks
- **Key Derivation**: PBKDF2 with 100,000 iterations for slow hashing
- **Algorithm**: AES-128-CBC encryption with HMAC-SHA256 authentication
- **Password Confirmation**: Requires password confirmation to prevent mistakes
- **Secure Storage**: Encrypted files store salt for proper decryption

## File Format
Encrypted files have the following format:
```
[salt_base64]:[encrypted_data]
```

Where:
- `salt_base64`: Base64-encoded random salt used for key derivation
- `encrypted_data`: The actual encrypted file content

## Security Considerations
- **Strong Passwords**: Use long, complex passwords for better security
- **Key File Safety**: Keep encryption key files secure and backed up
- **Password Management**: Consider using a password manager
- **File Backups**: Always keep backups of important files before encryption
- **Legal Compliance**: Ensure you have the right to encrypt the files

## Limitations
- **Password Recovery**: There is no password recovery mechanism
- **Large Files**: Very large files may take longer to encrypt/decrypt
- **Memory Usage**: Files are loaded into memory during processing

## Customization
You can extend the tool by:
- Adding support for different encryption algorithms
- Implementing file compression before encryption
- Adding progress indicators for large files
- Creating a graphical user interface
- Adding batch processing for multiple files
- Implementing cloud storage integration

## Troubleshooting
- Ensure the cryptography library is installed correctly
- Verify file permissions for reading/writing files
- Check that you're using the correct password for decryption
- Ensure sufficient disk space for output files

## Warning
⚠️ **IMPORTANT**: If you forget your password or lose your key file, your encrypted files will be permanently inaccessible. There is no recovery mechanism.

## Legal Notice
This tool is intended for legitimate personal use only. Ensure you have the right to encrypt the files you're working with and comply with all applicable laws and regulations.
