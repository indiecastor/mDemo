MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX           = 0.01, 10.0
MALT_INIT_POP_MIN, MALT_INIT_POP_MAX                   = 0.01, 10.0

L_GS_MIN, L_GS_MAX             = 0.01, 10.0
L_IP_MIN,     L_IP_MAX                 = 0.1, 20.0
L_C_MIN,     L_C_MAX                 = 0.1, 10.0
  
PPLV_A_MIN, PPLV_A_MAX                         = 0.1, 2
PPLV_B_MIN,  PPLV_B_MAX                          = 0.1, 2
PPLV_G_MIN, PPLV_G_MAX                         = 0.1, 2
PPLV_D_MIN, PPLV_D_MAX                         = 0.1, 2

PPLV_IP_PREY_MIN,     PPLV_IP_PREY_MAX     = 0.1, 2
PPLV_IP_PRED_MIN, PPLV_IP_PRED_MAX = 0.1, 2

COMPLV_GROWTH_RATE_MIN, COMPLV_GROWTH_RATE_MAX         = 0.1, 0.9
COMPLV_ALPHA_MIN, COMPLV_ALPHA_MAX                     = 0.1, 0.9
COMPLV_CAPACITY_MIN, COMPLV_CAPACITY_MAX               = 10.0, 100.0
COMPLV_INIT_POP_MIN, COMPLV_INIT_POP_MAX               = 10.0, 100.0

# Parameter lists do not include 'all' parameter!
LOG_PARAMS:  list[str]   = ['log_growth_speed', 'log_init_pop', 'log_capacity']
MALT_PARAMS: list[str]   = ['malt_growth_speed', 'malt_init_pop']
PPLV_PARAMS: list[str]   = ['pplv_alpha', 'pplv_beta', 'pplv_gamma', 'pplv_delta', 'pplv_init_prey_pop', 'pplv_init_pred_pop']
COMPLV_PARAMS: list[str] = ['complv_alpha', 'complv_growth_rate', 'complv_capacity', 'complv_init_pop']