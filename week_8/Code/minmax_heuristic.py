from math import inf
from copy import deepcopy

player = "X"
ai = "O"

scores = {
    "X": -10,
    "O": 10,
    "tie": 0,
}


# FIXED PLY: state in writing that to turn to fixed ply you terminate at specified depth
# Add alpha beta pruning

def minmax(board, depth, is_maximizing_player):
    eval = evaluate_board(board)
    if eval != None:
        return scores[eval] + depth if is_maximizing_player else scores[eval] - depth

    if is_maximizing_player:
        best_eval = -inf
    else:
        best_eval = inf

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == ' ':
                child = deepcopy(board)
                if is_maximizing_player:
                    child[i][j] = ai
                    eval = minmax(child, depth+1, False) + \
                        heuristic(child) + depth
                    best_eval = max(best_eval, eval)
                else:
                    child[i][j] = player
                    eval = minmax(child, depth+1, True) + \
                        heuristic(child) + depth
                    best_eval = min(best_eval, eval)
    return best_eval


def heuristic(board):
    # count all winning lines open to max and subtract all winning lines open to MIN
    player_count = 0
    ai_count = 0
    for indexes in win_indexes(len(board)):
        if all((board[r][c] == player or board[r][c] == ' ') for r, c in indexes):
            player_count += 1
        if all((board[r][c] == ai or board[r][c] == ' ') for r, c in indexes):
            ai_count += 1
    return ai_count - player_count


def evaluate_board(board):
    if is_winner(board, player):
        return player
    elif is_winner(board, ai):
        return ai
    else:
        if any(' ' in sublist for sublist in board):
            return None
        else:
            return "tie"


def win_indexes(n):
    # Rows
    for r in range(n):
        yield [(r, c) for c in range(n)]
    # Columns
    for c in range(n):
        yield [(r, c) for r in range(n)]
    # Diagonal top left to bottom right
    yield [(i, i) for i in range(n)]
    # Diagonal top right to bottom left
    yield [(i, n - 1 - i) for i in range(n)]


def is_winner(board, decorator):
    for indexes in win_indexes(len(board)):
        if all(board[r][c] == decorator for r, c in indexes):
            return True
    return False


def ai_move(board):
    print("Calculating optimal move...")
    print("")
    best_score = -inf

    for i in range(3):
        for j in range(3):

            if board[i][j] == ' ':
                child = deepcopy(board)
                child[i][j] = ai
                score = minmax(child, 0, False)
                # print(i, j, ":", score)
                print(f"{i},{j}: {score}")
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
            else:
                print(f"{i},{j}: N/A")

    board[best_move[0]][best_move[1]] = ai
    display_board(board)
    return board


def display_board(board):
    print("")

    for i in range(3):
        print("", board[i][0], "│", board[i][1], "│", board[i][2])
        if i != 2:
            print("───┼───┼───")
    print("")

    decision = evaluate_board(board)
    if decision != None:
        if decision == "tie":
            print("Its a Draw!")
        else:
            print(decision, "WINS!")
        quit()


if __name__ == "__main__":
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]

    display_board(board)

    def player_move(board):
        position = 0
        while (1):
            try:
                position = int(input("Enter position (1-9): "))
            except ValueError:
                print("Invalid input!")
            except Exception as e:
                print(e)

            column = (position - 1) % 3
            row = int((position - 1) / 3)

            if position >= 1 and position <= 9 and board[row][column] == ' ':
                board[row][column] = player
                display_board(board)
                return board

    while(1):
        board = ai_move(board)
        board = player_move(board)
