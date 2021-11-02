import random
import math
M_E = 2.71828182845904523536
M_PI = 3.14159265358979323846

class distribution():
    # return array of distributed floats
    # -> reworking it to be consistent across the methods
    # by separating single-value and array getters
    def get(self) -> float: pass
    def get_array(self, size: int) -> list: # also it will work without any additional code
        return [self.get() for i in range(size)]
    # returns SINGLE(!!!) Y values that corresponds to given X
    def get_true(self, x: int) -> float: pass


class Uniform(distribution):
    def __init__(self, lower_bound:float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get(self) -> float:
        return random.uniform(self.lower_bound, self.upper_bound)

    def get_true(self, x: int) -> float:
        return 1/(self.upper_bound - self.lower_bound)


class Normal(distribution):
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def get(self) -> float:
        return random.normalvariate(self.mu, self.sigma)

    def get_true(self, x: float) -> float:
        return 1 / (self.sigma * math.sqrt(2*M_PI))*pow(M_E, -0.5*pow((x-self.mu)/self.sigma, 2))


class Triangular(distribution):
    def __init__(self, low: float, high: float, mode: float):
        self.low = low
        self.high = high
        self.mode = mode

    def get(self) -> float:
        return random.triangular(self.low, self.high, self.mode)

    def get_true(self, x: float) -> float:
        # i have to think it by myself, there is not simple "copy-paste" solution on wiki

        # it looks horrible, but it works
        # you know the rule for code that works
        # yep, don't ever touch it

        # original:

        # at_c = 2/(self.high - self.low)
        # if x < self.mode:
        #     OP = at_c
        #     JP = self.mode - self.low
        #     J_tang = math.tan(OP/JP)
        #     JX = x-self.low
        #     return JX * J_tang
        # elif x > self.mode:
        #     OP = at_c
        #     PA = self.high - self.mode
        #     J_tang = math.tan(OP / PA)
        #     AX = self.high - x
        #     return AX * J_tang
        # elif x == self.mode: return at_c


        # but i will touch it:

        # if x != self.mode:
        #     if x < self.mode:
        #         divider = self.mode - self.low
        #         multiplier = x - self.low
        #     else:
        #         divider = self.high - self.mode
        #         multiplier = self.high - x
        #     return (multiplier * math.tan(2/(self.high - self.low) / divider))
        # else:
        #     return 2/(self.high - self.low)


        # and then i came up with this just for LOLs
        #prob_at_mode = 2 / (self.high - self.low)
        # return ((x - self.low) * (x < self.mode) + (self.high - x) * (x > self.mode)) * \
        #        (math.tan(prob_at_mode / ((self.mode - self.low))) * (x < self.mode) +
        #         math.tan(prob_at_mode / ((self.high - self.mode))) * (x > self.mode)) + \
        #        (prob_at_mode) * (x == self.mode)
        # yeah, ik, it doesn't accout for the cases where x<self.low and x>self.high, but it is fun


        # i'll fix it there:
        # it is probably final version of the code
        if x < self.mode: return (x - self.low) * math.tan(2 / (self.high - self.low) / (self.mode - self.low))
        elif x > self.mode: return (self.high - x) * math.tan(2/(self.high - self.low) / (self.high - self.mode))
        elif x < self.low or x > self.high: return 0.0
        elif x == self.mode: return 2/(self.high - self.low)



        # there is the solution from my good friend ITR
        # but it doesn't work as intended
        # at_c = 2 / (self.high - self.low)
        # if x == self.mode: return at_c
        #
        # left_add = -1
        # right_add = - self.low
        # if x > self.mode:
        #     left_add = 1
        #     right_add = self.high
        #
        # divide_on = self.mode * left_add + right_add
        # mult_by = x * left_add + right_add
        # return math.tan(at_c / divide_on) * mult_by





