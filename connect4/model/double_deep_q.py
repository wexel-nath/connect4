import os
import random

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
from keras.layers import Dense, Flatten, LeakyReLU
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.utils import to_categorical

import logger
from board import Board, ROWS, COLUMNS
from model import ModelInterface

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01

NUM_INPUTS = 42
NUM_ACTIONS = 7
SHAPE = (1, NUM_INPUTS)


def build_neural_net(lr=0.001):
    alpha = 0.1

    model = Sequential()
    model.add(Dense(42, input_shape=(NUM_INPUTS,)))
    model.add(LeakyReLU(alpha=alpha))
    num_neurons = NUM_INPUTS * 2
    model.add(Dense(num_neurons))
    model.add(LeakyReLU(alpha=alpha))
    model.add(Dense(num_neurons))
    model.add(LeakyReLU(alpha=alpha))
    model.add(Dense(num_neurons))
    model.add(LeakyReLU(alpha=alpha))
    model.add(Dense(NUM_ACTIONS, activation="linear"))
    model.compile(loss="mse", optimizer=Adam(lr=lr))

    return model


class Model(ModelInterface):
    def __init__(self, player, decay=0.9998, learning_rate=0.001, gamma=0.95):
        self.player = player
        self.decay = decay
        self.gamma = gamma
        self.exploration_rate = EXPLORATION_MAX
        self.model = build_neural_net(lr=learning_rate)
        self.target = build_neural_net(lr=learning_rate)

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.exploration_rate = EXPLORATION_MIN
        self.model = load_model(filepath)

    def _reshape_board(self, board):
        return np.array(self.player * board).reshape(SHAPE)

    def train(self, history_list):
        self.exploration_rate *= self.decay
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)
        self.target.set_weights(self.model.get_weights())

        num_history = len(history_list)
        for i, history in enumerate(history_list, start=1):
            for move in history.get_moves(self.player):
                state = self._reshape_board(move.board)
                q = move.get_reward()
                if not move.get_terminal():
                    next_state = self._reshape_board(move.next_board)
                    q += self.gamma * \
                        np.amax(self.target.predict(next_state)[0])
                q_values = self.model.predict(state)
                q_values[0][move.action] = q
                self.model.fit(state, q_values, verbose=0)

            if i % 100 == 0:
                logger.info("Trained {}/{} games", i, num_history)

    def predict(self, board: Board, player: int):
        actions = board.get_valid_actions()
        if np.random.rand() < self.exploration_rate:
            return random.choice(actions)

        state = self._reshape_board(board.board)
        q_values = self.model.predict(state)[0]
        logger.debug("q_values: {}", q_values)

        sorted_actions = np.argsort(q_values)[::-1]
        logger.debug("sorted_actions: {}", sorted_actions)
        return sorted_actions[0]

        # for a in sorted_actions:
        #     if a in actions:
        #         return a

        # return actions[0]
