import numpy as np


def knapsack(n, W, w, v):
    m = np.zeros((n + 1, W + 1), dtype=np.int32)
    used = np.zeros((n + 1, W + 1, len(w)), dtype=np.int32)

    for i in range(1, n + 1):
        for j in range(0, W + 1):
            if w[i] > j:
                m[i, j] = m[i - 1, j]
                used[i, j] = used[i - 1, j]
            else:
                prev = m[i - 1, j]
                new = m[i - 1, j - w[i]] + v[i]
                if prev > new:
                    m[i, j] = prev
                    used[i, j] = used[i - 1, j]
                else:
                    m[i, j] = new
                    used[i, j] = used[i - 1, j - w[i]]
                    used[i, j, i] = 1

    return m, used
