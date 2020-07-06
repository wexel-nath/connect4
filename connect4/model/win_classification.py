from copy import deepcopy

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

import logger
from board import Board
from model import ModelInterface

NUMBER_OF_INPUTS = 42
NUMBER_OF_OUTPUTS = 3  # draw/win/loss %

BATCH_SIZE = 50
EPOCHS = 100


class Model(ModelInterface):
    def __init__(self, player):
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
            input.append(history.final_board)
            output.append(history.result)

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
        max_value = 0
        actions = board.get_valid_actions()
        best_action = actions[0]
        for action in actions:
            logger.debug("action: {}", action)
            board_copy = deepcopy(board)
            board_copy.drop_piece(action, player)
            reshaped_array = np.array(
                board_copy.board).reshape((1, NUMBER_OF_INPUTS))
            result = self.model.predict(reshaped_array)[0]
            logger.debug("result: {}", result)

            value = result[player]
            if value > max_value:
                max_value = value
                best_action = action

        logger.debug("END-------------------------------")
        logger.debug("selected: {}", best_action)
        return best_action
