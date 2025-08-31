use tokio::net::{TcpListener, TcpStream, UdpSocket};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::error::Error;
use std::net::SocketAddr;

// TCP Server example
async fn tcp_server() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080").await?;
    println!("TCP server listening on port 8080");

    loop {
        let (mut socket, addr) = listener.accept().await?;
        println!("TCP client connected: {}", addr);

        tokio::spawn(async move {
            let mut buf = [0; 1024];
            loop {
                let n = match socket.read(&mut buf).await {
                    Ok(n) if n == 0 => break,
                    Ok(n) => n,
                    Err(e) => {
                        eprintln!("TCP read error: {}", e);
                        break;
                    }
                };

                println!("TCP received: {}", String::from_utf8_lossy(&buf[..n]));
                
                // Echo back
                if let Err(e) = socket.write_all(&buf[..n]).await {
                    eprintln!("TCP write error: {}", e);
                    break;
                }
            }
            println!("TCP client disconnected: {}", addr);
        });
    }
}

// TCP Client example
async fn tcp_client() -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080").await?;
    println!("TCP client connected to server");

    // Send a message
    let message = b"Hello TCP Server!";
    stream.write_all(message).await?;
    println!("TCP sent: {}", String::from_utf8_lossy(message));

    // Read response
    let mut buf = [0; 1024];
    let n = stream.read(&mut buf).await?;
    println!("TCP received: {}", String::from_utf8_lossy(&buf[..n]));

    Ok(())
}

// UDP Server example
async fn udp_server() -> Result<(), Box<dyn Error>> {
    let socket = UdpSocket::bind("0.0.0.0:8081").await?;
    println!("UDP server listening on port 8081");

    let mut buf = [0; 1024];
    loop {
        let (len, addr) = socket.recv_from(&mut buf).await?;
        let data = &buf[..len];
        println!("UDP received from {}: {}", addr, String::from_utf8_lossy(data));

        // Echo back
        socket.send_to(data, addr).await?;
        println!("UDP echoed back to {}", addr);
    }
}

// UDP Client example
async fn udp_client() -> Result<(), Box<dyn Error>> {
    let socket = UdpSocket::bind("0.0.0.0:0").await?;
    let server_addr: SocketAddr = "127.0.0.1:8081".parse()?;

    // Send a message
    let message = b"Hello UDP Server!";
    socket.send_to(message, server_addr).await?;
    println!("UDP sent: {}", String::from_utf8_lossy(message));

    // Receive response
    let mut buf = [0; 1024];
    let (len, _) = socket.recv_from(&mut buf).await?;
    println!("UDP received: {}", String::from_utf8_lossy(&buf[..len]));

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    println!("Raw Socket Examples");
    println!("1. TCP Server (port 8080)");
    println!("2. TCP Client");
    println!("3. UDP Server (port 8081)");
    println!("4. UDP Client");
    println!("Choose an option (1-4): ");

    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;

    match input.trim() {
        "1" => tcp_server().await,
        "2" => tcp_client().await,
        "3" => udp_server().await,
        "4" => udp_client().await,
        _ => {
            println!("Invalid option");
            Ok(())
        }
    }
}
