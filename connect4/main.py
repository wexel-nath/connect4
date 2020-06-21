from time import time

from manager import Manager, PLAYER_ID, OPPONENT_ID
from model import Model
from player import RandomPlayer, NeuralPlayer, PlayerInterface


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
        player = NeuralPlayer(PLAYER_ID, self.model)
        manager = Manager(player, opponent)
        manager.simulate(num_games, False)
        manager.print_results()
        return manager.history


if __name__ == "__main__":
    player = RandomPlayer(PLAYER_ID)
    opponent = RandomPlayer(OPPONENT_ID)

    manager = Manager(player, opponent)
    manager.simulate(10000, False)
    manager.print_results()

    history = manager.history
    for gen in range(3):
        generation = Generation(gen+1)
        generation.train(history)
        history = generation.run(opponent, 10000)
