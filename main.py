import dearpygui.dearpygui as dpg

from statlibs import Distributions, Stats, KDECores

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_debug()


def update_ui():
    groups = {
        "NORMAL": 'controls_normal',
        "UNIFORM": 'controls_uniform',
        "TRIANGULAR": 'controls_triangular'
    }
    for item in [*groups.values()]: dpg.hide_item(item)
    dpg.show_item(groups[dpg.get_value("combo_dist")])


def generate_data():
    selection_size = dpg.get_value('selection_size')

    if dpg.get_value('combo_dist') == 'NORMAL':
        return Stats.selection(distrib=Distributions.Normal(dpg.get_value("normal_mu"),
                                                            dpg.get_value("normal_sigma")), size=selection_size)
    elif dpg.get_value('combo_dist') == 'UNIFORM':
        return Stats.selection(distrib=Distributions.Uniform(dpg.get_value("uniform_min"),
                                                             dpg.get_value("uniform_max")), size=selection_size)
    elif dpg.get_value('combo_dist') == "TRIANGULAR":
        return Stats.selection(distrib=Distributions.Triangular(dpg.get_value("triangular_low"),
                                                                dpg.get_value("triangular_high"),
                                                                dpg.get_value('triangular_mode')), size=selection_size)


def update_plot():
    data = generate_data()
    x = data.sorted()
    y = [data.elems_less_than(i) / data.size() for i in x][::-1]
    dpg.set_value('series_line', [x, y])
    dpg.set_value('series_stair', [x, y])
    dpg.configure_item('series_hist', max_range=data.max(), min_range=data.min(), bins=dpg.get_value("histogram_bars"))
    dpg.set_value('series_hist', [data.get_values()])

    dpg.set_value('average', round(data.get_average(), 4))
    dpg.set_value('median', round(data.get_median(), 4))
    dpg.set_value('dispersion', round(data.get_dispersion(), 4))

    if dpg.get_value("combo_kde") == "GAUSS":
        dpg.set_value('KDE', data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200, core = KDECores.cores.GAUSS))
    if dpg.get_value("combo_kde") == "ECHPOCHMAK":
        dpg.set_value('KDE', data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200, core = KDECores.cores.ECHPOCHMAK))
    if dpg.get_value("combo_kde") == "KOSHI":
        dpg.set_value('KDE', data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200, core = KDECores.cores.KOSHI))
    if dpg.get_value("combo_kde") == "EMPTY":
        dpg.set_value('KDE', data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200, core = KDECores.cores.EMPTY))
    if dpg.get_value("combo_kde") == "LOG":
        dpg.set_value('KDE', data.get_estimated(window_width=dpg.get_value("kde_width"), resolution=200, core = KDECores.cores.LOG))



with dpg.window(label="plot test", tag="Primary Window", height=650, width=1250):
    with dpg.group(horizontal=True):

        with dpg.group():
            with dpg.plot(label="plot", height=300, width=900):
                # optionally create legend
                dpg.add_plot_legend()

                # REQUIRED: create x and y axes
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

                dpg.add_histogram_series([], label="Histogram", parent="y_axis", tag="series_hist", bins=10,
                                         density=True, bar_scale=0.95)

                dpg.add_line_series([], [], label="Kernel Density Estimation", parent="y_axis", tag="KDE")

            with dpg.plot(label="plot", height=300, width=900):
                # optionally create legend
                dpg.add_plot_legend()

                # REQUIRED: create x and y axes
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_2")

                dpg.add_stair_series([], [], label="Emepric Fucntion", parent="y_axis_2", tag="series_stair")
                dpg.add_line_series([], [], label="Polygon Something", parent="y_axis_2", tag="series_line")


        with dpg.group():
            with dpg.group():

                dpg.add_text('distribution controls: ') # DISTRIBUTION CONTROLS

                dpg.add_combo(['NORMAL', 'UNIFORM', 'TRIANGULAR'], label="distribution", tag="combo_dist", width=200, default_value="NORMAL", callback=update_ui)
                with dpg.group(tag="dist_controls"):
                    with dpg.group(tag="controls_normal"):
                        dpg.add_input_float(width=200, label="mu", tag="normal_mu", default_value=0)
                        dpg.add_input_float(width=200, label="sigma", tag="normal_sigma", default_value=1)
                    with dpg.group(tag="controls_uniform"):
                        dpg.add_input_float(width=200, label="min", tag="uniform_min", default_value=-5)
                        dpg.add_input_float(width=200, label="max", tag="uniform_max", default_value=5)
                    with dpg.group(tag="controls_triangular"):
                        dpg.add_input_float(width=200, label="low", tag="triangular_low", default_value=-5)
                        dpg.add_input_float(width=200, label="high", tag="triangular_high", default_value=5)
                        dpg.add_input_float(width=200, label="mode", tag="triangular_mode", default_value=0)
                update_ui()

                dpg.add_spacer(height=10) # SELECTION CONTROLS

                dpg.add_text('selection controls: ')
                dpg.add_input_int(tag="selection_size", label="selection size", width=200, default_value=100)
                dpg.add_input_int(tag="histogram_bars", label="histogram bars", width=200, default_value=20)
                dpg.add_combo(['GAUSS', 'ECHPOCHMAK', 'KOSHI', 'EMPTY', 'LOG'], label="kde core", tag="combo_kde", width=200,
                              default_value='GAUSS')
                dpg.add_input_float(tag="kde_width", label="KDE window width", default_value=0.2, width=200, step=0.05)

            with dpg.group():
                dpg.add_button(tag="btn_draw", small=False, label="draw", callback=update_plot, height=50, width=200)
            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="average: ")
                    dpg.add_text(tag="average", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="median: ")
                    dpg.add_text(tag="median", default_value='-')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value="dispersion: ")
                    dpg.add_text(tag="dispersion", default_value='-')



dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()