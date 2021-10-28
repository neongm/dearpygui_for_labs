import random
import math
M_E = 2.71828182845904523536
M_PI = 3.14159265358979323846


class distribution():
    _required_real_numbers = 1  # for some distributions that require more than 1 random real number

    def get(self, size: int) -> list:
        return [self._convert(self._real()) for element in range(size)]

    def get_true(self, size: int) -> list:
        _step = 1 / size
        return [self._convert(self._fake_real(_element=element, _step=_step)) for element in range(size)]

    # -> to be overriden by distribution child classes
    # should return the value in chosen distribution form
    # the value in Uniform from 0 to 1
    def _convert(self, _real: list) -> float:
        pass

    # to be converted to all the other distributions
    def _real(self):
        return [random.uniform(0, 1) for number in range(self._required_real_numbers)]

    # used to draw a true distribution density plot
    def _fake_real(self, _element: int, _step: float):
        return [_element * _step for number in range(self._required_real_numbers)]


class Uniform(distribution):
    def __init__(self, lower_bound: float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def _convert(self, _real: list) -> float:
        return _real[0]


class Normal(distribution):
    _required_real_numbers = 2

    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def _convert(self, _real: list) -> float:
        rvalue_1 = _real[0]
        rvalue_2 = _real[1]
        first_part = pow(-2 * math.log(rvalue_1), 0.5) * math.cos(2 * M_PI * rvalue_2)
        return first_part * self.mu + self.sigma


class Triangular(distribution):
    def __init__(self, low: float, high: float, mode: float):
        self.low = low
        self.high = high
        self.mode = mode

    def _convert(self, _real: list) -> float:

    #def get(self, size: int) -> list:
    #    return [random.triangular(self.low, self.high, self.mode) for value in range(size)]