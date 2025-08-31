# Chat Client

A simple TCP chat client written in Rust for connecting to chat servers.

## Features

- Connect to TCP chat servers
- Send and receive messages in real-time
- Multi-threaded design for simultaneous reading/writing
- Basic chat commands
- Username support

## Usage

1. Compile the project:
   ```bash
   cargo build
   ```

2. Run the executable:
   ```bash
   cargo run
   ```

3. Follow the interactive menu:
   - Choose option 1 to connect to a chat server
   - Choose option 2 to exit

## Connecting to a Server

When connecting to a server, you'll need to provide:
- Server address (e.g., `127.0.0.1:8080`)
- Your username

## Chat Commands

- `/quit` - Exit the chat and disconnect from server
- `/users` - Request list of online users (server must support this)
- `/help` - Show available commands

## Example Usage

```bash
# Connect to a local chat server
Enter server address (e.g., 127.0.0.1:8080): 127.0.0.1:8080
Enter your username: alice

# Once connected, you can start chatting
alice> Hello everyone!
alice> /users
alice> /quit
```

## Protocol

The client uses a simple text-based protocol:
- `USER <username>` - Set username when connecting
- `MSG <message>` - Send a chat message
- `QUIT` - Disconnect from server

## Multi-threading

The client uses separate threads for:
- Reading incoming messages from the server
- Handling user input and sending messages

This allows real-time message reception while typing.

## Dependencies

- Standard Rust library only (no external dependencies)

## Building

```bash
cargo build --release
```

The executable will be available in `target/release/chat-client`

## Server Compatibility

This client is designed to work with simple TCP chat servers that understand the basic protocol:
- Accepts TCP connections
- Understands `USER`, `MSG`, and `QUIT` commands
- Sends messages as plain text with newlines

## Testing

To test the client, you'll need a compatible chat server running. You can use the networking-application project included in this repository as a simple echo server for testing.

## Limitations

- No encryption or security features
- Basic error handling
- No message history or persistence
- Requires manual server address input
