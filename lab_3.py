import dearpygui.dearpygui as dpg

from statlibs import Distributions, Stats, KDECores

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


# https://www.geeksforgeeks.org/linear-regression-python-implementation/ - i think i should save it here
class Root():
    def __init__(self):
        self.values_input = Stats.selection(values=[])
        self.values_output = Stats.selection(values=[])
        self.dragpoints = None

    def generate_seleciton(self, selection_size: int = 10):
        self.values_input = Stats.selection(size=10, distrib=Distributions.Uniform(-1, 1))
        self.values_output = Stats.selection(size=10, distrib=Distributions.Uniform(-1, 1)) # wtf

        for i in range(self.values_input.size()):
            self.add_dragpoint(x = self.values_input[i], y = self.values_output[i])

        self.estimate_coefficients()

    def append(self, x, y):
        self.values_input.append(x)
        self.values_output.append(y)

    def draw_scatter(self): pass
        #dpg.set_value('series_scatter', value=[self.values_input.get_values(), self.values_output.get_values()])


    def estimate_coefficients(self):
        average_input = self.values_input.get_average()
        average_output = self.values_output.get_average()

        cross_deviation = sum(self.values_input * self.values_output) - self.values_input.size() * average_input * average_output
        input_deviation = sum(self.values_input * self.values_input) - self.values_input.size() * average_input * average_input

        self.coefficient_1 = cross_deviation / input_deviation
        self.coefficient_0 = average_output - self.coefficient_1 * average_input

        dpg.set_value(item='text_b0', value=f'{round(self.coefficient_0, 4)}')
        dpg.set_value(item='text_b1', value=f'{round(self.coefficient_1, 4)}')
        dpg.set_value(item='text_formula', value=f'f(x) = {round(self.coefficient_0, 4)} + {round(self.coefficient_1, 4)} * x')

        self.draw_regression_line()

    def draw_regression_line(self, x=None):
        max_x = self.values_input.max()
        min_x = self.values_input.min()
        min_y = self.coefficient_0 + self.coefficient_1 * min_x
        max_y = self.coefficient_0 + self.coefficient_1 * max_x

        dpg.set_value('series_regression_line', [[min_x, max_x], [min_y, max_y]])

    def add_dragpoint_fuck(self):
        self.add_dragpoint(x=0, y=0)

    def add_dragpoint(self, x: float = 0, y: float = 0):
        print(x, y)
        dp = dpg.add_drag_point(parent="plot_hist", default_value=[x, y])
        dpg.set_item_callback(dp, self.draw_dragpoints)

        if self.dragpoints is None: self.dragpoints = [dp]
        else: self.dragpoints.append(dp)

    def clear_plot(self):
        for point in self.dragpoints:
            dpg.delete_item(item=point)
        self.dragpoints = []


    def draw_dragpoints(self):
        self.values_input = Stats.selection(values=[dpg.get_value(dragpoint_tag)[0] for dragpoint_tag in self.dragpoints])
        self.values_output = Stats.selection(values=[dpg.get_value(dragpoint_tag)[1] for dragpoint_tag in self.dragpoints])
        self.draw_scatter()
        self.estimate_coefficients()






def print_val(sender):
    print(dpg.get_value(sender))

with dpg.window(label="plot test", tag="Primary Window", height=650, width=1250):
    ELEM_WIDTH = 200  # width of controls like buttons, inputs, etc.

    with dpg.group(horizontal=True):  # MAIN LAYOUT GROUP

        ROOT = Root()

        # LEFT SIDE OF THE WINDOW
        with dpg.group(tag="plots"):
            with dpg.plot(tag="plot_hist", label="plot", height=600, width=900, ):  # MAIN PLOT
                dpg.add_plot_legend()  # create legend
                dpg.add_plot_axis(dpg.mvXAxis, label="x")  # REQUIRED: create x axis
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")  # REQUIRED: create y axis
                # Drawing stuff (empty for now):)

                dpg.add_scatter_series([], [], label="Scatter", parent="y_axis", tag="series_scatter")
                dpg.add_line_series([], [], label="Linear Regression Line", parent="y_axis", tag="series_regression_line")


        with dpg.group():
            dpg.add_button(tag="btn_generate_selection", label="generate selection", width=ELEM_WIDTH, callback=ROOT.generate_seleciton)
            dpg.add_button(tag="btn_add_ragpoint", label="add drag point", width=ELEM_WIDTH, callback=ROOT.add_dragpoint_fuck)
            dpg.add_button(tag="btn_draw_dragpoints", label="draw_dragpoints", width=ELEM_WIDTH, callback=ROOT.draw_dragpoints)
            dpg.add_button(tag="btn_clear_plot", label="clear plot", width=ELEM_WIDTH, callback=ROOT.clear_plot)

            with dpg.group():  # RESULTS GROUP
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="b0: ")
                    dpg.add_text(tag="text_b0", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="b1: ")
                    dpg.add_text(tag="text_b1", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="formula: ")
                    dpg.add_text(tag="text_formula", default_value='f(x) = -')


dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()
