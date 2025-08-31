# Chat Application

A real-time chat application with both command-line and web-based interfaces. The application supports multiple users chatting simultaneously using socket programming and WebSockets.

## Features

### Command-Line Chat (main.py)
- **Server Mode**: Host a chat server that multiple clients can connect to
- **Client Mode**: Connect to a running chat server
- **Real-time Messaging**: Instant message delivery between users
- **Multiple Users**: Support for multiple concurrent users
- **Username Support**: Users can choose their display names
- **Broadcast Messages**: Messages are broadcast to all connected users
- **Connection Management**: Automatic handling of user join/leave events

### Web-Based Chat (server.py)
- **Web Interface**: Modern web-based chat interface
- **Socket.IO**: Real-time bidirectional communication
- **Responsive Design**: Works on desktop and mobile devices
- **User List**: Display online users
- **Message History**: View chat history in real-time

## Prerequisites
- Python 3.x
- Flask and Flask-SocketIO (for web version)
- Socket.io client library (included via CDN)

## Installation

### For Command-Line Chat:
```bash
# No additional packages required (uses standard library)
python main.py
```

### For Web-Based Chat:
```bash
pip install flask flask-socketio
python server.py
```

## Usage

### Command-Line Chat:
1. **Start Server**: Run `python main.py` and choose option 1
2. **Start Client**: Run `python main.py` on another machine/terminal and choose option 2
3. **Enter server IP** (default: localhost) and username
4. **Start chatting** by typing messages

### Web-Based Chat:
1. **Start Server**: Run `python server.py`
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Open multiple browser tabs/windows** to simulate multiple users
4. **Start chatting** in the web interface

## Port Configuration
- **Default Port**: 12345 (command-line)
- **Web Port**: 5000 (Flask development server)

## Network Configuration
- **Local Network**: Clients can connect using the server's local IP address
- **Internet**: Requires port forwarding for external connections
- **Firewall**: Ensure the chat port is open on the server

## Security Considerations
- This is a basic implementation without encryption
- For production use, implement SSL/TLS encryption
- Consider adding user authentication
- Validate and sanitize all user input

## File Structure
```
chat-app/
├── main.py          # Command-line chat application
├── server.py        # Web-based chat server
├── templates/
│   └── index.html   # Web chat interface
└── requirements.txt # Python dependencies
```

## Customization
You can extend the application by:
- Adding private messaging between users
- Implementing chat rooms/channels
- Adding file sharing capabilities
- Including message encryption
- Adding user authentication and registration
- Implementing message persistence (database)
- Adding emoji support and rich text formatting

## Troubleshooting

### Common Issues:
1. **Connection Refused**: Ensure the server is running and port is open
2. **Firewall Blocking**: Check firewall settings on server and client
3. **Port Already in Use**: Change the port number in the code
4. **Network Issues**: Verify network connectivity between devices

### Web Chat Issues:
- Ensure Flask and Flask-SocketIO are installed
- Check that port 5000 is available
- Verify JavaScript is enabled in the browser

## Performance
- The command-line version uses threading for multiple clients
- The web version uses Socket.IO for real-time communication
- Both versions can handle multiple concurrent connections

## Note
This project is intended for educational purposes and local network use. For production deployment, consider using a proper web server (like Gunicorn) and implementing additional security measures.
