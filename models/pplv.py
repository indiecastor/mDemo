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

t_values = np.arange(0.1, 500, 0.1)
solution = odeint(model, (pplv_init_prey_pop, pplv_init_pred_pop), t_values)

def update(param: str) -> None:
    """
    param ∈ ['pplv_alpha', 'pplv_beta', 'pplv_gamma', 'pplv_delta', 'pplv_init_prey_pop', 'pplv_init_pred_pop', 'all']
    """
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

            dpg.add_group(tag='plots_group', horizontal=True)
            with dpg.plot(parent='plots_group', tag='lv_main_plot',
                            width=(dpg.get_viewport_width()-40)/2,
                            height=dpg.get_viewport_height() - 240, equal_aspects=True): # MAIN PLOT
                x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Time')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Population')

                dpg.add_line_series(t_values, solution[: ,0].tolist(), parent=y, label='Prey', tag='prey_line')
                dpg.add_line_series(t_values, solution[: ,1].tolist(), parent=y, label='Predator', tag='pred_line')
                dpg.add_plot_legend()
            
            with dpg.plot(parent='plots_group', tag='lv_phase_diagram',
                            width=(dpg.get_viewport_width()-40)/2,
                            height=dpg.get_viewport_height() - 240, equal_aspects=True): # PHASE DIAGRAM
                x = dpg.add_plot_axis(dpg.mvXAxis, label='Prey population')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='Predator population')

                dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='phase_line')