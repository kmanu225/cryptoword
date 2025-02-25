from math import gcd, sqrt, floor
from matplotlib import pyplot as plt
import numpy as np
from gmpy2 import powmod, invert


### El Gamal cryptosystem.
def isInvertable(g, p):
    """Check if g is invertable in Z/pZ."""
    try:
        invert(g, p)
        return True
    except ZeroDivisionError:
        return False


def isGenerator(g, p):
    """Check if g is a generator of Z/pZ."""
    if gcd(g, p) != 1:
        return False

    for i in range(1, p - 2):
        if pow(g, i, p) == 1:
            return False
    return True


class KeyIntegers:
    def __init__(self, p, g, l):
        if not isGenerator(g, p):
            raise ValueError("g is not a generator of Z/pZ")

        if 1 < l and l > p - 2:
            raise ValueError("l is not in [1, p-2]")

        if not isInvertable(g, p):
            raise ValueError("g is not invertable in Z/pZ")

        # public: p, g, h | private: l
        self.p = p
        self.g = g
        self.l = l
        self.h = powmod(g, l, p)

    def __str__(self):
        return f"Key(p={self.p}, g={self.g}, l={self.l}, h={self.h})"


def encrypt_integers(key, m):
    """Encrypt a message."""
    p, g, h = key.p, key.g, key.h
    k = np.random.randint(1, p - 2)
    c1 = powmod(g, k, p)
    c2 = m * powmod(h, k, p)
    return c1, c2


def decrypt_integers(key, c1, c2):
    """Decrypt a message."""
    p, l = key.p, key.l
    return powmod(c2 * powmod(c1, -l, p), 1, p)


def base_signature(inf_prime):
    q = inf_prime
    while not np.isPrime(q):
        q += 1

    p = 2 * q + 1
    while not np.isprime(p):
        p += q

    return q, p


def dsa(key: KeyIntegers, m, r=None):
    if r is None:
        find_r = False
        while not find_r:
            r = np.random.randint(1, key.p - 2)
            if isInvertable(r, key.p - 1):
                find_r = True
    inverse = invert(r, key.p - 1)
    s1 = powmod(key.g, r, key.p)
    return s1, powmod((m - key.l * s1) * inverse, 1, key.p - 1)


def check_dsa(p, g, h, m, s1, s2):
    if not (0 <= s1 and s1 <= p - 1):
        return False
    if not (1 <= s2 and s2 <= p - 2):
        return False
    if powmod(g, m, p) != powmod(powmod(h, s1, p) * powmod(s1, s2, p), 1, p):
        return False
    return True


### Elliptic curve.###
class Point:
    def __init__(self, x, y, a, p):
        self.x = x
        self.y = y
        self.p = p
        self.a = a

    def __add__(self, Q):
        if self.p != Q.p or self.a != Q.a:
            raise ValueError("Points are not on the same curve")
        if self.x == Q.x and self.y == Q.y:
            return self.double()
        m = (Q.y - self.y) * pow(Q.x - self.x, -1, self.p)
        t = self.y - m * self.x
        x = pow(m**2 - self.x - Q.x, 1, self.p)
        y = pow(-m * x - t, 1, self.p)
        return Point(x, y, self.a, self.p)

    def double(self):
        m = (3 * self.x**2 + self.a) * pow(2 * self.y, -1, self.p)
        t = self.y - m * self.x
        x = pow(m**2 - 2 * self.x, 1, self.p)
        y = pow(-m * x - t, 1, self.p)
        return Point(x, y, self.a, self.p)

    def __mul__(self, n):
        if n == 0:
            return Point(0, 0, self.a, self.p)
        if n == 1:
            return self
        if n % 2 == 0:
            return self.double() * (n // 2)
        return (self.double() * (n // 2)) + self

    def __rmul__(self, n):
        return self.__mul__(n)

    def __eq__(self, Q):
        return self.x == Q.x and self.y == Q.y and self.p == Q.p and self.a == Q.a

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Curve:
    def __init__(self, a, b, p=1):
        self.a = a
        self.b = b
        self.p = p

    def curve(self, X, a, b, p=1):
        """Elliptic curve."""
        return powmod(pow(X, 3) + a * X + b, 1, p)

    def max_borne_veil(self, p):
        """Borne de Veil: [p+1-2*sqrt(p), p+1+2*sqrt(p)]"""
        return floor(p + 1 + 2 * sqrt(p))

    def onCuve(self, X, Y, a, b, p):
        """Elliptic curve."""
        if pow(pow(Y, 2), 1, p) == self.curve(X, a, b, p):
            return True
        return False

    def get_points(self, a, b, p):
        """Get the curve."""
        Points = []
        F = [i for i in range(p)]
        for i in F:
            for j in F:
                if self.onCuve(i, j, a, b, p):
                    Points.append(Point(i, j, a, p))
        return [i for i in Points]

    def set_E_F(self, a, b, p):
        """Plot the elliptic curve."""
        points = self.get_points(a, b, p)
        n = len(points)

        x_points = []
        y_points = []
        for i in range(n):
            x_points.append(points[i].x)
            y_points.append(points[i].y)

        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
        plt.scatter(x_points, y_points, color="red")
        plt.grid()
        plt.show()

    def __str__(self):
        Points = self.get_points(self.a, self.b, self.p)
        list_points = [str(i) for i in Points]
        return f"Curve(a={self.a}, b={self.b}, p={self.p}\n Points={list_points})"


class KeysElliptic:
    def __init__(self, elliptic_curve: Curve, P: Point, l: int):
        self.curve = elliptic_curve
        self.P = P
        self.Q = l * P
        self.l = l

    def pubKey(self):
        points = self.curve.get_points(self.curve.a, self.curve.b, self.curve.p)
        return [
            self.curve.p,
            str(self.curve),
            len(points),
            self.P,
            self.Q,
        ]

    def privKey(self):
        return self.l

    def __str__(self):
        pubkey = [str(i) for i in self.pubKey()]
        privkey = self.privKey()
        return f"Key(pubkey={pubkey}, privkey={privkey})"


def encrypt_elliptic_curve(key, M):
    """Encrypt a message."""
    p, P, Q = key.curve.p, key.P, key.Q
    k = np.random.randint(1, p - 2)
    C1 = k * P
    C2 = M + k * Q
    return [C1, C2]


def decrypt_elliptic_curve(key, C1, C2):
    """Decrypt a message."""
    l = key.l
    return C2 - l * C1


def ecdsa(key: KeysElliptic, M, r):
    n = key.pubKey()[2]
    s1 = powmod(r * key.P.x, 1, n)
    if s1 == 0:
        return None, None

    try:
        r_inv = powmod(r, -1, n)
        s2 = powmod((M + key.l * s1) * r_inv, 1, n)
        if s2 == 0:
            return None, None

    except ZeroDivisionError:
        return None, None

    return s1, s2


def check_ecdsa(pubkey: list, M, s1, s2):
    if not (1 <= s1 and s1 <= pubkey[2] - 1):
        return False
    if not (1 <= s2 and s2 <= pubkey[2] - 1):
        return False

    n = pubkey[2]
    P = pubkey[3]
    qP = M * powmod(s2, -1, n)
    Q = pubkey[4]
    qQ = s1 * powmod(s2, -1, n)

    R = qP * P + qQ * Q

    return R.x == s1 and R != Point(0, 0, P.a, P.p)


if __name__ == "__main__":
    # Base for elgamal encryption on natural numbers.
    key = KeyIntegers(101, 2, 37)
    m = 18
    (c1, c2) = encrypt_integers(key, m)
    m_ = decrypt_integers(key, c1, c2)

    print(f"Key: {key}")
    print(f"Message: {m}")
    print(f"Encrypted: ({c1}, {c2})")
    print(f"Decrypted: {m_}")

    # Base for elgamal signature on natural numbers.
    p = 17
    g = 5
    l = 2
    r = 3
    key = KeyIntegers(p, g, l)
    p, g, h = key.p, key.g, key.h  # public key
    h_m = 15
    s1, s2 = dsa(key, h_m, r)
    print(f"Signature: ({s1}, {s2})")
    print(check_dsa(p, g, h, h_m, s1, s2))

    # Base elgamal encryption on elliptic curve.
    a = 2
    b = 1
    p = 5
    l = 2
    r = 3  # random number dans [1, n-1]
    h_m = 4
    P = Point(
        0, 1, a, p
    )  # Si P est un point de la courbe elliptique c'est un générateur de E(Fp)
    ec = Curve(a, b, p)
    print(ec)
    keys = KeysElliptic(ec, P, l)
    pubkey = keys.pubKey()
    s1, s2 = ecdsa(keys, 15, r)

    print(f"Signature: ({s1}, {s2})")

    ec.set_E_F(a, b, p)
