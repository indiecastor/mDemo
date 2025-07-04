MALT_GR_MIN, MALT_GR_MAX  = 0.01, 10.0 # Growth rate
MALT_IP_MIN, MALT_IP_MAX  = 0.01, 10.0 # Initial population

L_GR_MIN, L_GR_MAX = 0.01, 10.0 # Growth rate
L_IP_MIN, L_IP_MAX = 0.1, 20.0  # initial population
L_C_MIN,  L_C_MAX  = 0.1, 10.0  # Capacity
  
PPLV_A_MIN, PPLV_A_MAX  = 0.1, 2 # Alpha
PPLV_B_MIN,  PPLV_B_MAX = 0.1, 2 # Beta
PPLV_G_MIN, PPLV_G_MAX  = 0.1, 2 # Gamma
PPLV_D_MIN, PPLV_D_MAX  = 0.1, 2 # Delta

PPLV_IP_PREY_MIN, PPLV_IP_PREY_MAX = 0.1, 2 # Initial PREY population
PPLV_IP_PRED_MIN, PPLV_IP_PRED_MAX = 0.1, 2 # Initial PREDATOR population

COMPLV_GR_MIN, COMPLV_GR_MAX   = 0.1, 0.9 # Growth rate
COMPLV_A_MIN, COMPLV_A_MAX     = 0.1, 0.9 # Alpha
COMPLV_CAP_MIN, COMPLV_CAP_MAX = 10.0, 100.0 # Capacity
COMPLV_IP_MIN, COMPLV_IP_MAX   = 10.0, 100.0 # Initial population

# Parameter lists do not include 'all' parameter!
LOG_PARAMS:  list[str]   = ['log_growth_speed', 'log_init_pop', 'log_capacity']
MALT_PARAMS: list[str]   = ['malt_growth_speed', 'malt_init_pop']
PPLV_PARAMS: list[str]   = ['pplv_alpha', 'pplv_beta', 'pplv_gamma', 'pplv_delta', 'pplv_init_prey_pop', 'pplv_init_pred_pop']
COMPLV_PARAMS: list[str] = ['complv_alpha', 'complv_growth_rate', 'complv_capacity', 'complv_init_pop']