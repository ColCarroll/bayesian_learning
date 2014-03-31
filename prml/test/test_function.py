from unittest import TestCase
import math
from prml.linear_regression.basis_functions import Function

__author__ = 'colinc'


class TestFunction(TestCase):
    def setUp(self):
        self.bias = Function('bias')
        self.identity = Function('identity')

        self.degree = 2  # polynomial degree
        self.poly = Function('polynomial', degree=self.degree)
        self.poly_derivative = self.poly.derivative()

        self.mu = 3
        self.std_dev = 4

        self.standard_gaussian = Function('gaussian')
        self.gaussian = Function('gaussian', mu=self.mu,
                                 sigma=self.std_dev)
        self.gaussian_derivative = self.gaussian.derivative()

        self.logistic_sigmoid = Function('sigmoid', mu=self.mu,
                                         sigma=self.std_dev,
                                         sig_func='logistic')
        self.logistic_sigmoid_derivative = self.logistic_sigmoid.derivative()

        self.tanh_sigmoid = Function('sigmoid', mu=self.mu,
                                     sigma=self.std_dev,
                                     sig_func='tanh')
        self.tanh_sigmoid_derivative = self.tanh_sigmoid.derivative()

        self.test_points = range(10)

    def test_bias(self):
        for x in self.test_points:
            self.assertEqual(1, self.bias(x), "Bias function should always equal 1")

    def test_identity(self):
        for x in self.test_points:
            self.assertEqual(x, self.identity(x), "Identity function returns argument")

    def test_poly(self):
        for x in self.test_points:
            self.assertEqual(x ** self.degree, self.poly(x),
                             "Polynomial function should raise number to {:d} degree".format(self.degree))

    def test_poly_derivative(self):
        """ For any polynomial, (x^n)' = n x^(n - 1), so x (x^n)' = n (x^n)
        """
        for x in self.test_points:
            self.assertAlmostEqual(x * self.poly_derivative(x), self.degree * self.poly(x), places=4,
                                   msg="{0:d} * x^{0:d} = x * (x^{0:d})'".format(self.degree))

    def test_gaussian(self):
        """ Gaussians are symmetric about their mean, and can be transformed to a standard
        gaussian by multiplying by the std deviation and adding mu
        """
        for x in self.test_points:
            self.assertAlmostEqual(self.gaussian(self.mu + x), self.gaussian(self.mu - x), places=4,
                                   msg="The gaussian is symmetric")
        for x in self.test_points:
            self.assertAlmostEqual(self.gaussian(self.mu + x * self.std_dev), self.standard_gaussian(x), places=4,
                                   msg="The gaussian is symmetric")

    def test_gaussian_derivative(self):
        """ f' = ((mu - x) / sigma^2) * f
        """
        for x in self.test_points:
            self.assertAlmostEqual(self.gaussian_derivative(x),
                                   float(self.mu - x) / float(self.std_dev ** 2) * self.gaussian(x),
                                   msg="""Gaussian derivative must satisfy
                                   f'({0:.0f})=((mu - {0:.0f})/sigma^2) f({0:.0f})""".format(x))

    def test_logistic_sigmoid_derivative(self):
        """ f' = f (1 - f)/sigma
        """
        f = self.logistic_sigmoid
        f_prime = self.logistic_sigmoid_derivative
        for x in self.test_points:
            self.assertAlmostEqual(f_prime(x),
                                   (f(x) * (1 - f(x))) / self.std_dev,
                                   msg="Logistic sigmoid satisfies f' = f(1-f)/sigma")

    def test_tanh_sigmoid_derivative(self):
        """ f' = (1 - f^2)/sigma and f(mu) = 0.5 defines the tanh sigmoid
        """
        f = self.tanh_sigmoid

        self.assertEqual(f(self.mu), 0., msg="Initial condition for tanh sigmoid is f(mu) = 0")

        f_prime = self.tanh_sigmoid_derivative

        for x in self.test_points:
            self.assertAlmostEqual(f_prime(x),
                                   (1 - f(x) * f(x)) / (2 * self.std_dev),
                                   msg="Tanh sigmoid must satisfy f'({0:.0f}) = (1-f({0:.0f})^2)/(2 * sigma)".format(x))

    def test_undefined_function(self):
        self.assertRaises(NotImplementedError, Function, "foo")

    def test_undefined_sigmoid(self):
        self.assertRaises(NotImplementedError,
                          lambda x: Function("sigmoid", sig_func=x),
                          "foo")

    def test_prints(self):
        """ Tests the __repr__ functions
        """
        self.assertEqual(str(self.logistic_sigmoid), "Sigmoid function")
        self.assertEqual(str(Function(func=lambda j: j)), "Custom function")

    def test_custom_function(self):
        """ Define a custom sin function, which is the unique solution to
        f'' = -f, f(0) = 0, f'(0) = 1
        """
        f = Function(func_type="sin", func=lambda j: math.sin(j))
        f_prime = f.derivative()
        f_prime_prime = f.derivative().derivative()

        self.assertEqual(str(f), "Sin function")
        self.assertEqual(f(0), 0)
        self.assertAlmostEqual(f_prime(0), 1, places=4)

        for x in self.test_points:
            self.assertAlmostEqual(f(x), -f_prime_prime(x), places=4)
