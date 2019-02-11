from functools import reduce
from timeit import timeit
import string

l = [97, 98, 110, 120] * 4

import array


def f1(list):
    string = ""
    for item in list:
        string = string + chr(item)
    return string


def f2(l):
    return reduce(lambda string, item: string + chr(item), l, "")


def f3(l):
    string = ""
    for character in map(chr, l):
        string = string + character
    return string


def f4(list):
    string = ""
    lchr = chr
    for item in list:
        string = string + lchr(item)
    return string


def f6(list):
    return ''.join(map(chr, list))


def f7(list):
    return array.array('B', list).tostring()


import time

# f = f6
# number = 200000
# t0 = time.time()
# for i in range(number):
#   f(l)
# t1 = time.time()

# dt = t1 - t0
# print("%.3f" % (dt))


def test_powers_by_dict():
    d = {i: 1 << i for i in range(72)}

    t0 = time.clock()
    number = 1000000
    for i in range(number):
        d[0]
        d[10]
        d[20]
        d[30]
        d[40]
        d[50]
        d[60]
        d[70]

    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))


def test_powers_by_shift():
    t0 = time.clock()
    number = 1000000
    for i in range(number):
        1 << 0
        1 << 10
        1 << 20
        1 << 30
        1 << 40
        1 << 50
        1 << 60
        1 << 70

    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))


def test_bit_length_shift():
    t0 = time.clock()
    number = 1000000
    x = 10
    for i in range(number):
        1 << 100
    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))


def test_bit_count():
    n = 0b100101000000100001000100010001010100100101000000100001000100010001010100
    number = 1000000
    t0 = time.clock()
    c = str.count
    for i in range(number):
        l = 0
        c = 0
        while i:
            c += i & 1
            l += 1
            i >>= 1
        c
    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))


def time_tuple_vs_bits():
    t0 = time.clock()
    number = 1000000
    # for i in range(number):
    #     move = (22, 3, 1)
    #     x = move[0]
    #     y = move[1]
    #     z = move[2]
    a = 0b111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000
    b = 0b000000000000000000000000000000001111111111111111111111111111111100000000000000000000000000000000
    c = 0b000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111
    for i in range(number):
        move = (22 << 64) & (3 << 32) & 1
        x = move & a
        y = move & b
        z = move & c
    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))

    '''
    Conclusion: use tuples instead of packing numbers into bits,
    '''



def test_move_bits_vs_tuple():
    number = 1000000
    # b = 0b100101000000100001000100010001010100100101000000100001000100010001010100
    b = [0b100101000000100001000100010001010100, 0b100101000000100001000100010001010100]
    t0 = time.clock()
    for i in range(number):
        # b |= 1 << (10 + 36)
        b[0] |= 1 << 10
    t1 = time.clock()
    d = t1 - t0
    print("%s iterations took %.3fs." % (number, d))


if __name__ == '__main__':
    # test_powers_by_dict()
    # test_powers_by_shift()
    # test_bit_length_shift()
    # test_bit_count()
    # time_tuple_vs_bits()
    test_move_bits_vs_tuple()