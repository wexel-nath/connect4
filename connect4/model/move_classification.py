import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

import logger
from board import Board

NUMBER_OF_INPUTS = 42
NUMBER_OF_OUTPUTS = 7  # move/position

BATCH_SIZE = 50
EPOCHS = 100


class Model:
    def __init__(self):
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

    def train(self, history_list):
        input = []
        output = []

        PLAYER_ID = 1
        for history in history_list:
            if history.is_winner(PLAYER_ID):
                for move in history.get_moves(PLAYER_ID):
                    input.append(move.board)
                    output.append(move.position - 1)

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
        result = self.model.predict(reshaped_array)
        logger.debug("result: {}", result)

        moves = result[0]
        valid_moves = board.get_valid_moves()
        move = -1
        while move == -1:
            best_move = np.argmax(moves)
            if best_move in valid_moves:
                move = best_move
            else:
                moves[best_move] = 0

        return move
