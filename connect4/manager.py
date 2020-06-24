from time import time

from board import Board
from player import PlayerInterface


PLAYER_ID = 1
OPPONENT_ID = 2

DRAW = 0
PLAYING = -2


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
        result = PLAYING
        while result == PLAYING:
            # board.print()
            player = self.player if turn % 2 == 0 else self.opponent
            position = player.get_position(board, turn)

            row = board.drop_piece(position, player.id)
            if not row == -1:
                turn += 1
                win = board.is_winner(player.id, row, position)
                if not win == "":
                    result = player.id
                elif turn == 42:
                    result = DRAW

        self.history.append((result, board.history))
        return result

    def simulate(self, num_games: int, print_result: bool):
        for _ in range(num_games):
            result = self.play()
            if result == DRAW:
                self.draws += 1
            elif result == PLAYER_ID:
                self.wins += 1
            elif result == OPPONENT_ID:
                self.losses += 1

            print(result) if print_result else None

    def get_results(self):
        return {
            'draws': self.draws,
            'wins': self.wins,
            'losses': self.losses,
            'elapsed': "{:.2f}s".format(time() - self.start)
        }

    def print_results(self):
        print("draws:", self.draws)
        print("player one wins:", self.wins)
        print("player one loss:", self.losses)
        print("elapsed:",  "{:.2f}s".format(time() - self.start))

        num_moves = 0
        for board_history in self.history:
            num_moves += len(board_history[1])

        print("avg:", num_moves / len(self.history))
