import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint
from constants import *

def model(y: float, t: any): return log_growth_speed * y * (1 - (y / log_capacity))

log_growth_speed  = round(random.uniform(LOG_GROWTH_SPEED_MIN, LOG_GROWTH_SPEED_MAX), 3)
log_init_pop      = round(random.uniform(LOG_INIT_POP_MIN, LOG_INIT_POP_MAX), 3)
log_capacity      = round(random.uniform(LOG_CAPACITY_MIN, LOG_CAPACITY_MAX), 3)

t_values = np.arange(0.0, 100.0, 0.1)
solution = odeint(model, log_init_pop, t_values)

def update(param) -> None:
    """
    param ∈ ['log_growth_speed', 'log_init_pop', 'log_capacity', 'all']
    """
    global log_growth_speed, log_init_pop, log_capacity, solution
    # Updating values of params
    match param:
        case 'log_growth_speed': log_growth_speed = dpg.get_value('log_growth_speed')
        case 'log_init_pop':    log_init_pop = dpg.get_value('log_init_pop')
        case 'log_capacity':    log_capacity = dpg.get_value('log_capacity')
        case 'all':
            log_growth_speed = dpg.get_value('log_growth_speed')
            log_init_pop = dpg.get_value('log_init_pop')
            log_capacity = dpg.get_value('log_capacity')
        case _: raise ValueError
    # Re-calculating solution
    solution = odeint(model, log_init_pop, t_values)
    # Updating sliders
    if param in LOG_PARAMS:
        dpg.configure_item(param, default_value=globals()[param])
    elif param == 'all':
        dpg.configure_item('log_growth_speed', default_value=log_growth_speed)
        dpg.configure_item('log_init_pop', default_value=log_init_pop)
        dpg.configure_item('log_capacity', default_value=log_capacity)
    else:
        raise ValueError
    # Updating plot
    dpg.set_value('log_pop_line', [t_values, solution])
    dpg.configure_item('log_capacity_line', default_value=log_capacity)
    dpg.configure_item('log_init_pop_line', default_value=log_init_pop)


def drag_line(param):
    """
    param ∈ ['log_capacity', 'log_init_pop']
    """
    global log_capacity, log_init_pop
    value = round(dpg.get_value(param + '_line'), 3)
    match param:
        case 'log_capacity':
            if value >= LOG_CAPACITY_MAX:           log_capacity = LOG_CAPACITY_MAX
            elif value <= LOG_CAPACITY_MIN:         log_capacity = LOG_CAPACITY_MIN
            else:                                   log_capacity = value
        case 'log_init_pop':
            if value >= LOG_INIT_POP_MAX:           log_init_pop = LOG_INIT_POP_MAX
            elif value <= LOG_INIT_POP_MIN:         log_init_pop = LOG_INIT_POP_MIN
            else:                                   log_init_pop = value
    dpg.configure_item(param, default_value=globals()[param])
    update(param)


class Window():
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Logistic'):
            dpg.add_slider_double(tag='log_growth_speed',
                                      min_value=LOG_GROWTH_SPEED_MIN, max_value=LOG_GROWTH_SPEED_MAX, default_value=log_growth_speed,
                                      width=200, label='Growth speed',
                                      callback=lambda: update('log_growth_speed'))
            dpg.add_slider_double(tag='log_init_pop',
                                  min_value=LOG_INIT_POP_MIN, max_value=LOG_INIT_POP_MAX, default_value=log_init_pop,
                                  width=200, label='Initial population',
                                  callback=lambda: update('log_init_pop'))
            dpg.add_slider_double(tag='log_capacity',
                                  min_value=LOG_CAPACITY_MIN, max_value=LOG_CAPACITY_MAX, default_value=log_capacity,
                                  width=200, label='Capacity',
                                  callback=lambda: update('log_capacity'))

            with dpg.plot(tag='log_main_plot',
                          width=dpg.get_viewport_width()-40,
                          height=dpg.get_viewport_height()-200,
                          equal_aspects=True):
                x = dpg.add_plot_axis(dpg.mvXAxis)
                y = dpg.add_plot_axis(dpg.mvYAxis)

                dpg.add_line_series(t_values, solution, parent=y, tag='log_pop_line')
                dpg.add_drag_line(tag='log_capacity_line',
                                  label='Capacity', vertical=False, color=[255, 255, 255, 100],
                                  default_value=log_capacity,
                                  callback=lambda: drag_line('log_capacity'))
                dpg.add_drag_line(tag='log_init_pop_line',
                                  label='Initial population', vertical=False, color=[0, 255, 0, 100],
                                  default_value=log_init_pop,
                                  callback=lambda: drag_line('log_init_pop'))
                