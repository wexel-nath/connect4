from time import time

import logger
from board import Board
from history import History, Move
from player import PlayerInterface

PLAYING = -2
DRAW = 0
PLAYER_ID = 1
OPPONENT_ID = 2


class Manager:
    def __init__(self, player: PlayerInterface, opponent: PlayerInterface):
        self.player = player
        self.opponent = opponent
        self.start = time()
        self.history = []
        self.draws = 0
        self.wins = 0
        self.losses = 0

    def play(self):
        turn = 0
        board = Board()
        moves = []
        result = PLAYING
        while result == PLAYING:
            board.print()
            player = self.player if turn % 2 == 0 else self.opponent
            action = player.get_action(board, turn)

            move = Move(board.board, action, player.id)
            row = board.drop_piece(action, player.id)
            if not row == -1:
                turn += 1
                win = board.is_winner(player.id, row, action)
                if not win == "":
                    # each player has played their last move
                    moves[-1].is_last_move = True
                    move.is_last_move = True
                    result = player.id
                elif turn == 42:
                    result = DRAW
                moves.append(move)

        self.history.append(History(result, moves, board.board))
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
            'draws': self.draws,
            'wins': self.wins,
            'losses': self.losses,
            'elapsed': "{:.2f}s".format(time() - self.start)
        }

    def print_results(self):
        logger.info("draws: {}", self.draws)
        logger.info("player one wins: {}", self.wins)
        logger.info("player one losses: {}", self.losses)
        logger.info("elapsed: {:.2f}s", time() - self.start)
