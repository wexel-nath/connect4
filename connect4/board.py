import copy

from numpy import zeros

import logger

COLUMNS = 7
ROWS = 6
EMPTY_CELL = 0

BOARD_DEBUG = False

PLAYING = 100
DRAW = 101
ILLEGAL_MOVE = 110


class Board:
    def __init__(self):
        self.board = zeros((ROWS, COLUMNS), dtype=int)

    def print(self):
        if not BOARD_DEBUG:
            return
        logger.debug("CONNECT 4")
        for row in self.board:
            logger.debug("| " + " | ".join(map(str, row)) + " |")

    def handle_action(self, action, player):
        row = self.drop_piece(action, player)
        if row == ILLEGAL_MOVE:
            return ILLEGAL_MOVE
        if self.is_winner(player, row, action):
            return player
        if self.is_draw():
            return DRAW
        return PLAYING

    def drop_piece(self, action: int, player: int):
        for row in reversed(range(ROWS)):
            if self.board[row][action] == 0:
                self.board[row][action] = player
                return row
        return ILLEGAL_MOVE

    def val(self, row: int, column: int):
        try:
            if row >= 0 and column >= 0:
                return int(self.board[row][column])
        except IndexError:
            pass
        return EMPTY_CELL

    def is_draw(self):
        for c in range(COLUMNS):
            if self.board[0][c] == EMPTY_CELL:
                return False
        return True

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

    def get_valid_actions(self):
        return [i for i, v in enumerate(self.board[0]) if v == EMPTY_CELL]
