from time import time as t
import matplotlib.pyplot as plt

# Iterative Function to calculate
# (x^y)%p in O(log y)


def fast_exponentiation_1(x, s, p):
    if s == 0:
        return 1

    if s == 1:
        return x % p

    s = bin(s)[2:][::-1]
    exp = 1
    for s_i in s:
        if s_i == "1":  # take more time than branch else
            exp = (exp * x) % p  # multiply by x
            x = (x**2) % p  # square x

        else:
            x = (x**2) % p  # square x
        # print((x, exp))

    return exp


def fast_exponentiation_2(x, s, p):
    if s == 0:
        return 1

    if s == 1:
        return x%p

    s = bin(s)[2:][::-1]
    exp = 1
    for s_i in s:
        exp = (exp * (1 + (x - 1) * int(s_i)))%p  # multiply by x
        x = (x**2)%p  # square x
    return exp


def fast_exponentiation_3(x, s, p):
    res = 1  # Initialize result

    if x == 0:
        return 0

    while s > 0:
        # If y is odd, multiply
        # x with result
        if (s & 1) == 1:
            res = (res * x)%p

        # y must be even now
        s = s >> 1  # y = y/2
        x = (x**2)%p
    return res


if __name__ == "__main__":
    x = 2
    p = 57
    print(fast_exponentiation_1(x, 123456789, p))
    print(fast_exponentiation_2(x, 123456789, p))
    print(fast_exponentiation_3(x, 123456789, p))
    print(pow(x, 123456789, p))

    time_fast_exponentiation_1 = []
    time_fast_exponentiation_2 = []
    time_fast_exponentiation_3 = []
    time_fast_exponentiation_4 = []

    s_vals = [i for i in range(0, 10000)]
    for s_val in s_vals:
        t1 = t()
        y = fast_exponentiation_1(x, s_val, p)
        time_fast_exponentiation_1.append(t() - t1)

        t2 = t()
        y = fast_exponentiation_2(x, s_val, p)
        time_fast_exponentiation_2.append(t() - t2)

        t3 = t()
        y = fast_exponentiation_2(x, s_val, p)
        time_fast_exponentiation_3.append(t() - t3)

        t4 = t()
        y =  pow(x, s_val, p)
        time_fast_exponentiation_4.append(t() - t4)

    plt.plot(s_vals, time_fast_exponentiation_1, "r.", label="Fast Exponentiation 1")
    plt.plot(s_vals, time_fast_exponentiation_2, "b.", label="Fast Exponentiation 2")
    plt.plot(s_vals, time_fast_exponentiation_3, "g.", label="Fast Exponentiation 3")
    plt.plot(s_vals, time_fast_exponentiation_4, "y.", label="Fast Exponentiation 4")
    plt.title("Comparison of Fast Exponentiations ")
    plt.xlabel("Value of s")
    plt.ylabel("Execution Time")
    plt.legend()
    plt.grid()
    plt.show()
