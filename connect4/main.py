from time import time

from manager import Manager, PLAYER_ID, OPPONENT_ID
from model import Model
from player import NeuralPlayer, RandomPlayer, PlayerInterface

DEBUG = False
MAX_GENS = 10

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
        self.model = Model(42, 3, 50, 100)

    def train(self, dataset):
        start = time()
        self.model.train(dataset)
        print("Training took {:.2f}s".format(time() - start))

    def run(self, number: int, num_games: int):
        print("Running Generation {}".format(number))
        player = NeuralPlayer(PLAYER_ID, self.model, DEBUG)
        opponent = RandomPlayer(OPPONENT_ID)
        manager = Manager(player, opponent)
        manager.simulate(num_games, False)
        manager.print_results()
        
        results = manager.get_results()
        f = File("/tmp/out/gen_{}.txt".format(number), "w")
        f.write("Generation {}".format(number))
        f.write_dict(results)
        f.close()

        return manager.history


if __name__ == "__main__":
    player = RandomPlayer(PLAYER_ID)
    opponent = RandomPlayer(OPPONENT_ID)

    manager = Manager(player, opponent)
    manager.simulate(10000, False)
    manager.print_results()

    history = manager.history
    generation = Generation()
    for gen in range(1, MAX_GENS+1):
        generation.train(history)
        history = generation.run(gen, 10000)
