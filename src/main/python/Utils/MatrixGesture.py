import numpy as np


def fill(m, n, c):
    return np.full((m, n), c)


def times(v1, v2):
    m = len(v1)  # row dimension
    n = len(v2[0])  # column dimension
    array = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            tmp = 0
            for k in range(len(v1[0])):
                tmp += v1[i][k] * v2[k][j]
            array[i][j] = tmp
    return array


def transpose(m):
    return np.transpose(m)


def plus(v1, v2):
    return np.add(v1, v2)


def divide(v1, v):
    return np.divide(v1, v)
