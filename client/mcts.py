import time

import numpy as np

from client.Gomoku import GomokuState, initial_state


class Node(object):
    def __init__(self, state: GomokuState, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.expand = False
        self.score_total = 0
        self.N = 0
        self.Q = 0

    def get_children(self):
        actions = self.state.valid_actions()
        children = []
        for action in actions:
            children.append(Node(self.state.perform(action), self))
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
            # for uct in uct_children:
            #     print(uct, end=" ")
            c = np.argmax(uct_children)
            if not self.children[c].expand:  # not expanded, done
                return self.children[c]
            return self.children[c].choose_child("uct")  # expanded, recursively find unexpanded child
        return None


CONFIDENT = 1.96  # constant C in UCT

def rollout(node):
    if node.state.is_leaf():
        result = node.state.score_for_max_player()
    else:
        result = rollout(node.choose_child("random"))
    return result

def back_propagate(node, result):
    node.score_total += result
    node.N += 1
    node.Q = node.score_total / node.N
    while (not node.parent == None):
        node = node.parent
        node.score_total += result
        node.N += 1
        node.Q = node.score_total / node.N

def mcts(node):
    iterate = 1
    time_start = time.time()
    # start mcst
    while (time.time() - time_start < 20):
        # print("\n======= iteration",iterate, "=======")
        selection_child = node.choose_child("uct")  # choose an unexpanded child using UCT
        expansion_child = selection_child.choose_child("random")  # expand the chosen child
        result = rollout(expansion_child)
        back_propagate(expansion_child, result)

        selection_child.expand = True
        iterate += 1

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


def cal_processed_nodes(node):
    count = 1
    if node.children == []:
        return count
    for child in node.children:
        if child.N != 0:
            count += cal_processed_nodes(child)
    return count


if __name__ == "__main__":
    curNode = Node(initial_state())
    print(curNode.state)

    child = mcts(curNode)

    print()
    print(child.state)
