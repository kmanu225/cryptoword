import numpy as np
import olll


def update_schmidt(B, B_star, k):
    for j in range(k + 1):
        B_star[j] = B[j]
        for i in range(j):
            B_star[j] -= (B[j] @ B_star[i]) / (B_star[i] @ B_star[i]) * B_star[i]
        B_star[j] = B_star[j]
    return B_star


def lovasz_condition(B, B_star, k, delta=3 / 4):
    mu = B[k] @ B_star[k - 1] / (B_star[k - 1] @ B_star[k - 1])
    return (
        np.linalg.norm(B_star[k]) ** 2
        >= (delta - mu**2) * np.linalg.norm(B_star[k - 1]) ** 2
    )


def swap(B, k):
    B_k = list(B[k][:])
    B[k] = B[k - 1][:]
    B[k - 1] = B_k
    return B


def lll_alg(B):
    n = B.shape[0]
    B_star = np.zeros(B.shape, dtype=float)
    B_star = update_schmidt(B, B_star, 0)

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            mu = abs(B[k] @ B_star[j] / (B_star[j] @ B_star[j]))
            if mu > 1 / 2:
                B[k] -= round(mu) * B[j]
                B_star = update_schmidt(B, B_star, k)

        if lovasz_condition(B, B_star, k):
            k += 1
        else:
            B = swap(B, k)
            B_star = update_schmidt(B, B_star, k)
            k = max(k - 1, 1)
    return B


if __name__ == "__main__":
    B = np.array(
        [
            [1, 1, 1],
            [-1, 0, 2],
            [3, 5, 6],
        ]
    )

    print(lll_alg(B).T)
    print(np.array(olll.reduction(B, 0.75)).T)
