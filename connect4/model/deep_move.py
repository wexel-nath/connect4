import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

import logger
from board import Board
from history import PLAYING

NUMBER_OF_INPUTS = 42
NUMBER_OF_OUTPUTS = 7  # number of actions

BATCH_SIZE = 50
EPOCHS = 100

LAST_MOVE_MULTIPLIER = 100


class Model:
    def __init__(self, player):
        self.player = player
        self.model = Sequential()
        self.model.add(
            Dense(42, activation='relu', input_shape=(NUMBER_OF_INPUTS,))
        )
        self.model.add(Dense(42 * 2, activation='relu'))
        self.model.add(Dense(42 * 2, activation='relu'))
        self.model.add(Dense(42 * 2, activation='relu'))
        self.model.add(Dense(NUMBER_OF_OUTPUTS, activation='linear'))
        self.model.compile(loss='mse', optimizer="adam")

    def save(self, filepath):
        self.model.save(filepath)

    def train(self, history_list):
        num_moves = 0

        for history in history_list:
            for move in history.get_moves(self.player):
                num_moves += 1

        input = []
        output = np.zeros((num_moves, NUMBER_OF_OUTPUTS))
        counter = 0
        for history in history_list:
            for move in history.get_moves(self.player):
                input.append(move.board)
                q = 1 if history.is_winner(self.player) else -1
                if move.result != PLAYING:
                    q *= LAST_MOVE_MULTIPLIER
                output[counter][move.action] = q
                counter += 1

        X = np.array(input).reshape((-1, NUMBER_OF_INPUTS))
        limit = int(0.8 * len(X))
        X_train = X[:limit]
        X_test = X[limit:]
        y_train = output[:limit]
        y_test = output[limit:]
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
