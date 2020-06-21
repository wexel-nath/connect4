import copy

from numpy import zeros

COLUMNS = 7
ROWS = 6
EMPTY_CELL = 0


class Board:
    def __init__(self):
        self.board = zeros((ROWS, COLUMNS))
        self.history = []

    def print(self):
        pass
        for row in self.board[::-1]:
            print("| " + " | ".join(str(int(c)) for c in row) + " |")
        print()

    def drop_piece(self, position: int, player: int):
        for row in range(ROWS):
            if self.board[row][position] == 0:
                self.board[row][position] = player
                self.history.append(copy.deepcopy(self.board))
                return row
        return -1

    def val(self, row: int, column: int):
        try:
            if row >= 0 and column >= 0:
                return int(self.board[row][column])
        except IndexError:
            pass
        return 0

    def is_win(self, player: int, row: int, column: int, r_delta: int, c_delta: int):
        board_slice = []
        for d in range(-3, 4):
            board_slice.append(self.val(row + d*r_delta, column + d*c_delta))
        for i in range(4):
            if (
                player == board_slice[i]
                and player == board_slice[i+1]
                and player == board_slice[i+2]
                and player == board_slice[i+3]
            ):
                return True
        return False

    def is_winner(self, player: int, row: int, column: int):
        if self.is_win(player, row, column, 0, 1):
            return "horizontal"
        if self.is_win(player, row, column, 1, 0):
            return "vertical"
        if self.is_win(player, row, column, 1, 1):
            return "positive diagonal"
        if self.is_win(player, row, column, -1, 1):
            return "negative diagonal"
        return ""

    def get_valid_moves(self):
        return [i+1 for i, v in enumerate(self.board[ROWS-1]) if v == EMPTY_CELL]
