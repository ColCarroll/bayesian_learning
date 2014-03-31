import math

__author__ = 'colinc'


class Function:
    def __init__(self, func_type=None, **kwargs):
        self.func_type = func_type
        if self.func_type == 'bias':
            self.func = bias()
        elif self.func_type == 'identity':
            self.func = identity()
        elif self.func_type == 'polynomial':
            self.func = polynomial(**kwargs)
        elif self.func_type == 'gaussian':
            self.func = gaussian(**kwargs)
        elif self.func_type == 'sigmoid':
            self.func = sigmoid(**kwargs)
        elif "func" in kwargs:
            if not self.func_type:
                self.func_type = "Custom"
            self.func = kwargs["func"]
        else:
            raise NotImplementedError("{:s} function not implemented!".format(func_type))

    def __repr__(self):
        return "{:s} function".format(self.func_type.title())

    def __call__(self, x):
        return self.func(x)

    def derivative(self, tol=0.001):
        def der(x):
            return (self(x + tol) - self(x - tol)) / (2 * tol)
        return Function(func_type="{:s} derivative".format(self.func_type), func=der)


def bias():
    """ Bias function, returns 1, regardless of input
    """
    return lambda x: 1


def identity():
    """ Identity function, returns input
    """
    return lambda x: x


def polynomial(degree):
    """ Polynomial basis function: "global functions of the input variable, so
    that changes in one region of input space affect all other regions" -p. 139
    """
    return lambda x: x ** degree


def gaussian(mu=0, sigma=1):
    """ Gaussian basis function: The parameter <mu> governs the location of the
    basis function in input space, and <sigma> governs the spatial scale.  "it
    should be noted that they are not required to have a probabilistic
    interpretation, and in particular the normalization coefficient is
    unimportant because these basis functions will be multiplied by adaptive
    parameters" - p. 139
    """
    return lambda x: math.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def _sigmoid(x):
    """ Helper function to define a logistic sigmoid
    """
    return 1.0 / (1 + math.exp(-x))


def sigmoid(mu=0, sigma=1, sig_func="logistic"):
    """  Supply <sig_func> with either "logistic" or "tanh" to use a desired
    sigmoid function.  Again, <mu> governs the location in input space, and
    <sigma> the scale.
    """

    def logistic_sigmoid(x):
        return _sigmoid(float(x - mu) / float(sigma))

    if sig_func == "logistic":
        return logistic_sigmoid
    elif sig_func == "tanh":
        return lambda x: 2 * logistic_sigmoid(x) - 1
    else:
        raise NotImplementedError("{:s} sigmoid not implemented: use 'logistic' or 'tanh'".format(sig_func))
