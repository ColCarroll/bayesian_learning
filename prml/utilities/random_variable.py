__author__ = 'colinc'


class Point:
    def __init__(self, point, is_open=True):
        self.value = point
        self.is_open = is_open

    @property
    def is_closed(self):
        return not self.is_open

    def __eq__(self, other):
        if isinstance(other, Point):
            return (other.value == self.value) and (other.is_open == self.is_open)
        raise NotImplementedError("Only compare Point to Point")

    def __gt__(self, other):
        if isinstance(other, Point):
            if other.value == self.value:
                return self.is_closed
            return self.value > other.value
        raise NotImplementedError("Only compare Point to Point")

    def __ge__(self, other):
        if isinstance(other, Point):
            return self > other or self == other

    def __lt__(self, other):
        if isinstance(other, Point):
            if other.value == self.value:
                return self.is_open
            return self.value < other.value
        raise NotImplementedError("Only compare Point to Point")

    def __le__(self, other):
        if isinstance(other, Point):
            return self < other or self == other

    @property
    def status(self):
        if self.is_open:
            return "open"
        return "closed"

    def __repr__(self):
        return "{:s} endpoint at {:.1f}".format(self.status, self.value)

    def __str__(self):
        return self.__repr__()


class Interval:
    def __init__(self, lower_point=Point(float("-inf")), upper_point=Point(float("inf"))):
        self.lower = lower_point
        self.upper = upper_point
        self.empty = (self.lower >= self.upper) or (self.lower.value == self.upper.value)

    def __eq__(self, other):
        if isinstance(other, Interval):
            return ((self.lower == other.lower and self.upper == other.upper) or
                    self.empty and other.empty)
        raise NotImplementedError

    def __repr__(self):
        if not self.empty:
            return "{:s} interval with {:s} and {:s}".format(self.state, str(self.lower), str(self.upper))
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

    @property
    def state(self):
        if self.empty:
            return "true and false"
        elif self.is_open:
            return "open"
        elif self.is_closed:
            return "closed"
        else:
            return "half open"

    def contains(self, x):
        if self.lower.is_open:
            low_cmp = lambda j: self.lower.__lt__(j)
        else:
            low_cmp = lambda j: self.lower.__le__(j)
        return self.lower <= x <= self.upper

    def _intersects(self, other):
        """ Tests whether two intervals intersect
        """
        if isinstance(other, Interval):
            return ((self.lower <= other.upper) and (other.lower <= self.upper)
                    or (other.contains(self.lower.value))
                    or (other.contains(self.upper.value))
                    or (self.contains(other.lower.value))
                    or (self.contains(other.upper.value)))
        raise NotImplementedError("Must intersect Interval with Interval")

    def split(self, *others):
        """ Splits a list of intervals into a list that is disjoint with self, and a list of intervals
         that intersect with self
        """
        disjoint, non_disjoint = [], []
        for interval in others:  # Clever way to split lists: http://stackoverflow.com/a/12135169/2620170
            (disjoint, non_disjoint)[self._intersects(interval)].append(interval)
        return disjoint, non_disjoint

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

