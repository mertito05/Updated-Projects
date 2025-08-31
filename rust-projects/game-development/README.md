# Game Development

A simple terminal-based game written in Rust that demonstrates basic game development concepts.

## Features

- Simple game loop with update and render cycles
- Random movement mechanics
- Score tracking
- Terminal-based graphics
- Basic input handling

## Gameplay

The player character (P) moves randomly within a bounded area. The game tracks your score and ends after reaching a certain threshold.

## Controls

- The game runs automatically with random movement
- Type "quit" and press Enter to exit the game
- Press Ctrl+C to force quit

## Usage

```bash
# Build the project
cargo build

# Run the game
cargo run

# The game will display in your terminal with:
# - A score counter
# - Player position
# - Simple grid-based graphics
```

## Project Structure

```
game-development/
├── Cargo.toml
├── src/
│   └── main.rs
└── README.md
```

## Dependencies

- `rand` - For random number generation

## Contributing

Feel free to contribute by submitting pull requests or creating issues.

## License

This project is open source and available under the MIT License.
