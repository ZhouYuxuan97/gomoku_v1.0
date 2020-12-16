import itertools as it
import numpy as np
import torch as tr
import csv
import client.net
from client.Gomoku import initial_state, SCORE_4, SCORE_3
from client.training_data import encode
from client.mcts import Node, mcts, nn_decide


def load_net(board_size):
    net = client.net.LeNet(board_size)
    net.load_state_dict(tr.load("model%d.pth" % board_size))
    return net


def nn_puct(node):
    # choice of net depends on size of board in node
    # put all children of 'node' into network, and choose one using softmax
    with tr.no_grad():
        net = load_net(board_size=node.state.board.shape[0])
        x = tr.stack(tuple(map(encode, [child.state for child in node.children])))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())
    return node.children[a]


def final_score(state):
    score = 0
    for x in range(state.board.shape[0] - 1):
        for y in range(state.board.shape[1] - 1):
            # check 4
            if x < state.board.shape[0] - 3 and y < state.board.shape[1] - 3:
                subBoard = state.board[x:x + 4, y:y + 4]
                if (subBoard == "X").all(axis=0).any(): score -= SCORE_4
                if (subBoard == "X").all(axis=1).any(): score -= SCORE_4
                if (np.diag(subBoard) == "X").all(): score -= SCORE_4
                if (np.diag(np.rot90(subBoard)) == "X").all(): score -= SCORE_4
                if (subBoard == "O").all(axis=0).any(): score += SCORE_4
                if (subBoard == "O").all(axis=1).any(): score += SCORE_4
                if (np.diag(subBoard) == "O").all(): score += SCORE_4
                if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_4
            # check 3
            if x < state.board.shape[0] - 2 and y < state.board.shape[1] - 2:
                subBoard = state.board[x:x + 3, y:y + 3]
                if (subBoard == "X").all(axis=0).any(): score -= SCORE_3
                if (subBoard == "X").all(axis=1).any(): score -= SCORE_3
                if (np.diag(subBoard) == "X").all(): score -= SCORE_3
                if (np.diag(np.rot90(subBoard)) == "X").all(): score -= SCORE_3
                if (subBoard == "O").all(axis=0).any(): score += SCORE_3
                if (subBoard == "O").all(axis=1).any(): score += SCORE_3
                if (np.diag(subBoard) == "O").all(): score += SCORE_3
                if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_3
    return score


if __name__ == "__main__":
    if __name__ == "__main__":
        for i in range(1):
            board_size = 10
            c_write = open("result_%d.csv" % board_size, "a+", newline='')
            writer = csv.writer(c_write)
            rlist = []
            state = initial_state(board_size, board_size)
            node = Node(state)
            for step in it.count():
                # Act immediately if only one action available
                valid_actions = state.valid_actions()
                if len(valid_actions) == 1:
                    state = state.perform(valid_actions[0])
                    continue

                print("player Tree AI")
                node = mcts(node, max_depth=5, run_time=10)
                if node.state.is_leaf():
                    print("Tree AI win! Final score is", final_score(node.state))
                    rlist.append("Tree")
                    rlist.append(final_score(node.state))
                    break
                print("player NN_AI")
                node = nn_decide(node, max_depth=5, run_time=10, method=nn_puct)
                print(node.state)
                if node.state.is_leaf():
                    print("NN AI win! Final score is", final_score(node.state))
                    rlist.append("NN")
                    rlist.append(final_score(node.state))
                    break
            writer.writerow(rlist)
            c_write.close()
