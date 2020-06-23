import copy

from board import Board
from model import Model
from random import randint


class PlayerInterface:
    def __init__(self, id: int):
        self.id = id

    def get_position(self, board: Board, turn: int):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def print_win_msg(self, win: str):
        pass
        f = "{n} wins on the {w}!"
        print(f.format(n=self.get_name(), w=win))


class HumanPlayer(PlayerInterface):
    def get_position(self, board: Board, turn: int):
        position = 0
        moves = board.get_valid_moves()
        while position not in moves:
            f = "{n} to move, enter {m}: "
            pos = input(f.format(n=self.get_name(), m=moves))
            try:
                position = int(pos)
            except:
                position = 0

        return position-1

    def get_name(self):
        return "Player {p}".format(p=self.id)


class RandomPlayer(PlayerInterface):
    def get_position(self, board: Board, turn: int):
        moves = board.get_valid_moves()
        position = moves[randint(0, len(moves)-1)]
        # print("{n} enters {p}".format(n=self.get_name(), p=position))
        return position-1

    def get_name(self):
        return "Random {p}".format(p=self.id)


class NeuralPlayer(RandomPlayer):
    def __init__(self, id: int, model: Model, debug: bool):
        super().__init__(id)
        self.model = model
        self.debug = debug

    def get_position(self, board: Board, turn: int):
        if turn <= 3:
            # random position for first 2 (each) turns of the game
            return super().get_position(board, turn)

        if self.debug:
            print()
            print("GET POSITION-------------------------------")
            board.print()
        max_value = 0
        moves = board.get_valid_moves()
        best_move = moves[0]
        for move in moves:
            if self.debug:
                print("move:", move)
            board_copy = copy.deepcopy(board)
            board_copy.drop_piece(move-1, self.id)
            value = self.model.predict(board_copy.board, self.id, self.debug)
            if value > max_value:
                max_value = value
                best_move = move

        if self.debug:
            print("END-------------------------------")
            print("selected:", best_move)
            print()
        return best_move - 1

    def get_name(self):
        return "Neural {p}".format(p=self.id)
