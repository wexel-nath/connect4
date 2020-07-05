import random

import numpy as np
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical

import logger
from board import Board, ROWS, COLUMNS
from model import ModelInterface

GAMMA = 0.95
LEARNING_RATE = 0.001

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.05
EXPLORATION_DECAY = 0.8

NUM_INPUTS = 42
NUM_ACTIONS = 7
SHAPE = (1, NUM_INPUTS)


class Model(ModelInterface):
    def __init__(self, player):
        self.exploration_rate = EXPLORATION_MAX

        self.player = player
        self.model = Sequential()
        self.model.add(Dense(42, activation='relu', input_shape=(NUM_INPUTS,)))
        num_neurons = NUM_INPUTS * NUM_ACTIONS * 2
        self.model.add(Dense(num_neurons, activation="relu"))
        self.model.add(Dense(num_neurons, activation="relu"))
        self.model.add(Dense(num_neurons, activation="relu"))
        self.model.add(Dense(num_neurons, activation="relu"))
        self.model.add(Dense(NUM_ACTIONS, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

        empty_board = np.zeros(SHAPE)
        initial_q_values = np.zeros((1, NUM_ACTIONS))
        self.model.fit(empty_board, initial_q_values, verbose=0)

    def save(self, filepath):
        self.model.save(filepath)

    def train(self, history_list):
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

        num_history = len(history_list)
        for i, history in enumerate(history_list, start=1):
            for move in history.get_moves(self.player):
                state = np.array(move.board).reshape(SHAPE)
                q = move.get_reward()
                if not move.get_terminal():
                    next_state = np.array(move.next_board).reshape(SHAPE)
                    q += GAMMA * np.amax(self.model.predict(next_state)[0])
                q_values = self.model.predict(state)
                q_values[0][move.action] = q
                self.model.fit(state, q_values, verbose=0)

            if i % 100 == 0:
                logger.info("Trained {}/{} games", i, num_history)

    def predict(self, board: Board, player: int):
        actions = board.get_valid_actions()
        if np.random.rand() < self.exploration_rate:
            return random.choice(actions)

        state = np.array(board.board).reshape(SHAPE)
        q_values = self.model.predict(state)[0]
        logger.debug("q_values: {}", q_values)

        sorted_actions = np.argsort(q_values)
        logger.debug("sorted_actions: {}", sorted_actions)

        for a in sorted_actions[::-1]:
            if a in actions:
                return a

        return actions[0]
