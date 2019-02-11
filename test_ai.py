from ai1 import PentagoGame, GameState
from games import alphabeta_cutoff_search
from timeit import timeit
import time
from pprint import pprint
game = PentagoGame()


def utility_test(win_threshold=15, not_win_threshold=5):

    tests = [
        [
            [
                [0, None, 0, 0, 0, 0],
                [None, 1, None, None, None, None],
                [None, None, 1, None, None, None],
                [None, None, None, 1, None, None],
                [None, None, None, None, 1, None],
                [None, None, None, None, None, None],
            ],
            (-1, not_win_threshold)
        ],

        [
            [
                [0, None, None, None, None, None],
                [None, 0, None, None, None, None],
                [None, None, 0, None, None, None],
                [None, None, None, 0, None, None],
                [None, None, None, None, 0, None],
                [None, None, None, None, None, 0],
            ],
            (win_threshold, 10000)
        ],

        [
            [
                [None, None, None, None, None, None],
                [0, None, None, None, None, None],
                [None, 0, None, None, None, None],
                [None, None, 0, None, None, None],
                [None, None, None, 0, None, None],
                [None, None, None, None, 0, None],
            ],
            (win_threshold, 10000)
        ],

        [
            [
                [None, None, None, None, None, 0],
                [None, None, None, None, 0, None],
                [None, None, None, 0, None, None],
                [None, None, 0, None, None, None],
                [None, 0, None, None, None, None],
                [None, None, None, None, None, None],
            ],
            (win_threshold, 10000)
        ],

        [
            [
                [None, None, None, None, None, 0],
                [None, None, None, None, 0, None],
                [None, None, None, 0, None, None],
                [None, None, 0, None, None, None],
                [None, 0, None, None, None, None],
                [0, None, None, None, None, None],
            ],
            (win_threshold, 10000)
        ],

        [
            [
                [1, 1, 1, 1, 1, 0],
                [None, None, None, None, 0, None],
                [None, None, None, 0, None, None],
                [None, None, 0, None, None, None],
                [None, 0, None, None, None, None],
                [0, None, None, None, None, None],
            ],
            (-win_threshold, win_threshold)
        ],

        [
            [
                [None, None, None, None, None, None],
                [None, None, None, None, 0, None],
                [None, None, None, 0, None, None],
                [None, None, 0, None, None, None],
                [None, 0, None, None, None, None],
                [1, None, None, None, None, None],
            ],
            (0, not_win_threshold)
        ],

        [
            [
                [None, 1, 0, None, 0, 0],
                [0, None, 1, None, None, None],
                [None, 0, None, 1, 0, 0],
                [None, None, None, None, 1, None],
                [None, None, None, 1, None, 1],
                [None, None, None, None, None, None],
            ],
            (-100000, -win_threshold)
        ],

        [
            [
                [0, 0, 0, 0, 0, None],
                [None, None, None, None, None, None],
                [1, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None]
            ],
            (win_threshold, 100)
        ],

        [
            [
                [0, 0, 0, None, 0, 0],
                [None, None, None, None, None, None],
                [1, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None]
            ],
            (0, not_win_threshold)
        ],
    ]

    for i, (array, (minv, maxv)) in enumerate(tests):
        ut = game.utility(array, 0)
        if not minv < ut < maxv:
            print("Utility Test %s failed." % i)
            pprint(array)
            print("%.2f" % ut)


def decision_test1():
    array = [
        [0, 0, 0, 0, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]
    state = game.make_state(array=array, num_moves=1)
    move = alphabeta_cutoff_search(state, game, d=1)
    print('move:', move)
    assert move[0] == (0, 4)
    print("passes decision_test1")


def decision_test2():
    array = [
        [0, None, None, None, None, None],
        [None, 0, None, None, None, None],
        [None, None, 0, None, None, None],
        [None, None, None, 0, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]
    state = GameState(array=array, num_moves=1, utility=None)
    move = alphabeta_cutoff_search(state, game, d=1)
    print(move)
    # assert  move[0] == (4, 4)
    print("passes decision_test2")


def time_utility():
    array = [
        [0, 1, 1, 1, None, 1],
        [None, 0, None, None, None, None],
        [None, 1, 0, None, None, None],
        [None, 1, None, 0, None, None],
        [None, 1, None, None, None, None],
        [None, 1, None, 0, None, None],
    ]
    state = GameState(array=array, num_moves=1, utility=None)
    number = 100000
    utility = game.utility

    t0 = time.clock()
    for i in range(number):
        utility(state, 0)
    t1 = time.clock()

    print('%s repetition in %.3fs.' % (number, t1 - t0))


def make_state_test():
    # 1
    game = PentagoGame()
    state = game.make_state()
    assert state.num_moves == 0

    # 2
    array = [
        [0, 1, 1, 1, None, 1],
        [None, 0, None, None, None, None],
        [None, 1, 0, None, None, None],
        [None, 1, None, 0, None, None],
        [None, 1, None, None, None, None],
        [None, 1, None, 0, None, None],
    ]
    state = game.make_state(array=array)
    assert state.num_moves == 13


def time_moves():
    from board import Board
    b = Board()

    t0 = time.clock()
    number = 10000
    for i in range(number):
        b.rotate(1, 1, 1)
        b.array[2][4] = 1
        b.rotate(1, 1, 0)
        b.array[4][4] = 1
        b.rotate(4, 1, 0)
        b.array[4][4] = 1
        b.rotate(4, 1, 1)
        b.array[4][4] = 1
        b.rotate(1, 4, 0)
        b.array[4][4] = 1
        b.rotate(1, 4, 1)
        b.array[4][4] = 1
        b.rotate(4, 4, 0)
        b.array[4][4] = 1
        b.rotate(4, 4, 1)
        b.array[4][4] = 1
    t1 = time.clock()
    dt = t1 - t0
    print("%i board operations in %.3fs." % (number * 8, dt))


def time_decision():
    arrays =  [
        [
            [None,    1, None, None, None, None],
            [None, None,    1, None,    0, None],
            [None,    0, None,    1, None,    0],
            [None, None, None, None,    1, None],
            [None, None, None,    0, None, None],
            [None, None, None, None, None, None],
        ],
        [
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ],
        [
            [   0,    0,    0,    0, None, None],
            [None, None,    1, None, None, None],
            [None, None,    1, None, None, None],
            [None, None,    1, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ],
        [
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None,    1, None, None, None, None],
            [   0,    0, None,    0,    0,    0],
            [None, None,     1, None,   1, None],
            [None, None,     1, None, None, None],
        ],
    ]
    game = PentagoGame()

    times = []
    for array in arrays:
        state = game.make_state(array =array)
        t0 = time.clock()
        alphabeta_cutoff_search(state, game, d=2)
        t1 = time.clock()
        d = t1 - t0
        times.append(d)
        print("%.3f" % d)

    print('search took %.3fs.' % sum(times))
    print("times = ", times)


def first_action_test():
    state = game.make_state()
    actions = game.actions(state)
    print("%s actions for the starting state" % len(actions))


if __name__ == '__main__':
    # utility_test()
    # time_utility()
    # make_state_test()
    # decision_test1()
    # decision_test2()
    # time_moves()
    time_decision()
    # first_action_test()
