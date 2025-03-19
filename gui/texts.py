# TAG SYSTEM
# prefix: tab
#     ov_        - overview
# root: model
#     malt       - malthusian model
#     log        - logistic model
#     lv         - predator-prey lotka-volterra model
#     complv     - competitive lotka-volterra model
#     genlv      - generalized lotka-volterra model
# postfix: text type
#     _header     - header (JetBrainsMonoNL-ExtraBold, 40)
#     _subheader - subheader (JetBrainsMonoNL-Bold, 30)
#     _paragraph - regular text (JetBrainsMonoNL-Regular, 18)

OV_INTRO_HEADER = 'Ecological Models Demo'
OV_INTRO_PARAGRAPH = """
This program is a demonstraion of population models for students. 
Here you can drag some sliders and see how the model changes!
""".replace('\n', '')

OV_MALT_SUBHEADER = 'Malthusian model'
OV_MALT_PARAGRAPH = """
This model was created by Thomas Robert Malthus in «An Essay on the Principle of Population» (1798). 
It is defined throuh differential equaion: dx/dt = rx, where r is a growth speed of the population 
a.k.a. «Malthusian marameter». This model does not take into accout the capacity of the environment, 
so according to this model population growth exponentially in presence of unlimited resources.
""".replace('\n', '')

OV_LOG_SUBHEADER = 'Logistic model'
OV_LOG_PARAGRAPH = """
This model was created by Pierre François Verhulst between 1838 and 1847. 
This model is also determined by a growth speed r but, unlike Malthusian model, 
here the population size is limited by a specific carrying capacity of the environment.
""".replace('\n', '')

OV_LV_SUBHEADER = 'Prey-predator Lotka-Volterra Model'
OV_LV_PARAGRAPH_1 = """
The Lotka-Volterra predator-prey model was initially proposed by Alfred J. Lotka in
the theory of autocatalytic chemical reactions in 1910. This was effectively the 
logistic equation, originally derived by Pierre François Verhulst. In 1920 
Lotka extended the model, via Andrey Kolmogorov, to "organic systems" using a 
plant species and a herbivorous animal species as an example and in 1925 he used 
the equations to analyse predator-prey interactions in his book on biomathematics. 
The same set of equations was published in 1926 by Vito Volterra, a mathematician 
and physicist, who had become interested in mathematical biology.
""".replace('\n', '')
OV_LV_PARAGRAPH_2 = """
This model takes four parameters: alpha (prey per capita growth rate), beta (effect of 
the presence of predators on the prey death rate), gamma (predator's per capita death rate) 
and delta (effect of the presence of prey on the predator's growth rate)
""".replace('\n', '')

OV_COMPLV_SUBHEADER = 'Competitive Lotka-Volterra Model'
OV_COMPLV_PARAGRAPH = """Competitive Lotka-Volterra Model test
""".replace('\n', '')

OV_GENLV_SUBHEADER = 'Generalized Lotka-Volterra Model'
OV_GENLV_PARAGRAPH = """Generalized Lotka-Volterra Model test
""".replace('\n', '')

TEXTS_EXTRA_BOLD: list[str] = ['ov_intro_header']
TEXTS_BOLD: tuple[str] = (
                            'ov_malt_subheader', 'ov_log_subheader',
                            'ov_lv_subheader', 'ov_complv_subheader', 'ov_genlv_subheader')
TEXTS_REGULAR: tuple[str] = (
                            'ov_intro_paragraph',
                            'ov_malt_paragraph',
                            'ov_log_paragraph',
                            'ov_lv_paragraph_1',
                            'ov_lv_paragraph_2',
                            'ov_complv_paragraph',
                            'ov_genlv_paragraph')
