import random
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


def carmichael(n):
    primes = get_primes_factors(n)
    print(f"Primes factors of {n}: {primes}")
    for prime in primes:
        if (n - 1) % (prime - 1) != 0:
            print(f"{n} is not a Carmichael number.")
            return False
    print(f"{n} is a Carmichael number.")
    return True


def pocklington(n, a=2):
    q_ = int(n**0.5)
    while (n - 1) % q_ != 0:
        q_ += 1
        if q_ > n:
            return False

    if pow(a, n - 1, n) != 1:
        return False

    p_ = (n - 1) // q_

    if gcd(pow(a, p_, n), n) != 1:
        return False

    return True

## Test de Fermat: Presque sûr pour tous les nombres sauf les nombres de Carmichael
def fermat(n, k=20):
    if n < 4:
        return n == 2 or n == 3
    for _ in range(k):
        a = random.randint(2, n - 2)
        if gcd(a, n) == 1:
            if pow(a, n - 1, n) != 1:
                print(f"{n} is not prime:", end=" ")
                print(f"{a}^{n-1}[{n}] = {pow(a, n - 1, n)}")

                return False
    print(f"{n} is probably prime.")
    return True


# Test de Miller-Rabin: Presque sûr pour tous les nombres
def miller_rabin(n, k=20):
    if n < 4:
        return n == 2 or n == 3

    if n % 2 == 0:
        return False

    s = get_primes_factors(n - 1).count(2)
    r = (n - 1) // (2**s)
    # print(f"n - 1 = 2^{s} * {r}")

    for _ in range(k):
        a = random.randint(2, n - 2)
        if gcd(a, n) == 1:
            if pow(a, r, n) != 1:
                j = 0
                while j < s and pow(a, 2**j * r, n) != n - 1:
                    # print(f"{a}^{2**j * r}[{n}] = {pow(a, 2**j * r, n)}")
                    j += 1

                    if j == s:
                        # print(f"{n} is not prime:", end=" ")
                        # print(f"{a}^{r}[{n}] = {pow(a, r, n)}")
                        return False
                if j < s:
                    print(f"{n} is probably prime.")
                    return True
            else:
                print(f"{n} is probably prime.")
                return True
    return True





def gen_prime(n):
    while True:
        p = random.randint(2 ** (n - 1), 2**n)
        if miller_rabin(p):
            return p


if __name__ == "__main__":
    p1 = gen_prime(16)
    p2 = gen_prime(16)
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    
    print(pocklington(59629))
