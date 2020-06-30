from time import time

import logger
from manager import Manager, PLAYER_ID, OPPONENT_ID
from model.deep_q import Model
from player import NeuralPlayer, RandomPlayer, PlayerInterface
from util import get_full_file_path

MAX_GENS = 10

RANDOM_GAMES = 0
GENERATION_GAMES = 1000


class File:
    def __init__(self, name: str, mode: str):
        self.file = open(name, mode)

    def write(self, line: str):
        self.file.write(line + "\n")

    def write_dict(self, dict):
        for k, v in dict.items():
            self.write("{}: {}".format(k, v))

    def close(self):
        self.file.close()


class Generation:
    def __init__(self):
        self.model = Model(player=1)

    def train(self, dataset):
        start = time()
        self.model.train(dataset)
        logger.info("Training took {:.2f}s", time() - start)

    def run(self, number: int):
        logger.info("Running Generation {}", number)
        player = NeuralPlayer(PLAYER_ID, self.model)
        opponent = RandomPlayer(OPPONENT_ID)
        manager = Manager(player, opponent)
        manager.simulate(GENERATION_GAMES)
        manager.print_results()

        results = manager.get_results()
        f = File(get_full_file_path("gen_{}.txt".format(number)), "w")
        f.write("Generation {}".format(number))
        f.write_dict(results)
        f.close()

        self.model.save(get_full_file_path("gen_{}.h5".format(number)))

        return manager.history


if __name__ == "__main__":
    player = RandomPlayer(PLAYER_ID)
    opponent = RandomPlayer(OPPONENT_ID)

    manager = Manager(player, opponent)
    manager.simulate(RANDOM_GAMES)
    manager.print_results()

    history = manager.history
    generation = Generation()
    for gen in range(1, MAX_GENS + 1):
        generation.train(history)
        history = generation.run(gen)
