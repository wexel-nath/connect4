from time import time

import logger
from manager import Manager, PLAYER_ID, OPPONENT_ID
from model.double_deep_q import Model
from player import NeuralPlayer, RandomPlayer, PlayerInterface
from util import get_full_file_path

MAX_GENS = 100
NUM_GAMES = 1000


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

    def run(self, gen: int):
        logger.info("Running Generation {}", gen)
        player = NeuralPlayer(PLAYER_ID, self.model)
        opponent = RandomPlayer(OPPONENT_ID)
        manager = Manager(gen, player, opponent)
        manager.simulate(NUM_GAMES)
        manager.print_results()

        results = manager.get_results()
        f = File(get_full_file_path(f"gen_{gen}.txt"), "w")
        f.write_dict(results)
        f.close()

        self.model.save(get_full_file_path(f"gen_{gen}.h5"))

        return manager.history, results


if __name__ == "__main__":
    best_win_rate = 0.0
    best_results = {}

    history = []
    generation = Generation()
    for gen in range(0, MAX_GENS + 1):
        if len(history) > 0:
            generation.train(history)
        history, results = generation.run(gen)

        win_rate = results['wins'] / NUM_GAMES * 100
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            logger.info("New best win rate. Generation {}: {}%", gen, win_rate)

            f = File(get_full_file_path("gen_best.txt"), "w")
            f.write_dict(results)
            f.close()
