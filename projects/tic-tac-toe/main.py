def print_board(board):
    """Print the Tic-Tac-Toe board"""
    print("\n")
    for i in range(3):
        print(f" {board[i][0]} | {board[i][1]} | {board[i][2]} ")
        if i < 2:
            print("-----------")
    print("\n")

def check_winner(board):
    """Check if there's a winner"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != ' ':
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    return None

def is_board_full(board):
    """Check if the board is full"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def get_player_move(board, player):
    """Get a valid move from the player"""
    while True:
        try:
            move = input(f"Player {player}, enter your move (1-9): ")
            position = int(move) - 1
            
            if position < 0 or position > 8:
                print("Please enter a number between 1 and 9.")
                continue
            
            row = position // 3
            col = position % 3
            
            if board[row][col] == ' ':
                return row, col
            else:
                print("That position is already taken. Choose another.")
        except ValueError:
            print("Please enter a valid number.")

def play_game():
    """Main game function"""
    # Initialize empty board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    
    print("Welcome to Tic-Tac-Toe!")
    print("Positions are numbered 1-9:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    
    while True:
        print_board(board)
        
        # Get player move
        row, col = get_player_move(board, current_player)
        board[row][col] = current_player
        
        # Check for winner
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! 🤝")
            break
        
        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
    
    # Ask if players want to play again
    play_again = input("\nWould you like to play again? (y/n): ").lower()
    if play_again == 'y':
        play_game()
    else:
        print("Thanks for playing!")

def main():
    """Main function"""
    play_game()

if __name__ == "__main__":
    main()
