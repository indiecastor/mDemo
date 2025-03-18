import dearpygui.dearpygui as dpg
import numpy as np
import random
from scipy.integrate import odeint

# TODO: rename variables (add model prefixes)

alpha: float = random.uniform(0.1, 2)
beta: float = random.uniform(0.1, 2)
gamma: float = random.uniform(0.1, 2)
delta: float = random.uniform(0.1, 2)

init_prey_pop: float = random.uniform(0.1, 2)
init_pred_pop: float = random.uniform(0.1, 2)

init_pops: tuple = (init_prey_pop, init_pred_pop)

t_values = np.arange(0.1, 500, 0.1)

def model(eq: tuple, t: any):
    x, y = eq
    return [(alpha - beta * y) * x,
            (-gamma + delta * x) * y]

solution = odeint(model, init_pops, t_values)


def set_random_defaults() -> tuple:
    global alpha, beta, gamma, delta, init_prey_pop, init_pred_pop

    alpha = random.uniform(0.1, 2)
    beta = random.uniform(0.1, 2)
    gamma = random.uniform(0.1, 2)
    delta = random.uniform(0.1, 2)

    init_prey_pop = random.uniform(0.1, 2)
    init_pred_pop = random.uniform(0.1, 2)

    return (alpha, beta, gamma, delta, init_prey_pop, init_pred_pop)

def update(param: str) -> None:
    global alpha, beta, gamma, delta, init_prey_pop, init_pred_pop, init_pops, solution

    # Updating values of params
    match param:
        case 'alpha':         alpha = dpg.get_value('alpha')
        case 'beta':          beta = dpg.get_value('beta')
        case 'gamma':         gamma = dpg.get_value('gamma')
        case 'delta':         delta = dpg.get_value('delta')
        case 'init_prey_pop':
            init_prey_pop = dpg.get_value('init_prey_pop')
            init_pops = (init_prey_pop, init_pred_pop)
        case 'init_pred_pop':
            init_pred_pop = dpg.get_value('init_pred_pop')
            init_pops = (init_prey_pop, init_pred_pop)
        case 'all': 
            alpha = dpg.get_value('alpha')
            beta = dpg.get_value('beta')
            gamma = dpg.get_value('gamma')
            delta = dpg.get_value('delta')
            init_prey_pop = dpg.get_value('init_prey_pop')
            init_pred_pop = dpg.get_value('init_pred_pop')
    
    # Printing debug message
    if param in ['alpha', 'beta', 'gamma', 'delta', 'init_prey_pop', 'init_pred_pop']:
        print(f'DEBUG: [LV] Param [{param}] set to {globals()[param]}')
    elif param == 'all':
        print('DEBUG: [LV] All params updated')
    else:
        print('DEBUG: [LV] Unknown param!')

    # Re-calculating solution
    solution = odeint(model, init_pops, t_values)
    
    # Updating plot
    dpg.set_value('prey_line', [t_values, solution[: ,0].tolist()])
    dpg.set_value('pred_line', [t_values, solution[: ,1].tolist()])
    dpg.set_value('phase_line', [solution[: ,0].tolist(), solution[: ,1].tolist()])

def randomize() -> None:
    set_random_defaults()

    dpg.configure_item('alpha', default_value=alpha)
    dpg.configure_item('beta', default_value=beta)
    dpg.configure_item('gamma', default_value=gamma)
    dpg.configure_item('delta', default_value=delta)

    dpg.configure_item('init_prey_pop', default_value=init_prey_pop)
    dpg.configure_item('init_pred_pop', default_value=init_pred_pop)

    update('all')







class Window():
    def __init__(self):
        with dpg.tab(parent='models_tabs', label='Lotka-Volterra Model'):
            with dpg.group():
                dpg.add_slider_double(tag='alpha',
                                      min_value=0.1, max_value=2.0, default_value=alpha,
                                      width=200, label='Alpha: Prey growth speed', callback=lambda: update('alpha'))
                dpg.add_slider_double(tag='beta',
                                      min_value=0.1, max_value=2.0, default_value=beta,
                                      width=200, label='Beta: Prey death speed', callback=lambda: update('beta'))
                dpg.add_slider_double(tag='gamma',
                                      min_value=0.1, max_value=2.0, default_value=gamma,
                                      width=200, label='Gamma: Predator growth speed', callback=lambda: update('gamma'))
                dpg.add_slider_double(tag='delta',
                                      min_value=0.1, max_value=2.0, default_value=delta,
                                      width=200, label='Delta: Predator death speed', callback=lambda: update('delta'))

                dpg.add_slider_double(tag='init_prey_pop',
                                      min_value=0.1, max_value=10.0, default_value=init_prey_pop,
                                      width=200, label='Initial prey population', callback=lambda: update('init_prey_pop'))
                dpg.add_slider_double(tag='init_pred_pop',
                                      min_value=0.1, max_value=10.0, default_value=init_pred_pop,
                                      width=200, label='Initial predator population', callback=lambda: update('init_pred_pop'))

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