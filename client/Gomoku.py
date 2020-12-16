import numpy as np

SCORE_5 = 100
SCORE_RIVAL_5 = 70
SCORE_4 = 10
SCORE_RIVAL_4 = 8
SCORE_3 = 5
SCORE_RIVAL_3 = 3
SCORE_2 = 2
SCORE_RIVAL_2 = 1


class GomokuState(object):
    def __init__(self, board, turn):
        self.board = board.copy()
        self.turn = turn  # 1:X(make first move) 2:O

    def __str__(self):
        return "\n".join(["".join(row) for row in self.board])

    def is_leaf(self):
        for x in range(self.board.shape[0] - 4):
            for y in range(self.board.shape[1] - 4):
                subBoard = self.board[x:x + 5, y:y + 5]
                if (subBoard == "X").all(axis=0).any() or (subBoard == "X").all(axis=1).any() or (
                        np.diag(subBoard) == "X").all() or (np.diag(np.rot90(subBoard)) == "X").all():
                    return True
                if (subBoard == "O").all(axis=0).any() or (subBoard == "O").all(axis=1).any() or (
                        np.diag(subBoard) == "O").all() or (np.diag(np.rot90(subBoard)) == "O").all():
                    return True
        return (self.board == "_").sum() == 0

    def score_for_max_player(self):
        score = 0
        for x in range(self.board.shape[0] - 1):
            for y in range(self.board.shape[1] - 1):
                # check 5
                if x < self.board.shape[0] - 4 and y < self.board.shape[1] - 4:
                    subBoard = self.board[x:x + 5, y:y + 5]
                    if self.turn == 1:
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_5
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_5
                        if (np.diag(subBoard) == "X").all(): score += SCORE_5
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_5
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_RIVAL_5
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_RIVAL_5
                        if (np.diag(subBoard) == "O").all(): score += SCORE_RIVAL_5
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_RIVAL_5
                    if self.turn == 2:
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_5
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_5
                        if (np.diag(subBoard) == "O").all(): score += SCORE_5
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_5
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_RIVAL_5
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_RIVAL_5
                        if (np.diag(subBoard) == "X").all(): score += SCORE_RIVAL_5
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_RIVAL_5
                # check 4
                if x < self.board.shape[0] - 3 and y < self.board.shape[1] - 3:
                    subBoard = self.board[x:x + 4, y:y + 4]
                    if self.turn == 1:
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_4
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_4
                        if (np.diag(subBoard) == "X").all(): score += SCORE_4
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_4
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_RIVAL_4
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_RIVAL_4
                        if (np.diag(subBoard) == "O").all(): score += SCORE_RIVAL_4
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_RIVAL_4
                    if self.turn == 2:
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_4
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_4
                        if (np.diag(subBoard) == "O").all(): score += SCORE_4
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_4
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_RIVAL_4
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_RIVAL_4
                        if (np.diag(subBoard) == "X").all(): score += SCORE_RIVAL_4
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_RIVAL_4
                # check 3
                if x < self.board.shape[0] - 2 and y < self.board.shape[1] - 2:
                    subBoard = self.board[x:x + 3, y:y + 3]
                    if self.turn == 1:
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_3
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_3
                        if (np.diag(subBoard) == "X").all(): score += SCORE_3
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_3
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_RIVAL_3
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_RIVAL_3
                        if (np.diag(subBoard) == "O").all(): score += SCORE_RIVAL_3
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_RIVAL_3
                    if self.turn == 2:
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_3
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_3
                        if (np.diag(subBoard) == "O").all(): score += SCORE_3
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_3
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_RIVAL_3
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_RIVAL_3
                        if (np.diag(subBoard) == "X").all(): score += SCORE_RIVAL_3
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_RIVAL_3
                # check 2
                if x < self.board.shape[0] - 1 and y < self.board.shape[1] - 1:
                    subBoard = self.board[x:x + 2, y:y + 2]
                    if self.turn == 1:
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_2
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_2
                        if (np.diag(subBoard) == "X").all(): score += SCORE_2
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_2
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_RIVAL_2
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_RIVAL_2
                        if (np.diag(subBoard) == "O").all(): score += SCORE_RIVAL_2
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_RIVAL_2
                    if self.turn == 2:
                        if (subBoard == "O").all(axis=0).any(): score += SCORE_2
                        if (subBoard == "O").all(axis=1).any(): score += SCORE_2
                        if (np.diag(subBoard) == "O").all(): score += SCORE_2
                        if (np.diag(np.rot90(subBoard)) == "O").all(): score += SCORE_2
                        if (subBoard == "X").all(axis=0).any(): score += SCORE_RIVAL_2
                        if (subBoard == "X").all(axis=1).any(): score += SCORE_RIVAL_2
                        if (np.diag(subBoard) == "X").all(): score += SCORE_RIVAL_2
                        if (np.diag(np.rot90(subBoard)) == "X").all(): score += SCORE_RIVAL_2
        return score

    def is_max_players_turn(self):
        # current player is X
        if self.turn == 1:
            return np.sum(self.board == "X") == np.sum(self.board == "O")
        # current player is O
        return np.sum(self.board == "X") > np.sum(self.board == "O")

    def valid_actions(self):
        """
        only choose actions within distance 4 to the outside-most stones?
            what should be the requirements? board_size>20 && stone_number<threshold?
        """
        return list(zip(*np.nonzero(self.board == "_")))  # all empty positions

    def perform(self, action):
        row, col = action
        if self.turn == 1:
            player = "X"
            new_state = GomokuState(self.board, 2)
        else:
            player = "O"
            new_state = GomokuState(self.board, 1)
        new_state.board[row, col] = player
        return new_state


def initial_state(x=10, y=10):
    board = np.empty((x, y), dtype=str)
    board[:] = "_"
    return GomokuState(board, 1)


if __name__ == "__main__":
    state = initial_state()
    print(state)
    print(state.valid_actions())
    while True:
        if state.is_leaf(): break
        actions = state.valid_actions()
        print(actions)
        state = state.perform(actions[0])
        print(state)
    print("max score, is over:")
    print(state.score_for_max_player())
    print(state.is_leaf())
