import numpy as np


def discretize(array, space, quanta):
    low = space.low
    high = space.high

    def check_inf(val, replace):
        if val == np.inf:
            return replace
        return val

    low = np.array([check_inf(val, 0) for val in low])
    high = np.array([check_inf(val, 10) for val in high])

    ranges = high - low

    return (((array - low) / ranges) * quanta).astype(int)
