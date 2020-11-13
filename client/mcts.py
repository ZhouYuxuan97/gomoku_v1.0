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
            print("choose child randomly")
            c = np.random.randint(len(self.children))
            return self.children[c]
        if choose == "uct":  # use UCT to choose a child
            print("choose child UCT")
            uct_children = [child.Q + np.sqrt(1.96 * np.log(self.N + 1) / (child.N + 0.01)) for child in self.children]
            for uct in uct_children:
                print(uct, end=" ")
            # uct_sorted_children = list(zip(uct_children, range(len(uct_children)))).sort(key=lambda arr:arr[0], reverse=True)
            # for (_, c) in uct_sorted_children:
            #     if not children[c].expand:  # not expanded, done
            #         return children[c]
            # # all expanded
            # return None
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
    # for _ in range(5):
    #     rollout(node)
    # i = np.argmax([child.score_estimate for child in node.children()])
    iterate = 1
    time_start = time.time()
    # start mcst
    while (time.time() - time_start < 60):
        print("=======iteration", iterate, "=======")
        selection_child = node.choose_child("uct")  # choose an unexpanded child using UCT
        expansion_child = selection_child.choose_child("random")  # expand the chosen child
        result = rollout(expansion_child)
        back_propagate(expansion_child, result)
        iterate += 1
    i = np.argmax([child.Q + np.sqrt(CONFIDENT * np.log(node.N) / (child.N + 0.01)) for child in node.children])
    return node.children[i]


if __name__ == "__main__":
    state = initial_state()
    print(state)

    curNode = Node(state)
    child = mcts(curNode)

    for child in curNode.children:
        print(child.N, child.Q, end=" | ")
    print(child.state)
