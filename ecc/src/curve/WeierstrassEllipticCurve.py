from matplotlib import pyplot as plt
import numpy as np


def weierstrass(x, y, a, b):
    return pow(y, 2) - pow(x, 3) - a * x - b


class Point:
    """
    Point on an elliptic curve
    x : Abscisse
    y : Ordinate
    a, b, p : coefficients of the elliptic curve y^2 = x^3 + a*x + b mod[p] (Weierstrass form)
    """

    def __init__(self, x, y, a, b, p):
        # Check if the point is on the specified curve
        if x == np.inf and y == np.inf:
            self.x = x
            self.y = y

        elif pow(weierstrass(x, y, a, b), 1, p) == 0:
            self.x = x
            self.y = y

        else:
            raise ValueError("Point is not on the curve")

        # Set parameters of the curve
        self.a = a
        self.b = b
        self.p = p

    # Double the point
    def __mul2__(self):
        # Add a point to itself
        if self.y == 0:
            return Point(np.inf, np.inf, self.a, self.b, self.p)  # Infinity point

        m = (3 * self.x**2 + self.a) * pow(2 * self.y, -1, self.p)
        t = self.y - m * self.x
        x = pow(m**2 - 2 * self.x, 1, self.p)
        y = pow(-m * x - t, 1, self.p)

        return Point(x, y, self.a, self.b, self.p)

    # Addition of two points
    def __add__(self, Q):

        # Check if the points are on the same curve
        if self.p != Q.p or self.a != Q.a or self.b != Q.b:
            raise ValueError("Points are not on the same curve")

        elif self.x == Q.x:

            # Point is added to itself
            if self.y == Q.y:
                return self.__mul2__()

            elif self.y == -Q.y:
                return Point(np.inf, np.inf, self.a, self.b, self.p)  # Infinity point
        else:
            # Adding two purely distint points
            m = (Q.y - self.y) * pow(Q.x - self.x, -1, self.p)
            t = self.y - m * self.x
            x = pow(m**2 - self.x - Q.x, 1, self.p)
            y = pow(-m * x - t, 1, self.p)

            return Point(x, y, self.a, self.b, self.p)

    def __radd__(self, Q):
        return self.__add__(Q)

    # Multiplication of a point by a scalar
    def __mul__(self, n):
        if n == 0:
            return self.O
        if n == 1:
            return self
        if n % 2 == 0:
            return (n // 2) * self.__mul2__()
        return ((n // 2) * self.__mul2__()) + self

    def __rmul__(self, n):
        return self.__mul__(n)

    # Compare two points
    def __eq__(self, Q):
        return self.x == Q.x and self.y == Q.y and self.p == Q.p and self.a == Q.a

    # Print the point
    def __str__(self):
        return f"({self.x}, {self.y})"


class EllipticCurve:
    """
    This curve is defined by the equation: y^2 = x^3 + a*x + b mod[p] which corresponds to the Weierstrass form.
    a and b are natural numbers.
    p is the prime number different from 2 and 3.
    """

    def __init__(self, a, b, p=5):
        self.a = a
        self.b = b
        self.p = p

    def onCuve(self, x, y):
        return pow(weierstrass(x, y, self.a, self.b), 1, p) == 0

    def get_points(self):
        """Get points on the curve."""
        points = [Point(np.inf, np.inf, self.a, self.b, self.p)]
        space = [i for i in range(self.p)]

        for x in space:
            for y in space:
                if self.onCuve(x, y):
                    points.append(Point(x, y, self.a, self.b, self.p))
        return points

    def cardinality(self):
        """Get the number of points on the curve. The infinity point is also counted."""
        return len(self.get_points())

    # Show the curve both over real numbers and natural numbers
    def plotCurve(self, a, b, p):
        """Plot the elliptic curve."""
        points = self.get_points()
        n = self.cardinality()

        x_points = []
        y_points = []
        for i in range(n):
            x_points.append(points[i].x)
            y_points.append(points[i].y)

        # Real numbers
        window = 5
        y, x = np.ogrid[-window:window:100j, -window:window:100j]
        plt.contour(x.ravel(), y.ravel(), weierstrass(x, y, self.a, self.b), [0])

        # Natural numbers
        plt.scatter(x_points, y_points, color="blue")

        plt.title(f"y^2 = x^3 + {self.a}x + {self.b} mod[{self.p}]\nCardinality : {n}")
        plt.grid()
        plt.show()

    # Print points on the curve
    def __str__(self):
        points = self.get_points()
        list_points = [str(i) for i in points]
        return f"Curve: y^2 = x^3 + {self.a}x + {self.b} mod[{self.p}]\n\n#E(Fp) : {self.cardinality()}\nPoints :\n{list_points}"


if __name__ == "__main__":
    a, b, p = -3, 0, 191
    ec = EllipticCurve(a, b, p)

    print(ec)
    ec.plotCurve(a, b, p)
