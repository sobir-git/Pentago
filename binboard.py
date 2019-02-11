from board import Board
from functools import lru_cache
import pickle

def walk_array(array):
    for i, row in enumerate(array):
        for j, v in enumerate(row):
            yield (i, j, v)


def array_to_bin(array, empty=None):
    b = 0
    for i, j, v in walk_array(array):
        idx = i * 6 + j
        if v is empty:
            continue
        b |= 1 << (idx + v * 36)
    return b


def bin_to_array(b, empty=None):
    array = [ [empty]*6 for _ in range(6) ]
    for i, j, v in walk_array(array):
        idx = 6 * i + j
        if b & (1 << idx):
            array[i][j] = 0
        elif b & (1 << (idx + 36)):
            array[i][j] = 1
    return array


def generate_all_diagonals(size):
    diagonals = []
    directions = ( (0, 1), (1, 0), (1, -1), (1, 1) )
    for di, dj in directions:
        for si in range(6):
            for sj in range(6):
                i, j = si, sj
                length = 0
                diagonal = []
                while 0 <= i < 6 and 0 <= j < 6:
                    diagonal.append((i, j))
                    i += di
                    j += dj
                    length += 1
                    if length == size:
                        break
                if length == size:
                    diagonals.append(diagonal)
    return diagonals


@lru_cache()
def generate_all_diagonal_masks(size, new=False):
    if not new:
        try:
            with open('diagonal_masks.pickle', 'rb') as f:
                return pickle.load(f)[size]
        except Exception as e:
            print("failed to load cached diagonal_masks from file: %s" % e)
            new = True

    masks_by_size = [None] * 6
    for size in range(3, 6):
        masks = []
        for diagonal in generate_all_diagonals(size):
            b = 0
            d = [0, 0]
            for i, j in diagonal:
                idx = i * 6 + j
                d[0] |= 1 << idx
                d[1] |= 1 << ( idx + 36 )
            masks.append(d)
        masks_by_size[size] = masks

    if new:
        with open('diagonal_masks.pickle', 'wb') as f:
            pickle.dump(masks_by_size, f)
    return masks_by_size[size]


def generate_rotation_map(new=False):
    if not new:
        try:
            with open('rotation_map.pickle', 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print("failed to load cached rotation_map file: %s." % e)
            new = True

    rotation_map = {}
    for i, binboard in enumerate(generate_all_board_quarters()):
        q = i % 4  # this is the quarter, thats how quarter boards are arranged
        if q == 0: center = (1, 1)
        if q == 1: center = (1, 4)
        if q == 2: center = (4, 1)
        if q == 3: center = (4, 4)

        for clockwise in (0, 1):
            array = bin_to_array(binboard)
            rotate_array(array, center, clockwise)
            rotated_binboard = array_to_bin(array)
            hash_ = binboard | (clockwise << 72)
            rotation_map[hash_] = rotated_binboard

    if new:
        with open('rotation_map.pickle', 'wb') as f:
            pickle.dump(rotation_map, f)

    return rotation_map


def generate_quarter_masks():
    masks = []
    for i in range(4):
        mask = 0
        start_idx = (i // 2) * 3 * 6 + (i % 2) * 3
        for idx in range(start_idx, start_idx + 13, 6):
            mask |= 0b111 << (idx)
            mask |= 0b111 << (idx + 36)
        masks.append(mask)

    return masks


def utility(b):
    ch0, ch1 = 0, 0
    for size in range(3, 6):
        for mask0, mask1 in generate_all_diagonal_masks(size):
            if mask0 & b == mask0:
                ch0 += 10 ** size
            if mask1 & b == mask1:
                ch1 += 10 ** size
    return ch0, ch1


def generate_all_board_quarters(new=False):
    # Warning: don't change the line "for q in range(4)"
    # it changes the ordering of the quarter boards, make a problem
    # in different function (generate_rotation_map())
    if not new:
        try:
            with open('board_quarters.pickle', 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print("failed to load cached board_quarters from file %s" % e)
            new = True
    binboards = []
    for qb0 in range(1<<9):  # all kinds of 0 placement in board
        for qb1 in range(1<<9): # all kinds of 1 placement in board
            # they can't make a suitable pair if they over lap
            if qb0 & qb1 != 0:
                continue

            # lets put it on a quarter of an empty board
            for q in range(4):
                # put it in quarter q
                start_idx = (q // 2) * 3 * 6 + (q % 2) * 3
                row_masks = ( 0b111 << shift for shift in (0, 3, 6) )
                rows = [ (qb0 & row_mask, qb1 & row_mask) for row_mask in row_masks ]
                idx = start_idx
                b = 0
                for row in rows:
                    b |= row[0] << idx
                    b |= row[1] << (idx + 36)
                    idx += 3
                binboards.append(b)
    if new:
        try:
            with open('board_quarters.pickle', 'wb') as f:
                pickle.dump(binboards, f)
        except Exception as e:
            print("failed to write to file: %s" % e)
    return binboards


def rotate_array(a,  center, clockwise):
    ind = {}
    for i, j in ((1, 1), (1, 4), (4, 1), (4, 4)):
        normal1 = ((i-1, j), (i, j+1), (i+1, j), (i, j-1))
        normal2 = ((i-1, j+1), (i+1, j+1), (i+1, j-1), (i-1,j-1))
        rev1 = tuple(reversed(normal1)) 
        rev2 = tuple(reversed(normal2)) 
        ind[(i, j)] = ((rev1, rev2), (normal1, normal2))


    for ind in ind[center][clockwise]:
        xor, yor = ind[0]
        prev = a[xor][yor]
        for x, y in ind:
            now = a[x][y]
            a[x][y] = prev
            prev = now
        a[xor][yor] = prev


