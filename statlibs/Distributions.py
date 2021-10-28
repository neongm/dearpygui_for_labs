import random



class distribution():
    def get(self, size: int) -> list: pass
    def get_true(self, size: int) -> list: pass


class Uniform(distribution):
    def __init__(self, lower_bound:float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get(self, size: int) -> list:
        return [random.uniform(self.lower_bound, self.upper_bound) for value in range(size)]


class Normal(distribution):
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def get(self, size: int) -> list:
        return [random.normalvariate(self.mu, self.sigma) for value in range(size)]


class Triangular(distribution):
    def __init__(self, low: float, high: float, mode: float):
        self.low = low
        self.high = high
        self.mode = mode

    def get(self, size: int) -> list:
        return [random.triangular(self.low, self.high, self.mode) for value in range(size)]