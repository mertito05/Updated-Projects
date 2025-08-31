# Rust SSH Server

A basic SSH server implementation in Rust using Tokio for asynchronous networking.

## Features

- Accepts SSH client connections
- Performs SSH protocol version exchange
- Asynchronous I/O with Tokio
- Basic error handling and logging

## Usage

### Running the Server

```bash
cd rust-projects/ssh-server
cargo run
```

The server will listen on port 22.

### Testing with SSH Client

You can test the server using any SSH client:

```bash
ssh localhost
```

Note: This is a minimal implementation and does not support full SSH features like authentication, encryption, or channel management.

## Future Enhancements

- Implement key exchange and encryption
- Add user authentication
- Support multiple SSH channels
- Implement SFTP and port forwarding
- Add logging and monitoring
