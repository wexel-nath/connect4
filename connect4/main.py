from time import time

import logger
from file import File
from hyperparameters import DECAY, DEPTH, GAMMA, LEARNING_RATE
from manager import Manager, PLAYER_ID, OPPONENT_ID
from model.double_deep_q import Model
from player import MinimaxPlayer, NeuralPlayer, RandomPlayer, PlayerInterface
from util import get_full_file_path

MAX_GENS = 100
NUM_GAMES = 1000


def sim_generation(gen: int, num_games: int, prev_model_path: str, player_turn: int):
    opponent_model = Model(player=OPPONENT_ID, decay=DECAY,
                           learning_rate=LEARNING_RATE, gamma=GAMMA,
                           explore_min=0.0)
    opponent_model.load(prev_model_path)
    opponent = NeuralPlayer(OPPONENT_ID, opponent_model, turn=0)

    player_model = Model(player=PLAYER_ID, decay=DECAY,
                         learning_rate=LEARNING_RATE, gamma=GAMMA,
                         explore_min=0.01)
    player = NeuralPlayer(PLAYER_ID, player_model, turn=player_turn)

    current_player = player.id if player_turn == 1 else opponent.id
    manager = Manager(gen, player, opponent, current_player)
    manager.simulate_and_learn(num_games, player.id)

    player.save(gen)


def run():
    number_of_games = 100000

    def run_gen(gen: int):
        player_model = Model(player=PLAYER_ID, decay=DECAY,
                             learning_rate=LEARNING_RATE, gamma=GAMMA,
                             explore_min=0.1)
        if gen > 0:
            prev_model_path = get_full_file_path("p1_model.h5", f"gen{gen-1}")
            player_model.load(prev_model_path)
        player = NeuralPlayer(PLAYER_ID, player_model, turn=1)

        opponent_model = Model(player=OPPONENT_ID, decay=DECAY,
                               learning_rate=LEARNING_RATE, gamma=GAMMA,
                               explore_min=0.1)
        if gen > 0:
            prev_model_path = get_full_file_path("p2_model.h5", f"gen{gen-1}")
            opponent_model.load(prev_model_path)
        opponent = NeuralPlayer(OPPONENT_ID, opponent_model, turn=2)

        # opponent = RandomPlayer(OPPONENT_ID, turn=1)

        manager = Manager(gen, player, opponent, player.id)
        manager.simulate_and_learn(number_of_games, player.id)

        player.save(gen)
        opponent.save(gen)

    run_gen(1)

    # for gen in range(4, 6):
    #     prev_model_path = get_full_file_path("p1_model.h5", f"gen{gen-1}")
    #     sim_generation(gen, number_of_games, prev_model_path, player_turn=2)

    #     prev_model_path = get_full_file_path("p2_model.h5", f"gen{gen}")
    #     sim_generation(gen, number_of_games, prev_model_path, player_turn=1)


if __name__ == "__main__":
    run()
