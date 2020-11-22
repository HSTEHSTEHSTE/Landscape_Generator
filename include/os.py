import os
import numpy as np

folder = ""

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(file_path)

map_files = {
    "main": "main.csv",
    "landmass": "landmass.csv"
}

save_file = "map_saves"

def save(maps):
    for map_name in maps:
        np.savetxt(save_file + '/' + map_files[map_name], maps[map_name], delimiter = ',')
    
def load(maps):
    for map_name in map_files:
        maps[map_name] = np.loadtxt(save_file + '/' + map_files[map_name], delimiter = ',')
    return maps