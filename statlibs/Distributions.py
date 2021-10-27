import random


class distribution():
    def get(self, size: int) -> list: pass


class Uniform(distribution):
    def __init__(self, lower_bound:int, upper_bound:int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get(self, size: int) -> list:
        return [random.randint(self.lower_bound, self.upper_bound) for value in range(size)]


class Normal(distribution):
    def __init__(self, mu: int, sigma: int):
        self.mu = mu
        self.sigma = sigma

    def get(self, size: int) -> list:
        return [random.normalvariate(self.mu, self.sigma) for value in range(size)]
