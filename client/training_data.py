import itertools as it
from client.mcts import *
import torch as tr


def generate(board_size, num_games):
    data = []
    for game in range(num_games):
        state = initial_state(board_size, board_size)
        node = Node(state)
        for turn in it.count():
            print("game %d, turn %d..." % (game, turn))

            if node.state.is_leaf(): break

            valid_actions = state.valid_actions()
            if len(valid_actions) == 1:
                state = state.perform(valid_actions[0])
                continue

            node = mcts(node, max_depth=5, run_time=15)
            for child in node.children:
                data.append((child.state, child.Q))
    return data


def encode(state):
    one_hot = tr.zeros([2, state.board.shape[0], state.board.shape[1]])
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[1]):
            if state.board[i][j] == "X":
                one_hot[0, i, j] = 1
            elif state.board[i][j] == "O":
                one_hot[1, i, j] = 1
    return one_hot


def get_batch(board_size=10, num_games=5):
    states = []
    scores = []
    gen = generate(board_size, num_games)
    for state, score in gen:
        states.append(encode(state))
        scores.append(score)
    inputs = tr.stack(states)
    outputs = tr.tensor(scores, dtype=tr.float32).reshape(len(scores), 1)
    return inputs, outputs


if __name__ == "__main__":
    board_size, num_games = 10, 3
    inputs, outputs = get_batch(board_size, num_games=num_games)
    print(inputs.shape)
    print(outputs.shape)
    print(inputs)
    print(outputs)

    import pickle as pk

    with open("data%d.pkl" % board_size, "wb") as f: pk.dump((inputs, outputs), f)
