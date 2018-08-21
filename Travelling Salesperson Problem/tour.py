import stdio
from point import Point


class Tour:
    """
    Represents a tour in the traveling salesperson problem.
    """

    def __init__(self):
        """
        Creates an empty tour.
        """

        self._tour = []

    def show(self):
        """
        Prints the tour to standard output.
        """

        for i in self._tour:
            stdio.writeln(str(i))

    def draw(self):
        """
        Draws the tour to standard draw.
        """

        for i in range(len(self._tour) - 1):
            self._tour[i].drawTo(self._tour[i + 1])

    def size(self):
        """
        Returns the number of points on the tour.
        """

        return len(self._tour)

    def distance(self):
        """
        Returns the total distance of the tour.
        """

        dis = 0
        for i in range(len(self._tour)):
            dis += self._tour[i].distanceTo(self._tour[i - 1])
        return dis

    def insertNearest(self, p):
        """
        Inserts the point p using the nearest neighbor heuristic.
        """

        I = 0
        d = float('inf')
        for i in range(len(self._tour)):
            a = self._tour[i].distanceTo(p)
            if a < d:
                d = a
                I = i
        self._tour.insert(I + 1, p)

    def insertSmallest(self, p):
        """
        Inserts the point p using the smallest increment heuristic.
        """

        I = 1
        l = float('inf')
        for i in range(1, len(self._tour) + 1):
            x = self._tour[i - 1]
            y = self._tour[i % len(self._tour)]
            a = x.distanceTo(p) + y.distanceTo(p) - x.distanceTo(y)
            if a < l:
                l = a
                I = i
        self._tour.insert(I, p)
