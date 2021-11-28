from statlibs import Distributions, Stats, KDECores
from statlibs.Utils import Utils
import random
from statlibs.Function import Function
import math
import sympy

# def main():
#     matrix = [[1, 0, 1, 0],
#              [-1, 1,-2, 1],
#              [ 4, 0, 1,-2],
#              [-4, 4, 0, 1]]
#
#     vector = [2, -2, 0, 5]
#
#     print(Utils.solve_linear_equation(matrix, vector))

def generate_testing_values(function: Function, size: int=100, start:int=-50, step: int=1):
    values_x = [i for i in range(100)]
    values_y_true = [function(i) for i in values_x]
    values_y_randomised = [i + random.normalvariate(0, 1) for i in values_y_true]

    return values_x, values_y_true, values_y_randomised


def generate_testing_values_sympy(function: sympy.Function, size: int=100, start:int=-50, step: int=1):
    values_x = [i for i in range(100)]
    values_y_true = [function for i in values_x]
    values_y_randomised = [i + random.normalvariate(0, 1) for i in values_y_true]

    return values_x, values_y_true, values_y_randomised


def test_multiple_functions():
    functions = [Function(lambda x: x ** 2),
                 Function(lambda x: math.sin(x)),
                 Function(lambda x: math.cos(x)),
                 Function(lambda x: math.log2(x) if x != 0 else 1),
                 Function(lambda x: x ** 3),
                 Function(lambda x: x/10),
                 Function(lambda x: x*10-math.sin(x*3)+math.tan(x**2)-math.pow(x, x/10))]


    for f in functions:
        set = generate_testing_values(function = f)
        x = Stats.selection(values=set[0])
        y_true = Stats.selection(values=set[1])
        y_rand = Stats.selection(values=set[2])

        print(f"TEST PASSED" if (sq:=Utils.sum_deviation_of_squares(x, y_true, f)) == 0 else f"FAILED: sum of sqares = {sq}",)
        print(f"TEST PASSED: sum of sqares on randomised = {sq}" if (sq := Utils.sum_deviation_of_squares(x, y_rand, f)) != 0 else f"TEST FAILED")


def find_original_using_sum_of_square_deviations_please():
    functions = [Function(lambda x: x ** 2),
                 Function(lambda x: math.sin(x)),
                 Function(lambda x: math.cos(x)),
                 Function(lambda x: math.log2(x) if x != 0 else 1),
                 Function(lambda x: x ** 3),
                 Function(lambda x: x/10),
                 Function(lambda x: x*10-math.sin(x*3)+math.tan(x**2)-math.pow(x, x/10))]

    lowest = None
    lowest_f_id = None
    orig_f_id = 4

    for id, f_testing in zip([id for id in range(len(functions))], functions):
        set = generate_testing_values(function=functions[orig_f_id])
        x = Stats.selection(values=set[0])
        y = Stats.selection(values=set[2])

        if lowest == None:
            lowest = Utils.sum_deviation_of_squares(x, y, f_testing)
            lowest_f_id = id
        else:
            if (s := Utils.sum_deviation_of_squares(x, y, f_testing)) < lowest:
                print(f"least squares for function {id}: {round(s,2)}")
                lowest = s
                lowest_f_id = id
            else: print(f"least squares for function {id}: {round(s,2)}")

    print(F"original function id: {orig_f_id}\nidententified funciton id: {lowest_f_id}")
    print(F"FIND TEST PASSED" if lowest_f_id == orig_f_id else F"FUCK U, TEST FAILED")


def sympy_solver_test():
    #set = generate_testing_values(function=Function[0])
    x_arr = [i for i in range(10)]
    y_arr = [2+5*i+10*(i**2)+random.normalvariate(0, 0.2) for i in range(10)]
    x = Stats.selection(values=x_arr)
    y = Stats.selection(values=y_arr)

    a, b, c, x = sympy.symbols('a b c x', real=True)
    f = sympy.Function('f')(a + b*x + c*(x**2))
    #sum = sympy.Function('sum'())


    f_diff_by_a = f.diff(a)
    f_diff_by_b = f.diff(b)
    f_diff_by_c = f.diff(c)
    solution = sympy.solve(f_diff_by_a, (a, b, c, x))
    print(solution)






def tests():
    # test_multiple_functions()
    find_original_using_sum_of_square_deviations_please()
    sympy_solver_test()

if __name__ == "__main__":
    tests()
