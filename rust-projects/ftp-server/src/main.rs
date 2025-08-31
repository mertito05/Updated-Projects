use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use std::error::Error;

async fn handle_client(mut stream: TcpStream) -> Result<(), Box<dyn Error>> {
    let (reader, mut writer) = stream.split();
    let mut reader = BufReader::new(reader);
    let mut line = String::new();

    // Send welcome message
    writer.write_all(b"220 Welcome to Rust FTP server\r\n").await?;

    loop {
        line.clear();
        let bytes_read = reader.read_line(&mut line).await?;
        if bytes_read == 0 {
            break; // connection closed
        }

        let command = line.trim_end();
        println!("Received command: {}", command);

        if command.starts_with("USER") {
            writer.write_all(b"331 Username OK, need password\r\n").await?;
        } else if command.starts_with("PASS") {
            writer.write_all(b"230 User logged in\r\n").await?;
        } else if command == "QUIT" {
            writer.write_all(b"221 Goodbye\r\n").await?;
            break;
        } else {
            writer.write_all(b"502 Command not implemented\r\n").await?;
        }
    }

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:21").await?;
    println!("FTP server listening on port 21");

    loop {
        let (stream, addr) = listener.accept().await?;
        println!("New client: {}", addr);
        tokio::spawn(async move {
            if let Err(e) = handle_client(stream).await {
                eprintln!("Error handling client {}: {}", addr, e);
            }
        });
    }
}
