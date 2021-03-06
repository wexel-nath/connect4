class ModelInterface:
    def save(self, filepath):
        raise NotImplementedError

    def load(self, filepath):
        raise NotImplementedError

    def train(self, history):
        raise NotImplementedError

    def predict(self, board, player):
        raise NotImplementedError
