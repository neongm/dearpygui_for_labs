import random
import math
M_E = 2.71828182845904523536
M_PI = 3.14159265358979323846

class distribution():
    # return array of distributed floats
    # -> probably should rework the entire class towards single values
    def get(self, size: int) -> list: pass

    # returns SINGLE(!!!) Y values that corresponds to given X
    def get_true(self, x: int) -> float: pass


class Uniform(distribution):
    def __init__(self, lower_bound:float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get(self, size: int) -> list:
        return [random.uniform(self.lower_bound, self.upper_bound) for value in range(size)]

    def get_true(self, x: int) -> float:
        return 1/(self.upper_bound - self.lower_bound)


class Normal(distribution):
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def get(self, size: int) -> list:
        return [random.normalvariate(self.mu, self.sigma) for value in range(size)]

    def get_true(self, x: float) -> float:
        return 1 / (self.sigma * math.sqrt(2*M_PI))*pow(M_E, -0.5*pow((x-self.mu)/self.sigma, 2))


class Triangular(distribution):
    def __init__(self, low: float, high: float, mode: float):
        self.low = low
        self.high = high
        self.mode = mode

    def get(self, size: int) -> list:
        return [random.triangular(self.low, self.high, self.mode) for value in range(size)]

    def get_true(self, x: float) -> float:
        # i have to think it by myself, there is not simple "copy-paste" solution on wiki

        # it looks horrible, but it works
        # you know the rule for code that works
        # yep, don't ever touch it

        at_c = 2/(self.high - self.low)
        if x < self.mode:
            OP = at_c
            JP = self.mode - self.low
            J_tang = math.tan(OP/JP)
            JX = x-self.low
            return JX*J_tang
        elif x > self.mode:
            OP = at_c
            PA = self.high - self.mode
            J_tang = math.tan(OP / PA)
            AX =  self.high - x
            return AX * J_tang
        elif x== self.mode: return at_c





