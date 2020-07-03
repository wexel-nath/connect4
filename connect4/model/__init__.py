class ModelInterface:
    def save(self, filepath):
        raise NotImplementedError

    def train(self, history_list):
        raise NotImplementedError

    def predict(self, board, player):
        raise NotImplementedError
