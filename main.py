from include import update_map
from include import ui
from include import resource

config = {
    "size_x": 240,
    "size_y": 120,
    "continent_number": 3,
    "ui": 'arcade'
}
       
# step_x, step_y = draw_map(map)

maps = update_map.generate_map(config)
resources = resource.generate_resources(config, maps)
ui_object = ui.choose_ui(config)