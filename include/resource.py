class Resource: 
    def __init__(self, name, size_x, size_y, continent_number, roughness, scale, type_desc, map, map_landmass): 
        self.name = name
        self.continent_number = continent_number
        self.type_desc = type_desc
        self.map = makeNoiseMap(size_x, size_y, continent_number, roughness, scale)
        self.map = np.absolute(self.map)
        if type_desc == 'land_only': 
            self.map = map_land_only(size_x, size_y, self.map, map_landmass, 1)
        if type_desc == 'sea_only': 
            self.map = map_sea_only(size_x, size_y, self.map, map_landmass, 0)