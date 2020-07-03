import random

import logger
from board import Board
from model import ModelInterface


class PlayerInterface:
    def __init__(self, id: int):
        self.id = id

    def get_action(self, board: Board, turn: int):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def print_win_msg(self, win: str):
        logger.debug("{} wins on the {}!", self.get_name(), win)


class HumanPlayer(PlayerInterface):
    def get_action(self, board: Board, turn: int):
        action = -1
        actions = board.get_valid_actions()
        while action not in actions:
            pos = input(f"{self.get_name()}'s turn, enter {actions}: ")
            try:
                action = int(pos)
            except:
                action = -1

        return action

    def get_name(self):
        return f"Player {self.id}"


class RandomPlayer(PlayerInterface):
    def get_action(self, board: Board, turn: int):
        actions = board.get_valid_actions()
        return random.choice(actions)

    def get_name(self):
        return f"Random {self.id}"


class NeuralPlayer(RandomPlayer):
    def __init__(self, id: int, model: ModelInterface):
        super().__init__(id)
        self.model = model

    def get_action(self, board: Board, turn: int):
        logger.debug("GET ACTION-------------------------------")
        return self.model.predict(board, self.id)

    def get_name(self):
        return f"Neural {self.id}"
