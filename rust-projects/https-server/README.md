# HTTPS Server in Rust

A simple HTTPS server implementation using Rust with Hyper and Rustls.

## Features

- HTTPS server running on port 443
- Uses Rustls for TLS encryption
- Simple request handler that responds with "Hello, HTTPS World!"
- Graceful shutdown support

## Prerequisites

- Rust and Cargo installed
- OpenSSL (for generating self-signed certificates)

## Setup

1. Generate self-signed certificates:

```bash
# Generate private key
openssl genrsa -out key.pem 2048

# Generate certificate signing request
openssl req -new -key key.pem -out csr.pem

# Generate self-signed certificate
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem

# Clean up CSR
rm csr.pem
```

2. Place the generated `cert.pem` and `key.pem` files in the project root directory.

## Building and Running

```bash
# Build the project
cargo build

# Run the server
cargo run
```

The server will start listening on `https://localhost:443`.

## Testing

You can test the server using curl:

```bash
curl -k https://localhost:443
```

Or using a web browser (you'll need to accept the self-signed certificate warning).

## Project Structure

- `src/main.rs` - Main server implementation
- `Cargo.toml` - Dependencies and project configuration
- `README.md` - This documentation

## Dependencies

- `hyper` - HTTP server framework
- `tokio` - Async runtime
- `rustls` - TLS implementation
- `hyper-rustls` - Hyper integration with Rustls

## Security Notes

- This implementation uses self-signed certificates for demonstration
- For production use, use certificates from a trusted Certificate Authority
- The server currently accepts all client connections (no client authentication)
- Consider adding proper error handling and logging for production use

## Extending

You can extend this server by:
- Adding route handling
- Implementing request parsing
- Adding middleware
- Supporting different content types
- Adding authentication
- Implementing file serving
