# Simple HTTP Server in C

A basic HTTP server implementation written in C that runs on Windows using Winsock.

## Features

- Listens on port 8080
- Responds to all HTTP requests with a "Hello, World!" message
- Simple and lightweight implementation
- Windows-compatible using Winsock API

## Requirements

- GCC compiler (MinGW recommended for Windows)
- Windows operating system

## Building

To compile the server, use the provided Makefile:

```bash
make
```

Or compile manually:

```bash
gcc -Wall -Wextra -std=c99 -o http-server main.c -lws2_32
```

## Running

After compilation, run the server:

```bash
http-server.exe
```

The server will start and display:
```
HTTP Server running on port 8080
```

## Testing

You can test the server by:
1. Opening a web browser and navigating to `http://localhost:8080`
2. Using curl: `curl http://localhost:8080`
3. Using telnet: `telnet localhost 8080` and then typing `GET / HTTP/1.1`

## Project Structure

- `main.c` - Main server implementation
- `Makefile` - Build configuration
- `README.md` - This documentation file

## How It Works

1. Initializes Winsock library
2. Creates a TCP socket
3. Binds to port 8080
4. Listens for incoming connections
5. Accepts connections and sends a simple HTTP response
6. Closes the connection and waits for the next one

## Notes

- This is a simple demonstration server
- It handles one connection at a time
- The server runs indefinitely until manually stopped (Ctrl+C)
- For production use, consider adding error handling, request parsing, and multi-threading
