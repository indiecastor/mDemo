import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint
from constants import *
from typing import Literal

def model(eq: tuple, t: any) -> tuple:
    x, y = eq
    return [(pplv_alpha - pplv_beta * y) * x,
            (-pplv_gamma + pplv_delta * x) * y]

pplv_alpha   = round(random.uniform(PPLV_ALPHA_MIN, PPLV_ALPHA_MAX), 3)
pplv_beta    = round(random.uniform(PPLV_BETA_MIN, PPLV_BETA_MAX), 3)
pplv_gamma   = round(random.uniform(PPLV_GAMMA_MIN, PPLV_GAMMA_MAX), 3)
pplv_delta   = round(random.uniform(PPLV_DELTA_MIN, PPLV_DELTA_MAX), 3)

pplv_init_prey_pop = random.uniform(PPLV_INIT_PREY_POP_MIN, PPLV_INIT_PREY_POP_MAX)
pplv_init_pred_pop = random.uniform(PPLV_INIT_PREDATOR_POP_MIN, PPLV_INIT_PREDATOR_POP_MAX)

t_values = np.arange(0.1, 500, 0.1)
solution = odeint(model, (pplv_init_prey_pop, pplv_init_pred_pop), t_values)

def update(param: Literal['pplv_alpha', 'pplv_beta', 'pplv_gamma', 'pplv_delta',
                          'pplv_init_prey_pop', 'pplv_init_pred_pop', 'all']) -> None:
    global pplv_alpha, pplv_beta, pplv_gamma, pplv_delta, pplv_init_prey_pop, pplv_init_pred_pop, solution
    # Updating values of params
    match param:
        case 'pplv_alpha':         pplv_alpha = dpg.get_value('pplv_alpha')
        case 'pplv_beta':          pplv_beta = dpg.get_value('pplv_beta')
        case 'pplv_gamma':         pplv_gamma = dpg.get_value('pplv_gamma')
        case 'pplv_delta':         pplv_delta = dpg.get_value('pplv_delta')
        case 'pplv_init_prey_pop': pplv_init_prey_pop = dpg.get_value('pplv_init_prey_pop')
        case 'pplv_init_pred_pop': pplv_init_pred_pop = dpg.get_value('pplv_init_pred_pop')
        case 'all': 
            pplv_alpha         = dpg.get_value('pplv_alpha')
            pplv_beta          = dpg.get_value('pplv_beta')
            pplv_gamma         = dpg.get_value('pplv_gamma')
            pplv_delta         = dpg.get_value('pplv_delta')
            pplv_init_prey_pop = dpg.get_value('pplv_init_prey_pop')
            pplv_init_pred_pop = dpg.get_value('pplv_init_pred_pop')
        case _: raise ValueError('Unknown Parameter!')
    # Re-calculating solution
    solution = odeint(model, (pplv_init_prey_pop, pplv_init_pred_pop), t_values)
    # Updating plot
    dpg.set_value('prey_line', [t_values, solution[: ,0].tolist()])
    dpg.set_value('pred_line', [t_values, solution[: ,1].tolist()])
    dpg.set_value('phase_line', [solution[: ,0].tolist(), solution[: ,1].tolist()])

def randomize() -> None:
    global pplv_alpha, pplv_beta, pplv_gamma, pplv_delta, pplv_init_prey_pop, pplv_init_pred_pop

    pplv_alpha = round(random.uniform(PPLV_ALPHA_MIN, PPLV_ALPHA_MAX), 3)
    pplv_beta  = round(random.uniform(PPLV_BETA_MIN, PPLV_BETA_MAX), 3)
    pplv_gamma = round(random.uniform(PPLV_GAMMA_MIN, PPLV_GAMMA_MAX), 3)
    pplv_delta = round(random.uniform(PPLV_DELTA_MIN, PPLV_DELTA_MAX), 3)

    pplv_init_prey_pop = round(random.uniform(PPLV_INIT_PREY_POP_MIN, PPLV_INIT_PREY_POP_MAX), 3)
    pplv_init_pred_pop = round(random.uniform(PPLV_INIT_PREDATOR_POP_MIN, PPLV_INIT_PREDATOR_POP_MAX), 3)

    dpg.configure_item('pplv_alpha', default_value=pplv_alpha)
    dpg.configure_item('pplv_beta', default_value=pplv_beta)
    dpg.configure_item('pplv_gamma', default_value=pplv_gamma)
    dpg.configure_item('pplv_delta', default_value=pplv_delta)

    dpg.configure_item('pplv_init_prey_pop', default_value=pplv_init_prey_pop)
    dpg.configure_item('pplv_init_pred_pop', default_value=pplv_init_pred_pop)

    update('all')


class Window():
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Predator-Prey Lotka-Volterra'):
            dpg.add_slider_double(tag='pplv_alpha',
                                    min_value=0.1, max_value=2.0, default_value=pplv_alpha,
                                    width=200, label='Alpha: Prey growth speed',
                                    callback=lambda: update('pplv_alpha'))
            dpg.add_slider_double(tag='pplv_beta',
                                    min_value=0.1, max_value=2.0, default_value=pplv_beta,
                                    width=200, label='Beta: Prey death speed',
                                    callback=lambda: update('pplv_beta'))
            dpg.add_slider_double(tag='pplv_gamma',
                                    min_value=0.1, max_value=2.0, default_value=pplv_gamma,
                                    width=200, label='Gamma: Predator growth speed',
                                    callback=lambda: update('pplv_gamma'))
            dpg.add_slider_double(tag='pplv_delta',
                                    min_value=0.1, max_value=2.0, default_value=pplv_delta,
                                    width=200, label='Delta: Predator death speed',
                                    callback=lambda: update('pplv_delta'))

            dpg.add_slider_double(tag='pplv_init_prey_pop',
                                    min_value=0.1, max_value=10.0, default_value=pplv_init_prey_pop,
                                    width=200, label='Initial prey population',
                                    callback=lambda: update('pplv_init_prey_pop'))
            dpg.add_slider_double(tag='pplv_init_pred_pop',
                                    min_value=0.1, max_value=10.0, default_value=pplv_init_pred_pop,
                                    width=200, label='Initial predator population',
                                    callback=lambda: update('pplv_init_pred_pop'))

            dpg.add_button(label='Randomize!', callback=randomize)

            dpg.add_group(tag='plots_group', horizontal=True)
            with dpg.plot(parent='plots_group', tag='lv_main_plot',
                            width=(dpg.get_viewport_width()-40)/2, height=dpg.get_viewport_height() - 240, equal_aspects=True): # MAIN PLOT
                x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')

                dpg.add_plot_legend()

                dpg.add_line_series(t_values, solution[: ,0].tolist(), parent=y, label='Prey', tag='prey_line')
                dpg.add_line_series(t_values, solution[: ,1].tolist(), parent=y, label='Predator', tag='pred_line')
            
            with dpg.plot(parent='plots_group', tag='lv_phase_diagram',
                            width=(dpg.get_viewport_width()-40)/2, height=dpg.get_viewport_height() - 240, equal_aspects=True): # PHASE DIAGRAM
                x = dpg.add_plot_axis(dpg.mvXAxis, label='Prey population')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='Predator population')

                dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='phase_line')