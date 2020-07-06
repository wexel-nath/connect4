import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

import logger
from board import Board
from model import ModelInterface

NUMBER_OF_INPUTS = 42
NUMBER_OF_OUTPUTS = 7  # number of actions

BATCH_SIZE = 50
EPOCHS = 100


class Model(ModelInterface):
    def __init__(self, player):
        self.player = 1
        self.model = Sequential()
        self.model.add(
            Dense(42, activation='relu', input_shape=(NUMBER_OF_INPUTS,))
        )
        self.model.add(Dense(42, activation='relu'))
        self.model.add(Dense(NUMBER_OF_OUTPUTS, activation='softmax'))
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer="rmsprop",
            metrics=['accuracy']
        )

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.model = load_model(filepath)

    def train(self, history_list):
        input = []
        output = []

        for history in history_list:
            if history.is_winner(self.player):
                for move in history.get_moves(self.player):
                    input.append(move.board)
                    output.append(move.action)

        X = np.array(input).reshape((-1, NUMBER_OF_INPUTS))
        y = to_categorical(output, num_classes=NUMBER_OF_OUTPUTS)
        limit = int(0.8 * len(X))
        X_train = X[:limit]
        X_test = X[limit:]
        y_train = y[:limit]
        y_test = y[limit:]
        self.model.fit(
            X_train,
            y_train,
            validation_data=(X_test, y_test),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE
        )

    def predict(self, board: Board, player: int):
        reshaped_array = np.array(board.board).reshape((1, NUMBER_OF_INPUTS))
        result = self.model.predict(reshaped_array)[0]
        logger.debug("result: {}", result)

        sorted_moves = np.argsort(result)
        logger.debug("sorted_moves: {}", sorted_moves)

        actions = board.get_valid_actions()
        for a in sorted_moves[::-1]:
            if a in actions:
                return a

        return actions[0]
