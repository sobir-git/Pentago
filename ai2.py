from games import GameState, Game, alphabeta_cutoff_search
from collections import namedtuple
GameState = namedtuple('GameState', 'num_moves, b, utility, results')
import pdb
from math import sqrt
from pprint import pprint
from binboard import (generate_all_diagonal_masks, 
                      generate_rotation_map,
                      generate_quarter_masks, array_to_bin,
                      bin_to_array)


class PentagoGame(Game):

    diagonal_masks_by_size = [None] * 6
    for i in range(3, 6):
        diagonal_masks_by_size[i] = generate_all_diagonal_masks(i)

    rotation_map = generate_rotation_map()
    quarter_masks = generate_quarter_masks()


    def make_state(self, b=None, num_moves=None):
        if b is None:
            b = 0
        if num_moves is None:
            num_moves = bin(b).count('1')
        utility = self.utility(b, 0, sep=True)
        state = GameState(b=b, num_moves=num_moves, utility=utility, results={})
        return state

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        moves = []
        b = state.b
        mask = 1 | (1<<36)
        for i in range(36):
            if mask << i & b:
                continue
            no_neutral_rotations_yet = True
            for q in range(4):
                for move in (i, q, 0), (i, q, 1):
                    if state.num_moves > 7:
                        moves.append(move)
                        continue
                    new_b = self.rotate(b, q, move[-1])
                    append = False
                    if new_b != b:
                        moves.append(move)
                    elif no_neutral_rotations_yet:
                        moves.append(move)
                        no_neutral_rotations_yet = False

        # print(moves)
        for move in moves:
            state.results[move] = self.result(state, move, cache=False)

        # reorder moves
        player = state.num_moves % 2
        uts = {move: game.utility(state.results[move], player) for move in moves}
        moves.sort(key=lambda m: uts[m], reverse=True)
        return moves


    def to_move(self, state):
        return state.num_moves % 2


    def result(self, state, move, cache=True):
        """Return the state that results from making a move from a state."""
        i, q, clockwise = move
        # print('move: %r' % (move,))
        # pprint(bin_to_array(state.b))
        if cache:
            try:
                return state.results[move]
            except KeyError:
                pass

        if state.num_moves % 2 == 0:
            new_b = state.b | 1 << i
        else:
            new_b = state.b | 1 << (36 + i)
        new_b = self.rotate(new_b, q, clockwise)
        games_state = game.make_state(b=new_b, num_moves=state.num_moves + 1)

        # print('resulted to')
        # pprint(bin_to_array(new_b))
        return games_state

    def rotate(self, b, q, clockwise):
        quarter_mask = self.quarter_masks[q]
        quarter_binboard = b & quarter_mask
        hash_ = quarter_binboard | (clockwise << 72)
        rotated_quarter_binboard = self.rotation_map[hash_]
        rotated_binboard = b & (~ quarter_mask) | rotated_quarter_binboard
        return rotated_binboard

    def utility(self, state, player, sep=False, verbous=False):
        """Return the value of this final state to player."""

        if isinstance(state, GameState):
            if state.utility:
                ut = state.utility
                return ut[player] - ut[1 - player]
            b = state.b
        else:
            b = state
        ut = self._utility(b)
        if sep:
            return ut
        else:
            return ut[player] - ut[1 - player]


    def _utility(self, b):
        ch0, ch1 = 0, 0
        for size in range(3, 6):
            for mask0, mask1 in self.diagonal_masks_by_size[size]:
                if mask0 & b == mask0:
                    ch0 += 10 ** size
                if mask1 & b == mask1:
                    ch1 += 10 ** size
        return ch0, ch1


    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        if max(state.utility) >= 100000:
            # print("terminal_test:\n%r" % state)
            return True
        return False


game = PentagoGame()


def move(array, token):
    b = array_to_bin(array)
    state = game.make_state(b=b)
    i, q, clockwise = alphabeta_cutoff_search(state, game, d=2)
    coor = (i // 6, i % 6)
    center = [(1, 1), (1, 4), (4, 1), (4, 4)][q]
    move = (coor, center, clockwise)
    print("token: %s  |  move: %s" % (state.num_moves % 2, move))
    return move


# def demo_play():
#     array = [[None] * 6 for _ in range(6)]
#     num_moves = 0
#     state = GameState(array=array, num_moves=num_moves, utility=None)
#     while True:
#         move = alphabeta_cutoff_search(state, game, d=3)

#         print("token: %s  |   move: %s" % (state.num_moves % 2, move))
#         game.display(state)
#         print()
#         # input('                                       ....continue?')
#         new_state = game.result(state, move)
#         state = new_state


if __name__ == '__main__':
    # utility_test()
    demo_play()
