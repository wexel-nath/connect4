
import os

from flask import Flask, request
from flask_cors import CORS, cross_origin
import numpy as np

from board import get_valid_actions, COLUMNS, ROWS
import logger
from manager import PLAYER_ID, OPPONENT_ID
from model.double_deep_q import Model
from util import get_full_file_path

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

p1_model = Model(player=PLAYER_ID, explore_min=0.0)
p1_model.load(get_full_file_path("p1_model.h5", "gen9"))
p2_model = Model(player=OPPONENT_ID, explore_min=0.0)
p2_model.load(get_full_file_path("p2_model.h5", "gen9"))


@app.route("/action/p1", methods=['POST'])
@cross_origin()
def process_p1():
    data = request.get_json()
    logger.debug("received /action POST. body: {}", data)
    board = data['board']
    new_board = np.zeros((ROWS, COLUMNS), dtype=int)

    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = board[row][col]
            if cell == 2:
                new_board[row][col] = OPPONENT_ID
            elif cell == 1:
                new_board[row][col] = PLAYER_ID

    valid_actions = get_valid_actions(new_board)
    action = p1_model.predict_with_board_array(new_board, valid_actions)

    return {
        'move': int(action)
    }


@app.route("/action/p2", methods=['POST'])
@cross_origin()
def process_p2():
    data = request.get_json()
    logger.debug("received /action POST. body: {}", data)
    board = data['board']
    new_board = np.zeros((ROWS, COLUMNS), dtype=int)

    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = board[row][col]
            if cell == 2:
                new_board[row][col] = OPPONENT_ID
            elif cell == 1:
                new_board[row][col] = PLAYER_ID

    valid_actions = get_valid_actions(new_board)
    action = p2_model.predict_with_board_array(new_board, valid_actions)

    return {
        'move': int(action)
    }


@app.route("/healthz")
def health():
    return {
        'result': {
            'status': 'ok',
            'image': os.environ.get('IMAGE_TAG')
        },
        'messages': [],
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3001')
