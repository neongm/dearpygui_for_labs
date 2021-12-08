import dearpygui.dearpygui as dpg

from statlibs import Distributions, Stats, KDECores

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


class root():
    def __init__(self):
        self.inp_parent = "input_area"
        self.input_matrix_arr = []

    def draw_input_matrix(self):
        rows = 5
        columns = 5
        INPUT_WIDTH = 60
        for x in range(columns):
            self.input_matrix_arr.append([])
            dpg.add_group(horizontal=True, parent=self.inp_parent, tag=f"column {x}")
            for y in range(rows):
                self.input_matrix_arr[x].append(0.0)
                _tag = f"{x} {y}"
                dpg.add_input_float(parent=f"column {x}", tag=_tag, default_value=0.0, callback=self.change_value_callback, width=INPUT_WIDTH)



    def add_row(self):
        _inp_width = 50 #px
        _current_x_size = len(self.input_matrix_arr)
        _current_y_size = len(self.input_matrix_arr[0])
        self.input_matrix_arr[_current_y_size].append(0.0)
        for column, idx in enumerate(self.input_matrix_arr):

            _tag = f"{idx} {_current_y_size}"
            dpg.add_input_float(parent=self.inp_parent, tag=_tag, default_value=0.0, width=_inp_width)

    def add_column(self):
        _inp_width = 50  # px
        _current_x_size = len(self.input_matrix_arr)
        _current_y_size = len(self.input_matrix_arr[0])
        self.input_matrix_arr.append([0.0])
        _tag = f"{_current_x_size} {_current_y_size}"
        dpg.add_input_float(parent=self.inp_parent, tag=_tag, default_value=0.0, width=_inp_width, callback=self.change_value_callback)
        print('fuck')

    def clear_input_area(self):
        dpg.delete_item(children_only=True, item=self.inp_parent)
        print('fuck')

    def change_value_callback(self, sender):
        _x, _y = sender.split(' ')
        self.input_matrix_arr[_x][_y].append(sender.get_value())
        print('fuck')
        dpg.set_value(item="debug_out", value=self.input_matrix_arr)




with dpg.window(label="window", tag="Primary Window", height=650, width=1250):
    ROOT = root()
    with dpg.group(horizontal=True):
        with dpg.group(width=1000):
            dpg.add_button(label="fuck!@")

            dpg.add_text(default_value="input area:")
            with dpg.group(tag="input_area" ): pass


            dpg.add_text(default_value="output area:")
            with dpg.group(tag="output_area"):
                dpg.add_text(default_value="", tag="debug_out")


        with dpg.group(width=224):
            dpg.add_button(label="fuck!@")
            dpg.add_button(label="add row", callback=ROOT.add_row)
            dpg.add_button(label="clear input area", callback=ROOT.clear_input_area)
            dpg.add_button(label="draw whole matrix", callback=ROOT.draw_input_matrix)


dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()