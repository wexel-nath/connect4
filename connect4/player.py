from copy import deepcopy

import logger
from board import Board
from model.move_classification import Model
from random import randint


class PlayerInterface:
    def __init__(self, id: int):
        self.id = id

    def get_position(self, board: Board, turn: int):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def print_win_msg(self, win: str):
        logger.debug("{} wins on the {}!", self.get_name(), win)


class HumanPlayer(PlayerInterface):
    def get_position(self, board: Board, turn: int):
        position = -1
        moves = board.get_valid_moves()
        while position not in moves:
            f = "{n} to move, enter {m}: "
            pos = input(f.format(n=self.get_name(), m=moves))
            try:
                position = int(pos)
            except:
                position = -1

        return position

    def get_name(self):
        return "Player {p}".format(p=self.id)


class RandomPlayer(PlayerInterface):
    def get_position(self, board: Board, turn: int):
        moves = board.get_valid_moves()
        position = moves[randint(0, len(moves) - 1)]
        return position

    def get_name(self):
        return "Random {p}".format(p=self.id)


class NeuralPlayer(RandomPlayer):
    def __init__(self, id: int, model: Model):
        super().__init__(id)
        self.model = model

    def get_position(self, board: Board, turn: int):
        if turn <= 3:
            # random position for first 2 (each) turns of the game
            return super().get_position(board, turn)

        logger.debug("GET POSITION-------------------------------")
        return self.model.predict(board, self.id)

    def get_name(self):
        return "Neural {p}".format(p=self.id)
