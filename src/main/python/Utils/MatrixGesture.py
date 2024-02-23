import numpy as np
import pandas as pd


def fill(m, n, c, index):
    return pd.DataFrame(np.full((m, n), c), index=index, columns=index)


def times(v1, v2):
    return v1.dot(v2)


def transpose(m):
    return np.transpose(m)


def plus(v1, v2):
    return np.add(v1, v2)


def divide(v1, v):
    return np.divide(v1, v)
