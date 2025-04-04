from sympy import isprime
import numpy as np


def get_primes_factors(n):
    if isprime(n):
        return [n]

    factors = []
    for i in range(2, n + 1):
        if isprime(i):
            while n % i == 0:
                factors.append(i)
                n = n // i
    factors.sort()
    return factors


if __name__ == "__main__":
    p = 229
    base = 6

    a = 77  # Permet de décompooser 13*6^77 dans B
    b = 13
    B = [2, 3, 5, 7, 11]
    power_set = [
        12,
        18,
        62,
        100,
        143,
        206,
    ]  # Tous les éléments de B^6 se décomposent dans B

    base_pow = [get_primes_factors(pow(base, i, p)) for i in power_set]
    print(base_pow)

    # A * X = Y
    A = np.array(
        [
            # [0, 1, 1, 0, 1],
            [4, 0, 0, 0, 1],
            [1, 0, 0, 1, 1],
            [2, 2, 1, 0, 0],
            [1, 2, 0, 0, 1],
            [1, 1, 1, 1, 0],
        ]
    )

    Y = np.array(power_set[1:])
    X = np.linalg.solve(A, Y)

    log_B = {B[i]: int(X[i]) for i in range(len(B))}
    print(log_B)

    print(get_primes_factors(pow(b * pow(base, a, p), 1, p)))
    log_13 = 2 * log_B[7] + log_B[3] - 77
    print(log_13)
    print(pow(13, 1, p) == pow(6, log_13, p))
