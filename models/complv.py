import dearpygui.dearpygui as dpg
import numpy as np
from scipy.integrate import odeint
from constants import *
from gui.indents import *


def model(eq: tuple, t: any) -> tuple:
    x1, x2 = eq
    return [
        complv_growth_rate_0 * x1 * (1 - ((x1 + (complv_alpha_0 * x2))/complv_capacity_0)),
        complv_growth_rate_1 * x2 * (1 - ((x2 + (complv_alpha_1 * x1))/complv_capacity_1)),
        ]


complv_alpha_0            = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX)
complv_alpha_1            = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX)
complv_growth_rate_0      = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX)
complv_growth_rate_1      = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX)
complv_capacity_0         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX)
complv_capacity_1         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX)
complv_init_pop_0         = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX)
complv_init_pop_1         = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX)

T_VALUES = np.arange(0.1, 50, 0.01)
solution = odeint(model, (complv_init_pop_0, complv_init_pop_1), T_VALUES)

def update_solution() -> None:
    global solution
    solution = odeint(model, (complv_init_pop_0, complv_init_pop_1), T_VALUES)

def update_sliders() -> None:
    for slider in COMPLV_SLIDERS: dpg.set_value(slider, globals()[slider])


def update_plots() -> None:
    dpg.set_value('complv_pop_line_0', [T_VALUES, solution[: ,0].tolist()])
    dpg.set_value('complv_pop_line_1', [T_VALUES, solution[: ,1].tolist()])
    dpg.set_value('complv_phase_line', [solution[: ,0].tolist(), solution[: ,1].tolist()])


def update_param(sender, app_data) -> None:
    globals()[sender] = app_data
    update_solution()
    update_sliders()
    update_plots()


def randomize() -> None:
    global complv_alpha_0, complv_alpha_1
    global complv_growth_rate_0, complv_growth_rate_1
    global complv_capacity_0, complv_capacity_1
    global complv_init_pop_0, complv_init_pop_1
    complv_alpha_0            = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX)
    complv_alpha_1            = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX)
    complv_growth_rate_0      = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX)
    complv_growth_rate_1      = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX)
    complv_capacity_0         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX)
    complv_capacity_1         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX)
    complv_init_pop_0         = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX)
    complv_init_pop_1         = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX)
    update_sliders()
    update_solution()
    update_plots()


def zero_out() -> None:
    global complv_alpha_0, complv_alpha_1
    global complv_growth_rate_0, complv_growth_rate_1
    global complv_capacity_0, complv_capacity_1
    global complv_init_pop_0, complv_init_pop_1
    complv_alpha_0, complv_alpha_1 = COMPLV_A_MIN, COMPLV_A_MIN
    complv_growth_rate_0, complv_growth_rate_1 = COMPLV_GR_MIN, COMPLV_GR_MIN
    complv_capacity_0, complv_capacity_1 = COMPLV_CAP_MIN, COMPLV_CAP_MIN
    complv_init_pop_0, complv_init_pop_1 = COMPLV_IP_MIN, COMPLV_IP_MIN
    update_sliders()
    update_solution()
    update_plots()

def window() -> None:
    with dpg.tab(parent='models_tabs', label='Competitive Lotka-Volterra'):
        
        with dpg.group(horizontal=True): # SLIDERS
            # SPECIES 1
            with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_0'): # Species 1
                dpg.add_text('Species 1')
                dpg.add_slider_double(label='Alpha21', tag='complv_alpha_0',
                                        default_value=complv_alpha_0,
                                        min_value=COMPLV_A_MIN, max_value=COMPLV_A_MAX, 
                                        callback=update_param) # a21
                dpg.add_slider_double(label='Initial population', tag='complv_init_pop_0',
                                        default_value=complv_init_pop_0,
                                        min_value=COMPLV_IP_MIN, max_value=COMPLV_IP_MAX,
                                        callback=update_param)
                dpg.add_slider_double(label='Growth rate', tag='complv_growth_rate_0',
                                        default_value=complv_growth_rate_0,
                                        min_value=COMPLV_GR_MIN, max_value=COMPLV_GR_MAX,
                                        callback=update_param)
                dpg.add_slider_double(label='Capacity', tag='complv_capacity_0',
                                        default_value=complv_capacity_0,
                                        min_value=COMPLV_CAP_MIN, max_value=COMPLV_CAP_MAX,
                                        callback=update_param)
            # SPECIES 2
            with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_1'): # Species 2
                dpg.add_text('Species 2')
                dpg.add_slider_double(label='Alpha12', tag='complv_alpha_1',
                                        default_value=complv_alpha_1,
                                        min_value=COMPLV_A_MIN, max_value=COMPLV_A_MAX, 
                                        callback=update_param) # a12
                dpg.add_slider_double(label='Initial population', tag='complv_init_pop_1',
                                        default_value=complv_init_pop_1,
                                        min_value=COMPLV_IP_MIN, max_value=COMPLV_IP_MAX,
                                        callback=update_param)
                dpg.add_slider_double(label='Growth rate', tag='complv_growth_rate_1',
                                        default_value=complv_growth_rate_1,
                                        min_value=COMPLV_GR_MIN, max_value=COMPLV_GR_MAX,
                                        callback=update_param)
                dpg.add_slider_double(label='Capacity', tag='complv_capacity_1',
                                        default_value=complv_capacity_1,
                                        min_value=COMPLV_CAP_MIN, max_value=COMPLV_CAP_MAX,
                                        callback=update_param)
        # Randomize & Zero out buttons
        with dpg.group(horizontal=True):
            dpg.add_button(label='Ranzdomize', callback=randomize)
            dpg.add_button(label='Zero out', callback=zero_out)

        dpg.add_group(tag='complv_plots_group', horizontal=True)
        with dpg.plot(equal_aspects=True,
                        width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R,
                        height=dpg.get_viewport_height()-COMPLV_BOTH_D,
                        parent='complv_plots_group', tag='complv_plot'):
            x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
            y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')
            dpg.add_line_series(T_VALUES, solution[: ,0].tolist(), parent=y, tag='complv_pop_line_0', label='Species 1')
            dpg.add_line_series(T_VALUES, solution[: ,1].tolist(), parent=y, tag='complv_pop_line_1', label='Species 2')
            dpg.add_plot_legend()
        with dpg.plot(equal_aspects=True,
                        width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R,
                        height=dpg.get_viewport_height()-COMPLV_BOTH_D,
                        parent='complv_plots_group', tag='complv_phase'):
            x = dpg.add_plot_axis(dpg.mvXAxis, label='Species 1 population')
            y = dpg.add_plot_axis(dpg.mvYAxis, label='Species 2 population')
            dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='complv_phase_line')