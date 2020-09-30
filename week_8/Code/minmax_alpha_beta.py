from math import inf
from copy import deepcopy

# User/AI icon definitions
user = "X"
ai = "O"


def minmax(board, is_maximizing_player, alpha=-inf, beta=+inf, depth=0):
    # Get current board state
    eval = evaluate_board(board)
    # Check if this is a terminal (win/draw) state
    if eval != None:
        # If it is, we return the corresponding min/max win value
        # We add depth to penalize states that take longer to win
        return eval + depth if is_maximizing_player else eval - depth

    # Set the initial min/max evaluation to -inf or inf
    if is_maximizing_player:
        best_eval = -inf
    else:
        best_eval = inf

    # Itterate through all board positions
    for i in range(len(board)):
        for j in range(len(board)):
            # If there is no icon in this location
            if board[i][j] == ' ':
                # Create a copy of the board
                child = deepcopy(board)
                # If this is the maximizing player
                if is_maximizing_player:
                    # Set the current index to the AI icon
                    child[i][j] = ai
                    # This line will recursively call the minmax function until we get a terminal state
                    # We add the heuristic to the evaluation for each step of the path
                    eval = minmax(child, False, alpha, beta,
                                  depth+1,) + heuristic(child)
                    # Find the path that maximizes a win for AI
                    best_eval = max(best_eval, eval)
                    # Perform the alpha/beta pruning
                    alpha = max(beta, eval)
                    # If the current eval is less than previous eval
                    if beta <= alpha:
                        # We don't need to continue as previous eval was optimal
                        break
                else:
                    # Same method as above, only now for the minimizing player
                    child[i][j] = user
                    eval = minmax(child, True, alpha, beta, depth+1) + \
                        heuristic(child)
                    best_eval = min(best_eval, eval)
                    alpha = min(beta, eval)
                    if beta <= alpha:
                        break
    return best_eval


def heuristic(board):
    user_count = 0
    ai_count = 0

    # Itterate throguh all win configurations (defined in win_indexes)
    for win_configuration in win_indexes(len(board)):
        # Check if all row/column combinations of a given win configuration are either the User icon or empty
        if all((board[r][c] == user or board[r][c] == ' ') for r, c in win_configuration):
            # Add 1 to the count for each configuration that could result in a win
            user_count += 1
        # Check if all row/column combinations of a given win configuration are either the AI icon or empty
        if all((board[r][c] == ai or board[r][c] == ' ') for r, c in win_configuration):
            # Add 1 to the count for each configuration that could result in a win
            ai_count += 1
    """
    We subtract the minimzing players (User) win configuration count, from the maximizing players (AI) win configuration count
        - Negative result: the minimizing player (User) has more win configurations available
        - Positive result: the maximizing player (AI) has more win configurations available
        - 0 result: both players have the same number of win configurations available
    """
    return ai_count - user_count


def evaluate_board(board):
    scores = {
        user: -10,
        ai: 10,
        "draw": 0,
    }
    # Check to see if there is a winner in the current board configuration
    if is_winner(board, user):
        # Return "X" if User has winning configuration.
        return scores[user]
    elif is_winner(board, ai):
        # Return "O" if AI has winning configuration.
        return scores[ai]
    else:
        if any(' ' in sublist for sublist in board):
            # If any of the indexes in board are empty, board is not a terminal state.
            return None
        else:
            # If there are no empty places, and no winner, this is a draw state.
            return scores["draw"]


def is_winner(board, player):
    # Takes the current board configuration and checks if player has won

    # For all of the (row, column) pairs generated in win_indexes
    for indexes in win_indexes(len(board)):
        # If all of these board positions contain the players icon
        if all(board[r][c] == player for r, c in indexes):
            # This is a win state
            return True
    # Else, if none of the win configurations are triggered
    return False


def win_indexes(n):
    # Gets all index pairs (row, column) for winning configuration checks
    # Indexes for all 3 Row checks
    for r in range(n):
        yield [(r, c) for c in range(n)]
    # Indexes for all 3 Column check
    for c in range(n):
        yield [(r, c) for r in range(n)]
    # Indexes for Diagonal check (top left to bottom right)
    yield [(i, i) for i in range(n)]
    # indexes for Diagonal check (top right to bottom left)
    yield [(i, n - 1 - i) for i in range(n)]


def ai_move(board):
    print(f"\nAI Evaluating Configurations\n\n(r,c): eval \n───────────")
    best_score = -inf

    # Itterate throguh all positions on the board
    for i in range(3):
        for j in range(3):
            # If the current position is empty
            if board[i][j] == ' ':
                # Create a copy of the board
                child = deepcopy(board)
                # Place the AI's icon in this position
                child[i][j] = ai
                # Retrieve a score for the modified board
                score = minmax(child, False)
                print(f"({i},{j}): {score}")
                # If the score at this position is the best score
                if score > best_score:
                    # Store the score and position
                    best_score = score
                    best_move = (i, j)
            else:
                print(f"({i},{j}): N/A")
    # Once we've gone through all available board positions
    # Place the AI's icon in the position of the best move
    board[best_move[0]][best_move[1]] = ai
    display_board(board)
    return board


def user_move(board):
    user_position = 0
    while (1):
        # Loop over user input until we recieve a valid input
        try:
            user_position = int(input("Enter position (1-9): "))
        except ValueError:
            print("Invalid input!")

        # Calculate column and row from input
        column = (user_position - 1) % 3
        row = int((user_position - 1) / 3)

        # If the user input is 1-9 and the selected position is empty
        if user_position >= 1 and user_position <= 9 and board[row][column] == ' ':
            # apply the move and return the modified board
            board[row][column] = user
            display_board(board)
            return board


def display_board(board):
    # Utility function to diplay the board, and final winner/draw
    scores = {
        -10: "User",
        10: "AI",
    }
    print("")

    for i in range(3):
        print("", board[i][0], "│", board[i][1], "│", board[i][2])
        if i != 2:
            print("───┼───┼───")

    decision = evaluate_board(board)
    if decision != None:
        if decision == "draw":
            print(f"\nIts a Draw!")
        else:
            print(f"\n{scores[decision]} WINS!")
        quit()
    else:
        print("")


if __name__ == "__main__":
    # Define the board
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]

    # Display the initial board
    display_board(board)
    turn = 0
    # Get user input for turn selection
    while turn is not "y" and turn is not "n":
        turn = input("Your Turn First? (y/n): ")

    while(1):
        # Main loop
        if turn == "y":
            # User turn first
            board = user_move(board)
            board = ai_move(board)
        elif turn == "n":
            # AI move first
            board = ai_move(board)
            board = user_move(board)


# FIXED PLY: state in writing that to turn to fixed ply you terminate at specified depth
# Add alpha beta pruning

"""
This evaluation is made up of 3 parts

The first 2 parts of the eval are calculated once minmax() finds a terminal state.
At this point minmax() will return both:
    1) The terminal state evaluation,
        - For a winning terminal state, we get: 10
        - For a losing terminal state, we get: -10
        - For a drawing terminal state, we get: 0
    2) penalizing this evaluation based on depth.
        -For maximizing player, reduce eval by depth
        -For minimizing player, increase eval by depth

3) The third part of the evauation is the heuristic.
    This is added to the eval at each depth of minmax()
    This will make minmax select the position that:
        -minimizes oppositions available moves,
        -and maximizes current players available moves
"""
