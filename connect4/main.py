from time import time

import logger
from file import File
from hyperparameters import DECAY, GAMMA, LEARNING_RATE
from manager import Manager, PLAYER_ID, OPPONENT_ID
from model.double_deep_q import Model
from player import NeuralPlayer, RandomPlayer, PlayerInterface
from util import get_full_file_path

MAX_GENS = 100
NUM_GAMES = 1000


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
        manager = Manager(gen, player, opponent, player.id)
        manager.simulate(NUM_GAMES)
        manager.print_results()

        results = manager.get_results()
        f = File(get_full_file_path(f"gen_{gen}.txt"), "w")
        f.write_dict(results)
        f.close()

        self.model.save(get_full_file_path(f"gen_{gen}.h5"))

        return manager.history, results


def run_generation():
    best_win_rate = 0.0

    history = []
    generation = Generation()
    for gen in range(0, MAX_GENS + 1):
        if len(history) > 0:
            generation.train(history)
        history, results = generation.run(gen)

        win_rate = results['wins'] / NUM_GAMES * 100
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            logger.info("New best win rate. Gen {}: {:.1f}%", gen, win_rate)

            f = File(get_full_file_path("gen_best.txt"), "w")
            f.write_dict(results)
            f.close()


def run_single_and_train():
    number_of_games = 1000000
    model = Model(player=PLAYER_ID, decay=DECAY,
                  learning_rate=LEARNING_RATE, gamma=GAMMA)
    player = NeuralPlayer(PLAYER_ID, model)
    opponent = RandomPlayer(OPPONENT_ID)

    # fixed_model = Model(player=OPPONENT_ID, decay=DECAY,
    #                     learning_rate=LEARNING_RATE, gamma=GAMMA)
    # fixed_model.load(m)
    # opponent = NeuralPlayer(OPPONENT_ID, fixed_model)

    manager = Manager(1, player, opponent, player.id)

    manager.simulate_and_train(number_of_games, model)


if __name__ == "__main__":
    run_single_and_train()
