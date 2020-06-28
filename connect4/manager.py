from time import time

from board import Board
from history import History, Move
from player import PlayerInterface

PLAYING = -2
DRAW = 0
PLAYER_ID = 1
OPPONENT_ID = 2


class Manager:
    def __init__(self, player: PlayerInterface, opponent: PlayerInterface, debug: bool):
        self.player = player
        self.opponent = opponent
        self.debug = debug
        self.start = time()
        self.history = []
        self.draws = 0
        self.wins = 0
        self.losses = 0

    def play(self):
        turn = 0
        board = Board(self.debug)
        moves = []
        result = PLAYING
        while result == PLAYING:
            board.print()
            player = self.player if turn % 2 == 0 else self.opponent
            position = player.get_position(board, turn)

            move = Move(board.board, position, player.id)
            row = board.drop_piece(position, player.id)
            if not row == -1:
                turn += 1
                win = board.is_winner(player.id, row, position)
                if not win == "":
                    move.is_winning = True
                    result = player.id
                elif turn == 42:
                    result = DRAW
                moves.append(move)

        self.history.append(History(result, moves, board.board))
        return result

    def simulate(self, num_games: int):
        for _ in range(num_games):
            result = self.play()
            if result == DRAW:
                self.draws += 1
            elif result == PLAYER_ID:
                self.wins += 1
            elif result == OPPONENT_ID:
                self.losses += 1

            if self.debug:
                print(result)

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
