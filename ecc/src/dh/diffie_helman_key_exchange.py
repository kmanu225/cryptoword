
"""Diffie-Hellman key exchange."""

from ecc.src.dlp.elgamal_discret_logarithm import *


def diffie_helman_key_real(xA, xB, g, p):
    """Cas réele de l'échange de clé de Diffie-Hellman."""
    yA = pow(g, xA, p)
    yB = pow(g, xB, p)
    kA = pow(yB, xA, p)
    kB = pow(yA, xB, p)
    return kA, kB


def diffie_helman_key_curve(nA, nB, P):
    """Diffie-Hellman key exchange with elliptic curve."""
    Q = P * nA
    R = nB * P
    kA = nA * R
    kB = nB * Q
    return str(kA), str(kB)


if __name__ == "__main__":
    """Real case of Diffie-Hellman key exchange."""
    # Base
    g = 5
    p = 23

    # Secret keys
    xA = 7
    xB = 8
    print([i for i in range(p)])
    print(diffie_helman_key_real(xA, xB, g, p))

    """Diffie-Hellman key exchange with elliptic curve."""
    # Base
    a = 0
    b = 1
    p = 5
    P = Point(2, 3, a, p)

    # Secret keys
    nA = 2
    nB = 4
    elliptic_curve = Curve(a, b, p)
    points = elliptic_curve.get_points(a, b, p)
    print([str(i) for i in points])
    print(diffie_helman_key_curve(nA, nB, P))
    elliptic_curve.set_E_F(a, b, p)
