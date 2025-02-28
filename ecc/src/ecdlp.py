from utils import isInvertable, np, invert, randint
from WeierstrassECC import ECC, Point


class EC_Key:
    """
    Elliptic Curve Cryptography Key.\n
    @param ecc: Elliptic curve.
    @param P: Elliptic curve point public parameter.
    @param l: Integer private parameter.
    """

    def __init__(self, ecc: ECC, P: Point, l: int):
        self.ecc = ecc
        self.P = P
        self.Q = l * P
        self.l = l

    def pubKey(self):
        """
        Elliptic Curve Cryptography public key parameters.\n
        @return :
        - p: Prime number defining the group Z/pZ.\n
        - ecc: Elliptic curve.\n
        - cardinality: Elliptic curve cardinality.\n
        - P: Elliptic curve point public parameter.\n
        - Q: Elliptic curve point public parameter
        """
        return [
            self.ecc.p,
            self.ecc.cardinality(),
            self.ecc,
            self.P,
            self.Q,
        ]

    def privKey(self):
        return self.l

    def __str__(self):
        pubkey = [str(i) for i in self.pubKey()]
        privkey = self.privKey()
        return f"Key(pubkey = {pubkey}, privkey = {privkey})"


class Elgamal:
    """
    Elgamal encryption scheme.\n
    @param key: Elliptic Curve Cryptography Key.
    """

    def __init__(self, key: EC_Key):
        self.key = key

    def encrypt(self, M: Point):
        """
        Encrypt a message.\n
        @param M: Message to encrypt.
        @return: Encrypted Points.
        """
        p, P, Q = self.key.ecc.p, self.key.P, self.key.Q
        k = np.random.randint(1, p - 2)  # Inialization vector
        C1 = k * P
        C2 = M + k * Q
        return [C1, C2]

    def decrypt(self, C1: Point, C2: Point):
        """
        Decrypt a message.\n
        @param C1: Point.
        @param C2: Point.
        @return: Point.
        """
        l = self.key.l
        return C2 - l * C1


class DSA:
    """
    Elliptic Curve Digital Signature Algorithm.\n
    @param key: Elliptic Curve Cryptography Key.
    """

    def __init__(self, key: EC_Key):
        self.key = key

    def sign(self, h_M: int):
        r = np.random.randint(1, self.key.ecc.cardinality() - 2)
        n = self.key.ecc.cardinality()
        s1 = pow(r * self.key.P.x, 1, n)

        if s1 == 0:
            return self.sign(h_M)

        try:
            if isInvertable(r, n):
                r_inv = pow(r, -1, n)
                s2 = pow((h_M + self.key.l * s1) * r_inv, 1, n)
                if s2 == 0:
                    return self.sign(h_M)
                return r, s1, s2
            else:
                return self.sign(h_M)
        except ValueError:
            return self.sign(h_M)

    def verify(self, h_M: int, s1: int, s2: int) -> bool:
        n = self.key.ecc.cardinality()

        if not (1 <= s1 and s1 <= n - 1):
            return False
        if not (1 <= s2 and s2 <= n - 1):
            return False

        v = h_M * invert(s2, n)
        u = s1 * invert(s2, n)
        R = u * self.key.P + v * self.key.Q

        if R == Point(np.inf, np.inf, self.key.ecc.a, self.key.ecc.b, self.key.ecc.p):
            return False

        return R.x == s1


if __name__ == "__main__":
    a, b, p = -3, 1, 1217
    print(f"Initializing elliptic curve with parameters: a = {a}, b = {b}, p = {p}")
    ec = ECC(a, b, p)

    ################################################################ Elgamal ################################################################
    l = 83
    keys = EC_Key(ec, Point(743, 473, a, b, p), l)
    print(f"Generating EC key pair with private key length: {l}\n{keys}")

    M = Point(1130, 1138, a, b, p)
    print(f"Message to encrypt (as a point on the curve): M = {M}")

    elgamal = Elgamal(keys)
    C1, C2 = elgamal.encrypt(M)
    print(f"Encrypted message: C1 = {C1}, C2 = {C2}")

    decM = elgamal.decrypt(C1, C2)
    print(f"Decrypted message: {decM}")

    # Verify if decryption was successful
    print(f"Decryption successful: {M == decM}")

    ################################################################# DSA #################################################################
    n, G = ec.get_prime_order()
    print(f"Base point {G} of order {n}.")

    s = randint(0, n-1)
    Q = s*G
    keys = EC_Key(ec, Q, s)

    dsa = DSA(keys)
    h_M = 20
    sig = dsa.sign(h_M)
    print(sig)

    checkSig = dsa.verify(h_M, sig[0], sig[1])
    print(checkSig)
