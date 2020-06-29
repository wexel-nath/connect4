import copy

import logger
from numpy import zeros

COLUMNS = 7
ROWS = 6
EMPTY_CELL = 0


class Board:
    def __init__(self):
        self.board = zeros((ROWS, COLUMNS))
        self.history = []

    def print(self):
        logger.debug("CONNECT 4")
        for row in self.board:
            logger.debug("| " + " | ".join(str(int(c)) for c in row) + " |")

    def drop_piece(self, position: int, player: int):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][position] == 0:
                self.board[row][position] = player
                return row
        return -1

    def val(self, row: int, column: int):
        try:
            if row >= 0 and column >= 0:
                return int(self.board[row][column])
        except IndexError:
            pass
        return EMPTY_CELL

    def is_win(self, player: int, row: int, column: int, r_delta: int, c_delta: int):
        board_slice = []
        for d in range(-3, 4):
            board_slice.append(
                self.val(row + d * r_delta, column + d * c_delta))
        for i in range(4):
            if (
                player == board_slice[i]
                and player == board_slice[i + 1]
                and player == board_slice[i + 2]
                and player == board_slice[i + 3]
            ):
                self.history.append(copy.deepcopy(self.board))
                logger.debug("Player {} won", player)
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
        return [i for i, v in enumerate(self.board[0]) if v == EMPTY_CELL]
