# Basic AI for Chess Game

A simple chess game implementation with basic AI using the minimax algorithm with alpha-beta pruning.

## Features

- Complete chess board representation
- Legal move generation for all pieces
- Basic AI opponent using minimax algorithm
- Alpha-beta pruning for optimization
- Simple evaluation function
- Text-based interface
- Move validation and game state tracking

## Chess Rules Implemented

### Piece Movement
- **Pawn**: Forward movement, captures diagonally, en passant, promotion
- **Rook**: Horizontal and vertical movement
- **Knight**: L-shaped movement
- **Bishop**: Diagonal movement
- **Queen**: Combination of rook and bishop movement
- **King**: One square in any direction, castling

### Special Rules
- Castling (kingside and queenside)
- En passant captures
- Pawn promotion
- Check and checkmate detection
- Stalemate detection
- Draw by repetition
- Draw by 50-move rule

## AI Implementation

### Minimax Algorithm
- Recursive search through possible moves
- Depth-limited search (configurable)
- Evaluation function based on material and position

### Alpha-Beta Pruning
- Optimizes minimax by eliminating unnecessary branches
- Reduces search space exponentially
- Maintains optimal move selection

### Evaluation Function
- Material value: Piece values (pawn=1, knight=3, bishop=3, rook=5, queen=9)
- Positional bonuses: Center control, piece development
- King safety: Castling status, pawn structure
- Mobility: Number of legal moves available

## Board Representation

### FEN Notation Support
- Load games from FEN strings
- Save game state to FEN format
- Standard chess starting position: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

### Bitboard Representation (Optional)
- Efficient piece location tracking
- Fast move generation using bitwise operations
- Attack detection and checking

## Game Interface

### Text-Based Display
```
  a b c d e f g h
8 r n b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 P P P P P P P P
1 R N B Q K B N R
```

### Move Input
- Algebraic notation (e.g., "e2e4", "g1f3")
- SAN notation support (e.g., "Nf3", "exd5")
- Coordinate-based input

## AI Configuration

### Search Parameters
- Search depth (1-6 ply recommended for basic AI)
- Time limits for move calculation
- Transposition table for move caching
- Iterative deepening

### Difficulty Levels
- Beginner: Depth 1-2, simple evaluation
- Intermediate: Depth 3-4, improved evaluation
- Advanced: Depth 5-6, complex evaluation

## Implementation Details

### Data Structures
- Board state representation
- Move generation tables
- Game history tracking
- Evaluation cache

### Algorithms
- Move generation for all piece types
- Check detection
- Game state validation
- AI search and evaluation

## Usage

```bash
# Compile the chess game
g++ main.cpp -o chess -std=c++11

# Run the game
./chess
```

## Game Flow

1. Initialize board with starting position
2. Display board and current player
3. Accept player move or AI calculates move
4. Validate move and update board
5. Check for game end conditions
6. Switch players and repeat

## Controls

- Human vs Human: Two players take turns
- Human vs AI: Player plays against computer
- AI vs AI: Watch computer play against itself

## Future Enhancements

- GUI interface using SDL or OpenGL
- Opening book database
- Endgame tablebase support
- Improved evaluation function
- Machine learning-based evaluation
- Network multiplayer
- Game recording and playback
- Tournament mode
- Custom position setup
- Puzzle mode with tactical exercises

## Educational Value

This implementation demonstrates:
- Game tree search algorithms
- Heuristic evaluation functions
- Optimization techniques (alpha-beta pruning)
- Board game AI concepts
- State space representation
- Recursive algorithms
- Performance optimization

## Dependencies

- Standard C++11 library
- (Optional) GUI libraries for graphical interface
- (Optional) Network libraries for multiplayer

## Performance Considerations

- Move generation efficiency
- Search depth vs response time
- Memory usage for transposition tables
- Evaluation function complexity

## Learning Resources

- Chess Programming Wiki
- "Artificial Intelligence: A Modern Approach"
- "How to Create a Chess Engine"
- Stockfish and other open-source chess engines
- Chess theory and strategy books
