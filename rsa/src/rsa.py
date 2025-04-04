### Indicatrice d'Euler ou de Carmichael dans ce cas
phi = lambda p, q: (p - 1) * (q - 1)
inverse_modulo = lambda e, phi_n: pow(e, -1, phi_n)

### c = m^e mod n et m = c^d mod n
encrypt = lambda m, e, n: pow(m, e, n)
decrypt = lambda c, d, n: pow(c, d, n)
