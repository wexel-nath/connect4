import numpy as np

COLUMNS = 7
ROWS = 6

PLAYER_ONE = 1
PLAYER_TWO = 2


class Board:
    def __init__(self):
        self.game_board = np.zeros((ROWS, COLUMNS))

    def print(self):
        for row in self.game_board:
            print("| " + " | ".join(str(int(c)) for c in row) + " |")
        print()

    def drop_piece(self, position, player):
        for row in range(ROWS-1, 0, -1):
            if self.game_board[row][position] == 0:
                self.game_board[row][position] = player
                return row
        return -1

    def val(self, row, column):
        try:
            return int(self.game_board[row][column])
        except IndexError:
            pass
        return 0

    def is_win(self, player, row, column, r_delta, c_delta):
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

    def is_winner(self, player, row, column):
        return (
            self.is_win(player, row, column, 0, 1)
            or self.is_win(player, row, column, 1, 0)
            or self.is_win(player, row, column, 1, 1)
            or self.is_win(player, row, column, -1, 1)
        )


def handle_move(turn):
    player = PLAYER_ONE if turn % 2 == 0 else PLAYER_TWO

    position = ""
    while position == "":
        position = input("Player {p} to move, enter 1-7: ".format(p=player))
    print()

    position = int(position)
    if position < 1:
        position = 1
    if position > COLUMNS:
        position = COLUMNS
    return position-1, player


def run():
    turn = 0
    board = Board()
    playing = True

    while playing:
        board.print()
        position, player = handle_move(turn)

        row = board.drop_piece(position, player)
        if not row == -1:
            turn += 1
            if board.is_winner(player, row, position):
                playing = False
                print("Player {p} wins!".format(p=player))
        else:
            print("That column is full, try again")
            print()

    board.print()


run()
