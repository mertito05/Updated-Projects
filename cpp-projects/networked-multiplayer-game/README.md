# Networked Multiplayer Game

A simple networked multiplayer game in C++ using socket programming for basic client-server communication.

## Features

- Client-server architecture
- Basic game state synchronization
- Simple text-based game mechanics
- Multiple client support

## Requirements

- C++11 or later
- Socket programming libraries (Winsock on Windows, BSD sockets on Unix/Linux)

## Usage

1. Compile the server:
   ```bash
   g++ server.cpp -o server -lws2_32 (on Windows)
   g++ server.cpp -o server (on Unix/Linux)
   ```

2. Compile the client:
   ```bash
   g++ client.cpp -o client -lws2_32 (on Windows)
   g++ client.cpp -o client (on Unix/Linux)
   ```

3. Run the server:
   ```bash
   ./server
   ```

4. Run clients in separate terminals:
   ```bash
   ./client
   ```

## Game Mechanics

- Players can join the game
- Basic movement commands
- Simple game state updates
- Player interaction

## Future Enhancements

- Graphical interface
- More complex game mechanics
- Database integration for player stats
- Chat functionality
- Game lobbies and matchmaking
