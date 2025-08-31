#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

using namespace std;

enum Piece {
    EMPTY = 0,
    WHITE_PAWN = 1, WHITE_KNIGHT = 2, WHITE_BISHOP = 3, WHITE_ROOK = 4, WHITE_QUEEN = 5, WHITE_KING = 6,
    BLACK_PAWN = -1, BLACK_KNIGHT = -2, BLACK_BISHOP = -3, BLACK_ROOK = -4, BLACK_QUEEN = -5, BLACK_KING = -6
};

enum GameState {
    PLAYING,
    WHITE_WIN,
    BLACK_WIN,
    STALEMATE,
    DRAW
};

class ChessBoard {
private:
    int board[8][8];
    bool whiteToMove;
    GameState state;

public:
    ChessBoard() {
        initializeBoard();
        whiteToMove = true;
        state = PLAYING;
    }

    void initializeBoard() {
        // Initialize empty board
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                board[i][j] = EMPTY;
            }
        }

        // Set up pawns
        for (int i = 0; i < 8; i++) {
            board[1][i] = BLACK_PAWN;
            board[6][i] = WHITE_PAWN;
        }

        // Set up other pieces
        board[0][0] = board[0][7] = BLACK_ROOK;
        board[0][1] = board[0][6] = BLACK_KNIGHT;
        board[0][2] = board[0][5] = BLACK_BISHOP;
        board[0][3] = BLACK_QUEEN;
        board[0][4] = BLACK_KING;

        board[7][0] = board[7][7] = WHITE_ROOK;
        board[7][1] = board[7][6] = WHITE_KNIGHT;
        board[7][2] = board[7][5] = WHITE_BISHOP;
        board[7][3] = WHITE_QUEEN;
        board[7][4] = WHITE_KING;
    }

    void displayBoard() {
        cout << "  a b c d e f g h" << endl;
        for (int i = 0; i < 8; i++) {
            cout << 8 - i << " ";
            for (int j = 0; j < 8; j++) {
                char pieceChar = getPieceChar(board[i][j]);
                cout << pieceChar << " ";
            }
            cout << 8 - i << endl;
        }
        cout << "  a b c d e f g h" << endl;
    }

    char getPieceChar(int piece) {
        switch (piece) {
            case EMPTY: return '.';
            case WHITE_PAWN: return 'P';
            case WHITE_KNIGHT: return 'N';
            case WHITE_BISHOP: return 'B';
            case WHITE_ROOK: return 'R';
            case WHITE_QUEEN: return 'Q';
            case WHITE_KING: return 'K';
            case BLACK_PAWN: return 'p';
            case BLACK_KNIGHT: return 'n';
            case BLACK_BISHOP: return 'b';
            case BLACK_ROOK: return 'r';
            case BLACK_QUEEN: return 'q';
            case BLACK_KING: return 'k';
            default: return '?';
        }
    }

    bool isValidMove(int fromRow, int fromCol, int toRow, int toCol) {
        // Basic move validation
        if (fromRow < 0 || fromRow >= 8 || fromCol < 0 || fromCol >= 8 ||
            toRow < 0 || toRow >= 8 || toCol < 0 || toCol >= 8) {
            return false;
        }

        int piece = board[fromRow][fromCol];
        if (piece == EMPTY) return false;

        // Check if piece belongs to current player
        if ((whiteToMove && piece < 0) || (!whiteToMove && piece > 0)) {
            return false;
        }

        // Simple move logic for demonstration
        // In a real implementation, this would be much more complex
        return true;
    }

    void makeMove(int fromRow, int fromCol, int toRow, int toCol) {
        if (isValidMove(fromRow, fromCol, toRow, toCol)) {
            board[toRow][toCol] = board[fromRow][fromCol];
            board[fromRow][fromCol] = EMPTY;
            whiteToMove = !whiteToMove;
        }
    }

    int evaluate() {
        // Simple material evaluation
        int score = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                score += getPieceValue(board[i][j]);
            }
        }
        return score;
    }

    int getPieceValue(int piece) {
        switch (abs(piece)) {
            case WHITE_PAWN: return (piece > 0) ? 1 : -1;
            case WHITE_KNIGHT: return (piece > 0) ? 3 : -3;
            case WHITE_BISHOP: return (piece > 0) ? 3 : -3;
            case WHITE_ROOK: return (piece > 0) ? 5 : -5;
            case WHITE_QUEEN: return (piece > 0) ? 9 : -9;
            case WHITE_KING: return (piece > 0) ? 100 : -100;
            default: return 0;
        }
    }

    vector<pair<pair<int, int>, pair<int, int>>> generateMoves() {
        vector<pair<pair<int, int>, pair<int, int>>> moves;
        // Simple move generation for demonstration
        // In a real implementation, this would generate all legal moves
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if ((whiteToMove && board[i][j] > 0) || (!whiteToMove && board[i][j] < 0)) {
                    // Generate some simple moves
                    for (int di = -1; di <= 1; di++) {
                        for (int dj = -1; dj <= 1; dj++) {
                            if (di == 0 && dj == 0) continue;
                            int ni = i + di, nj = j + dj;
                            if (ni >= 0 && ni < 8 && nj >= 0 && nj < 8) {
                                if (isValidMove(i, j, ni, nj)) {
                                    moves.push_back({{i, j}, {ni, nj}});
                                }
                            }
                        }
                    }
                }
            }
        }
        return moves;
    }

    int minimax(int depth, int alpha, int beta, bool maximizingPlayer) {
        if (depth == 0) {
            return evaluate();
        }

        auto moves = generateMoves();
        if (moves.empty()) {
            return evaluate(); // Game over
        }

        if (maximizingPlayer) {
            int maxEval = INT_MIN;
            for (auto move : moves) {
                // Make move
                int temp = board[move.second.first][move.second.second];
                board[move.second.first][move.second.second] = board[move.first.first][move.first.second];
                board[move.first.first][move.first.second] = EMPTY;
                whiteToMove = !whiteToMove;

                int eval = minimax(depth - 1, alpha, beta, false);
                
                // Undo move
                board[move.first.first][move.first.second] = board[move.second.first][move.second.second];
                board[move.second.first][move.second.second] = temp;
                whiteToMove = !whiteToMove;

                maxEval = max(maxEval, eval);
                alpha = max(alpha, eval);
                if (beta <= alpha) break;
            }
            return maxEval;
        } else {
            int minEval = INT_MAX;
            for (auto move : moves) {
                // Make move
                int temp = board[move.second.first][move.second.second];
                board[move.second.first][move.second.second] = board[move.first.first][move.first.second];
                board[move.first.first][move.first.second] = EMPTY;
                whiteToMove = !whiteToMove;

                int eval = minimax(depth - 1, alpha, beta, true);
                
                // Undo move
                board[move.first.first][move.first.second] = board[move.second.first][move.second.second];
                board[move.second.first][move.second.second] = temp;
                whiteToMove = !whiteToMove;

                minEval = min(minEval, eval);
                beta = min(beta, eval);
                if (beta <= alpha) break;
            }
            return minEval;
        }
    }

    bool isWhiteToMove() const {
        return whiteToMove;
    }

    pair<pair<int, int>, pair<int, int>> findBestMove(int depth) {
        auto moves = generateMoves();
        if (moves.empty()) return {{-1, -1}, {-1, -1}};
        
        int bestValue = INT_MIN;
        pair<pair<int, int>, pair<int, int>> bestMove = moves[0];

        for (auto move : moves) {
            // Make move
            int temp = board[move.second.first][move.second.second];
            board[move.second.first][move.second.second] = board[move.first.first][move.first.second];
            board[move.first.first][move.first.second] = EMPTY;
            whiteToMove = !whiteToMove;

            int moveValue = minimax(depth - 1, INT_MIN, INT_MAX, false);
            
            // Undo move
            board[move.first.first][move.first.second] = board[move.second.first][move.second.second];
            board[move.second.first][move.second.second] = temp;
            whiteToMove = !whiteToMove;

            if (moveValue > bestValue) {
                bestValue = moveValue;
                bestMove = move;
            }
        }

        return bestMove;
    }
};

int main() {
    ChessBoard game;
    cout << "Basic Chess AI Game" << endl;
    cout << "===================" << endl;

    while (true) {
        game.displayBoard();
        
        if (game.isWhiteToMove()) {
            cout << "White's turn. Enter your move (e.g., e2e4): ";
            string move;
            cin >> move;
            
            if (move.length() == 4) {
                int fromCol = move[0] - 'a';
                int fromRow = 8 - (move[1] - '0');
                int toCol = move[2] - 'a';
                int toRow = 8 - (move[3] - '0');
                
                game.makeMove(fromRow, fromCol, toRow, toCol);
            }
        } else {
            cout << "AI is thinking..." << endl;
            auto bestMove = game.findBestMove(3); // Search depth 3
            game.makeMove(bestMove.first.first, bestMove.first.second, 
                         bestMove.second.first, bestMove.second.second);
            cout << "AI moved." << endl;
        }
    }

    return 0;
}
