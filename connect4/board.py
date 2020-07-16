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
        self.state = PLAYING

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
            self.state = player
            return player
        if self.is_draw():
            self.state = DRAW
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
        return get_valid_actions(self.board)


def get_valid_actions(board):
    return [i for i, v in enumerate(board[0]) if v == EMPTY_CELL]


def static_eval(board, player, opponent):
    player_score = piece_eval(board, player, opponent)
    opponent_score = piece_eval(board, opponent, player)
    return player_score - opponent_score


def piece_eval(board, player, opponent):  # static evaluation of the current board state
    score = 0
    WINDOW_LENGTH = 4

    # Score center column
    score += evaluate_center(board, player, opponent)

    # Score Horizontal
    for r in range(ROWS):
        row_array = [i for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, player, opponent)

    # Score Vertical
    for c in range(COLUMNS):
        col_array = [i for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, player, opponent)

    # Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player, opponent)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player, opponent)

    return score


def evaluate_center(board, player, opponent):
    center_array = [i for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(player)
    return center_count * 3


def evaluate_window(window, player, opponent):  # evaluate score of current window
    score = 0

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY_CELL) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY_CELL) == 2:
        score += 2

    # BLOCK OPPONENTS TRIPLES
    if window.count(opponent) == 3 and window.count(EMPTY_CELL) == 1:
        score -= 4
    # elif window.count(opp_piece) == 2 and window.count(self.EMPTY_PIECE) == 2:
    #     score -= 9

    return score
