from enum import Enum
import math
M_E = 2.71828182845904523536
M_PI = 3.14159265358979323846


class cores(Enum):
    @staticmethod
    def _gauss_core(x: float):
        part1 = 1 / math.pow(2 * M_PI, 0.5)
        part2 = pow(M_E, -1 * x ** 2 / 2)
        return part1 * part2

    @staticmethod
    def _echpochmak_core(x: float):
        sverhu_hren = 3 * (1- (x**2)/5)
        divider = 4 * math.sqrt(5)
        return sverhu_hren/divider

    @staticmethod
    def _koshi_core(x: float):
        return 1/M_PI * 1/(1+x**2)

    @staticmethod
    def _empty(x: float):
        return 1/math.sqrt(2*M_PI) * pow(M_E, -1*(x**2/2))

    @staticmethod
    def _log_core(x: float):
        return pow(M_E, -1*x) / (1+pow(M_E, -1*x))**2


    GAUSS = _gauss_core
    ECHPOCHMAK = _echpochmak_core
    EMPTY = _empty
    KOSHI = _koshi_core
    LOG = _log_core
