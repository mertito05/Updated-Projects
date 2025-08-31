# File Encryption Tool

A simple command-line file encryption and decryption tool written in Rust using XOR encryption.

## Features

- File encryption using XOR algorithm
- File decryption using the same XOR algorithm
- Simple command-line interface
- Error handling for file operations

## Usage

1. Compile the project:
   ```bash
   cargo build
   ```

2. Run the executable:
   ```bash
   cargo run
   ```

3. Follow the interactive menu:
   - Choose option 1 to encrypt a file
   - Choose option 2 to decrypt a file
   - Choose option 3 to exit

## How It Works

The tool uses a simple XOR encryption algorithm:
- Each byte of the file is XORed with a byte from the encryption key
- The same key is used for both encryption and decryption
- The key is repeated to match the length of the data

## Example

```bash
# Encrypt a file
Enter input file path: secret.txt
Enter output file path: secret.enc
Enter encryption key: mysecretkey

# Decrypt the file
Enter input file path: secret.enc
Enter output file path: secret_decrypted.txt
Enter encryption key: mysecretkey
```

## Security Note

This uses a simple XOR encryption which is not cryptographically secure for production use. It's intended for educational purposes and simple obfuscation.

## Dependencies

- Standard Rust library only (no external dependencies)

## Building

```bash
cargo build --release
```

The executable will be available in `target/release/file-encryption-tool`
