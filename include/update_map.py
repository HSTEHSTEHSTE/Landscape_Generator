import random
import noise
import src.map.map as map

# Takes previous map state, update function
# Return new map state

def update_map(maps, update_function, config):
    new_maps = copy(maps)
    for new_map in new_maps:
        new_map = update_function(maps, config)
    return new_maps
    
# Takes config
# Generate initial maps
def generate_map(config):
    maps = {}
    maps['map_base'] = map.Map()
    maps['main'], maps['map_landmass'] = maps['map_base'].initial_map()
    return maps