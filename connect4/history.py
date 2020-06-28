
class Move:
    def __init__(self, board, position: int, player: int):
        self.board = board
        self.position = position
        self.player = player
        self.is_winning = False


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
