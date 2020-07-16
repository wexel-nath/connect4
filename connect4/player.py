from copy import deepcopy
import math
import random

import logger
from board import Board, DRAW, PLAYING, static_eval
from history import History
from model import ModelInterface
from util import get_full_file_path

PLAYER_ID = 1
OPPONENT_ID = -1


class PlayerInterface:
    def __init__(self, id: int, turn: int):
        self.id = id
        self.turn = turn

    def get_name(self):
        raise NotImplementedError

    def get_action(self, board: Board):
        raise NotImplementedError

    def learn(self, history: History):
        raise NotImplementedError

    def save(self, gen: int):
        raise NotImplementedError

    def print_win_msg(self, win: str):
        logger.debug("{} wins on the {}!", self.get_name(), win)


class HumanPlayer(PlayerInterface):
    def get_name(self):
        return f"Player {self.id}"

    def get_action(self, board: Board):
        action = -1
        actions = board.get_valid_actions()
        while action not in actions:
            pos = input(f"{self.get_name()}'s turn, enter {actions}: ")
            try:
                action = int(pos)
            except:
                action = -1

        return action

    def learn(self, history: History):
        pass

    def save(self, gen: int):
        pass


class RandomPlayer(PlayerInterface):
    def get_name(self):
        return f"Random {self.id}"

    def get_action(self, board: Board):
        actions = board.get_valid_actions()
        return random.choice(actions)

    def learn(self, history: History):
        pass

    def save(self, gen: int):
        pass


class NeuralPlayer(RandomPlayer):
    def __init__(self, id: int, model: ModelInterface, turn: int):
        super().__init__(id, turn)
        self.model = model

    def get_name(self):
        return f"Neural {self.id}"

    def get_action(self, board: Board):
        logger.debug("GET ACTION-------------------------------")
        return self.model.predict(board, self.id)

    def learn(self, history: History):
        self.model.train(history)

    def save(self, gen: int):
        filepath = get_full_file_path(f"p{self.turn}_model.h5", f"gen{gen}")
        self.model.save(filepath)


class MinimaxPlayer(PlayerInterface):
    def __init__(self, id: int, depth: int, turn: int):
        super().__init__(id, turn)
        self.depth = depth

    def get_name(self):
        return f"Minimax {self.id}"

    def get_action(self, board: Board):
        values = self._minimax(
            board, self.id, self.depth, -math.inf, math.inf, True)
        return values[0]

    def learn(self, history: History):
        pass

    def save(self, gen: int):
        pass

    def _minimax(self, board: Board, player, depth, alpha, beta, maximizingPlayer):
        valid_actions = board.get_valid_actions()
        opponent = OPPONENT_ID if player == PLAYER_ID else PLAYER_ID

        if depth == 0 or board.state != PLAYING:
            if board.state != PLAYING:
                if board.state == DRAW:
                    return None, 0
                if board.state == player:
                    return None, 10000000000000
                return None, -10000000000000
            return None, static_eval(board.board, player, opponent)
        if maximizingPlayer:
            value = -math.inf
            best_action = random.choice(valid_actions)
            for action in valid_actions:
                board_copy = deepcopy(board)
                board_copy.drop_piece(action, player)
                new_score = self._minimax(
                    board_copy, player, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_action = action
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_action, value

        else:
            value = math.inf
            best_action = random.choice(valid_actions)
            for action in valid_actions:
                board_copy = deepcopy(board)
                board_copy.drop_piece(action, opponent)
                new_score = self._minimax(
                    board_copy, player, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_action = action
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_action, value
