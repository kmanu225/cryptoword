"""
Réalise l'attaque pas de bébé pas de géant pour résoudre
le logarithme discret sur les entiers
# On cherche l tel que y = g^l[p]
"""

from math import sqrt, ceil


def pasBebePasGeant(y, g, p):
    # Dictionnaire des puissance modulaire jusqu'à sqrt(p):  Cela correspond aux pas de bébé jusqu'à sqrt(p)
    m = ceil(sqrt(p))
    bebe = {pow(g, k, p): k for k in range(m)}
    print("Pas de bébé : ", bebe)

    x = y
    j = 0
    inv_g_pow_m = pow(g, -m, p)
    print(f"Inverse modulo n de g^m : {inv_g_pow_m}")

    all_x = [x]
    while x not in bebe.keys():
        x = pow(x * inv_g_pow_m, 1, p)
        all_x.append(x)
        j += 1

    print("Pas de géant : ", all_x)

    l = j * m + bebe[x]
    print(f"{g}^{l} = {pow(g, l, p)}[{p}]\n")
    return l


if __name__ == "__main__":
    ## Exemple de l'attaque du DL par la méthode "pas de bébé pas de géant"
    p = 101
    m = ceil(sqrt(p))
    g = 2
    y = 48
    l = pasBebePasGeant(y, g, p)
