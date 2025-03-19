import random
from typing import Literal

import dearpygui.dearpygui as dpg
import numpy as np
from scipy.integrate import odeint

from constants import *

def model(y, t: any) -> float: return malt_growth_speed * y

malt_growth_speed: float = random.uniform(MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX)
malt_init_pop: float = random.uniform(MALT_INIT_POP_MIN, MALT_INIT_POP_MAX)
t_values = np.arange(0, 2, .01)
solution = odeint(model, malt_init_pop, t_values)


def update(param: Literal['malt_growth_speed', 'malt_init_pop', 'all']) -> None:
    global malt_growth_speed, malt_init_pop, solution

    # Updating values of params
    # eggs
    match param:
        case 'malt_growth_speed':
            malt_growth_speed = dpg.get_value('malt_growth_speed')
        case 'malt_init_pop':
            malt_init_pop = dpg.get_value('malt_init_pop')
        case 'all':
            malt_growth_speed = dpg.get_value('malt_growth_speed')
            malt_init_pop = dpg.get_value('malt_init_pop')
    # Printing debug message
    if param in MALT_PARAMS:
        print(f'[MALT] PARAM UPDATED [{param}: {globals()[param]}]')
    elif param == 'all':
        print(f'[MALT] All params updated')
        print(f'       malt_growth_speed: {malt_growth_speed}')
        print(f'       malt_init_pop: {malt_init_pop}')
    else:
        print('[MALT] Unknown param!')
    # Re-calculating solution
    solution = odeint(model, malt_init_pop, t_values)
    # Updating plot
    dpg.set_value('malt_pop_line', [t_values, solution])
    dpg.set_value('malt_init_pop_line', malt_init_pop)


def drag_line():
    global malt_growth_speed, malt_init_pop
    value = round(dpg.get_value('malt_init_pop_line'), 3)
    if value >= MALT_INIT_POP_MAX:
        malt_init_pop = MALT_INIT_POP_MAX
    elif value <= MALT_INIT_POP_MIN:
        malt_init_pop = MALT_INIT_POP_MIN
    else:
        malt_init_pop = value
    dpg.configure_item('malt_init_pop', default_value=malt_init_pop)
    dpg.configure_item('malt_init_pop_line', default_value=malt_init_pop)
    update('malt_init_pop')
    


def randomize() -> None:
    _malt_growth_speed_temp: float = round(random.uniform(MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX), 3)
    _malt_init_pop_temp: float = round(random.uniform(MALT_INIT_POP_MIN, MALT_INIT_POP_MAX), 3)
    dpg.configure_item('malt_growth_speed', default_value=_malt_growth_speed_temp)
    dpg.configure_item('malt_init_pop', default_value=_malt_init_pop_temp)
    update('all')


class Window:
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Malthusian'):
            dpg.add_slider_double(tag='malt_growth_speed',
                                  min_value=MALT_GROWTH_SPEED_MIN, max_value=MALT_GROWTH_SPEED_MAX,
                                  default_value=malt_growth_speed,
                                  width=200, label='Growth speed',
                                  callback=lambda: update('malt_growth_speed'))
            dpg.add_slider_double(tag='malt_init_pop',
                                  min_value=MALT_INIT_POP_MIN, max_value=MALT_INIT_POP_MAX, default_value=malt_init_pop,
                                  width=200, label='Initial population',
                                  callback=lambda: update('malt_init_pop'))

            dpg.add_button(label='Randomize!', callback=randomize)

            with dpg.plot(tag='malt_main_plot',
                          width=dpg.get_viewport_width() - 40, height=dpg.get_viewport_height() - 150,
                          equal_aspects=True):
                x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')

                dpg.add_line_series(t_values, solution, parent=y, tag='malt_pop_line')
                dpg.add_drag_line(tag='malt_init_pop_line',
                                  label='Initial population', vertical=False, color=[0, 255, 0, 100],
                                  default_value=malt_init_pop,
                                  callback=drag_line)
