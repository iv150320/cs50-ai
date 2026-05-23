"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count X and O moves
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # X goes first, then alternate
    if x_count > o_count:
        return O
    elif x_count == o_count:
        return X
    else:
        return X  # Invalid state, default to X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available.add((i, j))
    return available


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    if board[i][j] != EMPTY:
        raise ValueError("Invalid action: cell is not empty")
    
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise ValueError("Invalid action: coordinates out of range")
    
    # Deep copy the board
    new_board = [[board[r][c] for c in range(3)] for r in range(3)]
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if there's a winner
    if winner(board) is not None:
        return True
    
    # Game is over if no empty cells (tie)
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    
    # If terminal state, return None
    if terminal(board):
        return None
    
    if current_player == X:
        # Maximizing player
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            value = min_value(new_board)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        # Minimizing player
        best_value = math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            value = max_value(new_board)
            if value < best_value:
                best_value = value
                best_action = action
        return best_action


def max_value(board):
    """Max value for minimax (X's turn)."""
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    """Min value for minimax (O's turn)."""
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value
