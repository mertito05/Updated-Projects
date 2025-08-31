# Sudoku Solver

A Python program that solves Sudoku puzzles using a backtracking algorithm.

## Features
- **Backtracking Algorithm**: Efficiently solves Sudoku puzzles
- **Visual Display**: Prints the puzzle in a readable 9x9 grid format
- **Validation**: Checks for valid number placements
- **Example Puzzle**: Includes a sample puzzle to demonstrate functionality

## How to Run
```bash
python main.py
```

## Algorithm
The solver uses a recursive backtracking approach:
1. Find the next empty cell
2. Try numbers 1-9 in the empty cell
3. Check if the number is valid (no conflicts in row, column, or 3x3 box)
4. If valid, place the number and recursively solve the rest
5. If no number works, backtrack to the previous cell

## Puzzle Format
- Represented as a 9x9 list of lists
- 0 represents empty cells
- Numbers 1-9 represent filled cells

## Example
The program includes a sample puzzle:
```
5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9
```

## Customization
You can modify the `board` variable in `main.py` to solve different puzzles:
```python
board = [
    [your, puzzle, values, here, ...],
    # ... 9 rows total
]
```

## Note
This implementation uses a simple backtracking algorithm. For very difficult puzzles, more advanced techniques like constraint propagation could be added.
