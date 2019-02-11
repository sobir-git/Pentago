from ai2 import PentagoGame, GameState
from games import alphabeta_cutoff_search
from timeit import timeit
import time
from pprint import pprint
game = PentagoGame()
from binboard import bin_to_array, array_to_bin


def utility_test(win_threshold=60000, not_win_threshold=40000):
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
            (-1000, not_win_threshold)
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
            (win_threshold, 1000000)
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
            (win_threshold, 1000000)
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
            (win_threshold, 1000000)
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
            (win_threshold, 1000000)
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
            (0, win_threshold * 2)
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
            (-10000000, -win_threshold)
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
            (win_threshold, 100000000000)
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
        b = array_to_bin(array)
        ut = game.utility(b, 0)
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
    b = array_to_bin(array)
    state = game.make_state(b=b, num_moves=1)
    move = alphabeta_cutoff_search(state, game, d=1)
    print('move:', move)
    assert move[0] == 4
    print("passes decision_test1")


def decision_test2():
    array = [
        [   0, None, None, None, None, None],
        [None,    0, None, None, None, None],
        [None, None,    0, None, None, None],
        [None, None, None,    0, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]
    b = array_to_bin(array)
    state = game.make_state(b=b, num_moves=1)
    move = alphabeta_cutoff_search(state, game, d=1)
    print('move:', move)
    assert move[0] == 28
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

    b = array_to_bin(array)
    number = 100000
    utility = game.utility

    t0 = time.clock()
    for i in range(number):
        game.utility(b, 0)
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
    b = array_to_bin(array)
    state = game.make_state(b=b)
    assert state.num_moves == 13


def time_decision():
    game = PentagoGame()
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

    times = []
    for b in map(array_to_bin, arrays):
        state = game.make_state(b=b)

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
    print("%s actions fo r the starting state" % len(actions))


def test_terminal_state():
    game = PentagoGame()
    array = [
        [0,    0,    0,    0,    0, None],
        [None, 0, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, 0, None, None],
        [None, None, None, None, 0, None],
        [None, None, None, None, None, None],
    ]
    b = array_to_bin(array)
    state = game.make_state(b=b, num_moves=1)
    assert game.terminal_test(state)
    print("passes terminal test")


if __name__ == '__main__':
    # utility_test()
    # time_utility()
    # make_state_test()
    # decision_test1()
    # decision_test2()
    # time_moves()
    time_decision()
    # first_action_test()
    # test_terminal_state()
