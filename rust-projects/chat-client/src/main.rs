use std::io::{self, BufRead, BufReader, Write};
use std::net::TcpStream;
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Simple Chat Client ===");
    println!("Connect to a chat server and send/receive messages");

    loop {
        println!("\nOptions:");
        println!("1. Connect to chat server");
        println!("2. Exit");
        print!("Choose an option: ");
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim();

        match choice {
            "1" => connect_to_server(),
            "2" => {
                println!("Goodbye!");
                break;
            }
            _ => println!("Invalid option. Please try again."),
        }
    }
}

fn connect_to_server() {
    println!("\n--- Connect to Chat Server ---");
    
    print!("Enter server address (e.g., 127.0.0.1:8080): ");
    io::stdout().flush().unwrap();
    let mut server_addr = String::new();
    io::stdin().read_line(&mut server_addr).unwrap();
    let server_addr = server_addr.trim();

    print!("Enter your username: ");
    io::stdout().flush().unwrap();
    let mut username = String::new();
    io::stdin().read_line(&mut username).unwrap();
    let username = username.trim();

    match TcpStream::connect(server_addr) {
        Ok(mut stream) => {
            println!("Connected to server at {}", server_addr);
            
            // Send username to server
            if let Err(e) = stream.write_all(format!("USER {}\n", username).as_bytes()) {
                println!("Error sending username: {}", e);
                return;
            }

            // Clone stream for reading
            let mut read_stream = stream.try_clone().expect("Failed to clone stream");
            
            // Spawn a thread to read messages from server
            thread::spawn(move || {
                let reader = BufReader::new(&mut read_stream);
                for line in reader.lines() {
                    match line {
                        Ok(message) => {
                            if !message.is_empty() {
                                println!("{}", message);
                            }
                        }
                        Err(e) => {
                            println!("Error reading from server: {}", e);
                            break;
                        }
                    }
                }
            });

            // Main thread handles user input
            chat_loop(&mut stream, username);
        }
        Err(e) => {
            println!("Failed to connect to server: {}", e);
            println!("Make sure the server is running and the address is correct.");
        }
    }
}

fn chat_loop(stream: &mut TcpStream, username: &str) {
    println!("\n--- Chat Started ---");
    println!("Type your messages below. Type '/quit' to exit.");
    println!("Commands:");
    println!("  /quit - Exit the chat");
    println!("  /users - List online users");
    println!("  /help - Show this help");

    let mut input = String::new();
    let stdin = io::stdin();

    loop {
        print!("{}> ", username);
        io::stdout().flush().unwrap();
        
        input.clear();
        stdin.read_line(&mut input).unwrap();
        let message = input.trim();

        if message.is_empty() {
            continue;
        }

        match message {
            "/quit" => {
                println!("Disconnecting from chat...");
                break;
            }
            "/help" => {
                println!("Available commands:");
                println!("  /quit - Exit the chat");
                println!("  /users - List online users");
                println!("  /help - Show this help");
                continue;
            }
            _ => {}
        }

        // Send message to server
        if let Err(e) = stream.write_all(format!("MSG {}\n", message).as_bytes()) {
            println!("Error sending message: {}", e);
            break;
        }

        // Small delay to prevent flooding
        thread::sleep(Duration::from_millis(50));
    }

    // Send quit command to server
    let _ = stream.write_all(b"QUIT\n");
}

// Simulated server response handler for demonstration
fn handle_server_commands(message: &str) {
    if message.starts_with("USERLIST") {
        let users = message.split_whitespace().skip(1).collect::<Vec<&str>>();
        println!("\nOnline users: {}", users.join(", "));
    } else if message.starts_with("ERROR") {
        println!("Server error: {}", message);
    } else if message.starts_with("INFO") {
        println!("Server: {}", message);
    }
}
