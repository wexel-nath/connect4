from time import time

import logger
from board import Board, DRAW, ILLEGAL_MOVE, PLAYING
from history import History, Move
from player import PlayerInterface

PLAYER_ID = 1
OPPONENT_ID = 2


class Manager:
    def __init__(self, gen: int, player: PlayerInterface, opponent: PlayerInterface):
        self.gen = gen
        self.current_player = player.id
        self.player = player
        self.opponent = opponent
        self.start = time()
        self.history = []
        self.draws = 0
        self.wins = 0
        self.losses = 0
        self.actions = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        }
        self.illegal_moves = 0

    def get_player(self):
        if self.current_player == self.player.id:
            return self.player
        return self.opponent

    def switch_player(self):
        if self.current_player == self.player.id:
            self.current_player = self.opponent.id
        else:
            self.current_player = self.player.id

    def play(self):
        board = Board()
        moves = []
        result = PLAYING
        while result == PLAYING:
            board.print()
            player = self.get_player()
            action = player.get_action(board)

            move = Move(board.board.copy(), action, player.id)
            result = board.handle_action(action, player.id)
            if result == ILLEGAL_MOVE:
                result = self.opponent.id
                self.illegal_moves += 1

            if len(moves) > 0:
                moves[-1].result = result
                moves[-1].next_board = board.board.copy()
            move.result = result
            moves.append(move)
            self.actions[action] += 1
            self.switch_player()

        self.history.append(History(result, moves, board.board.copy()))
        return result

    def simulate(self, num_games: int):
        for i in range(1, num_games + 1):
            result = self.play()
            if result == DRAW:
                self.draws += 1
            elif result == PLAYER_ID:
                self.wins += 1
            elif result == OPPONENT_ID:
                self.losses += 1

            logger.debug("result: {}", result)
            if i % 100 == 0:
                logger.info("Simulated {}/{} games", i, num_games)

    def get_results(self):
        return {
            'generation': self.gen,
            'draws': self.draws,
            'wins': self.wins,
            'losses': self.losses,
            'elapsed': "{:.2f}s".format(time() - self.start),
            'actions': self.actions,
            'illegal_moves': self.illegal_moves,
        }

    def print_results(self):
        logger.info("Generation {} results", self.gen)
        logger.info("draws: {}", self.draws)
        logger.info("player one wins: {}", self.wins)
        logger.info("player one losses: {}", self.losses)
        logger.info("elapsed: {:.2f}s", time() - self.start)
        logger.info("actions: {}", self.actions)
        logger.info("illegal moves: {}", self.illegal_moves)
