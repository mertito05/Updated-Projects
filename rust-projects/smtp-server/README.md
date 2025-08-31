# Rust SMTP Server

A simple SMTP server implementation in Rust using Tokio for asynchronous networking.

## Features

- Basic SMTP protocol support
- Asynchronous I/O with Tokio
- Support for common SMTP commands:
  - HELO/EHLO
  - MAIL FROM
  - RCPT TO
  - DATA
  - QUIT
- Multi-client support

## Usage

### Running the Server

```bash
cd rust-projects/smtp-server
cargo run
```

The server will listen on port 25.

### Testing with SMTP Client

You can test the server using any SMTP client or telnet:

```bash
telnet localhost 25
```

### Example Session

```
220 localhost ESMTP Rust SMTP Server
HELO localhost
250 localhost Hello
MAIL FROM:<user@example.com>
250 OK
RCPT TO:<recipient@example.com>
250 OK
DATA
354 End data with <CR><LF>.<CR><LF>
Subject: Test email

This is a test email.
.
250 OK: Message accepted
QUIT
221 Bye
```

## Future Enhancements

- Add authentication support
- Implement TLS encryption (STARTTLS)
- Support for more SMTP commands
- Email storage and forwarding
- Logging and monitoring
