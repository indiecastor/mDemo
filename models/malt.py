import random

import dearpygui.dearpygui as dpg
import numpy as np
from scipy.integrate import odeint

from constants import *

def model(y, t: any) -> float: return malt_growth_speed * y

malt_growth_speed: float = random.uniform(MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX)
malt_init_pop: float     = random.uniform(MALT_INIT_POP_MIN, MALT_INIT_POP_MAX)

t_values = np.arange(0, 2, .01)
solution = odeint(model, malt_init_pop, t_values)


def update(param) -> None:
    """ param ∈ ['malt_growth_speed', 'malt_init_pop', 'all'] """
    global malt_growth_speed, malt_init_pop, solution
    # Updating values of params
    match param:
        case 'malt_growth_speed': malt_growth_speed = dpg.get_value('malt_growth_speed')
        case 'malt_init_pop':     malt_init_pop = dpg.get_value('malt_init_pop')
        case 'all':
            malt_growth_speed = dpg.get_value('malt_growth_speed')
            malt_init_pop = dpg.get_value('malt_init_pop')
    # Re-calculating solution
    solution = odeint(model, malt_init_pop, t_values)
    # Updating sliders
    dpg.configure_item('malt_init_pop', default_value=malt_init_pop)
    dpg.configure_item('malt_init_pop_line', default_value=malt_init_pop)
    # Updating plot
    dpg.set_value('malt_pop_line', [t_values, solution])
    dpg.set_value('malt_init_pop_line', malt_init_pop)


def drag_line():
    global malt_growth_speed, malt_init_pop
    
    value = round(dpg.get_value('malt_init_pop_line'), 3)
    if value >= MALT_INIT_POP_MAX:        malt_init_pop = MALT_INIT_POP_MAX
    elif value <= MALT_INIT_POP_MIN:      malt_init_pop = MALT_INIT_POP_MIN
    else:
        malt_init_pop = value
        dpg.configure_item('malt_init_pop', default_value=value)

    update('malt_init_pop')


class Window:
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Модель Мальтуса'):
            dpg.add_slider_double(tag='malt_growth_speed',
                                  min_value=MALT_GROWTH_SPEED_MIN, max_value=MALT_GROWTH_SPEED_MAX,
                                  default_value=malt_growth_speed,
                                  width=200, label='Скорость роста',
                                  callback=lambda: update('malt_growth_speed'))
            dpg.add_slider_double(tag='malt_init_pop',
                                  min_value=MALT_INIT_POP_MIN, max_value=MALT_INIT_POP_MAX, default_value=malt_init_pop,
                                  width=200, label='Начальная численность',
                                  callback=lambda: update('malt_init_pop'))

            with dpg.plot(tag='malt_main_plot',
                          width=dpg.get_viewport_width() - 40, height=dpg.get_viewport_height() - 150,
                          equal_aspects=True):
                x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Время')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Численность')

                dpg.add_line_series(t_values, solution, parent=y, tag='malt_pop_line')
                dpg.add_drag_line(tag='malt_init_pop_line',
                                  label='Начальная численность', vertical=False, color=[0, 255, 0, 100],
                                  default_value=malt_init_pop,
                                  callback=drag_line)
