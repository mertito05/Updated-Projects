use std::fs;
use std::io::{self, Read, Write};
use std::path::Path;

fn main() {
    println!("=== File Encryption Tool ===");
    println!("Simple XOR-based file encryption/decryption");

    loop {
        println!("\nOptions:");
        println!("1. Encrypt file");
        println!("2. Decrypt file");
        println!("3. Exit");
        print!("Choose an option: ");
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim();

        match choice {
            "1" => encrypt_file(),
            "2" => decrypt_file(),
            "3" => {
                println!("Goodbye!");
                break;
            }
            _ => println!("Invalid option. Please try again."),
        }
    }
}

fn encrypt_file() {
    println!("\n--- File Encryption ---");
    
    let (input_path, output_path, key) = get_file_and_key_info();
    
    match process_file(&input_path, &output_path, &key, true) {
        Ok(_) => println!("File encrypted successfully: {}", output_path),
        Err(e) => println!("Error encrypting file: {}", e),
    }
}

fn decrypt_file() {
    println!("\n--- File Decryption ---");
    
    let (input_path, output_path, key) = get_file_and_key_info();
    
    match process_file(&input_path, &output_path, &key, false) {
        Ok(_) => println!("File decrypted successfully: {}", output_path),
        Err(e) => println!("Error decrypting file: {}", e),
    }
}

fn get_file_and_key_info() -> (String, String, String) {
    print!("Enter input file path: ");
    io::stdout().flush().unwrap();
    let mut input_path = String::new();
    io::stdin().read_line(&mut input_path).unwrap();
    let input_path = input_path.trim().to_string();

    print!("Enter output file path: ");
    io::stdout().flush().unwrap();
    let mut output_path = String::new();
    io::stdin().read_line(&mut output_path).unwrap();
    let output_path = output_path.trim().to_string();

    print!("Enter encryption key: ");
    io::stdout().flush().unwrap();
    let mut key = String::new();
    io::stdin().read_line(&mut key).unwrap();
    let key = key.trim().to_string();

    (input_path, output_path, key)
}

fn process_file(input_path: &str, output_path: &str, key: &str, encrypt: bool) -> io::Result<()> {
    if !Path::new(input_path).exists() {
        return Err(io::Error::new(io::ErrorKind::NotFound, "Input file not found"));
    }

    let mut input_file = fs::File::open(input_path)?;
    let mut buffer = Vec::new();
    input_file.read_to_end(&mut buffer)?;

    let processed_data = if encrypt {
        xor_encrypt(&buffer, key)
    } else {
        xor_decrypt(&buffer, key)
    };

    let mut output_file = fs::File::create(output_path)?;
    output_file.write_all(&processed_data)?;

    Ok(())
}

fn xor_encrypt(data: &[u8], key: &str) -> Vec<u8> {
    let key_bytes = key.as_bytes();
    let mut result = Vec::with_capacity(data.len());
    
    for (i, &byte) in data.iter().enumerate() {
        let key_byte = key_bytes[i % key_bytes.len()];
        result.push(byte ^ key_byte);
    }
    
    result
}

fn xor_decrypt(data: &[u8], key: &str) -> Vec<u8> {
    // XOR decryption is the same as encryption
    xor_encrypt(data, key)
}
