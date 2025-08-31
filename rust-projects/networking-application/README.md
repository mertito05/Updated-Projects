# Networking Application

A Rust networking application that demonstrates TCP client-server communication with multi-threading support.

## Features

- TCP server that can handle multiple clients simultaneously
- TCP client that connects to the server
- Echo functionality with message processing
- Multi-threaded client handling
- Simple command-line interface

## Usage

### Running the Server

```bash
# Build and run the server
cargo run

# Choose option 1 when prompted
# Server will listen on 127.0.0.1:8080
```

### Running the Client

```bash
# In a separate terminal, build and run the client
cargo run

# Choose option 2 when prompted
# Client will connect to the server and allow you to send messages
```

## Project Structure

```
networking-application/
├── Cargo.toml
├── src/
│   └── main.rs
└── README.md
```

## Functionality

### Server
- Listens on port 8080
- Handles multiple clients using threads
- Echoes back messages in uppercase
- Logs client connections and disconnections

### Client
- Connects to localhost:8080
- Allows interactive message sending
- Displays server responses
- Can disconnect by typing "quit"

## Dependencies

This project uses only the Rust standard library - no external dependencies.

## Example Usage

1. Start the server in one terminal
2. Start one or more clients in other terminals
3. Type messages in client terminals and see them echoed back in uppercase
4. Type "quit" to disconnect

## Contributing

Feel free to contribute by submitting pull requests or creating issues.

## License

This project is open source and available under the MIT License.
