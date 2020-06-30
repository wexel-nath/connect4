
class Move:
    def __init__(self, board, action: int, player: int):
        self.board = board
        self.action = action
        self.player = player
        self.is_last_move = False


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
