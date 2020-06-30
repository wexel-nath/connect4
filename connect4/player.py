import random
from copy import deepcopy

import logger
from board import Board
from history import Move
from model.deep_q import Model

PLAYING = -2
DRAW = 0


class PlayerInterface:
    def __init__(self, id: int):
        self.id = id

    def get_action(self, board: Board, turn: int):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def learn(self, move: Move, next_board, result):
        pass

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

    def learn(self, move: Move, next_board, result):
        pass


class RandomPlayer(PlayerInterface):
    def get_action(self, board: Board, turn: int):
        actions = board.get_valid_actions()
        return random.choice(actions)

    def get_name(self):
        return f"Random {self.id}"

    def learn(self, move: Move, next_board, result):
        pass


class NeuralPlayer(RandomPlayer):
    def __init__(self, id: int, model: Model):
        super().__init__(id)
        self.model = model

    def get_action(self, board: Board, turn: int):
        # if turn <= 3:
        #     # random action for first 2 (each) turns of the game
        #     return super().get_action(board, turn)

        logger.debug("GET POSITION-------------------------------")
        return self.model.predict(board, self.id)

    def get_name(self):
        return f"Neural {self.id}"

    def learn(self, move: Move, next_board, result):
        self.model.remember(
            move.board,
            move.action,
            get_reward(self.id, result),
            next_board,
            result != PLAYING,
        )
        self.model.experience_replay()


def get_reward(player: int, result: int) -> int:
    if result in (DRAW, PLAYING):
        return 0
    if player == result:
        return 1
    return -1
