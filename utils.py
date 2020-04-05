import numpy as np


def compute_error(x, y, m):
    x = np.array(x)
    y = np.array(y)
    m = np.float64(m)

    assert len(x) == len(y)
    assert len(x) != 0

    return np.mean(np.linalg.norm(y - m * x)**2) / 2
