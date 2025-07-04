import dearpygui.dearpygui as dpg
import numpy as np
from scipy.integrate import odeint

from constants import *

def model(y, t: any) -> float: return malt_growth_speed * y

malt_growth_speed: float = np.random.uniform(MALT_GR_MIN, MALT_GR_MAX)
malt_init_pop: float     = np.random.uniform(MALT_IP_MIN, MALT_IP_MAX)

T_VALUES = np.arange(0, 2, .01)
solution = odeint(model, malt_init_pop, T_VALUES)


def update_solution() -> None:
    global solution
    solution = odeint(model, malt_init_pop, T_VALUES)


def update_sliders():
    dpg.configure_item('malt_growth_speed', default_value=malt_growth_speed)
    dpg.configure_item('malt_init_pop', default_value=malt_init_pop)


def update_plot():
    dpg.set_value('malt_pop_line', [T_VALUES, solution]) # Plot line
    dpg.set_value('malt_init_pop_line', malt_init_pop) # Drag line


def update_param(sender, app_data) -> None:
    globals()[sender] = app_data
    update_solution()
    update_sliders()
    update_plot()


def drag_line():
    global malt_init_pop
    _value = dpg.get_value('malt_init_pop_line')
    if _value >= MALT_IP_MAX:
        malt_init_pop = MALT_IP_MAX
    elif _value <= MALT_IP_MIN:
        malt_init_pop = MALT_IP_MIN
    else:
        malt_init_pop = _value
    update_sliders()
    update_solution()
    update_plot()
    dpg.configure_item('malt_init_pop_line', default_value=malt_init_pop)
    

def randomize() -> None:
    global malt_growth_speed, malt_init_pop, solution
    malt_growth_speed = np.random.uniform(MALT_GR_MIN, MALT_GR_MAX)
    malt_init_pop     = np.random.uniform(MALT_IP_MIN, MALT_IP_MAX)
    update_solution()
    update_sliders()
    update_plot()


def zero_out() -> None:
    global malt_growth_speed, malt_init_pop, solution
    malt_growth_speed = MALT_GR_MIN
    malt_init_pop = MALT_IP_MIN
    update_solution()
    update_sliders()
    update_plot()


def window() -> None:
    with dpg.tab(parent='models_tabs', label='Malthusian'):
        dpg.add_slider_double(tag='malt_growth_speed',
                                min_value=MALT_GR_MIN, max_value=MALT_GR_MAX,
                                default_value=malt_growth_speed,
                                width=200, label='Growth speed',
                                callback=update_param)
        dpg.add_slider_double(tag='malt_init_pop',
                                min_value=MALT_IP_MIN, max_value=MALT_IP_MAX, default_value=malt_init_pop,
                                width=200, label='Initial population',
                                callback=update_param)

        with dpg.group(horizontal=True): # Randomize and zero out buttons
            dpg.add_button(label='Randomize!', callback=randomize)
            dpg.add_button(label='Zero out!', callback=zero_out)

        with dpg.plot(tag='malt_main_plot',
                        width=dpg.get_viewport_width()-40, height=dpg.get_viewport_height()-150,
                        equal_aspects=True):
            x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
            y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')

            dpg.add_line_series(T_VALUES, solution, parent=y, tag='malt_pop_line')
            dpg.add_drag_line(tag='malt_init_pop_line',
                                label='Initial population', vertical=False, color=[0, 255, 0, 100],
                                default_value=malt_init_pop,
                                callback=drag_line)