import math
import random

DEPTH_LIMIT = 6


class Connect4:

    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.game_over = False
        self.level = ""

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
        print('+-+-+-+-+-+-+')

    def get_column(self):
        if self.current_player == 1:
            # Human player
            while True:
                try:
                    column = int(input(f'Player {self.current_player}, choose a column (1-7): ')) - 1
                    if column < 0 or column > 6:
                        print('Invalid column. Please choose a number between 1 and 7.')
                    elif self.board[0][column] != ' ':
                        print('Column is full. Please choose another column.')
                    else:
                        return column
                except ValueError:
                    print('Invalid input. Please enter a number between 1 and 7.')
        else:
            # AI player
            _, column = self.minimax(self.board, DEPTH_LIMIT, True)
            return column

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                if self.current_player == 1:
                    self.board[row][column] = str("X")
                else:
                    self.board[row][column] = str("O")
                return

    def check_win(self):
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != ' ':
                    return True

        for col in range(len(self.board[0])):
            for i in range(len(self.board) - 3):
                if self.board[i][col] == self.board[i + 1][col] == self.board[i + 2][col] == self.board[i + 3][col] and \
                        self.board[i][col] != ' ':
                    return True

        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == \
                        self.board[row + 3][col + 3] and self.board[row][col] != ' ':
                    return True

        for row in range(3, len(self.board)):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == \
                        self.board[row - 3][col + 3] and self.board[row][col] != ' ':
                    return True

        return False

    # TYPE 1 completely random (not optimal by any means but quick)x
    def rand_ai_move(self):
        valid_moves = [i for i in range(7) if self.board[0][i] == ' ']
        return random.choice(valid_moves)

# Extremely simple evaluation that checks for a possible 4 in a row (if it doesn't know what to do place in first
    # possible spot)
    def evaluate_easy(self, board):
        if self.current_player == 2 and self.check_win():
            return 100
        elif self.current_player == 1 and self.check_win():
            return -100
        return 0

    # Checks for wins but also takes into account 2 in a row and 3 in a rows as well.
    def evaluate_medium(self, board):
        score = 0
        for row in board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != ' ':
                    if row[i] == 'O':
                        return -100
                    else:
                        return 100
                if row[i:i + 4].count('O') == 3 and row[i:i + 4].count(' ') == 1:
                    score += 50
                elif row[i:i + 4].count('X') == 3 and row[i:i + 4].count(' ') == 1:
                    score -= 50
                elif row[i:i + 4].count('O') == 2 and row[i:i + 4].count(' ') == 2:
                    score += 10
                elif row[i:i + 4].count('X') == 2 and row[i:i + 4].count(' ') == 2:
                    score -= 10

        for col in range(len(board[0])):
            for i in range(len(board) - 3):
                if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] and board[i][
                    col] != ' ':
                    if board[i][col] == 'O':
                        return -100
                    else:
                        return 100
                if [board[j][col] for j in range(i, i + 4)].count('O') == 3 and [board[j][col] for j in
                                                                                 range(i, i + 4)].count(' ') == 1:
                    score += 50
                elif [board[j][col] for j in range(i, i + 4)].count('X') == 3 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 1:
                    score -= 50
                elif [board[j][col] for j in range(i, i + 4)].count('O') == 2 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 2:
                    score += 10
                elif [board[j][col] for j in range(i, i + 4)].count('X') == 2 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 2:
                    score -= 10

        # Check for diagonal wins (top-left to bottom-right)
        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] and \
                        board[row][col] != ' ':
                    if board[row][col] == 'O':
                        return -100
                    else:
                        return 100
                if [board[row + j][col + j] for j in range(4)].count('O') == 3 and [board[row + j][col + j] for j in
                                                                                    range(4)].count(' ') == 1:
                        score += 50
                elif [board[row + j][col + j] for j in range(4)].count('X') == 3 and [board[row + j][col + j] for j
                                                                                          in range(4)].count(' ') == 1:
                        score -= 50
                elif [board[row+j][col+j] for j in range(4)].count('O') == 2 and [board[row+j][col+j] for j in range(4)].count(' ') == 2:
                        score += 10
                elif [board[row+j][col+j] for j in range(4)].count('X') == 2 and [board[row+j][col+j] for j in range(4)].count(' ') == 2:
                        score -= 10
                for row in range(3, len(board)):
                    for col in range(len(board[0]) - 3):
                        if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][
                            col + 3] and \
                                board[row][col] != ' ':
                            if board[row][col] == 'O':
                                return -100
                            else:
                                return 100
                        if [board[row - j][col + j] for j in range(4)].count('O') == 3 and [board[row - j][col + j] for j in
                                                                                                range(4)].count(' ') == 1:
                                score += 50
                        elif [board[row - j][col + j] for j in range(4)].count('X') == 3 and [board[row - j][col + j] for j in
                                                                                              range(4)].count(' ') == 1:
                                score -= 50
                        elif [board[row - j][col + j] for j in range(4)].count('O') == 2 and [board[row - j][col + j] for j in
                                                                                              range(4)].count(' ') == 2:
                                score += 10
                        elif [board[row - j][col + j] for j in range(4)].count('X') == 2 and [board[row - j][col + j] for j in
                                                                                              range(4)].count(' ') == 2:
                                score -= 10

                return score

    def minimax(self, board, depth, maximizing):
        if depth == 0 or self.game_over:
            if self.level == "easy":
                return self.evaluate_easy(board), -1
            elif self.level == "medium":
                return self.evaluate_medium(board), -1

        if maximizing:
            best_score = float('-inf')
            best_column = -1
            for col in range(7):
                if board[0][col] == ' ':
                    row = self.get_next_open_row(board, col)
                    board[row][col] = 'X'
                    score, _ = self.minimax(board, depth - 1, False)
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_column = col
            return best_score, best_column
        else:
            best_score = float('inf')
            best_column = -1
            for col in range(7):
                if board[0][col] == ' ':
                    row = self.get_next_open_row(board, col)
                    board[row][col] = 'O'
                    score, _ = self.minimax(board, depth - 1, True)
                    board[row][col] = ' '
                    if score < best_score:
                        best_score = score
                        best_column = col
            return best_score, best_column

    def get_next_open_row(self, board, col):
        for row in range(5, -1, -1):
            if board[row][col] == ' ':
                return row
        return -1

    def undo_move(self, column):
        for row in range(6):
            if self.board[row][column] != ' ':
                self.board[row][column] = ' '
                break



def play_game():
    """
    Main function to play the game
    """
    game = Connect4()
    print("Welcome to Connect 4!")
    while game.level == "":
        prompt = "Difficulty:" + "\n\t1.Easy" + "\n\t2.Medium" + "\n\t3.Hard\n"
        option = int(input(prompt))
        if option == 1:
            game.level = "easy"
        elif option == 2:
            game.level = "medium"
        elif option == 3:
            game.level = "hard"
        else:
            "Invalid choice "+str(option)
    game.print_board()

    while not game.game_over:
        if game.current_player == 1:
            column = game.get_column()
            game.make_move(column)
        else:
            column = game.minimax(game.board, DEPTH_LIMIT, True)
            game.make_move(column[1])

        game.print_board()

        if game.check_win():
            print(f"Player {game.current_player} wins!")
            game.game_over = True

        if all([piece != ' ' for row in game.board for piece in row]):
            print("Tie game.")
            game.game_over = True

        game.current_player = 3 - game.current_player


if __name__ == '__main__':
    play_game()