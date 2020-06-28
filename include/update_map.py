import random
import noise
import src.map.map as map
from collections import OrderedDict

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
    maps = OrderedDict()
    maps['map_base'] = map.Map()
    maps['map'], maps['map_landmass'] = maps['map_base'].initial_map()
    return maps