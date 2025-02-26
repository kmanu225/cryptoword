from utils import np, plt, invert, weierstrass

INF = np.inf  # Represents the point at infinity


class Point:
    """
    Point on an elliptic curve in Weierstrass form: y² = x³ + ax + b mod p
    """

    def __init__(self, x, y, a, b, p):

        if x == np.inf and y == np.inf:
            self.x = x
            self.y = y

        elif pow(weierstrass(x, y, a, b), 1, p) == 0:
            self.x = x
            self.y = y

        else:
            raise ValueError("Point is not on the curve")

        self.a, self.b, self.p = a, b, p

    def __str__(self):
        return "∞" if self.x == INF else f"({self.x}, {self.y})"

    def __eq__(self, Q):
        return self.x == Q.x and self.y == Q.y and self.p == Q.p and self.a == Q.a

    def __neg__(self):
        if self.x == INF:
            return self
        return Point(self.x, (-self.y) % self.p, self.a, self.b, self.p)

    def square(self):
        """
        Add a point to itself, the number is squared.
        @return: Point
        """
        if self == Point(INF, INF, self.a, self.b, self.p):
            return Point(INF, INF, self.a, self.b, self.p)

        elif self.y == 0:
            return Point(INF, INF, self.a, self.b, self.p)

        else:
            m = (3 * self.x**2 + self.a) * invert(2 * self.y, self.p)
            t = self.y - m * self.x
            x = pow(m**2 - 2 * self.x, 1, self.p)
            y = pow(-m * x - t, 1, self.p)
            return Point(x, y, self.a, self.b, self.p)

    def __add__(self, Q):
        """
        Add two points of the same curve.
        @param Q: Point
        @return: Point
        """

        if self.p != Q.p or self.a != Q.a or self.b != Q.b:
            raise ValueError("Points are not on the same curve")

        elif self.x == Q.x and self.y == Q.y:
            return self.square()
        
        elif self.x == Q.x and self.y == -Q.y:
            return Point(INF, INF, self.a, self.b, self.p)
        
        else:
            if self == Point(INF, INF, self.a, self.b, self.p):
                return Q

            elif Q == Point(INF, INF, self.a, self.b, self.p):
                return self

            else:
                # Adding two purely distint points
                delta_x = pow(Q.x - self.x, 1, self.p)
                delta_y = pow(Q.y - self.y, 1, self.p)

                if delta_x == 0:    # Points are inverses
                    return Point(INF, INF, self.a, self.b, self.p)
                
                else:
                    m = delta_y * invert(delta_x, self.p)
                    t = self.y - m * self.x
                    x = pow(m**2 - self.x - Q.x, 1, self.p)
                    y = pow(-m * x - t, 1, self.p)

                return Point(x, y, self.a, self.b, self.p)

    def __radd__(self, Q):
        return self.__add__(Q)

    # Exponentiation of a point
    def __pow__(self, n: int):
        if self == Point(INF, INF, self.a, self.b, self.p):
            return self

        elif self.x == INF or self.y == INF:
            return Point(INF, INF, self.a, self.b, self.p)

        elif n == 0:
            return Point(INF, INF, self.a, self.b, self.p)

        elif n == 1:
            return self

        power, base = Point(INF, INF, self.a, self.b, self.p), self
        # i = 0
        while n:
            # print(f"n: {n}, base: {base}, Point^{i}: {power}")
            if n & 1:
                power += base

            base += base
            if base == Point(INF, INF, self.a, self.b, self.p):
                # print(f"n: {n}, base: {base}, Point^{i}: {power}")
                return power

            n >>= 1
            # i += 1
        # print(f"n: {n}, base: {base}, Point^{i}: {power}")
        return power


class ECC:
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
        return pow(weierstrass(x, y, self.a, self.b), 1, self.p) == 0

    def get_points(self):
        """Get points on the curve."""
        points = [Point(INF, INF, self.a, self.b, self.p)]
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
        return f"Curve: y^2 = x^3 + {self.a}x + {self.b} mod[{self.p}]\n\n#E(Fp) : {self.cardinality()}\nPoints : {list_points}"


if __name__ == "__main__":
    a, b, p = 0, 1, 5
    ec = ECC(a, b, p)

    print(ec)
    ec.plotCurve(a, b, p)
