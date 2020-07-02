DRAW = 0
PLAYING = -2

REWARD_DRAW = -1
REWARD_MOVE = -1
REWARD_WIN = 20
REWARD_LOSS = -20


class Move:
    def __init__(self, board, action: int, player: int):
        self.board = board
        self.next_board = None
        self.action = action
        self.player = player
        self.result = PLAYING

    def get_terminal(self):
        return self.result not in (DRAW, PLAYING)

    def get_reward(self):
        rewards = {
            DRAW: REWARD_DRAW,
            PLAYING: REWARD_MOVE,
            self.player: REWARD_WIN,
        }
        return rewards.get(self.result, REWARD_LOSS)


class History:
    def __init__(self, result: int, moves, final_board):
        self.result = result
        self.moves = moves
        self.final_board = final_board

    def get_moves(self, player: int):
        def filter_moves(move):
            return move.player == player
        return filter(filter_moves, self.moves)

    def is_winner(self, player: int):
        return self.result == player
