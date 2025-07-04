import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint
from constants import *

def model(y: float, t: any): return log_growth_speed * y * (1 - (y / log_capacity))

log_growth_speed  = round(random.uniform(L_GR_MIN, L_GR_MAX), 3)
log_init_pop      = round(random.uniform(L_IP_MIN, L_IP_MAX), 3)
log_capacity      = round(random.uniform(L_C_MIN, L_C_MAX), 3)

t_values = np.arange(0.0, 100.0, 0.1)
solution = odeint(model, log_init_pop, t_values)

def update(param) -> None:
    """ param ∈ ['log_growth_speed', 'log_init_pop', 'log_capacity', 'all'] """
    global log_growth_speed, log_init_pop, log_capacity, solution
    match param:
        case 'log_growth_speed': log_growth_speed = dpg.get_value('log_growth_speed')
        case 'log_init_pop':    log_init_pop = dpg.get_value('log_init_pop')
        case 'log_capacity':    log_capacity = dpg.get_value('log_capacity')
        case 'all':
            log_growth_speed = dpg.get_value('log_growth_speed')
            log_init_pop = dpg.get_value('log_init_pop')
            log_capacity = dpg.get_value('log_capacity')
        case _: raise ValueError
    solution = odeint(model, log_init_pop, t_values)
    if param in LOG_PARAMS:
        dpg.configure_item(param, default_value=globals()[param])
    elif param == 'all':
        dpg.configure_item('log_growth_speed', default_value=log_growth_speed)
        dpg.configure_item('log_init_pop', default_value=log_init_pop)
        dpg.configure_item('log_capacity', default_value=log_capacity)
    else:
        raise ValueError
    dpg.set_value('log_pop_line', [t_values, solution])
    dpg.configure_item('log_capacity_line', default_value=log_capacity)
    dpg.configure_item('log_init_pop_line', default_value=log_init_pop)


def drag_line(param):
    """
    param ∈ ['log_capacity', 'log_init_pop']
    """
    global log_capacity, log_init_pop
    value = dpg.get_value(f'{param}_line')
    match param:
        case 'log_capacity':
            if value >= L_C_MAX:    
                log_capacity = L_C_MAX
            elif value <= L_C_MIN:      
                log_capacity = L_C_MIN
            else:                                 
                log_capacity = value
        case 'log_init_pop':
            if value >= L_IP_MAX:
                 log_init_pop = L_IP_MAX
            elif value <= L_IP_MIN:
                log_init_pop = L_IP_MIN
            else: 
                 log_init_pop = value
    dpg.configure_item(param, default_value=globals()[param])
    update(param)

def randomize() -> None:
    global log_capacity, log_growth_speed, log_init_pop, solution
    log_capacity = round(random.uniform(L_C_MIN, L_C_MAX), 3)
    log_growth_speed = round(random.uniform(L_GR_MIN, L_GR_MAX), 3)
    log_init_pop = round(random.uniform(L_IP_MIN, L_IP_MAX))
    solution = odeint(model, log_init_pop, t_values)
    dpg.set_value('log_growth_speed', log_growth_speed)
    dpg.set_value('log_init_pop', log_init_pop)
    dpg.set_value('log_capacity', log_capacity)
    dpg.set_value('log_init_pop_line', log_init_pop)
    dpg.set_value('log_capacity_line', log_capacity)
    dpg.set_value('log_pop_line', [t_values, solution])

def zero_out() -> None:
    global log_capacity, log_growth_speed, log_init_pop, solution
    log_capacity = L_C_MIN
    log_growth_speed = L_GR_MIN
    log_init_pop = L_IP_MIN
    solution = odeint(model, log_init_pop, t_values)
    dpg.set_value('log_growth_speed', log_growth_speed)
    dpg.set_value('log_init_pop', log_init_pop)
    dpg.set_value('log_capacity', log_capacity)
    dpg.set_value('log_init_pop_line', log_init_pop)
    dpg.set_value('log_capacity_line', log_capacity)
    dpg.set_value('log_pop_line', [t_values, solution])

class Window():
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Logistic'):
            dpg.add_slider_double(tag='log_growth_speed',
                                      min_value=L_GR_MIN, max_value=L_GR_MAX, default_value=log_growth_speed,
                                      width=200, label='Growth speed',
                                      callback=lambda: update('log_growth_speed'))
            dpg.add_slider_double(tag='log_init_pop',
                                  min_value=L_IP_MIN, max_value=L_IP_MAX, default_value=log_init_pop,
                                  width=200, label='Initial population',
                                  callback=lambda: update('log_init_pop'))
            dpg.add_slider_double(tag='log_capacity',
                                  min_value=L_C_MIN, max_value=L_C_MAX, default_value=log_capacity,
                                  width=200, label='Capacity',
                                  callback=lambda: update('log_capacity'))

            with dpg.group(horizontal=True):
                dpg.add_button(label='Randomize!', callback=randomize)
                dpg.add_button(label='Zero out!', callback=zero_out)

            with dpg.plot(tag='log_main_plot',
                          width=dpg.get_viewport_width()-40,
                          height=dpg.get_viewport_height()-200,
                          equal_aspects=True):
                x = dpg.add_plot_axis(dpg.mvXAxis)
                y = dpg.add_plot_axis(dpg.mvYAxis)

                dpg.add_line_series(t_values, solution, parent=y, tag='log_pop_line')
                dpg.add_drag_line(tag='log_capacity_line',
                                  label='Capacity', vertical=False, color=[255, 0, 0, 100],
                                  default_value=log_capacity,
                                  callback=lambda: drag_line('log_capacity'))
                dpg.add_drag_line(tag='log_init_pop_line',
                                  label='Initial population', vertical=False, color=[0, 255, 0, 100],
                                  default_value=log_init_pop,
                                  callback=lambda: drag_line('log_init_pop'))
                