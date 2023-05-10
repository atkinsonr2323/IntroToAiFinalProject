import math
import random
import time
import tracemalloc

DEPTH_LIMIT = 4



class Colors:
    P1 = '\033[94m'
    P2 = '\033[91m'
    BOARD = '\33[33m'
    ENDC = '\033[0m'

x_mark = str(f"{Colors.P1}X{Colors.ENDC}")
o_mark = str(f"{Colors.P2}O{Colors.ENDC}")
class Connect4:

    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.game_over = False
        self.level_player1 = ""
        self.level_player2 = ""
        self.style = ""

    def print_board(self):
        for row in self.board:
            print(f'{Colors.BOARD}|{Colors.ENDC}'.join(row))
        print(f'{Colors.BOARD}-+-+-+-+-+-+-{Colors.ENDC}\n')

    def get_column(self):
        if self.current_player == 1:
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
            score, column = self.minimax(self.board, DEPTH_LIMIT, True)
            return column

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == ' ':
                if self.current_player == 1:
                     self.board[row][column] = str(f"{Colors.P1}X{Colors.ENDC}")
                else:
                     self.board[row][column] = str(f"{Colors.P2}O{Colors.ENDC}")
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

    def get_random_column(self):
        available_columns = [col for col in range(7) if self.board[0][col] == ' ']
        return random.choice(available_columns) if available_columns else None

    def evaluate_simple(self, board):
        if self.current_player == 2 and self.check_win():
            return 100
        elif self.current_player == 1 and self.check_win():
            return -100
        return 0

    # Checks for wins but also takes into account 2 in a row and 3 in a rows as well.
    def evaluate_block_pref(self, board):
        score = 0
        for row in board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != ' ':
                    if row[i] == o_mark:
                        return -100
                    else:
                        return 100
                if row[i:i + 4].count(o_mark) == 3 and row[i:i + 4].count(' ') == 1:
                    score += 50
                elif row[i:i + 4].count(x_mark) == 3 and row[i:i + 4].count(' ') == 1:
                    score -= 50
                elif row[i:i + 4].count(o_mark) == 2 and row[i:i + 4].count(' ') == 2:
                    score += 10
                elif row[i:i + 4].count(x_mark) == 2 and row[i:i + 4].count(' ') == 2:
                    score -= 10

        for col in range(len(board[0])):
            for i in range(len(board) - 3):
                if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] and board[i][col] != ' ':
                    if board[i][col] == o_mark:
                        return -100
                    else:
                        return 100
                if [board[j][col] for j in range(i, i + 4)].count(o_mark) == 3 and [board[j][col] for j in
                                                                                 range(i, i + 4)].count(' ') == 1:
                    score += 50
                elif [board[j][col] for j in range(i, i + 4)].count(x_mark) == 3 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 1:
                    score -= 50
                elif [board[j][col] for j in range(i, i + 4)].count(o_mark) == 2 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 2:
                    score += 10
                elif [board[j][col] for j in range(i, i + 4)].count(x_mark) == 2 and [board[j][col] for j in
                                                                                   range(i, i + 4)].count(' ') == 2:
                    score -= 10

        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] and \
                        board[row][col] != ' ':
                    if board[row][col] == o_mark:
                        return -100
                    else:
                        return 100
                if [board[row + j][col + j] for j in range(4)].count(o_mark) == 3 and [board[row + j][col + j] for j in
                                                                                    range(4)].count(' ') == 1:
                    score += 50
                elif [board[row + j][col + j] for j in range(4)].count(x_mark) == 3 and [board[row + j][col + j] for j
                                                                                      in range(4)].count(' ') == 1:
                    score -= 50
                elif [board[row + j][col + j] for j in range(4)].count(o_mark) == 2 and [board[row + j][col + j] for j in
                                                                                      range(4)].count(' ') == 2:
                    score += 10
                elif [board[row + j][col + j] for j in range(4)].count(x_mark) == 2 and [board[row + j][col + j] for j in
                                                                                      range(4)].count(' ') == 2:
                    score -= 10
                for row in range(3, len(board)):
                    for col in range(len(board[0]) - 3):
                        if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][
                            col + 3] and \
                                board[row][col] != ' ':
                            if board[row][col] == o_mark:
                                return -100
                            else:
                                return 100
                        if [board[row - j][col + j] for j in range(4)].count(o_mark) == 3 and [board[row - j][col + j] for
                                                                                            j in
                                                                                            range(4)].count(' ') == 1:
                            score += 50
                        elif [board[row - j][col + j] for j in range(4)].count(x_mark) == 3 and [board[row - j][col + j]
                                                                                              for j in
                                                                                              range(4)].count(' ') == 1:
                            score -= 50
                        elif [board[row - j][col + j] for j in range(4)].count(o_mark) == 2 and [board[row - j][col + j]
                                                                                              for j in
                                                                                              range(4)].count(' ') == 2:
                            score += 10
                        elif [board[row - j][col + j] for j in range(4)].count(x_mark) == 2 and [board[row - j][col + j]
                                                                                              for j in
                                                                                              range(4)].count(' ') == 2:
                            score -= 10

                return score

    def evaluate_loc_pref(self, board):
        # Define weights for different scenarios
        edge_weight = 10
        center_weight = 5
        vertical_weight = 4
        horizontal_weight = 4
        diagonal_weight = 8
        block_2_weight = 2
        block_3_weight = 6

        score = 0
        num_rows = len(board)
        num_cols = len(board[0])

        for row in range(num_rows):
            for col in range(num_cols - 3):
                window = board[row][col:col + 4]
                score += self.evaluate_window(window, horizontal_weight, block_2_weight, block_3_weight)

        for col in range(num_cols):
            for row in range(num_rows - 3):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, vertical_weight, block_2_weight, block_3_weight)

        for row in range(num_rows - 3):
            for col in range(num_cols - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, diagonal_weight, block_2_weight, block_3_weight)

        for row in range(3, num_rows):
            for col in range(num_cols - 3):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, diagonal_weight, block_2_weight, block_3_weight)

        center_col = num_cols // 2
        center_window = [board[row][center_col] for row in range(num_rows)]
        center_count = center_window.count(x_mark) - center_window.count(o_mark)
        score += center_count * center_weight

        edge_window = [board[row][0] for row in range(num_rows)] + [board[row][num_cols - 1] for row in range(num_rows)]
        edge_count = edge_window.count(x_mark) - edge_window.count(o_mark)
        score += edge_count * edge_weight
        return score

    # Helper function to evaluate a window of 4 cells
    def evaluate_window(self, window, weight, block_2_weight, block_3_weight):
        score = 0
        num_X = window.count(x_mark)
        num_O = window.count(o_mark)
        num_empty = window.count(' ')
        if num_X == 4:
            score += 1000
        elif num_O == 4:
            score -= 1000
        elif num_X == 3 and num_empty == 1:
            score += block_3_weight
        elif num_O == 3 and num_empty == 1:
            score -= block_3_weight
        elif num_X == 2 and num_empty == 2:
            score += block_2_weight
        elif num_O == 2 and num_empty == 2:
            score -= block_2_weight
        score += weight * (num_X - num_O)
        return score

    def benchmark_evaluate(self, evaluation_method, board):
        """
        Benchmarking method for measuring time and memory usage of an evaluation method argument.

        Returns the score of the evaluation method, elapsed time in seconds, and peak traced memory
        block size in bytes.
        """
        start_time = time.perf_counter()
        tracemalloc.start()

        score = evaluation_method(board)

        memory_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return score, elapsed_time, memory_usage[1]

    def benchmark_evaluation_p1(self, board):
        """
        Helper method for selecting correct evaluation method when benchmarking player one's turn.

        Returns the score from the evaluation method, the elapsed time in seconds, the peak traced
        memory block size in bytes, and a placeholder for the 'best' column.
        """
        if self.level_player1 == "simple":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_simple, board)
            return score, elapsed, memory, -1
        elif self.level_player1 == "block":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_block_pref, board)
            return score, elapsed, memory, -1
        elif self.level_player1 == "loc":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_loc_pref, board)
            return score, elapsed, memory, -1

    def benchmark_evaluation_p2(self, board):
        """
        Helper method for selecting correct evaluation method when benchmarking player two's turn.

        Returns the score from the evaluation method, the elapsed time in seconds, the peak traced
        memory block size in bytes, and a placeholder for the 'best' column.
        """
        if self.level_player2 == "simple":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_simple, board)
            return score, elapsed, memory, -1
        elif self.level_player2 == "block":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_block_pref, board)
            return score, elapsed, memory, -1
        elif self.level_player2 == "loc":
            score, elapsed, memory = self.benchmark_evaluate(self.evaluate_loc_pref, board)
            return score, elapsed, memory, -1

    def benchmarked_minimax(self, board, depth, maximizing):
        """
        Minimax algorithm with time and memory benchmarking
        """
        total_mem = 0
        total_time = 0
        if self.current_player == 1 and (depth == 0 or self.game_over):
            return self.benchmark_evaluation_p1(board)
        elif self.current_player == 2 and (depth == 0 or self.game_over):
            return self.benchmark_evaluation_p2(board)
        if maximizing:
            best_score = float('-inf')
            elapsed = 0
            memory = 0
            best_column = -1
            for col in range(7):
                if board[0][col] == ' ':
                    row = self.get_next_open_row(board, col)
                    board[row][col] = x_mark
                    score, elapsed, memory, _ = self.benchmarked_minimax(board, depth - 1, False)
                    total_time += elapsed
                    total_mem += memory
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_column = col
            return best_score, elapsed, memory, best_column
        else:
            best_score = float('inf')
            elapsed = 0
            memory = 0
            best_column = -1
            for col in range(7):
                if board[0][col] == ' ':
                    row = self.get_next_open_row(board, col)
                    board[row][col] = o_mark
                    score, elapsed, memory, _ = self.benchmarked_minimax(board, depth - 1, True)
                    total_time += elapsed
                    total_mem += memory
                    board[row][col] = ' '
                    if score < best_score:
                        best_score = score
                        best_column = col
            return best_score, total_time, total_mem, best_column

    def minimax(self, board, depth, maximizing):
        if self.current_player == 1 and (depth == 0 or self.game_over):
            if self.level_player1 == "simple":
                return self.evaluate_simple(board), -1
            elif self.level_player1 == "block":
                return self.evaluate_block_pref(board), -1
            elif self.level_player1 == "loc":
                return self.evaluate_loc_pref(board), -1
        elif self.current_player == 2 and (depth == 0 or self.game_over):
            if self.level_player2 == "simple":
                return self.evaluate_simple(board), -1
            elif self.level_player2 == "block":
                return self.evaluate_block_pref(board), -1
            elif self.level_player2 == "loc":
                return self.evaluate_loc_pref(board), -1
        if maximizing:
            best_score = float('-inf')
            best_column = -1
            for col in range(7):
                if board[0][col] == ' ':
                    row = self.get_next_open_row(board, col)
                    board[row][col] = x_mark
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
                    board[row][col] = o_mark
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
    while game.style == "":
        prompt = "Style:" + "\n\t1.Player vs AI" + "\n\t2.AI vs AI" \
                 + "\n\t3.Benchmarked Player vs AI" + "\n\t4.Benchmarked AI vs AI" + "\n\t5. Ai Vs Random\n"
        try:
            option = int(input(prompt))
            if option == 1:
                game.style = "pva"
            if option == 2:
                game.style = "ava"
            if option == 3:
                game.style = "bpva"
            if option == 4:
                game.style = "bava"
            if option == 5:
                game.style = "avr"
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 4.')

    if game.style == "pva":
        while game.level_player2 == "":
            prompt = "Difficulty:" + "\n\t1.Simple" + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player2 = "simple"
                elif option == 2:
                    game.level_player2 = "block"
                elif option == 3:
                    game.level_player2 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
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

    if game.style == "ava":
        while game.level_player1 == "":
            prompt = f"Difficulty for P1:" + "\n\t1.Simple" \
                     + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player1 = "simple"
                elif option == 2:
                    game.level_player1 = "block"
                elif option == 3:
                    game.level_player1 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
        while game.level_player2 == "":
            prompt = f"Difficulty for P2:" + "\n\t1.Simple" \
                     + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player2 = "simple"
                elif option == 2:
                    game.level_player2 = "block"
                elif option == 3:
                    game.level_player2 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
        game.print_board()

        while not game.game_over:
            if game.current_player == 1:
                column = game.minimax(game.board, DEPTH_LIMIT, True)
                game.make_move(column[1])
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

    if game.style == "bpva":
        while game.level_player2 == "":
            prompt = "Difficulty:" + "\n\t1.Simple" + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player2 = "simple"
                elif option == 2:
                    game.level_player2 = "block"
                elif option == 3:
                    game.level_player2 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
        game.print_board()

        while not game.game_over:
            if game.current_player == 1:
                column = game.get_column()
                game.make_move(column)
            else:
                start_time = time.perf_counter()
                column = game.benchmarked_minimax(game.board, DEPTH_LIMIT, True)
                end_time = time.perf_counter()
                print(f'Time elapsed: {end_time-start_time}')
                print(f'Memory usage: {column[2]}')
                game.make_move(column[3])

            game.print_board()

            if game.check_win():
                print(f"Player {game.current_player} wins!")
                game.game_over = True

            if all([piece != ' ' for row in game.board for piece in row]):
                print("Tie game.")
                game.game_over = True

            game.current_player = 3 - game.current_player

    if game.style == "bava":
        while game.level_player1 == "":
            prompt = "Difficulty for P1:" + "\n\t1.Simple" \
                     + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player1 = "simple"
                elif option == 2:
                    game.level_player1 = "block"
                elif option == 3:
                    game.level_player1 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
        while game.level_player2 == "":
            prompt = f"Difficulty for P2:" + "\n\t1.Simple" \
                     + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player2 = "simple"
                elif option == 2:
                    game.level_player2 = "block"
                elif option == 3:
                    game.level_player2 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')
        game.print_board()

        while not game.game_over:
            if game.current_player == 1:
                start_time = time.perf_counter()
                column = game.benchmarked_minimax(game.board, DEPTH_LIMIT, True)
                end_time = time.perf_counter()
                print(f'Time elapsed: {end_time-start_time}')
                print(f'Memory usage: {column[2]}')
                game.make_move(column[3])
            else:
                start_time = time.perf_counter()
                column = game.benchmarked_minimax(game.board, DEPTH_LIMIT, True)
                end_time = time.perf_counter()
                print(f'Time elapsed: {end_time-start_time}')
                print(f'Memory usage: {column[2]}')
                game.make_move(column[3])

            game.print_board()

            if game.check_win():
                print(f"Player {game.current_player} wins!")
                game.game_over = True

            if all([piece != ' ' for row in game.board for piece in row]):
                print("Tie game.")
                game.game_over = True

            game.current_player = 3 - game.current_player
    if game.style == "avr":
        while game.level_player1 == "":
            prompt = f"Difficulty for P1:" + "\n\t1.Simple" \
                     + "\n\t2.Block Preference" + "\n\t3.Location Preference\n"
            try:
                option = int(input(prompt))
                if option == 1:
                    game.level_player1 = "simple"
                elif option == 2:
                    game.level_player1 = "block"
                elif option == 3:
                    game.level_player1 = "loc"
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 3.')

        game.print_board()

        while not game.game_over:
            if game.current_player == 1:
                column = game.minimax(game.board, DEPTH_LIMIT, True)
                game.make_move(column[1])
            else:
                column = game.get_random_column()
                game.make_move(column)

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
