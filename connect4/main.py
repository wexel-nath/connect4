import os
from time import time

import logger
from file import File
from hyperparameters import DECAY, DEPTH, GAMMA, LEARNING_RATE
from manager import Manager, PLAYER_ID, OPPONENT_ID
from model.double_deep_q import Model
from player import MinimaxPlayer, NeuralPlayer, RandomPlayer, PlayerInterface
from util import get_full_file_path


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
                             explore_min=0.05)

        opponent_model = Model(player=OPPONENT_ID, decay=DECAY,
                               learning_rate=LEARNING_RATE, gamma=GAMMA,
                               explore_min=0.05)

        if gen > 0:
            player_path = get_full_file_path("p1_model.h5", f"gen{gen-1}")
            player_model.load(player_path)
            opponent_path = get_full_file_path("p2_model.h5", f"gen{gen-1}")
            opponent_model.load(opponent_path)

        player = NeuralPlayer(PLAYER_ID, player_model, turn=1)
        opponent = NeuralPlayer(OPPONENT_ID, opponent_model, turn=2)

        manager = Manager(gen, player, opponent, player.id)
        manager.simulate_and_learn(number_of_games, player.id)

        player.save(gen)
        opponent.save(gen)

        random_player = RandomPlayer(PLAYER_ID, turn=1)
        random_opponent = RandomPlayer(OPPONENT_ID, turn=2)
        manager = Manager(gen, player, random_opponent, player.id)
        manager = Manager(gen, random_player, opponent, player.id)

    gen = int(os.environ.get('GEN'))
    run_gen(gen)

    # for gen in range(4, 6):
    #     prev_model_path = get_full_file_path("p1_model.h5", f"gen{gen-1}")
    #     sim_generation(gen, number_of_games, prev_model_path, player_turn=2)

    #     prev_model_path = get_full_file_path("p2_model.h5", f"gen{gen}")
    #     sim_generation(gen, number_of_games, prev_model_path, player_turn=1)


if __name__ == "__main__":
    run()
