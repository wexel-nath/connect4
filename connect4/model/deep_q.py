from collections import deque
import random

import numpy as np
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical

import logger
from board import Board, ROWS, COLUMNS

NUMBER_OF_INPUTS = 42
NUMBER_OF_OUTPUTS = 7  # number of actions


class Model:
    def __init__(self, player):
        self.BATCH_SIZE = 32
        self.GAMMA = 0.95
        self.LEARNING_RATE = 0.001

        self.EXPLORATION_MAX = 1.0
        self.EXPLORATION_MIN = 0.0
        self.EXPLORATION_DECAY = 0.995

        self.exploration_rate = self.EXPLORATION_MAX
        self.is_fit = False
        self.memory = deque(maxlen=512)

        self.player = player
        self.model = Sequential()
        self.model.add(
            Dense(42, activation='relu', input_shape=(NUMBER_OF_INPUTS,))
        )
        hidden_neurons = NUMBER_OF_INPUTS * NUMBER_OF_OUTPUTS * 2
        self.model.add(Dense(hidden_neurons, activation="relu"))
        self.model.add(Dense(hidden_neurons, activation="relu"))
        self.model.add(Dense(hidden_neurons, activation="relu"))
        self.model.add(Dense(hidden_neurons, activation="relu"))
        self.model.add(Dense(NUMBER_OF_OUTPUTS, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=self.LEARNING_RATE))

    def save(self, filepath):
        self.model.save(filepath)

    def remember(self, state, action, reward, next_state, terminal):
        state = np.array(state).reshape((1, NUMBER_OF_INPUTS))
        next_state = np.array(next_state).reshape((1, NUMBER_OF_INPUTS))
        self.memory.append((state, action, reward, next_state, terminal))

    def experience_replay(self):
        if self.is_fit:
            self.exploration_rate *= self.EXPLORATION_DECAY
            self.exploration_rate = max(
                self.EXPLORATION_MIN, self.exploration_rate)

        if len(self.memory) < self.BATCH_SIZE:
            return
        batch = random.sample(self.memory, self.BATCH_SIZE)
        batch[-1] = self.memory[-1]
        if self.BATCH_SIZE > 1:
            batch[-2] = self.memory[-1]
        if not self.is_fit:
            states = list(map(lambda _: _[0][0], batch))
            states = np.array(states)
            self.model.fit(states, np.zeros(
                (len(batch), NUMBER_OF_OUTPUTS)), verbose=0)

        for state, action, reward, next_state, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + self.GAMMA *
                            np.amax(self.model.predict(next_state)[0]))
            q_values = self.model.predict(state)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.is_fit = True

    def train(self, history_list):
        pass

    def predict(self, board: Board, player: int):
        actions = board.get_valid_actions()
        if np.random.rand() < self.exploration_rate:
            return random.choice(actions)

        state = np.array(board.board).reshape((1, NUMBER_OF_INPUTS))
        q_values = self.model.predict(state)[0]
        logger.debug("q_values: {}", q_values)

        sorted_actions = np.argsort(q_values)
        logger.debug("sorted_actions: {}", sorted_actions)

        for a in sorted_actions[::-1]:
            if a in actions:
                return a

        return actions[0]
