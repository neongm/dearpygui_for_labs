import dearpygui.dearpygui as dpg

from statlibs import Distributions, Stats

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_documentation()
dpg.show_metrics()
from math import sin


def generate_data():
    selection_size = dpg.get_value('selection_size')

    if dpg.get_value('combo_dist') == 'NORMAL':
        return Stats.selection(distrib=Distributions.Normal(0, 1), size=selection_size)
    elif dpg.get_value('combo_dist') == 'UNIFORM':
        return Stats.selection(distrib=Distributions.Uniform(0, 100), size=selection_size)


def update_plot():
    data = generate_data()
    x = data.sorted()
    y = [data.elems_less_than(i) / data.size() for i in x][::-1]
    dpg.set_value('series_line', [x, y])
    dpg.set_value('series_stair', [x, y])
    dpg.configure_item('series_hist', max_range=data.max(), min_range=data.min(), bins=dpg.get_value("histogram_bars"))
    dpg.set_value('series_hist', [data.get_values()])


with dpg.window(label="plot test", tag="Primary Window", height=650, width=1250):
    with dpg.group(horizontal=True):
        with dpg.plot(label="hist", height=600, width=900):
            # optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

            dpg.add_histogram_series([], label="Histogram", parent="y_axis", tag="series_hist", bins=10,
                                     density=True, bar_scale=1)
            dpg.add_stair_series([], [], label="Emepric Fucntion", parent="y_axis", tag="series_stair")
            dpg.add_line_series([], [], label="Polygon Something", parent="y_axis", tag="series_line")

        with dpg.group():
            with dpg.group():
                dpg.add_combo(['NORMAL', 'UNIFORM'], label="distribution", tag="combo_dist", width=200, default_value="NORMAL")
                dpg.add_input_int(tag="selection_size", label="selection size", width=200, default_value=100)
                dpg.add_input_int(tag="histogram_bars", label="histogram bars", width=200, default_value=20)
            with dpg.group():
                dpg.add_button(tag="btn_draw", small=False, label="draw", callback=update_plot, height=50, width=200)



dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()