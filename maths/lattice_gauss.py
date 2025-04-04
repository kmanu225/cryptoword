"""Gauss Lattice base reduction algorithm."""
import numpy as np

def gauss_reduction(v1, v2):
    while True:
        # (a) If ||v2|| < ||v1||, swap v1, v2
        if np.linalg.norm(v2) < np.linalg.norm(v1):
            v1, v2 = v2, v1

        # (b) Compute m = ⌊ v1∙v2 / v1∙v1 ⌉
        dot_product = np.dot(v1, v2)
        norm_sq = np.dot(v1, v1)
        m = int(dot_product / norm_sq)
        print(f"m: {m}")

        # (c) If m = 0, return v1, v2
        if m == 0:
            return v1, v2

        # (d) v2 = v2 - m*v1
        v2 = v2 - m * v1

if __name__=="__main__":
    v = (846835985, 9834798552)
    u = (87502093, 123094980)
    v1 = np.array(v)
    v2 = np.array(u)
    print(f"v1: {v1}, v2: {v2}")
    v1, v2 = gauss_reduction(v1, v2)
    print(f"v1: {v1}, v2: {v2}")
    # inner product of v1 and v2
    print(f"inner product of v1 and v2: {np.dot(v1, v2)}")