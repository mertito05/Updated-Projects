use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::error::Error;

async fn handle_ssh_client(mut stream: TcpStream) -> Result<(), Box<dyn Error>> {
    // SSH protocol version exchange
    let server_version = "SSH-2.0-RustSSH_0.1.0\r\n";
    stream.write_all(server_version.as_bytes()).await?;

    // Read client version
    let mut buffer = [0; 1024];
    let n = stream.read(&mut buffer).await?;
    let client_version = String::from_utf8_lossy(&buffer[..n]);
    println!("Client version: {}", client_version.trim());

    // For a real SSH server, we would now handle:
    // 1. Key exchange
    // 2. Encryption setup
    // 3. Authentication
    // 4. Channel management
    
    // For now, just send a simple message and close
    stream.write_all(b"Protocol mismatch.\r\n").await?;
    
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:22").await?;
    println!("SSH server listening on port 22");

    loop {
        let (stream, addr) = listener.accept().await?;
        println!("New SSH client: {}", addr);
        
        tokio::spawn(async move {
            if let Err(e) = handle_ssh_client(stream).await {
                eprintln!("Error handling SSH client {}: {}", addr, e);
            }
        });
    }
}
