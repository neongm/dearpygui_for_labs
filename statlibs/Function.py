import sympy


class Function():
    func = None
    def __init__(self, set_func: 'function' = None):
        if set_func is not None: self.func = set_func

    def __call__(self, x):
        return self.func(x)

    def get_values_y(self, values_x: list):
        return [self.__call__(value) for value in values_x]

