# Chat Application

A real-time chat application built with Go and WebSockets using the Gorilla WebSocket library.

## Features
- Real-time bidirectional communication using WebSockets
- Simple echo server that sends received messages back to clients
- Cross-origin requests enabled for development
- Connection management with proper cleanup

## Requirements
- Go 1.21 or later
- Gorilla WebSocket library

## Installation
```bash
go mod download
```

## How to Run
```bash
go run main.go
```

The server will start on `localhost:8080`

## Usage
1. Start the server
2. Connect to `ws://localhost:8080/ws` using a WebSocket client
3. Send messages and receive echoes

## WebSocket Client Example
You can test the server using JavaScript in a browser:
```javascript
const ws = new WebSocket('ws://localhost:8080/ws');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.onopen = () => ws.send('Hello Server!');
```

## API Endpoints
- `GET /ws` - WebSocket connection endpoint

## Dependencies
- github.com/gorilla/websocket v1.5.1
