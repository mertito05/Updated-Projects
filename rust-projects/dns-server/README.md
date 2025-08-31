# Rust DNS Server

A simple DNS server implementation in Rust using Tokio for asynchronous UDP networking.

## Features

- Basic DNS protocol support
- Asynchronous UDP socket handling with Tokio
- Responds to A record queries for "localhost" with 127.0.0.1
- Simple DNS header parsing and response construction

## Usage

### Running the Server

```bash
cd rust-projects/dns-server
cargo run
```

The server will listen on UDP port 53.

### Testing with dig

You can test the server using the `dig` command:

```bash
dig @localhost localhost
```

You should receive a response with the IP address 127.0.0.1.

## Future Enhancements

- Full DNS query parsing and support for multiple record types
- Support for recursive queries and caching
- Zone file loading and management
- DNSSEC support
- Logging and monitoring
