""" Polard's p-1 algorithm to find a non-trivial factor of n."""

from sympy import isprime, gcd


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


# Get prime numbers lower than B.
def get_primes(B):
    primes = []
    for i in range(2, B + 1):
        if isprime(i):
            primes.append(i)
    return primes


# ppcm the prime less than B  powers of the primes which are lower than n.
def get_Q(B, n):
    primes = get_primes(B)
    high_power_lower_n = []
    for prime in primes:
        power = 1
        while prime**power <= n:
            power += 1
        high_power_lower_n.append(prime ** (power - 1))

    Q = 1
    for prime_power in high_power_lower_n:
        Q *= prime_power
    return Q


if __name__ == "__main__":
    a = 3
    B = 19
    n = 19048567
    Q = get_Q(B, n)
    aq_min_one_mod_n = pow(a, Q, n) - 1

    GCD = gcd(aq_min_one_mod_n, n)
    print(f"Factors found of {n} are: {GCD} {n / GCD}")
