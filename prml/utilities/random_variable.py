__author__ = 'colinc'


class Point:
    def __init__(self, point, is_open=True, endpoint="left"):
        self.value = point
        self.is_open = is_open
        self.endpoint = endpoint

    @property
    def test_val(self):
        if self.endpoint == "left":
            return self.value + int(self.is_open)
        return self.value - int(self.is_open)

    @property
    def is_closed(self):
        return not self.is_open  # I understand closed is not "not open"...

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.endpoint == other.endpoint) and (other.value == self.value) and (other.is_open == self.is_open)
        raise NotImplementedError("Only compare Point to Point")

    def __gt__(self, other):
        if isinstance(other, Point):
            if other.value == self.value:
                return self.test_val > other.test_val
            return self.value > other.value
        raise NotImplementedError("Only compare Point to Point")

    def __lt__(self, other):
        if isinstance(other, Point):
            if other.value == self.value:
                return self.test_val < other.test_val
            return self.value < other.value
        raise NotImplementedError("Only compare Point to Point")

    def __ge__(self, other):
        if isinstance(other, Point):
            return self > other or self == other
        if other == self.value:
            if self.endpoint == "left":
                return self.is_open
            return self.is_closed
        return self.value > other

    def __le__(self, other):
        if isinstance(other, Point):
            return self < other or self == other
        if other == self.value:
            if self.endpoint == "left":
                return self.is_closed
            return self.is_open
        return self.value < other

    def __repr__(self):
        if self.is_open:
            if self.endpoint == "left":
                sym = "("
            else:
                sym = ")"
        else:
            if self.endpoint == "left":
                sym = "["
            else:
                sym = "]"
        if self.endpoint == "left":
            return "{:s}{:s}".format(sym, str(self.value))
        else:
            return "{:s}{:s}".format(str(self.value), sym)


class Interval:
    def __init__(self, lower_point=Point(float("-inf")), upper_point=Point(float("inf"))):
        self.lower = Point(lower_point.value, lower_point.is_open, endpoint="left")
        self.upper = Point(upper_point.value, upper_point.is_open, endpoint="right")
        self.empty = (self.lower.value >= self.upper.value)

    def __eq__(self, other):
        if isinstance(other, Interval):
            return ((self.lower == other.lower and self.upper == other.upper) or
                    self.empty and other.empty)
        raise NotImplementedError

    def __repr__(self):
        if not self.empty:
            return "{:s}, {:s}".format(str(self.lower), str(self.upper))
        return "empty interval"

    @property
    def is_closed(self):
        if self.empty:
            return True
        return self.lower.is_closed and self.upper.is_closed

    @property
    def is_open(self):
        if self.empty:
            return True
        return self.lower.is_open and self.upper.is_open

    def contains(self, x):
        return self.lower <= x <= self.upper

    def _intersects(self, other):
        """ Tests whether two intervals intersect
        """
        if isinstance(other, Interval):
            return ((self.lower <= other.upper and other.lower <= self.upper) or
                    self.contains(other.upper.value) or
                    self.contains(other.lower.value) or
                    other.contains(self.upper.value) or
                    other.contains(self.lower.value))
        raise NotImplementedError("Must intersect Interval with Interval")

    def split(self, *others):
        """ Splits a list of intervals into a list that is disjoint with self, and a list of intervals
         that intersect with self
        """
        non_intersections, intersections = [], []
        for interval in others:  # Clever way to split lists: http://stackoverflow.com/a/12135169/2620170
            (non_intersections, intersections)[self._intersects(interval)].append(interval)
        return non_intersections, intersections

    def union(self, *others):
        """ Takes the union of a collection of intervals.  If the starting list was disjoint,
         the return list will be disjoint
        """
        non_intersections, intersections = self.split(*others)
        if intersections:
            intersections.append(self)
            non_intersections.append(Interval(
                min([j.lower for j in intersections]),
                max([j.upper for j in intersections])))
        else:
            non_intersections.append(self)
        return non_intersections

    def intersect(self, *others):
        """ Intersects an interval with a list of other intervals. If there is no intersection,
        returns None
        """
        others = list(others) + [self]
        return Interval(
            max([j.lower for j in others]),
            min([j.upper for j in others]))


class Set:
    def __init__(self, *args, **kwargs):
        self.intervals = []
        if args:
            self.singletons = set(args)
        else:
            self.singletons = set()
        if "intervals" in kwargs:
            for interval in kwargs["intervals"]:
                self.intervals = interval.union(self.intervals)


class Algebra:
    def __init__(self, prob_set):
        self.set = prob_set


class RandomVariable:
    def __init__(self, func):
        self.__func = func

    def __call__(self, x):
        return self.__func(x)
