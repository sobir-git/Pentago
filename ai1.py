from games import GameState, Game, alphabeta_cutoff_search
from collections import namedtuple
GameState = namedtuple('GameState', 'num_moves, array, utility')
import pdb
from math import sqrt
from pprint import pprint


def run_diagonals():
    diagonals = []

    for i in range(6):
        for j in range(6):
            if i * j * (5-i) * (5-j) != 0:
                continue
            for di, dj in ((0, 1), (1, 0), (1, 1), (-1, 1)):
                ii = i
                jj = j
                d = []
                while 0 <= ii <= 5 and 0 <= jj <= 5:
                    d.append( (ii,jj) )
                    ii, jj = ii + di, jj + dj
                if len(d) >= 6:
                    diagonals.append(tuple(sorted(d)))

            if (i, j) in ((1, 0), (0, 1), (0, 4), (1, 5)):
                for di, dj in ((1, 1), (1, -1)):
                    ii = i
                    jj = j
                    d = []
                    while 0 <= ii <= 5 and 0 <= jj <= 5:
                        d.append( (ii,jj) )
                        ii, jj = ii + di, jj + dj
                    if len(d) >= 5:
                        diagonals.append(tuple(sorted(d)))

    return diagonals


class PentagoGame(Game):
    centers = ((1, 1), (1, 4), (4, 1), (4, 4))
    diagonals = run_diagonals()

    ind = {}
    for i, j in ((1, 1), (1, 4), (4, 1), (4, 4)):
        normal1 = ((i-1, j), (i, j+1), (i+1, j), (i, j-1))
        normal2 = ((i-1, j+1), (i+1, j+1), (i+1, j-1), (i-1,j-1))
        rev1 = tuple(reversed(normal1)) 
        rev2 = tuple(reversed(normal2)) 
        ind[(i, j)] = ((rev1, rev2), (normal1, normal2))

    chess_black = [
                    [
                        [(0, 1), (1, 2), (2, 1), (1, 0)],
                        []
                    ],
                    [   
                        [],
                        [(5, 4), (4, 5), (4, 3), (3, 4)]
                    ]
                  ]

    def make_state(self, array=None, num_moves=None):
        if array is None:
            array = [ [None] * 6 for _ in range(6) ]
        if num_moves is None:
            num_moves = sum(sum(i is not None for i in row) for row in array)
        utility = self.utility(array, 0, sep=True)
        state = GameState(array=array, num_moves=num_moves, utility=utility)
        return state

    def rotate(self, a,  center, clockwise):
        for ind in self.ind[center][clockwise]:
            xor, yor = ind[0]
            prev = a[xor][yor]
            for x, y in ind:
                now = a[x][y]
                a[x][y] = prev
                prev = now
            a[xor][yor] = prev

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        moves = []
        array = state.array
        for i, row in enumerate(array):
            for j, token in enumerate(row):
                if array[i][j] is not None:
                    continue

                no_neutral_rotation_yet = True
                for center in self.centers:
                    for move in  (((i, j), center, 0), ((i, j), center, 1)):
                        if state.num_moves > 7:
                            moves.append( move )
                            continue

                        new_array = [row[:] for row in array]
                        self.rotate(new_array, center, move[-1])
                        if new_array != array:
                            moves.append( move )
                        elif no_neutral_rotation_yet:
                            moves.append( move )
                            no_neutral_rotation_yet = False
        return moves

    def to_move(self, state):
        return state.num_moves % 2

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        coor, center, clockwise = move
        array_new = [row[:] for row in state.array]
        num_moves = state.num_moves
        array_new[coor[0]][coor[1]] = state.num_moves % 2
        self.rotate(array_new, center, clockwise)
        games_state = game.make_state(array=array_new, num_moves=num_moves + 1)
        return games_state

    def utility(self, state, player, sep=False, verbous=False):
        """Return the value of this final state to player."""

        if isinstance(state, GameState):
            if state.utility:
                ut = state.utility
                return ut[player] - ut[1 - player]
            array = state.array
        else:
            array = state
        token = player
        stats = []
        for diagonal in self.diagonals:
            if verbous: print("checking diagonal:", diagonal)
            if len(diagonal) == 5:
                free = 0
                one = 0
                zero = 0
                for i, j in diagonal:
                    v = array[i][j]
                    if v == 1: one += 1
                    elif v == 0: zero += 1
                    else: free += 1
                stat = (zero, one, free, 5)
                stats.append(stat)
                if verbous: print(stat)
            else:  # len diagonal = 6
                zero = 0
                one = 0
                free = 0
                owe = 0
                count = 0
                last_token = -10
                li = -1
                for n, (i, j) in enumerate(diagonal):
                    v = array[i][j]
                    if v is None:
                        count += 1
                        free += 1
                        owe += 1
                    elif v == last_token:
                        count += 1
                        li = n
                    else:
                        # if enough up to this point
                        if count >= 5:
                            continue
                        elif 5 - li < 5:
                            break
                        if last_token == -10:
                            last_token = v
                            li = n
                            count = n + 1
                            owe = n
                        else:
                            count = n - li
                            last_token = v
                            owe = count - 1
                            li = n
                    if owe > 2:
                        break
                    if v == 1: one += 1
                    elif v == 0: zero += 1
                else:
                    if count == 6:
                        i, j = diagonal[0]
                        first = array[i][j]
                        i, j = diagonal[5]
                        last = array[i][j]
                        count = 5
                        if (first is None) or (last is None):
                            owe -= 1
                        if (first is None) and (last is None) and owe == 2:
                            owe = 0
                            # this is a check mate position
                    stat = (owe, count, last_token, 6)
                    if verbous: print(stat)
                    stats.append(stat)

        # working with stats
        chance = [0, 0]
        for stat in stats:
            if stat[-1] == 5:
                zero, one, free, size = stat
                if one + free == 5:
                    chance[1] += 1 / (free + 0.1)**1.5
                if zero + free == 5:
                    chance[0] += 1 / (free + 0.1)**1.5
            else:
                owe, count, last_token, size = stat
                if 0 <= last_token <= 1 and owe < 3:
                    chance[last_token] += 1 / (owe + 0.1)**1.5

        if verbous:
            pprint(array)
            print('utility:', chance)

        if sep:
            return (chance[0], chance[1])
        else:
            return chance[token] - chance[1-token]


    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        if state.utility is None:
            return False
        if max(state.utility) > 10:
            # print('hurray, terminal test detected')
            # pprint(state.array)
            # print('utility: %.2f, %.2f' % state.utility)
            return True
        return max(state.utility) > 10


    def display(self, state):
        p = lambda el: "%2s" % (el if el is not None else '.')
        res = []
        for row in state.array:
            res.append(''.join(map(p, row)))
        res = '\n'.join(res)
        print(res)


game = PentagoGame()


def move(array, token):
    num_moves = token
    state = GameState(array=array, num_moves=num_moves, utility=None)
    move = alphabeta_cutoff_search(state, game, d=2)
    print("token: %s  |  move: %s" % (state.num_moves % 2, move))
    return move


def demo_play():
    array = [[None]*6 for _ in range(6)]
    num_moves = 0
    state = GameState(array=array, num_moves=num_moves, utility=None)
    while True:
        move = alphabeta_cutoff_search(state, game, d=3)

        print("token: %s  |   move: %s"% (state.num_moves % 2, move))
        game.display(state)
        print()
        # input('                                       ....continue?')
        new_state = game.result(state, move)
        state = new_state


if __name__ == '__main__':
    # utility_test()
    demo_play()
