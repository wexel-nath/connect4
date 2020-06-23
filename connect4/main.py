from time import time

from manager import Manager, PLAYER_ID, OPPONENT_ID
from model import Model
from player import RandomPlayer, NeuralPlayer, PlayerInterface

DEBUG = False


class Generation:
    def __init__(self, number: int):
        self.number = number
        self.model = Model(42, 3, 50, 100)

    def train(self, dataset):
        start = time()
        self.model.train(dataset)
        print("gen{} training took {:.2f}s".format(self.number, time() - start))

    def run(self, opponent: PlayerInterface, num_games: int):
        print("Running gen{}".format(self.number))
        player = NeuralPlayer(PLAYER_ID, self.model, DEBUG)
        manager = Manager(player, opponent)
        manager.simulate(num_games, False)
        manager.print_results()
        return manager.history


if __name__ == "__main__":
    player = RandomPlayer(PLAYER_ID)
    opponent = RandomPlayer(OPPONENT_ID)

    manager = Manager(player, opponent)
    manager.simulate(1000, False)
    manager.print_results()
    model = Model(42, 3, 50, 100)

    history = manager.history
    for gen in range(1, 5):
        start = time()
        model.train(history)
        print("gen{} training took {:.2f}s".format(gen, time() - start))

        player = NeuralPlayer(PLAYER_ID, model, DEBUG)
        opponent = NeuralPlayer(OPPONENT_ID, model, DEBUG)

        manager = Manager(player, opponent)
        manager.simulate(100, False)
        manager.print_results()
        history = manager.history

        manager = Manager(player, RandomPlayer(OPPONENT_ID))
        manager.simulate(100, False)
        print("gen{} results against random".format(gen))
        manager.print_results()
