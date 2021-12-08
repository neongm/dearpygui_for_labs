import dearpygui.dearpygui as dpg

class UI():
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()

        with dpg.window(label="plot test", tag="PrimaryWindow", height=650, width=1250): pass

        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()
