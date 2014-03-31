from unittest import TestCase
from prml.utilities.random_variable import Interval, Point

__author__ = 'colinc'


class TestInterval(TestCase):
    def setUp(self):
        self.lower = 0
        self.upper = 2
        self.open_interval = Interval(
            Point(self.lower, True),
            Point(self.upper, True))
        self.closed_interval = Interval(
            Point(self.lower, False),
            Point(self.upper, False))
        self.half_open_interval = Interval(
            Point(self.lower, True),
            Point(self.upper, False))
        self.disjoint_with_open = Interval(
            Point(self.lower - 1, True),
            Point(self.lower, True)
        )
        self.sort_of_intersects_with_open = Interval(
            Point(self.lower - 1, True),
            Point(self.lower, False)
        )
        self.merged = Interval(
            Point(self.lower - 1, True),
            Point(self.upper, True)
        )
        self.empty_interval = Interval(
            Point(self.upper),
            Point(self.lower)
        )

        interval_range = self.upper - self.lower
        self.subset_of_open = Interval(
            Point(self.lower + 0.25 * interval_range),
            Point(self.lower + 0.75 * interval_range)
        )

    def test_knows_status(self):
        self.assertTrue(self.open_interval.is_open)
        self.assertTrue(self.closed_interval.is_closed)
        self.assertFalse(self.half_open_interval.is_closed)
        self.assertFalse(self.half_open_interval.is_closed)

    def test_endpoint_containment(self):
        # open interval contains neither endpoint
        self.assertFalse(self.open_interval.contains(self.lower))
        self.assertFalse(self.open_interval.contains(self.upper))

        # closed interval contains both endpoints
        self.assertTrue(self.closed_interval.contains(self.lower))
        self.assertTrue(self.closed_interval.contains(self.upper))

        # half open interval contains one endpoint
        self.assertFalse(self.half_open_interval.contains(self.lower))
        self.assertTrue(self.half_open_interval.contains(self.upper))

    def test_string(self):
        self.assertEqual(
            str(self.open_interval),
            "open interval with open endpoint at 0.0 and open endpoint at 2.0")
        self.assertEqual(
            str(self.closed_interval),
            "closed interval with closed endpoint at 0.0 and closed endpoint at 2.0")
        self.assertEqual(
            str(self.half_open_interval),
            "half open interval with open endpoint at 0.0 and closed endpoint at 2.0")

    def test_equality(self):
        self.assertTrue(self.open_interval == self.open_interval)
        self.assertFalse(self.open_interval == self.half_open_interval)
        self.assertRaises(NotImplementedError, lambda: self.open_interval == 2)

    def test_union(self):
        self.assertEqual(self.open_interval.union(self.sort_of_intersects_with_open), [self.merged])
        self.assertListEqual(
            self.open_interval.union(self.disjoint_with_open),
            [self.disjoint_with_open, self.open_interval])
        self.assertListEqual(
            self.open_interval.union(*[]),
            [self.open_interval]
        )
        self.assertListEqual(
            self.open_interval.union(self.closed_interval),
            [self.closed_interval]
        )
        self.assertRaises(NotImplementedError, self.open_interval.union, 3)

    def test_intersection(self):
        self.assertEqual(self.open_interval.intersect(self.sort_of_intersects_with_open), self.empty_interval)
        self.assertEqual(
            self.open_interval.intersect(self.disjoint_with_open),
            self.empty_interval)
        self.assertEqual(
            self.open_interval.intersect(self.subset_of_open),
            self.subset_of_open
        )
        self.assertEqual(
            self.open_interval.intersect(self.closed_interval),
            self.open_interval
        )
        self.assertRaises(NotImplementedError, self.open_interval.intersect, 3)
