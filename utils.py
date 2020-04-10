import numpy as np


def compute_error(x, y, m):
    x = np.array(x)
    y = np.array(y)
    m = np.float64(m)

    assert len(x) == len(y)
    assert len(x) != 0

    return (np.linalg.norm(y - m * x) ** 2) / (2 * len(x))


def compute_error_gradient(x, y, m):
    x = np.array(x)
    y = np.array(y)
    m = np.float64(m)

    assert len(x) == len(y)
    assert len(x) != 0

    return ((m * (x @ x)) - (x @ y)) / len(x)


if __name__ == "__main__":
    data = np.genfromtxt('data.txt')
    x = data[:, 0].copy()
    y = data[:, 1].copy()

    ms = np.arange(0, 6, 0.1)
    errors = []
    grads = []

    for m in ms:
        errors.append(compute_error(x, y, m))
        grads.append(compute_error_gradient(x, y, m))

    errors = np.array(errors)
    grads = np.array(grads)

    np.savetxt('errors.txt', np.column_stack([ms, errors, grads]))
