from binboard import (
    array_to_bin, bin_to_array, generate_all_diagonals,
    generate_quarter_masks, generate_all_board_quarters,
    generate_rotation_map, rotate_array, utility,
    generate_all_diagonal_masks)

from pprint import pprint
import time
import random


def test_array_bin_array():
    array = [
        [0, 1, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 1, 0],
    ]
    bin_rep = 0b010000000000000000000000000000000010100000000000000000000000000000000001
    b = array_to_bin(array, empty=2)
    assert b == bin_rep

    # binary to array test
    assert bin_to_array(b, empty=2) == array


def test_generate_quarter_masks():
    masks = generate_quarter_masks()
    arrays = []
    for mask in masks:
        b = mask | (0 << 36)
        arrays.append(bin_to_array(b, empty=2))
    assert arrays == [
        [[0, 0, 0, 2, 2, 2],
         [0, 0, 0, 2, 2, 2],
         [0, 0, 0, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2]],

        [[2, 2, 2, 0, 0, 0],
         [2, 2, 2, 0, 0, 0],
         [2, 2, 2, 0, 0, 0],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2]],

        [[2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [0, 0, 0, 2, 2, 2],
         [0, 0, 0, 2, 2, 2],
         [0, 0, 0, 2, 2, 2]],

        [[2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2],
         [2, 2, 2, 0, 0, 0],
         [2, 2, 2, 0, 0, 0],
         [2, 2, 2, 0, 0, 0]]
    ]


def test_generate_all_board_quarters():
    binboards = generate_all_board_quarters(new=True)

    assert len(binboards) == 4 * 3 ** 9

    assert bin_to_array(binboards[-1]) == [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, 0, 0, 0],
        [None, None, None, 0, 0, 0],
        [None, None, None, 0, 0, 0]
    ]

    assert bin_to_array(binboards[0]) == [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
    ]

    assert bin_to_array(binboards[5]) == [
        [None, None, None, 1, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
    ]

    assert bin_to_array(binboards[6]) == [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [1, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
    ]

    assert bin_to_array(binboards[7]) == [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, 1, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
    ]


def test_generate_rotation_map():
    import random
    rotation_map = generate_rotation_map(new=True)

    for t in range(1000):
        array = [[random.choice((None, 0, 1)) for _ in range(6)]
                 for _ in range(6)]

        # array = [
        #     [   0,    1, None, None, None, None],
        #     [None, None, None, None, None, None],
        #     [None, None, None, None, None, None],
        #     [None, None, None, None, None, None],
        #     [None, None, None, None, None, None],
        #     [None, None, None, None, None, None],
        # ]

        array_copy = [row[:] for row in array]
        clockwise = random.randint(0, 1)
        # clockwise = 1

        centers = ((1, 1), (1, 4), (4, 1), (4, 4))
        center = random.choice(centers)
        # center = (1, 1)

        rotate_array(array_copy, center, clockwise)

        binboard = array_to_bin(array)
        q = centers.index(center)  # quarter
        quarter_mask = generate_quarter_masks()[q]
        quarter_binboard = binboard & quarter_mask

        hash_ = quarter_binboard | (clockwise << 72)
        rotated_quarter_binboard = rotation_map[hash_]
        rotated_binboard = binboard & (
            ~ quarter_mask) | rotated_quarter_binboard
        try:
            assert bin_to_array(rotated_binboard) == array_copy
        except AssertionError:
            print("array = ")
            pprint(array)
            print("array_copy = ")
            pprint(array_copy)
            print("binboard = ")
            pprint(bin(binboard))
            print("rotated_binboard = ")
            pprint(bin(rotated_binboard))
            print("rotated_binboard = ")
            pprint(bin_to_array(rotated_binboard))
            print("rotated_quarter_binboard = ")
            pprint(bin(rotated_quarter_binboard))
            print("hash_ = ")
            print(bin(hash_))
            print("q = %s" % q)
            print('quarter_mask = ')
            print(bin(quarter_mask))
            print('quarter_binboard = ')
            print(bin(quarter_binboard))


def test_generate_all_diagonals():
    diags = generate_all_diagonals(5)
    assert len(diags) == 32


def test_generate_all_diagonal_masks():
    generate_all_diagonal_masks(size=2, new=True)


def time_moves():
    array = [[random.choice((None, 0, 1)) for _ in range(6)]
             for _ in range(6)]

    quarter_masks = generate_quarter_masks()
    b = array_to_bin(array)
    rotation_map = generate_rotation_map()

    def rotate_binboard(b, q, clockwise):
        quarter_mask = quarter_masks[q]
        quarter_binboard = b & quarter_mask
        hash_ = quarter_binboard | (clockwise << 72)
        rotated_quarter_binboard = rotation_map[hash_]
        rotated_binboard = b & (~ quarter_mask) | rotated_quarter_binboard
        return rotated_binboard

    t0 = time.clock()
    number = 10000
    for i in range(number):
        rotate_binboard(b, 1, 1)
        b1 = b | (1 << (10))

        rotate_binboard(b, 1, 0)
        b1 = b | (1 << (22 + 36))

        rotate_binboard(b, 2, 1)
        b1 = b | (1 << (22 + 36))

        rotate_binboard(b, 2, 0)
        b1 = b | (1 << (22))

        rotate_binboard(b, 3, 0)
        b1 = b | (1 << (11))

        rotate_binboard(b, 3, 1)
        b1 = b | (1 << (11 + 36))

        rotate_binboard(b, 0, 0)
        b1 = b | (1 << (1))

        rotate_binboard(b, 0, 1)
        b1 = b | (1 << (1 + 36))

    t1 = time.clock()
    dt = t1 - t0
    print("%i board operations in %.3fs." % (number * 8, dt))


def test_utility():
    array = [
        [1, 1, 1, 1, 1, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]
    b = array_to_bin(array)
    utility(b)


def time_utility():
    t0 = time.clock()
    b = 0b100101000000100001000100010001010100100101000000100001000100010001010100
    number = 100000
    for i in range(number):
        utility(b)
    t1 = time.clock()
    d = t1 - t0
    print("%s iterations in %.3fs." % (number, d))




if __name__ == '__main__':
    test_array_bin_array()
    test_generate_all_diagonals()
    test_generate_quarter_masks()
    test_generate_all_board_quarters()
    test_generate_rotation_map()
    time_moves()
    test_utility()
    time_utility()
    test_generate_all_diagonal_masks()