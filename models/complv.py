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
complv_alphas             = np.random.uniform(COMPLV_ALPHA_MIN, COMPLV_ALPHA_MAX, 2) # 0 - a21; 1 - a12
complv_growth_rates       = np.random.uniform(COMPLV_GROWTH_RATE_MIN, COMPLV_GROWTH_RATE_MAX, 2)
complv_capacities         = np.random.uniform(COMPLV_CAPACITY_MIN, COMPLV_CAPACITY_MAX, 2)
complv_init_pops          = np.random.uniform(COMPLV_INIT_POP_MIN, COMPLV_INIT_POP_MAX, 2)

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


class Window:
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Конкурентная модель Лотки-Вольтерры'):
            
            with dpg.group(horizontal=True): # SLIDERS
                # SPECIES 1
                with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_0'): # Species 1
                    dpg.add_text('Вид #1')
                    dpg.add_slider_double(label='a21', tag='complv_alpha_0',
                                          default_value=complv_alphas[0],
                                          min_value=COMPLV_ALPHA_MIN, max_value=COMPLV_ALPHA_MAX, 
                                          callback=lambda: update(param='complv_alpha', species=0)) # a21
                    dpg.add_slider_double(label='Начальная численность', tag='complv_init_pop_0',
                                          default_value=complv_init_pops[0],
                                          min_value=COMPLV_INIT_POP_MIN, max_value=COMPLV_INIT_POP_MAX,
                                          callback=lambda: update(param='complv_init_pop', species=0))
                    dpg.add_slider_double(label='Скорость роста', tag='complv_growth_rate_0',
                                          default_value=complv_growth_rates[0],
                                          min_value=COMPLV_GROWTH_RATE_MIN, max_value=COMPLV_GROWTH_RATE_MAX,
                                          callback=lambda: update(param='complv_growth_rate', species=0))
                    dpg.add_slider_double(label='Ёмкость среды', tag='complv_capacity_0',
                                          default_value=complv_capacities[0],
                                          min_value=COMPLV_CAPACITY_MIN, max_value=COMPLV_CAPACITY_MAX,
                                          callback=lambda: update(param='complv_capacity', species=0))
                # SPECIES 2
                with dpg.group(width=dpg.get_viewport_width() / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R, tag='complv_sliders_1'): # Species 2
                    dpg.add_text('Вид #2')
                    dpg.add_slider_double(label='a12', tag='complv_alpha_1',
                                          default_value=complv_alphas[1],
                                          min_value=COMPLV_ALPHA_MIN, max_value=COMPLV_ALPHA_MAX, 
                                          callback=lambda: update(param='complv_alpha', species=1)) # a12
                    dpg.add_slider_double(label='Начальная численность', tag='complv_init_pop_1',
                                          default_value=complv_init_pops[1],
                                          min_value=COMPLV_INIT_POP_MIN, max_value=COMPLV_INIT_POP_MAX,
                                          callback=lambda: update(param='complv_init_pop', species=1))
                    dpg.add_slider_double(label='Скорость роста', tag='complv_growth_rate_1',
                                          default_value=complv_growth_rates[1],
                                          min_value=COMPLV_GROWTH_RATE_MIN, max_value=COMPLV_GROWTH_RATE_MAX,
                                          callback=lambda: update(param='complv_growth_rate', species=1))
                    dpg.add_slider_double(label='Ёмкость среды', tag='complv_capacity_1',
                                          default_value=complv_capacities[1],
                                          min_value=COMPLV_CAPACITY_MIN, max_value=COMPLV_CAPACITY_MAX,
                                          callback=lambda: update(param='complv_capacity', species=1))

            dpg.add_group(tag='complv_plots_group', horizontal=True)
            with dpg.plot(equal_aspects=True,
                          width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R,
                          height=dpg.get_viewport_height()-COMPLV_BOTH_D,
                          parent='complv_plots_group', tag='complv_plot'):
                x = dpg.add_plot_axis(dpg.mvXAxis, label='T, Время')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='P, Численность')
                dpg.add_line_series(t_values, solution[: ,0].tolist(), parent=y, tag='complv_pop_line_0', label='Вид #1')
                dpg.add_line_series(t_values, solution[: ,1].tolist(), parent=y, tag='complv_pop_line_1', label='Вид #2')
                dpg.add_plot_legend()
            with dpg.plot(equal_aspects=True,
                          width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R,
                          height=dpg.get_viewport_height()-COMPLV_BOTH_D,
                          parent='complv_plots_group', tag='complv_phase'):
                x = dpg.add_plot_axis(dpg.mvXAxis, label='Численность вида #1')
                y = dpg.add_plot_axis(dpg.mvYAxis, label='Численность вида #2')
                dpg.add_line_series(solution[: ,0].tolist(), solution[: ,1].tolist(), parent=y, tag='complv_phase_line')

                
                            
