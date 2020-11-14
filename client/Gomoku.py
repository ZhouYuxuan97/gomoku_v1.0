import numpy as np


class GomokuState(object):
    def __init__(self, board):
        self.board = board.copy()

    def __str__(self):
        return "\n".join(["".join(row) for row in self.board])

    def is_leaf(self):
        if self.score_for_max_player() != 0: return True
        return (self.board == "_").sum() == 0

    def score_for_max_player(self):
        for x in range(self.board.shape[0] - 5):
            for y in range(self.board.shape[1] - 5):
                for player, score in zip("XO", [+1, -1]):
                    subBoard = self.board[x:x + 5, y:y + 5]
                    if (subBoard == player).all(axis=0).any(): return score
                    if (subBoard == player).all(axis=1).any(): return score
                    if (np.diag(subBoard) == player).all(): return score
                    if (np.diag(np.rot90(subBoard)) == player).all(): return score
        return 0

    def is_max_players_turn(self):
        return (self.board == "O").sum() == (self.board == "X").sum()

    def is_min_players_turn(self):
        return not self.is_max_players_turn()

    def valid_actions(self):
        """
        only choose actions within distance 4 to the outside-most stones?
            what should be the requirements? board_size>20 && stone_number<threshold?
        """
        return list(zip(*np.nonzero(self.board == "_")))  # all empty positions

    def perform(self, action):
        player = "X" if self.is_max_players_turn() else "O"
        row, col = action
        new_state = GomokuState(self.board)
        new_state.board[row, col] = player
        return new_state


def initial_state(x=20, y=20):
    board = np.empty((x, y), dtype=str)
    board[:] = "_"
    return GomokuState(board)


if __name__ == "__main__":
    state = initial_state()
    print(state)
    print(state.valid_actions())
    while True:
        if state.is_leaf(): break
        actions = state.valid_actions()
        print(actions)
        # if len(actions) == 0: break # useless line?
        state = state.perform(actions[0])
        print(state)
    print("max score, is over:")
    print(state.score_for_max_player())
    print(state.is_leaf())
