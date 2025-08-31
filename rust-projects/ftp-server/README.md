# Rust FTP Server

A simple FTP server implementation in Rust using Tokio for asynchronous networking.

## Features

- Basic FTP protocol support
- Asynchronous I/O with Tokio
- Support for common FTP commands:
  - USER (username authentication)
  - PASS (password authentication)
  - QUIT (disconnect)
- Multi-client support

## Usage

### Running the Server

```bash
cd rust-projects/ftp-server
cargo run
```

The server will listen on port 21.

### Testing with FTP Client

You can test the server using any FTP client:

```bash
# Using command line ftp
ftp localhost 21

# Or using curl for basic testing
curl ftp://localhost/ --user username:password
```

### Example Session

```
$ ftp localhost 21
Connected to localhost.
220 Welcome to Rust FTP server
Name (localhost:user): testuser
331 Username OK, need password
Password:
230 User logged in
ftp> quit
221 Goodbye
```

## Protocol Support

Currently supports:
- USER - Username authentication
- PASS - Password authentication  
- QUIT - Disconnect from server

## Implementation Details

- Uses Tokio for asynchronous networking
- Handles multiple clients concurrently
- Basic error handling and logging
- Follows FTP protocol response codes

## Future Enhancements

- Add file transfer support (STOR, RETR)
- Implement directory listing (LIST, NLST)
- Add passive/active mode support
- Support for more FTP commands
- TLS/SSL encryption support
- User authentication system
- File system integration
