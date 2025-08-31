use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use std::error::Error;

async fn handle_smtp_client(mut stream: TcpStream) -> Result<(), Box<dyn Error>> {
    let (reader, mut writer) = stream.split();
    let mut reader = BufReader::new(reader);
    let mut line = String::new();

    // Send SMTP welcome message
    writer.write_all(b"220 localhost ESMTP Rust SMTP Server\r\n").await?;

    let mut state = "initial"; // Tracks SMTP conversation state
    let mut from = String::new();
    let mut to = Vec::new();
    let mut data = String::new();

    loop {
        line.clear();
        let bytes_read = reader.read_line(&mut line).await?;
        if bytes_read == 0 {
            break; // connection closed
        }

        let command = line.trim_end();
        println!("SMTP command: {}", command);

        match state {
            "initial" => {
                if command.starts_with("HELO") || command.starts_with("EHLO") {
                    writer.write_all(b"250 localhost Hello\r\n").await?;
                    state = "ready";
                } else if command == "QUIT" {
                    writer.write_all(b"221 Bye\r\n").await?;
                    break;
                } else {
                    writer.write_all(b"500 Syntax error, command unrecognized\r\n").await?;
                }
            }
            "ready" => {
                if command.starts_with("MAIL FROM:") {
                    from = command[10..].trim_matches(|c| c == '<' || c == '>').to_string();
                    writer.write_all(b"250 OK\r\n").await?;
                    state = "from";
                } else if command == "QUIT" {
                    writer.write_all(b"221 Bye\r\n").await?;
                    break;
                } else {
                    writer.write_all(b"503 Bad sequence of commands\r\n").await?;
                }
            }
            "from" => {
                if command.starts_with("RCPT TO:") {
                    let recipient = command[8..].trim_matches(|c| c == '<' || c == '>').to_string();
                    to.push(recipient);
                    writer.write_all(b"250 OK\r\n").await?;
                    state = "to";
                } else if command == "QUIT" {
                    writer.write_all(b"221 Bye\r\n").await?;
                    break;
                } else {
                    writer.write_all(b"503 Bad sequence of commands\r\n").await?;
                }
            }
            "to" => {
                if command == "DATA" {
                    writer.write_all(b"354 End data with <CR><LF>.<CR><LF>\r\n").await?;
                    state = "data";
                } else if command.starts_with("RCPT TO:") {
                    let recipient = command[8..].trim_matches(|c极 c == '<' || c == '>').to_string();
                    to.push(recipient);
                    writer.write_all(b"250 OK\r\n").await?;
                } else if command == "QUIT" {
                    writer.write_all(b"221 Bye\r\n").await?;
                    break;
                } else {
                    writer.write_all(b"503 Bad sequence of commands\r\n").await?;
                }
            }
            "data" => {
                if command == "." {
                    // End of data
                    println!("Received email:");
                    println!("From: {}", from);
                    println!("To: {:?}", to);
                    println!("Data:\n{}", data);
                    writer.write_all(b"250 OK: Message accepted\r\n").await?;
                    state = "ready";
                    from.clear();
                    to.clear();
                    data.clear();
                } else {
                    data.push_str(command);
                    data.push_str("\r\n");
                }
            }
            _ => {
                writer.write_all(b"500 Syntax error\r\n").await?;
            }
        }
    }

    Ok(())
}

#[tok极 main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:25").await?;
    println!("SMTP server listening on port 25");

    loop {
        let (stream, addr) = listener.accept().await?;
        println!("New SMTP client: {}", addr);
        
        tokio::spawn(async move {
            if let Err(e) = handle_smtp_client(stream).await {
                eprintln!("Error handling SMTP client {}: {}", addr, e);
            }
        });
    }
}
