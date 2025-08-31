use tokio::net::UdpSocket;
use std::error::Error;
use std::net::SocketAddr;

// Simple DNS header structure
struct DnsHeader {
    id: u16,
    flags: u16,
    questions: u16,
    answer_rrs: u16,
    authority_rrs: u16,
    additional_rrs: u16,
}

impl DnsHeader {
    fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::new();
        bytes.extend_from_slice(&self.id.to_be_bytes());
        bytes.extend_from_slice(&self.flags.to_be_bytes());
        bytes.extend_from_slice(&self.questions.to_be_bytes());
        bytes.extend_from_slice(&self.answer_rrs.to_be_bytes());
        bytes.extend_from_slice(&self.authority_rrs.to_be_bytes());
        bytes.extend_from_slice(&self.additional_rrs.to_be_bytes());
        bytes
    }
}

async fn handle_dns_query(socket: &UdpSocket, buf: &[u8], addr: SocketAddr) -> Result<(), Box<dyn Error>> {
    if buf.len() < 12 {
        return Ok(()); // Too short for DNS header
    }

    // Parse DNS header (simplified)
    let id = u16::from_be_bytes([buf[0], buf[1]]);
    let flags = u16::from_be_bytes([buf[2], buf[3]]);
    let questions = u16::from_be_bytes([buf[4], buf[5]]);

    println!("DNS query from {}: ID={}, Questions={}", addr, id, questions);

    // Create response header
    let response_header = DnsHeader {
        id,
        flags: 0x8180, // Standard response with recursion available
        questions,
        answer_rrs: 1, // One answer
        authority_rrs: 0,
        additional_rrs: 0,
    };

    let mut response = response_header.to_bytes();

    // For simplicity, just respond with a hardcoded A record for "localhost"
    // This is a very simplified response - real DNS would parse the query
    response.extend_from_slice(&[
        // Query section (echo back)
        0x05, 0x6c, 0x6f, 0x63, 0x61, 0x6c, 0x68, 0x6f, 0x73, 0x74, 0x00, // "localhost"
        0x00, 0x01, // Type A
        0x00, 0x01, // Class IN
        // Answer section
        0xc0, 0x0c, // Pointer to name
        0x00, 0x01, // Type A
        0x00, 0x01, // Class IN
        0x00, 0x00, 0x0e, 0x10, // TTL (1 hour)
        0x00, 0x04, // Data length (4 bytes)
        0x7f, 0x00, 0x00, 0x01, // 127.0.0.1
    ]);

    socket.send_to(&response, addr).await?;
    println!("Sent DNS response to {}", addr);

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let socket = UdpSocket::bind("0.0.0.0:53").await?;
    println!("DNS server listening on port 53");

    let mut buf = [0; 512];

    loop {
        let (len, addr) = socket.recv_from(&mut buf).await?;
        let data = &buf[..len];
        
        tokio::spawn(async move {
            if let Err(e) = handle_dns_query(&socket, data, addr).await {
                eprintln!("Error handling DNS query from {}: {}", addr, e);
            }
        });
    }
}
