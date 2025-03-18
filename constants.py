LOG_GROWTH_SPEED_MIN, LOG_GROWTH_SPEED_MAX = 0.01, 10.0
LOG_INIT_POP_MIN, LOG_INIT_POP_MAX = 0.1, 20.0
LOG_CAPACITY_MIN, LOG_CAPACITY_MAX = 0.1, 10.0

MALT_GROWTH_SPEED_MIN, MALT_GROWTH_SPEED_MAX = 0.01, 10.0
MALT_INIT_POP_MIN, MALT_INIT_POP_MAX = 0.01, 10.0

LOG_PARAMS: list[str] = ['log_growth_speed', 'log_init_pop', 'log_capacity']
MALT_PARAMS: list[str] = ['malt_growth_speed', 'malt_init_pop']