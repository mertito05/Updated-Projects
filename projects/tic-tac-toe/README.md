# Tic-Tac-Toe Game

A classic command-line Tic-Tac-Toe game for two players.

## Features
- **Two-Player Game**: Players take turns as X and O
- **Visual Board**: Clear ASCII art board display
- **Input Validation**: Ensures valid moves and prevents overwriting
- **Win Detection**: Automatically detects wins and draws
- **Replay Option**: Play multiple games in one session

## How to Run
```bash
python main.py
```

## Game Rules
1. Players take turns placing their mark (X or O) on a 3x3 grid
2. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
3. If all 9 squares are full and no player has 3 in a row, the game is a draw

## Board Positions
The board positions are numbered 1-9:
```
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 
```

## Game Flow
1. Player X goes first
2. Enter a number 1-9 to place your mark
3. Players alternate turns
4. Game continues until someone wins or the board is full
5. Option to play again after each game

## Controls
- Enter numbers 1-9 to make moves
- Input validation prevents invalid moves
- Case-insensitive 'y'/'n' for replay option

## Example Game
```
Player X, enter your move (1-9): 5

   |   |   
-----------
   | X |   
-----------
   |   |   

Player O, enter your move (1-9): 1

 O |   |   
-----------
   | X |   
-----------
   |   |
