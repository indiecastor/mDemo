import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint
from constants import *

def model(eq: tuple, t: any) -> tuple:
    x, y = eq
    return [(pplv_alpha - pplv_beta * y) * x,
            (-pplv_gamma + pplv_delta * x) * y]

pplv_alpha   = round(random.uniform(PPLV_A_MIN, PPLV_A_MAX), 3)
pplv_beta    = round(random.uniform(PPLV_B_MIN, PPLV_B_MAX), 3)
pplv_gamma   = round(random.uniform(PPLV_G_MIN, PPLV_G_MAX), 3)
pplv_delta   = round(random.uniform(PPLV_D_MIN, PPLV_D_MAX), 3)

pplv_init_prey_pop = random.uniform(PPLV_IP_PREY_MIN, PPLV_IP_PREY_MAX)
pplv_init_pred_pop = random.uniform(PPLV_IP_PRED_MIN, PPLV_IP_PRED_MAX)

T_VALUES = np.arange(0.1, 500, 0.1)
solution = odeint(model, (pplv_init_prey_pop, pplv_init_pred_pop), T_VALUES)


def update_solution() -> None:
    global solution
    solution = odeint(model, (pplv_init_prey_pop, pplv_init_pred_pop), T_VALUES)


def update_sliders():
    for slider in PPLV_SLIDERS:
        dpg.set_value(slider, globals()[slider])


def update_plots():
    dpg.set_value('pplv_prey_line', [T_VALUES, solution[: ,0].tolist()])
    dpg.set_value('pplv_pred_line', [T_VALUES, solution[: ,1].tolist()])
    dpg.set_value('pplv_phase_line', [solution[: ,0].tolist(), solution[: ,1].tolist()])


def update_param(sender, app_data) -> None:
    globals()[sender] = app_data
    update_solution()
    update_sliders()
    update_plots()


def randomize() -> None:
    global pplv_alpha, pplv_beta, pplv_delta, pplv_gamma, pplv_init_pred_pop, pplv_init_prey_pop, solution
    pplv_alpha = random.uniform(PPLV_A_MIN, PPLV_A_MAX)
    pplv_beta  = random.uniform(PPLV_B_MIN, PPLV_B_MAX)
    pplv_delta = random.uniform(PPLV_D_MIN, PPLV_D_MAX)
    pplv_gamma = random.uniform(PPLV_G_MIN, PPLV_G_MAX)
    pplv_init_prey_pop = random.uniform(PPLV_IP_PREY_MIN, PPLV_IP_PREY_MAX)
    pplv_init_pred_pop = random.uniform(PPLV_IP_PRED_MIN, PPLV_IP_PRED_MAX)
    update_solution()
    update_sliders()
    update_plots()


def zero_out() -> None:
    global pplv_alpha, pplv_beta, pplv_delta, pplv_gamma, pplv_init_pred_pop, pplv_init_prey_pop, solution
    pplv_alpha = PPLV_A_MIN
    pplv_beta  = PPLV_B_MIN
    pplv_delta = PPLV_D_MIN
    pplv_gamma = PPLV_G_MIN
    pplv_init_prey_pop = PPLV_IP_PREY_MIN
    pplv_init_pred_pop = PPLV_IP_PRED_MIN
    update_solution()
    update_sliders()
    update_plots()


def window() -> None:
    with dpg.tab(parent='models_tabs', label='Predator-Prey Lotka-Volterra'):
        dpg.add_slider_double(tag='pplv_alpha',
                                min_value=0.1, max_value=2.0, default_value=pplv_alpha,
                                width=200, label='Alpha: Prey growth speed',
                                callback=update_param)
        dpg.add_slider_double(tag='pplv_beta',
                                min_value=0.1, max_value=2.0, default_value=pplv_beta,
                                width=200, label='Beta: Prey death speed',
                                callback=update_param)
        dpg.add_slider_double(tag='pplv_gamma',
                                min_value=0.1, max_value=2.0, default_value=pplv_gamma,
                                width=200, label='Gamma: Predator growth speed',
                                callback=update_param)
        dpg.add_slider_double(tag='pplv_delta',
                                min_value=0.1, max_value=2.0, default_value=pplv_delta,
                                width=200, label='Delta: Predator death speed',
                                callback=update_param)

        dpg.add_slider_double(tag='pplv_init_prey_pop',
                                min_value=0.1, max_value=10.0, default_value=pplv_init_prey_pop,
                                width=200, label='Initial prey population',
                                callback=update_param)
        dpg.add_slider_double(tag='pplv_init_pred_pop',
                                min_value=0.1, max_value=10.0, default_value=pplv_init_pred_pop,
                                width=200, label='Initial predator population',
                                callback=update_param)
        with dpg.group(horizontal=True): 
            dpg.add_button(label='Randomize', callback=randomize)
            dpg.add_button(label='Zero out', callback=zero_out)
        dpg.add_group(tag='plots_group', horizontal=True)
        with dpg.plot(parent='plots_group', tag='lv_main_plot',
                        width=(dpg.get_viewport_width()-40)/2,
                        height=dpg.get_viewport_height() - 240, equal_aspects=True): # MAIN PLOT
            x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
            y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')

            dpg.add_line_series(T_VALUES, solution[: ,0].tolist(), parent=y, label='Prey', tag='pplv_prey_line')
            dpg.add_line_series(T_VALUES, solution[: ,1].tolist(), parent=y, label='Predator', tag='pplv_pred_line')
            dpg.add_plot_legend()
        
        with dpg.plot(parent='plots_group', tag='lv_phase_diagram',
                        width=(dpg.get_viewport_width()-40)/2,
                        height=dpg.get_viewport_height() - 240, equal_aspects=True): # PHASE DIAGRAM
            x = dpg.add_plot_axis(dpg.mvXAxis, label='Prey population')
            y = dpg.add_plot_axis(dpg.mvYAxis, label='Predator population')

            dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='pplv_phase_line')