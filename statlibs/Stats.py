from . import Distributions
from . import KDECores
import math


class selection():
    values = []
    values_normalised = []
    distrib = None
    lower_bound = None
    upper_bound = None

    def __init__(self, distrib: Distributions.distribution, size: int = None, values: list = None):
        if values is not None: self.values = values
        self.distrib = distrib
        if size is not None: self._fill_values(size)

    def _fill_values(self, size: int):
        self.values = self.distrib.get_array(size=size)

    def _update_bounds(self):
        self.lower_bound = min(self.values)
        self.upper_bound = max(self.values)

    def sorted(self, reversed: bool = False):
        return sorted(self.values, reverse=reversed)

    def get_propagation(self):
        return [self.elems_less_than(i) / self.size() for i in self.sorted()][::-1]

    def get_real_density_xy(self, resolution: int = 200):

        x = self.get_range(resolution=resolution)
        y = self.get_real_density(resolution=resolution)
        return [x, y]

    def get_real_density(self, resolution: int = 200):
        max = self.max()
        min = self.min()
        step = max-min/resolution
        return [self.distrib.get_true(x) for x in self.get_range(resolution=resolution)]

    def get_range(self, resolution: int = 200):
        max = self.max()
        min = self.min()
        step = (max - min) / resolution
        return [min + (i * step) for i in range(resolution)]

    def normalize(self):
        max_value = max(self.values)
        self.values_normalised = [value/max_value for value in self.values]

    def get_normalised(self):
        if len(self.values_normalised) != len(self.values): self.normalize()
        return self.values_normalised

    def slice_by_value(self, amount_of_slices: int) -> list:
        max_value = max(self.values)
        step = max_value/amount_of_slices
        return [self.get_values_in_range(slice*step, (slice+1)*step) for slice in range(amount_of_slices)]

    def get_average(self):
        return sum(self.values)/len(self.values)

    def get_median(self):
        return sorted(self.values)[len(self.values)//2]

    def kernel_density_estimation(self, x: float, window_width: float = 0.3, core = KDECores.cores.GAUSS):
        kde_kernel_sum = 0
        for xi in self.values:
            kde_kernel_sum += core((x - xi) / window_width)

        return (1 / (self.size() * window_width)) * kde_kernel_sum

    def get_estimated(self, window_width: float = 0.3, resolution: int = 1000, core = KDECores.cores.GAUSS):
        _min = self.min()
        _max = self.max()
        step = (_max - _min)/resolution
        return [[_min+x*step for x in range(resolution)],
                [self.kernel_density_estimation(x=_min+x*step, window_width = window_width, core = core) for x in range(resolution)]]

    def get_dispersion(self):
        avg = self.get_average()
        return sum([(x-avg)**2 for x in self.values])/self.size()

    def get_values_in_range(self, lower_bound: int = None, upper_bound: int = None) -> list:
        if lower_bound is not None and upper_bound is not None:
            return [val for val in self.values if lower_bound < val <= upper_bound]
        elif lower_bound is None and upper_bound is not None:
            return [val for val in self.values if val <= upper_bound]
        elif lower_bound is not None and upper_bound is None:
            return [val for val in self.values if lower_bound < val]
        else: return self.values

    def sum_less_than(self, upper_bound):
        return sum(self.get_values_in_range(upper_bound))

    def elems_less_than(self, upper_bound):
        return len(self.get_values_in_range(upper_bound))

    def size(self): return len(self.values)

    def __str__(self):
        return f"selection: {str(self.values)}"

    def __repr__(self): return self.values

    def __len__(self): return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

    def __iter__(self):
        return self.values.__iter__()

    def get_values(self): return self.values

    def max(self): return max(self.values)

    def min(self): return min(self.values)
