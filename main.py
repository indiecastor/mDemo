import dearpygui.dearpygui as dpg
import scipy.integrate as difur
import numpy as np

from models import malthusian, logistic, lotka_volterra


dpg.create_context()
dpg.create_viewport(title='Models Demo',
                    large_icon='icon.ico', small_icon='icon.ico',
                    width=1280, height=720, x_pos=20, y_pos=20)


def update_geometry():
    _wp_width: int = dpg.get_viewport_width()
    _wp_height: int = dpg.get_viewport_height()

    # Malthusian Model Plot
    dpg.configure_item('malt_main_plot', width=_wp_width-40, height=_wp_height-150)
    # Logistic Model Plot
    dpg.configure_item('log_main_plot', width=_wp_width-40, height=_wp_height-176)
    # Lotka-Volterra Model Plots
    dpg.configure_item('lv_main_plot', width=(_wp_width-40)/2, height=_wp_height-240)
    dpg.configure_item('lv_phase_diagram', width=(_wp_width-40)/2, height=_wp_height-240)
    
    

# MAIN WINDOW
dpg.add_window(tag='main_window')
with dpg.tab_bar(parent='main_window', tag='models_tabs'):
    malthusian.Window()
    logistic.Window()    
    lotka_volterra.Window()
   
dpg.setup_dearpygui()
dpg.set_primary_window('main_window', True)

dpg.set_viewport_resize_callback(update_geometry)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()