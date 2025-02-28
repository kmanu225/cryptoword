from utils import randint, np
from WeierstrassECC import Point, ECC


def dh(nA: int, nB: int, P: Point) -> str:
    """
    Diffie-Hellman key exchange with elliptic curve.
    @param nA: Secret key of A.
    @param nB: Secret key of B.
    @param P: Base point.
    @return: Shared key for Alice and Bob.
    """

    # Computation realized by participant A
    print(f"\nSecret key of A: {nA}")
    print(f"Received value from B: {nB}")
    rcv_A = nB*P
    kA = nA*rcv_A
    print(f"Computed shared key by A: {kA}")

    # Computation realized by participant B
    print(f"\nSecret key of B: {nB}")
    print(f"Received value from A: {nA}")
    rcv_B = nA*P
    kB = nB*rcv_B
    print(f"Computed shared key by B: {kB}\n")

    if kA == kB:
        print(f"Shared key by participants: {kA}\n")
    else:
        print("Key agreement failed.\n")


if __name__ == "__main__":
    """Diffie-Hellman key exchange with elliptic curve."""
    # Base
    a, b, p = -3, 1, 197
    P = Point(195, 183, a, b, p)

    ecc = ECC(a, b, p)
    print(ecc)

    for i in range(10):
        nA, nB = randint(1, 10), randint(1, 10)
        dh(nA, nB, P)
        print("--------------------------------------------------")
