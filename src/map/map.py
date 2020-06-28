import numpy as np
import noise
import random
        
class Map():
    def __init__(self, size_x = 240, size_y = 120, continent_number = 3, roughness = 5, scale = 20):
        self.size_x = size_x
        self.size_y = size_y
        self.continent_number = continent_number
        self.roughness = roughness
        self.scale = scale
        self.map = np.zeros((self.size_x, self.size_y))
        self.map_landmass = np.zeros((self.size_x, self.size_y))
        
    def make_noise_map(self):
        seedx = random.randint(-1, 1024)
        octave_number = int(2 ** self.roughness)
        for x in range(0, self.size_x, 1):
            for y in range(0, self.size_y, 1): 
                self.map[x, y] = int(noise.pnoise2(seedx + self.continent_number * y/self.size_y, self.continent_number * x/self.size_x, octaves = octave_number, repeaty = self.continent_number) * self.scale)
        roll_amount = random.randint(-1, self.size_x)
        self.map = np.roll(self.map, roll_amount, axis = 0)
        return self.map
        
    def map_sea_only(self, base_height): 
        for x in range(0, self.size_x, 1): 
            for y in range(0, self.size_y, 1): 
                if self.map[x, y] > base_height: 
                    self.map[x, y] = 0
        return self.map
    
    def map_land_only(self, base_height): 
        for x in range(0, self.size_x, 1): 
            for y in range(0, self.size_y, 1): 
                if self.map[x, y] < base_height: 
                    self.map[x, y] = 0
        return self.map
        
    def initial_map(self): 
        sum = 0
        while sum == 0: 
            self.map = self.make_noise_map()
            self.map_landmass = np.zeros((self.size_x, self.size_y))
            for x in range(0, self.size_x, 1): 
                for y in range(0, self.size_y, 1):
                    if self.map[x, y] > 0:
                        self.map_landmass[x, y] = 1  
            sum = np.sum(self.map_landmass)
        return self.map, self.map_landmass