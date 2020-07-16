from collections import deque
from copy import deepcopy
from statistics import mean
from time import time

import logger
from board import Board, DRAW, ILLEGAL_MOVE, PLAYING
from file import File
from graph import plot_win_rates
from history import History, Move
from model import ModelInterface
from player import PlayerInterface, RandomPlayer, NeuralPlayer
from util import get_full_file_path

PLAYER_ID = 1
OPPONENT_ID = -1


class Manager:
    def __init__(self, gen: int, player: PlayerInterface, opponent: PlayerInterface, current_player=PLAYER_ID):
        self.gen = gen
        self.initial_player = current_player
        self.current_player = current_player
        self.player = player
        self.opponent = opponent

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
        self.current_player = self.initial_player
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

            if len(moves) > 0:
                moves[-1].result = result
                moves[-1].next_board = board.board.copy()
            move.result = result
            moves.append(move)
            self.switch_player()

        history = History(result, moves, board.board.copy())
        return result, history

    def simulate_and_learn(self, num_games: int, player: int):
        result_history = deque(maxlen=100)
        win_rate_history = deque(maxlen=100)
        best_win_rate = 0.0
        win_rate_csv = get_full_file_path(
            f"p{self.player.turn}_win_rates.csv", f"gen{self.gen}")

        for i in range(1, num_games + 1):
            result, history = self.play()
            result_history.append(result)
            self.player.learn(history)
            self.opponent.learn(history)

            win_rate = result_history.count(player)
            if len(result_history) >= 100 and win_rate >= best_win_rate:
                best_win_rate = win_rate
                logger.debug(f"Win rate: {win_rate}% PB")

            win_rate_history.append(win_rate)
            ma = mean(win_rate_history)
            logger.debug(f"Win rate MA-100: {ma:.1f}%")
            logger.debug("result: {}", result)
            if i % 10 == 0:
                f = File(win_rate_csv, "a")
                f.write(f"{i},{win_rate},{ma:.1f}")
                f.close()
            if i % 100 == 0:
                logger.info("Simulated and trained {}/{} games", i, num_games)

        plot_win_rates(win_rate_csv, display=False)

    def vs_random(self, gen, model):
        player = NeuralPlayer(PLAYER_ID, model, turn=1)
        opponent = RandomPlayer(OPPONENT_ID, turn=2)

        result_history = []
        manager = Manager(gen, player, opponent, player.id)
        num_games = 100
        for _ in range(num_games):
            result, _ = manager.play()
            result_history.append(result)

        win_rate = result_history.count(PLAYER_ID) / num_games
        logger.info(f"Win rate against random: {win_rate * 100:.1f}%")
