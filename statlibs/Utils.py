import numpy as np
import sympy

from . import Stats
from . import Function

class Utils():

    @staticmethod
    def linear_regression_simple(values_input: Stats.selection, values_output: Stats.selection):
        """ Simple linear regression, uses values of the object itself as input if
        none input_values is provided.

        :param (selection) values_output: Y values of the selection - result of f(x) on corresponding X values
        :param (selection) values_input: X values of the selection corresponding to results in Y values
        :return: tuple(float: coefficient_0, float: coefficient_1)
        """

        # checking if objects have different sizes
        if len(values_output) != len(values_input):
            raise ValueError(f'Arrays have different length: \n{len(values_input)} for input and {len(values_output)} for output')
        else:
            average_input = values_input.get_average()
            average_output = values_output.get_average()

            cross_deviation = sum(values_input * values_output) - values_input.size() * average_input * average_output
            input_deviation = sum(values_input * values_input) - values_input.size() * average_input * average_input

            coefficient_1 = cross_deviation / input_deviation
            coefficient_0 = average_output - coefficient_1 * average_input

        return (coefficient_0, coefficient_1)


    @staticmethod
    def sum_deviation_of_squares(values_x: Stats.selection, values_y: Stats.selection, function: Function.Function):
        return sum([ (function(values_x[i]) - values_y[i])**2 for i in range(values_x.size()) ])


    @staticmethod
    def solve_linear_equation_sympy(self, Func: Function.Function):
        pass


    @staticmethod
    def solve_linear_equation(left_matrix: list, vector: list):
        """ Solves system of linear equations using Gaussian elimination by heavily utilizing cheating
        :param (list) left_matrix: list of lists representing the matrix
        :param (list) vector: list of numbers representing the vector
        :return: (tuple) tuple of numbers, representing the solution
        """

        # yeah, this is kinda cheating, but i wanna solve other stuff first, it works for now
        return tuple(np.linalg.solve(np.array(left_matrix), np.array(vector)))

