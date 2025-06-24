import dearpygui.dearpygui as dpg

from gui.texts import *
from gui.indents import *
from models import log, malt, pplv, complv


dpg.create_context()
dpg.create_viewport(title='Models Demo',
                    large_icon='icon.ico', small_icon='icon.ico',
                    width=1280, height=720, x_pos=20, y_pos=20)


def update_geometry(sender, app_data):
    vp_width:  int = dpg.get_viewport_width()
    vp_height: int = dpg.get_viewport_height()

    # Malthusian Model Plot
    dpg.configure_item('malt_main_plot', width=vp_width-MALT_R, height=vp_height-MALT_D)
    # Logistic Model Plot
    dpg.configure_item('log_main_plot', width=vp_width-LOG_R, height=vp_height-LOG_D)
    # Lotka-Volterra Model Plots
    dpg.configure_item('lv_main_plot', width=(vp_width-LV_BOTH_R)/LV_BOTH_W_DIV, height=vp_height-LV_BOTH_D)
    dpg.configure_item('lv_phase_diagram', width=(vp_width-LV_BOTH_R)/LV_BOTH_W_DIV, height=vp_height-LV_BOTH_D)
    # COMPLV - Plots
    dpg.configure_item('complv_plot', width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R, height=vp_height-COMPLV_BOTH_D)
    dpg.configure_item('complv_phase', width=(dpg.get_viewport_width()/COMPLV_BOTH_W_DIV)-COMPLV_BOTH_R, height=vp_height-COMPLV_BOTH_D)
    # COMPLV - Sliders
    dpg.configure_item('complv_sliders_0', width=vp_width / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R)
    dpg.configure_item('complv_sliders_1', width=vp_width / COMPLV_HEADER_BOTH_DIV - COMPLV_HEADER_BOTH_R)

    for paragraph in TEXTS_REGULAR: dpg.configure_item(paragraph, wrap=vp_width-40)

with dpg.handler_registry():
    dpg.add_mouse_down_handler(callback=update_geometry)
    
# MAIN WINDOW
dpg.add_window(tag='main_window', autosize=True)
with dpg.tab_bar(parent='main_window', tag='models_tabs'):
    with dpg.tab(label='Обзор'): # OVERVIEW

        dpg.add_text(OV_INTRO_HEADER,     tag='ov_intro_header')
        dpg.add_text(OV_INTRO_PARAGRAPH,  tag='ov_intro_paragraph',
                     wrap=dpg.get_viewport_width()-PARAG_R)
        dpg.add_text(OV_MALT_SUBHEADER,   tag='ov_malt_subheader')
        dpg.add_text(OV_MALT_PARAGRAPH,   tag='ov_malt_paragraph',
                     wrap=dpg.get_viewport_width()-PARAG_R)
        dpg.add_text(OV_LOG_SUBHEADER,    tag='ov_log_subheader')
        dpg.add_text(OV_LOG_PARAGRAPH,    tag='ov_log_paragraph',
                     wrap=dpg.get_viewport_width()-PARAG_R)
        dpg.add_text(OV_LV_SUBHEADER,     tag='ov_lv_subheader')
        dpg.add_text(OV_LV_PARAGRAPH_1,   tag='ov_lv_paragraph_1', wrap=dpg.get_viewport_width()-PARAG_R)
        dpg.add_text(OV_LV_PARAGRAPH_2,   tag='ov_lv_paragraph_2', wrap=dpg.get_viewport_width()-PARAG_R)

        dpg.add_text(OV_COMPLV_SUBHEADER, tag='ov_complv_subheader')
        dpg.add_text(OV_COMPLV_PARAGRAPH, tag='ov_complv_paragraph',
                     wrap=dpg.get_viewport_width()-PARAG_R)

    malt.Window()
    log.Window()    
    pplv.Window()
    complv.Window()
   
dpg.setup_dearpygui()
dpg.set_primary_window('main_window', True)

with dpg.font_registry():
        jb_mono_extra_bold = dpg.add_font('gui/fonts/JetBrainsMonoNL-ExtraBold.ttf', 40)
        jb_mono_bold       = dpg.add_font('gui/fonts/JetBrainsMonoNL-Bold.ttf', 30)
        jb_mono_regular    = dpg.add_font('gui/fonts/JetBrainsMonoNL-Regular.ttf', 18)

        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=jb_mono_extra_bold)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=jb_mono_bold)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=jb_mono_regular)
        dpg.bind_font(jb_mono_regular)


for item in TEXTS_EXTRA_BOLD: dpg.bind_item_font(item, font=jb_mono_extra_bold)
for item in TEXTS_BOLD:       dpg.bind_item_font(item, font=jb_mono_bold)
for item in TEXTS_REGULAR:    dpg.bind_item_font(item, font=jb_mono_regular)



dpg.set_viewport_resize_callback(update_geometry)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()