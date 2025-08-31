def print_board(board):
    """Print the Sudoku board in a readable format"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(f"{board[i][j] if board[i][j] != 0 else '.'} ", end="")
        print()

def find_empty(board):
    """Find an empty cell (represented by 0)"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, pos):
    """Check if placing num at position pos is valid"""
    row, col = pos
    
    # Check row
    for j in range(9):
        if board[row][j] == num and j != col:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num and i != row:
            return False
    
    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    
    return True

def solve_sudoku(board):
    """Solve the Sudoku puzzle using backtracking"""
    empty = find_empty(board)
    if not empty:
        return True  # Puzzle solved
    
    row, col = empty
    
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            board[row][col] = 0  # Backtrack
    
    return False

def main():
    """Main function to run the Sudoku solver"""
    # Example Sudoku puzzle (0 represents empty cells)
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("Original Sudoku puzzle:")
    print_board(board)
    print("\n" + "="*40 + "\n")
    
    if solve_sudoku(board):
        print("Solved Sudoku puzzle:")
        print_board(board)
    else:
        print("No solution exists for this puzzle")

if __name__ == "__main__":
    main()
