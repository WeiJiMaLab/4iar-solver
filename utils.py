import numpy as np


def is_legal(c):
    if isinstance(c, int) or isinstance(c, float):
        return 0 <= c <= 35
    elif isinstance(c, list) or isinstance(c, tuple):
        return 0 <= c[0] <= 3 and 0 <= c[1] <= 8
    else:
        return False


def coordinate_to_index(x, y):
    if is_legal((x, y)):
        return x * 9 + y
    else:
        return -1


def batch_index_to_coordinate(idx_vec):
    if isinstance(idx_vec, list):
        vec = np.array(idx_vec)
    else:
        vec = idx_vec
    x = vec // 9
    y = vec % 9
    return x, y
