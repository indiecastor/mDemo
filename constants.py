LOG_GROWTH_SPEED_MIN, LOG_GROWTH_SPEED_MAX = 0.01, 10.0
LOG_INIT_POP_MIN, LOG_INIT_POP_MAX = 0.1, 20.0
LOG_CAPACITY_MIN, LOG_CAPACITY_MAX = 0.1, 10.0

MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX = 0.01, 10.0
MALT_INIT_POP_MIN, MALT_INIT_POP_MAX = 0.01, 10.0

LV_ALPHA_MIN, LV_ALPHA_MAX = 0.1, 2
LV_BETA_MIN, LV_BETA_MAX = 0.1, 2
LV_GAMMA_MIN, LV_GAMMA_MAX = 0.1, 2
LV_DELTA_MIN, LV_DELTA_MAX = 0.1, 2

LV_INIT_PREY_POP_MIN, LV_INIT_PREY_POP_MAX = 0.1, 2
LV_INIT_PREDATOR_POP_MIN, LV_INIT_PREDATOR_POP_MAX = 0.1, 2

# Parameter lists do not include 'all' parameter!
LOG_PARAMS:  tuple[str] = ('log_growth_speed', 'log_init_pop', 'log_capacity')
MALT_PARAMS: tuple[str] = ('malt_growth_speed', 'malt_init_pop')
PPLV_PARAMS: tuple[str] = ('pplv_alpha', 'pplv_beta', 'pplv_gamma', 'pplv_delta', 'pplv_init_prey_pop', 'pplv_init_pred_pop')