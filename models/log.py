import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint
from constants import *

def model(y: float, t: any): return log_growth_speed * y * (1 - (y / log_capacity))

log_growth_speed  = round(random.uniform(L_GR_MIN, L_GR_MAX), 3)
log_init_pop      = round(random.uniform(L_IP_MIN, L_IP_MAX), 3)
log_capacity      = round(random.uniform(L_C_MIN, L_C_MAX), 3)

T_VALUES = np.arange(0.0, 100.0, 0.1)
solution = odeint(model, log_init_pop, T_VALUES)


def update_solution() -> None:
    global solution
    solution = odeint(model, log_init_pop, T_VALUES)

def update_sliders() -> None:
    dpg.set_value('log_growth_speed', log_growth_speed)
    dpg.set_value('log_init_pop', log_init_pop)
    dpg.set_value('log_capacity', log_capacity)


def update_plot() -> None:
    dpg.set_value('log_pop_line', [T_VALUES, solution])
    dpg.set_value('log_init_pop_line', log_init_pop)
    dpg.set_value('log_capacity_line', log_capacity)


def update_param(sender, app_data) -> None:
    globals()[sender] = app_data
    update_solution()
    update_sliders()
    update_plot()

def drag_init_pop_line() -> None:
    global log_init_pop
    _value = dpg.get_value('log_init_pop_line')
    if _value >= L_IP_MAX:     log_init_pop = L_IP_MAX
    elif _value <= L_IP_MIN:   log_init_pop = L_IP_MIN
    else:                      log_init_pop = _value
    update_sliders()
    update_solution()
    update_plot()
    dpg.configure_item('log_init_pop_line', default_value=log_init_pop)

def drag_capacity_line() -> None:
    global log_capacity
    _value = dpg.get_value('log_capacity_line')
    if _value >= L_C_MAX:   log_capacity = L_C_MAX
    elif _value <= L_C_MIN: log_capacity = L_C_MIN
    else:                   log_capacity = _value
    update_sliders()
    update_solution()
    update_plot()
    dpg.configure_item('log_capacity_line', default_value=log_capacity)

def randomize() -> None:
    global log_capacity, log_growth_speed, log_init_pop, solution
    log_capacity = round(random.uniform(L_C_MIN, L_C_MAX), 3)
    log_growth_speed = round(random.uniform(L_GR_MIN, L_GR_MAX), 3)
    log_init_pop = round(random.uniform(L_IP_MIN, L_IP_MAX))
    update_solution()
    update_sliders()
    update_plot()

def zero_out() -> None:
    global log_capacity, log_growth_speed, log_init_pop, solution
    log_capacity = L_C_MIN
    log_growth_speed = L_GR_MIN
    log_init_pop = L_IP_MIN
    update_solution()
    update_sliders()
    update_plot()

def window() -> None:
    with dpg.tab(parent='models_tabs', label='Logistic'):
        dpg.add_slider_double(tag='log_growth_speed',
                                    min_value=L_GR_MIN, max_value=L_GR_MAX, default_value=log_growth_speed,
                                    width=200, label='Growth speed',
                                    callback=update_param)
        dpg.add_slider_double(tag='log_init_pop',
                                min_value=L_IP_MIN, max_value=L_IP_MAX, default_value=log_init_pop,
                                width=200, label='Initial population',
                                callback=update_param)
        dpg.add_slider_double(tag='log_capacity',
                                min_value=L_C_MIN, max_value=L_C_MAX, default_value=log_capacity,
                                width=200, label='Capacity',
                                callback=update_param)

        with dpg.group(horizontal=True):
            dpg.add_button(label='Randomize!', callback=randomize)
            dpg.add_button(label='Zero out!', callback=zero_out)

        with dpg.plot(tag='log_main_plot',
                        width=dpg.get_viewport_width()-40,
                        height=dpg.get_viewport_height()-200,
                        equal_aspects=True):
            x = dpg.add_plot_axis(dpg.mvXAxis)
            y = dpg.add_plot_axis(dpg.mvYAxis)

            dpg.add_line_series(T_VALUES, solution, parent=y, tag='log_pop_line')
            dpg.add_drag_line(tag='log_capacity_line',
                                label='Capacity', vertical=False, color=[255, 0, 0, 100],
                                default_value=log_capacity,
                                callback=drag_capacity_line)
            dpg.add_drag_line(tag='log_init_pop_line',
                                label='Initial population', vertical=False, color=[0, 255, 0, 100],
                                default_value=log_init_pop,
                                callback=drag_init_pop_line)
            