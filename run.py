from numpy import zeros
from random import randint

COLUMNS = 7
ROWS = 6


class Board:
    def __init__(self):
        self.game_board = zeros((ROWS, COLUMNS))

    def print(self):
        for row in self.game_board[::-1]:
            print("| " + " | ".join(str(int(c)) for c in row) + " |")
        print()

    def drop_piece(self, position: int, player: int):
        for row in range(ROWS):
            if self.game_board[row][position] == 0:
                self.game_board[row][position] = player
                return row
        return -1

    def val(self, row: int, column: int):
        try:
            if row >= 0 and column >= 0:
                return int(self.game_board[row][column])
        except IndexError:
            pass
        return -1

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


class PlayerInterface:
    def __init__(self, id: int):
        self.id = id

    def get_position(self, game_board: tuple):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def print_win_msg(self, win: str):
        f = "{n} wins on the {w}!"
        print(f.format(n=self.get_name(), w=win))


class HumanPlayer(PlayerInterface):
    def get_position(self, game_board: tuple):
        pos = ""
        while pos == "":
            f = "{n} to move, enter 1-7: "
            pos = input(f.format(n=self.get_name()))

        position = int(pos)
        if position < 1:
            position = 1
        if position > COLUMNS:
            position = COLUMNS
        return position-1

    def get_name(self):
        return "Player {p}".format(p=self.id)


class ComputerPlayer(PlayerInterface):
    def get_position(self, game_board: tuple):
        # just return a random int for now
        position = randint(1, COLUMNS)
        print("{n} enters {p}".format(n=self.get_name(), p=position))
        return position-1

    def get_name(self):
        return "Computer {p}".format(p=self.id)


def run():
    turn = 0
    board = Board()
    player_one = ComputerPlayer(1)
    player_two = ComputerPlayer(2)
    playing = True

    while playing:
        board.print()
        player = player_one if turn % 2 == 0 else player_two
        position = player.get_position(board.game_board)

        row = board.drop_piece(position, player.id)
        if not row == -1:
            turn += 1
            win = board.is_winner(player.id, row, position)
            if not win == "":
                playing = False
                player.print_win_msg(win)
        else:
            print("That column is full, try again")
            print()

    board.print()


run()
