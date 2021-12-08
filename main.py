import dearpygui.dearpygui as dpg

from statlibs import Distributions, Stats, KDECores

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_debug()
dpg.show_implot_demo()
dpg.show_style_editor()


def update_ui():
    groups = {
        "NORMAL": 'controls_normal',
        "UNIFORM": 'controls_uniform',
        "TRIANGULAR": 'controls_triangular'
    }
    for item in [*groups.values()]: dpg.hide_item(item)
    dpg.show_item(groups[dpg.get_value("combo_dist")])



class Updater():
    def __init__(self):
        self.data = None

    def generate_data(self):
        selection_size = dpg.get_value('selection_size')
        if dpg.get_value('combo_dist') == 'NORMAL':
            self.data = Stats.selection(distrib=Distributions.Normal(dpg.get_value("normal_mu"),
                                                                     dpg.get_value("normal_sigma")),
                                        size=selection_size)
        elif dpg.get_value('combo_dist') == 'UNIFORM':
            self.data = Stats.selection(distrib=Distributions.Uniform(dpg.get_value("uniform_min"),
                                                                      dpg.get_value("uniform_max")),
                                        size=selection_size)
        elif dpg.get_value('combo_dist') == "TRIANGULAR":
            self.data = Stats.selection(distrib=Distributions.Triangular(dpg.get_value("triangular_low"),
                                                                         dpg.get_value("triangular_high"),
                                                                         dpg.get_value('triangular_mode')),
                                        size=selection_size)

    def update(self):
        self.generate_data()
        self.update_graphs()
        self.update_results()

    def update_graphs(self):
        # getting values from series to draw graphs from
        self.x = self.data.sorted()
        self.y = [self.data.elems_less_than(i) / self.data.size() for i in self.x][::-1]
        # drawing all the series
        self.update_kde()
        self.update_line_series()
        self.update_stair_series()
        self.update_hist_series()
        self.update_real_density_series()

    def update_real_density_series(self):
        dpg.set_value('series_real_density', self.data.get_real_density_xy(resolution=1000))

    def update_line_series(self):
        dpg.set_value('series_line', [self.x, self.y])

    def update_stair_series(self):
        dpg.set_value('series_stair', [self.x, self.y])

    def update_hist_series(self):
        self.update_hist_series_config()
        dpg.set_value('series_hist', [self.data.get_values()])

    def update_hist_series_config(self):
        dpg.configure_item('series_hist', max_range=self.data.max(), min_range=self.data.min(),
                           bins=dpg.get_value("histogram_bars"))

    def update_kde(self):
        if dpg.get_value("combo_kde") == "GAUSS":
            dpg.set_value('kde_graph', self.data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200,
                                                               core=KDECores.cores.GAUSS))
        if dpg.get_value("combo_kde") == "ECHPOCHMAK":
            dpg.set_value('kde_graph', self.data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200,
                                                               core=KDECores.cores.ECHPOCHMAK))
        if dpg.get_value("combo_kde") == "KOSHI":
            dpg.set_value('kde_graph', self.data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200,
                                                               core=KDECores.cores.KOSHI))
        if dpg.get_value("combo_kde") == "EMPTY":
            dpg.set_value('kde_graph', self.data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200,
                                                               core=KDECores.cores.EMPTY))
        if dpg.get_value("combo_kde") == "LOG":
            dpg.set_value('kde_graph', self.data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200,
                                                               core=KDECores.cores.LOG))

    def update_results(self):
        dpg.set_value('average', round(self.data.get_average(), 4))
        dpg.set_value('median', round(self.data.get_median(), 4))
        dpg.set_value('dispersion', round(self.data.get_dispersion(), 4))


with dpg.window(label="plot test", tag="Primary Window", height=650, width=1250):
    ELEM_WIDTH = 200  # width of controls like buttons, inputs, etc.
    upd = Updater()

    with dpg.group(horizontal=True):  # MAIN LAYOUT GROUP

        # LEFT SIDE OF THE WINDOW
        with dpg.group(tag="plots"):
            with dpg.plot(tag="plot_hist", label="plot", height=300, width=900):  # MAIN PLOT
                dpg.add_plot_legend()  # create legend
                dpg.add_plot_axis(dpg.mvXAxis, label="x")  # REQUIRED: create x axis
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")  # REQUIRED: create y axis
                # Drawing stuff (empty for now):
                dpg.add_histogram_series([], label="Histogram", parent="y_axis", tag="series_hist", bins=10,
                                         density=True, bar_scale=0.95)
                dpg.add_line_series([], [], label="Kernel Density Estimation", parent="y_axis", tag="kde_graph")
                dpg.add_line_series([], [], label="Real Density", parent="y_axis", tag="series_real_density")
                # print(mvPlotStyleVar_LineWeight=2)

            with dpg.plot(label="plot", height=300, width=900):  # SECONDARY PLOT
                dpg.add_plot_legend()  # create legend
                dpg.add_plot_axis(dpg.mvXAxis, label="x")  # REQUIRED: create x axis
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_2")  # REQUIRED: create y axis
                # Drawing stuff (empty for now):
                dpg.add_stair_series([], [], label="Emepric Fucntion", parent="y_axis_2", tag="series_stair")
                dpg.add_line_series([], [], label="Polygon Something", parent="y_axis_2", tag="series_line")

        # RIGHT SIDE OF THE WINDOW
        with dpg.group():
            with dpg.group():  # DISTRIBUTION CONTROLS
                dpg.add_text('distribution controls: ')
                dpg.add_combo(['NORMAL', 'UNIFORM', 'TRIANGULAR'], label="distribution", tag="combo_dist",
                              width=ELEM_WIDTH, default_value="NORMAL", callback=update_ui)
                with dpg.group(tag="dist_controls"):
                    with dpg.group(tag="controls_normal"):
                        dpg.add_input_float(width=ELEM_WIDTH, label="mu", tag="normal_mu", default_value=0)
                        dpg.add_input_float(width=ELEM_WIDTH, label="sigma", tag="normal_sigma", default_value=1)
                    with dpg.group(tag="controls_uniform"):
                        dpg.add_input_float(width=ELEM_WIDTH, label="min", tag="uniform_min", default_value=-5)
                        dpg.add_input_float(width=ELEM_WIDTH, label="max", tag="uniform_max", default_value=5)
                    with dpg.group(tag="controls_triangular"):
                        dpg.add_input_float(width=ELEM_WIDTH, label="low", tag="triangular_low", default_value=-5)
                        dpg.add_input_float(width=ELEM_WIDTH, label="high", tag="triangular_high", default_value=5)
                        dpg.add_input_float(width=ELEM_WIDTH, label="mode", tag="triangular_mode", default_value=0)
                    update_ui()

                dpg.add_spacer(height=10)

                with dpg.group(tag="selection_controls"):  # SELECTION CONTROLS
                    dpg.add_text('selection controls: ')
                    dpg.add_input_int(tag="selection_size", label="selection size", width=ELEM_WIDTH, default_value=100,
                                      step=50, min_clamped=True, min_value=10)
                    dpg.add_input_int(tag="histogram_bars", label="histogram bars", width=ELEM_WIDTH, default_value=20,
                                      min_clamped=True,
                                      min_value=3, callback=upd.update_hist_series_config)
                    dpg.add_combo(['GAUSS', 'ECHPOCHMAK', 'KOSHI', 'EMPTY', 'LOG'], label="kde core", tag="combo_kde",
                                  width=ELEM_WIDTH,
                                  default_value='GAUSS', callback=upd.update_kde)
                    dpg.add_input_float(label="kde window width", tag="kde_width", default_value=0.2, width=ELEM_WIDTH,
                                        step=0.05,
                                        min_clamped=True, min_value=0.01, callback=upd.update_kde)

            with dpg.group():  # DRAW BUTTON
                dpg.add_button(label="draw", tag="btn_draw", small=False, callback=upd.update, height=50,
                               width=ELEM_WIDTH)

            with dpg.group():  # RESULTS GROUP
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="average: ")
                    dpg.add_text(tag="average", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="median: ")
                    dpg.add_text(tag="median", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="dispersion: ")
                    dpg.add_text(tag="dispersion", default_value='-')

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 2, category=dpg.mvThemeCat_Plots)

dpg.bind_item_theme('plots', global_theme)

dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()
