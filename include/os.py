import os
import numpy

folder = ""

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(file_path)

def save(folder, map):
    np.savetxt('map_saves/main.csv', map, delimiter = ',')