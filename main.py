import json
from include import update_map
from include import ui

config = {
    "map_mode": "none",
    "size_x": 240,
    "size_y": 120,
    "continent_number": 3,
    "ui": 'arcade'
}

# class PopulationMap: 
    # def __init__(self, name, size, continent_number, roughness, scale, type_desc, map, map_landmass):
        # self.name = name
        # self.continent_number = continent_number
        # self.type_desc = type_desc
        
#resource_magnesium = Resource('Magnesium', size_x, size_y, 8, 5, 5, 'sea_only', map, map_landmass)
#print(map)
#print(resource_magnesium.map)

# step_x, step_y = draw_map(map)

maps = update_map.generate_map(config)
ui_object = ui.choose_ui(config)