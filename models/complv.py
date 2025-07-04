import dearpygui.dearpygui as dpg
import numpy as np
from scipy.integrate import odeint
from constants import *
from gui.indents import *


def model(eq: tuple, t: any) -> tuple:
    global complv_alphas, complv_growth_rates, complv_capacities
    x1, x2 = eq
    return [
        complv_growth_rates[0] * x1 * (1 - ((x1 + (complv_alphas[0] * x2))/complv_capacities[0])),
        complv_growth_rates[1] * x2 * (1 - ((x2 + (complv_alphas[1] * x1))/complv_capacities[1])),
        ]


complv_total_species      = 2
complv_alphas             = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX, 2) # 0 - a21; 1 - a12
complv_growth_rates       = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX, 2)
complv_capacities         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX, 2)
complv_init_pops          = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX, 2)

t_values = np.arange(0.1, 50, 0.01)
solution = odeint(model, complv_init_pops, t_values)

def update(param: str, species: int):
    """
    param ∈ ['complv_alpha', 'complv_growth_rate', 'complv_capacity', 'complv_init_pop', 'all']  
    species ∈ [0, 1]
    """
    global complv_alphas, complv_growth_rates, complv_capacities, complv_init_pops, solution
    # Updating params
    match param:
        case 'complv_alpha':         complv_alphas[species]       = dpg.get_value(f'complv_alpha_{species}')
        case 'complv_growth_rate':   complv_growth_rates[species] = dpg.get_value(f'complv_growth_rate_{species}')
        case 'complv_capacity':      complv_capacities[species]   = dpg.get_value(f'complv_capacity_{species}')
        case 'complv_init_pop':      complv_init_pops[species]    = dpg.get_value(f'complv_init_pop_{species}')
        case 'all':
            complv_alphas[species]       = dpg.get_value(f'complv_alpha_{species}')
            complv_growth_rates[species] = dpg.get_value(f'complv_growth_rate_{species}')
            complv_capacities[species]   = dpg.get_value(f'complv_capacity_{species}')
            complv_init_pops[species]    = dpg.get_value(f'complv_init_pop_{species}')
    # Re-calculating solution
    solution = odeint(model, complv_init_pops, t_values)
    # Updating plot
    dpg.set_value('complv_pop_line_0', [t_values, solution[:, 0].tolist()])
    dpg.set_value('complv_pop_line_1', [t_values, solution[:, 1].tolist()])
    dpg.set_value('complv_phase_line', [solution[:, 0].tolist(), solution[:, 1].tolist()])

def update_sliders() -> None:
    dpg.set_value('complv_alpha_0', complv_alphas[0])
    dpg.set_value('complv_alpha_1', complv_alphas[1])
    dpg.set_value('complv_growth_rate_0', complv_growth_rates[0])
    dpg.set_value('complv_growth_rate_1', complv_growth_rates[1])
    dpg.set_value('complv_capacity_0', complv_capacities[0])
    dpg.set_value('complv_capacity_1', complv_capacities[1])
    dpg.set_value('complv_init_pop_0', complv_init_pops[0])
    dpg.set_value('complv_init_pop_1', complv_init_pops[1])

def update_plots() -> None:
    dpg.set_value('complv_pop_line_0', [t_values, solution[: ,0].tolist()])
    dpg.set_value('complv_pop_line_1', [t_values, solution[: ,1].tolist()])
    dpg.set_value('complv_phase_line', [solution[: ,0].tolist(), solution[: ,1].tolist()])

def randomize() -> None:
    global complv_alphas, complv_growth_rates, complv_capacities, complv_init_pops, solution
    complv_alphas             = np.random.uniform(COMPLV_A_MIN, COMPLV_A_MAX, 2) # 0 - a21; 1 - a12
    complv_growth_rates       = np.random.uniform(COMPLV_GR_MIN, COMPLV_GR_MAX, 2)
    complv_capacities         = np.random.uniform(COMPLV_CAP_MIN, COMPLV_CAP_MAX, 2)
    complv_init_pops          = np.random.uniform(COMPLV_IP_MIN, COMPLV_IP_MAX, 2)
    update_sliders()
    solution = odeint(model, complv_init_pops, t_values)
    update_plots()


def zero_out() -> None:
    global complv_alphas, complv_growth_rates, complv_capacities, complv_init_pops, solution
    complv_alphas             = (COMPLV_A_MIN, COMPLV_A_MIN)
    complv_growth_rates       = (COMPLV_GR_MIN, COMPLV_GR_MIN)
    complv_capacities         = (COMPLV_CAP_MIN, COMPLV_CAP_MIN)
    complv_init_pops          = (COMPLV_IP_MIN, COMPLV_IP_MIN)
    update_sliders()
    solution = odeint(model, complv_init_pops, t_values)
    update_plots()

class Window:
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Competitive Lotka-Volterra'):
            
            with dpg.group(horizontal=True): # SLIDERS
                # SPECIES 1
                with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_0'): # Species 1
                    dpg.add_text('Species 1')
                    dpg.add_slider_double(label='Alpha21', tag='complv_alpha_0',
                                          default_value=complv_alphas[0],
                                          min_value=COMPLV_A_MIN, max_value=COMPLV_A_MAX, 
                                          callback=lambda: update(param='complv_alpha', species=0)) # a21
                    dpg.add_slider_double(label='Initial population', tag='complv_init_pop_0',
                                          default_value=complv_init_pops[0],
                                          min_value=COMPLV_IP_MIN, max_value=COMPLV_IP_MAX,
                                          callback=lambda: update(param='complv_init_pop', species=0))
                    dpg.add_slider_double(label='Growth rate', tag='complv_growth_rate_0',
                                          default_value=complv_growth_rates[0],
                                          min_value=COMPLV_GR_MIN, max_value=COMPLV_GR_MAX,
                                          callback=lambda: update(param='complv_growth_rate', species=0))
                    dpg.add_slider_double(label='Capacity', tag='complv_capacity_0',
                                          default_value=complv_capacities[0],
                                          min_value=COMPLV_CAP_MIN, max_value=COMPLV_CAP_MAX,
                                          callback=lambda: update(param='complv_capacity', species=0))
                # SPECIES 2
                with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_1'): # Species 2
                    dpg.add_text('Species 2')
                    dpg.add_slider_double(label='Alpha12', tag='complv_alpha_1',
                                          default_value=complv_alphas[1],
                                          min_value=COMPLV_A_MIN, max_value=COMPLV_A_MAX, 
                                          callback=lambda: update(param='complv_alpha', species=1)) # a12
                    dpg.add_slider_double(label='Initial population', tag='complv_init_pop_1',
                                          default_value=complv_init_pops[1],
                                          min_value=COMPLV_IP_MIN, max_value=COMPLV_IP_MAX,
                                          callback=lambda: update(param='complv_init_pop', species=1))
                    dpg.add_slider_double(label='Growth rate', tag='complv_growth_rate_1',
                                          default_value=complv_growth_rates[1],
                                          min_value=COMPLV_GR_MIN, max_value=COMPLV_GR_MAX,
                                          callback=lambda: update(param='complv_growth_rate', species=1))
                    dpg.add_slider_double(label='Capacity', tag='complv_capacity_1',
                                          default_value=complv_capacities[1],
                                          min_value=COMPLV_CAP_MIN, max_value=COMPLV_CAP_MAX,
                                          callback=lambda: update(param='complv_capacity', species=1))
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
                dpg.add_line_series(t_values, solution[: ,0].tolist(), parent=y, tag='complv_pop_line_0', label='Species 1')
                dpg.add_line_series(t_values, solution[: ,1].tolist(), parent=y, tag='complv_pop_line_1', label='Species 2')
                dpg.add_plot_legend()
            with dpg.plot(equal_aspects=True,
                          width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R,
                          height=dpg.get_viewport_height()-COMPLV_BOTH_D,
                          parent='complv_plots_group', tag='complv_phase'):
                x = dpg.add_plot_axis(dpg.mvXAxis, label='Species 1 population')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='Species 2 population')
                dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='complv_phase_line')

                
                            
