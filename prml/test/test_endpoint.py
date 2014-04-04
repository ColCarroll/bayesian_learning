from unittest import TestCase
from prml.utilities.random_variable import Point

__author__ = 'colinc'


class TestPoint(TestCase):
    def setUp(self):
        self.low_open_point = Point(0, True, "left")
        self.high_open_point = Point(1, True, "right")
        self.low_closed_point = Point(0, False, "left")
        self.high_closed_point = Point(1, False, "right")
        self.high_open_left_point = Point(1, True, "left")

    def test_equals(self):
        self.assertEqual(self.low_open_point, self.low_open_point)
        self.assertEqual(self.high_closed_point, self.high_closed_point)

    def test_less_than(self):
        self.assertLess(self.low_open_point, self.high_closed_point)
        self.assertLess(self.low_open_point, self.high_open_point)
        self.assertLess(self.low_closed_point, self.low_open_point)

    def test_greater_than(self):
        self.assertGreater(self.high_closed_point, self.low_open_point)
        self.assertGreater(self.high_open_point, self.low_open_point)
        self.assertGreater(self.high_closed_point, self.high_open_point)
        self.assertGreater(self.high_open_left_point, self.high_open_point)

    def test_greater_or_equal(self):
        self.assertTrue(self.low_open_point >= self.low_closed_point)
        self.assertTrue(self.high_open_point <= self.high_closed_point)
        self.assertFalse(self.high_open_left_point == self.high_open_point)

    def test_status(self):
        self.assertTrue(self.low_open_point.is_open)
        self.assertFalse(self.low_open_point.is_closed)

    def test_compare_two_points(self):
        self.assertLess(self.low_open_point, self.high_closed_point)
        self.assertFalse(self.low_open_point == self.high_closed_point)
        self.assertTrue(self.low_open_point == self.low_open_point)

    def test_string(self):
        self.assertEqual(str(self.low_open_point), "(0")
        self.assertEqual(str(self.high_closed_point), "1]")

    def test_min(self):
        self.assertEqual(min(self.low_open_point, self.high_closed_point), self.low_open_point)
