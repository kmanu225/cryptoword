from math import sqrt, floor
from matplotlib import pyplot as plt
import numpy as np
from gmpy2 import powmod


### Elliptic curve.###
class Point:
    """
    Point on an elliptic curve
    x : Abscisse
    y : Ordinate
    a, b, p : coefficients of the elliptic curve y^2 = x^3 + a*x + b mod[p]
    """

    def __init__(self, x, y, a, b, p):
        if (
            powmod(x**3 + a * x + b - y**2, 1, p) == 0
        ):  # Check if the point is on the specified curve
            self.x = x
            self.y = y

            self.a = a
            self.b = b
            self.p = p

        else:
            raise ValueError("Point is not on the curve")

    def __mul2__(self):
        # Add a point to itself
        if self.y == 0:
            raise ValueError("Infinite point")
        m = (3 * self.x**2 + self.a) * pow(2 * self.y, -1, self.p)
        t = self.y - m * self.x
        x = pow(m**2 - 2 * self.x, 1, self.p)
        y = pow(-m * x - t, 1, self.p)
        return Point(x, y, self.a, self.b, self.p)

    def __add__(self, Q):
        # Add two points
        if (
            self.p != Q.p or self.a != Q.a or self.b != Q.b
        ):  # Check if the points are on the same curve
            raise ValueError("Points are not on the same curve")

        if self.x == Q.x:
            if self.y == Q.y:  # Point is added to itself
                return self.__mul2__()
            else:
                raise ValueError("Infinite point")

        m = (Q.y - self.y) * pow(Q.x - self.x, -1, self.p)
        t = self.y - m * self.x
        x = pow(m**2 - self.x - Q.x, 1, self.p)
        y = pow(-m * x - t, 1, self.p)

        return Point(x, y, self.a, self.b, self.p)

    def __mul__(self, n):
        if n == 0:
            return Point(0, 0, self.a, self.b, self.p)
        if n == 1:
            return self
        if n % 2 == 0:
            return self.__mul2__() * (n // 2)
        return (self.__mul2__() * (n // 2)) + self

    def __rmul__(self, n):
        return self.__mul__(n)

    def __eq__(self, Q):
        return self.x == Q.x and self.y == Q.y and self.p == Q.p and self.a == Q.a

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class EllipticCurve:
    """
    This curve is defined by the equation: y^2 = x^3 + a*x + b mod[p] (Weirstrass form)
    a and b are the curve parameters.
    p is the prime number.
    """

    def __init__(self, a, b, p=2):
        self.a = a
        self.b = b
        self.p = p

    def weirstrass(self, x, y):
        return pow(y, 2) - pow(x, 3) - self.a * x - self.b

    def onCuve(self, x, y):
        return pow(self.weirstrass(x, y), 1, p) == 0

    def get_points(self):
        """Get the curve."""
        points = []
        space = [i for i in range(self.p)]
        for i in space:
            for j in space:
                if self.onCuve(i, j):
                    points.append(Point(i, j, self.a, self.b, self.p))
        return [i for i in points]

    def plotCurve(self, a, b, p):
        """Plot the elliptic curve."""
        points = self.get_points()
        n = len(points)

        x_points = []
        y_points = []
        for i in range(n):
            x_points.append(points[i].x)
            y_points.append(points[i].y)

        window = 5
        y, x = np.ogrid[-window:window:100j, -window:window:100j]
        plt.contour(x.ravel(), y.ravel(), self.weirstrass(x, y), [0])
        plt.scatter(x_points, y_points, color="red")
        plt.grid()
        plt.show()

    def __str__(self):
        Points = self.get_points()
        list_points = [str(i) for i in Points]
        return f"Curve(a={self.a}, b={self.b}, p={self.p}\n Points={list_points})"


if __name__ == "__main__":
    """Real case of Diffie-Hellman key exchange."""
    # Base
    a = -1
    b = 1
    p = 47
    ec = EllipticCurve(a, b, p)

    ec.plotCurve(a, b, p)
