import csv
import time
import random
import numpy as np

from client.Gomoku import GomokuState, initial_state


class Node(object):
    def __init__(self, state: GomokuState, depth=0):
        self.state = state
        # self.parent = parent
        self.children = []
        self.expand = False
        self.depth = depth
        self.score_total = 0
        self.N = 0
        self.Q = 0

    def get_children(self):
        actions = self.state.valid_actions()
        children = []
        for action in actions:
            children.append(Node(self.state.perform(action), self.depth + 1))
        return children

    def choose_child(self, choose="random"):
        if self.children == []:
            self.children = self.get_children()
        if choose == "random":  # randomly choose a child
            c = np.random.randint(len(self.children))
            return self.children[c]
        if choose == "uct":  # use UCT to choose a child
            uct_children = [child.Q + np.sqrt(CONFIDENT * np.log(self.N + 1) / (child.N + 1)) for child in
                            self.children]
            c = np.argmax(uct_children)
            return self.children[c]

    def choose_child_nn(self, method):
        if self.children == []:
            self.children = self.get_children()
        return method(self)


CONFIDENT = 1.96  # constant C in UCT


def rollout(node, max_depth=None):
    if node.depth == max_depth or node.state.is_leaf():
        result = node.state.score_for_max_player()
    else:
        result = rollout(node.choose_child("random"), max_depth)
    node.N += 1
    node.score_total += result
    node.Q = node.score_total / node.N
    return result


def rollout_nn(node, max_depth, method):
    if node.depth == max_depth or node.state.is_leaf():
        result = node.state.score_for_max_player()
    else:
        result = rollout_nn(node.choose_child_nn(method), max_depth, method)
    node.N += 1
    node.score_total += result
    node.Q = node.score_total / node.N
    return result


def mcts(node, max_depth=None, run_time=20):
    node.depth = 0
    print("current player:", node.state.turn)

    # start mcst
    time_start = time.time()
    while (time.time() - time_start < run_time):
        rollout(node, max_depth)

    # choose a middle-most position among largest uct?
    # i = np.argmax([child.Q + np.sqrt(CONFIDENT * np.log(node.N+1) / (child.N + 1)) for child in node.children])
    uct_children = [child.Q + np.sqrt(CONFIDENT * np.log(node.N + 1) / (child.N + 1)) for child in node.children]
    max_uct = max(uct_children)
    positions = []  # (x,y) of max uct
    for i, uct in enumerate(uct_children):
        if uct == max_uct:
            positions.append((int(i / node.state.board.shape[1]), i % node.state.board.shape[1], i))
    min_dis_2_mid_x = 9999
    min_dis_2_mid_y = 9999
    middle_most_i = -1
    for x, y, i in positions:
        dis_2_mid_x = abs(node.state.board.shape[0] / 2 - x)
        dis_2_mid_y = abs(node.state.board.shape[1] / 2 - y)
        if dis_2_mid_x < min_dis_2_mid_x and dis_2_mid_y < min_dis_2_mid_y:
            min_dis_2_mid_x = dis_2_mid_x
            min_dis_2_mid_y = dis_2_mid_y
            middle_most_i = i

    print("======= MCTS Finish=======")
    print("Total number of processed ACTIONs(direct children) of current root node is",
          sum(np.array([child.N for child in node.children]) != 0))
    print("Total number of all processed nodes is", cal_processed_nodes(node))
    print(node.children[middle_most_i].state)
    return node.children[middle_most_i]


def nn_decide(node, max_depth, run_time, method):
    node.depth = 0
    time_start = time.time()
    while (time.time() - time_start < run_time):
        rollout_nn(node, max_depth, method)
    i = np.argmax([child.Q for child in node.children])
    return node.children[i]

def cal_processed_nodes(node):
    count = 1
    if node.children == []:
        return count
    for child in node.children:
        if child.N != 0:
            count += cal_processed_nodes(child)
    return count


def random_put(state: GomokuState):
    # computer plays white
    choice = {}
    count = 0
    for i in range(np.size(state.board, 0)):
        for j in range(np.size(state.board, 1)):
            if state.board[i][j] == '_':
                count += 1
                choice[count] = [i, j]
    random_pick = random.randint(1, count)
    state.board[choice[random_pick][0]][choice[random_pick][1]] = 'O'
    state.turn = 1
    return state


if __name__ == "__main__":
    c_write = open("result_10_1.csv", "a+", newline='')
    writer = csv.writer(c_write)
    for i in range(10):
        # rootNode = Node(random_put(initial_state(15,15)))
        rootNode = Node(initial_state(10, 10))
        rlist = []
        curNode = rootNode
        print(curNode.state)
        total = 0
        final_Q = 0
        while not curNode.state.is_leaf():
            child = mcts(curNode, 10)
            final_Q = child.Q
            total += cal_processed_nodes(curNode)
            print(total)
            print("-----------------")
            print(child.state)
            curNode = Node(random_put(child.state))
            # curNode = child.choose_child()
            print("-----------------")
            print(curNode.state)

        print("{} game finish, number of tree nodes processed is {}".format(i, total))
        rlist.append(curNode.state.score_for_max_player())
        rlist.append(total)
        rlist.append(final_Q)
        writer.writerow(rlist)
    # rootNode = Node(random_put(initial_state()))
    # curNode = rootNode
    # print(curNode.state)
    c_write.close()
