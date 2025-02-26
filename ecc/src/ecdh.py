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
    rcv_A = P**nB 
    kA = rcv_A**nA
    print(f"Computed shared key by A: {kA}")

    # Computation realized by participant B
    print(f"\nSecret key of B: {nB}")
    print(f"Received value from A: {nA}")
    rcv_B = P**nA 
    kB = rcv_B**nB
    print(f"Computed shared key by B: {kB}\n")

 
    if kA == kB:
        print(f"Shared key by participants: {kA}\n")
    else:
        print("Key agreement failed.\n")


if __name__ == "__main__":
    """Diffie-Hellman key exchange with elliptic curve."""
    # Base
    a, b, p = 0, 1, 5
    P = Point(2, 2, a, b, p)

    ecc = ECC(a, b, p)
    print(ecc)

    for i in range(10):
        nA, nB = randint(1, 10), randint(1, 10)
        dh(nA, nB, P)
        print("--------------------------------------------------")
