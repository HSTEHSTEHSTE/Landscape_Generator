import sys
import noise
import numpy as np
import random
import arcade
import math
import os

size_x = 240
size_y = 120
continent_number = 3

window_width = 1500
window_height = 800
window_title = "Map"
map_width = 1200
map_height = 600

map_height_start = (window_height - map_height)/2
map_height_end = window_height - map_height_start
map_width_start = (window_width - map_width)/2
map_width_end = window_width - map_width_start

class Main(arcade.Window): 

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.map, self.map_landmass = initialMap(size_x, size_y, continent_number)
        self.map_mode = 'none'
        arcade.set_background_color(arcade.color.WHITE)
        # self.set_mouse_visible(False)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.button_list = None
        self.shape_list = None
        self.button_list = []
        self.text_list = []
        
        play_button = MapModeUpdateButton(75, 685, self.update_map_mode, 'main')
        self.button_list.append(play_button)
        quit_button = MapModeUpdateButton(75, 650, self.update_map_mode, 'landmass')
        self.button_list.append(quit_button)
        
        new_button = MapModeUpdateButton(1425, 685, self.data_change, 'new')
        self.button_list.append(new_button)
        load_button = MapModeUpdateButton(1425, 650, self.data_change, 'load')
        self.button_list.append(load_button)
        save_button = MapModeUpdateButton(1425, 615, self.data_change, 'save')
        self.button_list.append(save_button)
        
        self.step_x = 0
        self.step_y = 0
    
    def data_change(self, text): 
        if text == 'new': 
            self.map, self.map_landmass = initialMap(size_x, size_y, continent_number)
            self.update_map_mode('main')
        
        if text == 'save': 
            np.savetxt('map_saves/main.csv', self.map, delimiter = ',')
            np.savetxt('map_saves/landmass.csv', self.map_landmass, delimiter = ',')
            
        if text == 'load': 
            self.map = np.loadtxt('map_saves/main.csv', delimiter = ',')
            self.map_landmass = np.loadtxt('map_saves/landmass.csv', delimiter = ',')
            self.update_map_mode('main')
    
    def setup(self): 
        self.shape_list = arcade.ShapeElementList()
        self.update_map_mode('none')
        
    def on_draw(self):
        arcade.start_render()
        for button in self.button_list:
            button.draw()
        self.shape_list.draw()
        for text in self.text_list: 
            arcade.draw_text(text[0], text[1], text[2], text[3], text[4])
    #    arcade.start_render()
        # self.ball.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        # self.ball.position_x = x
        # self.ball.position_y = y        
        check_mouse_unhover_for_buttons(x, y, self.button_list)
        check_mouse_hover_for_buttons(x, y, self.button_list)

    def on_mouse_press(self, x, y, button, modifiers):
        check_mouse_press_for_buttons(x, y, self.button_list)
        # print(f"You clicked button number: {button}")
        # if button == arcade.MOUSE_BUTTON_LEFT:
        #    self.ball.color = arcade.color.BLACK

    def on_mouse_release(self, x, y, button, modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)
        # if button == arcade.MOUSE_BUTTON_LEFT:
        #    self.ball.color = arcade.color.AUBURN

    def edit_map(self, x, y, color_0, color_1, color_2): 
        arcade.draw_lrtb_rectangle_filled(x * step_x, (x + 1) * step_x, (y + 1) * step_y, y * step_y, (color_0, color_1, color_2))
        arcade.finish_render()
        
    def update_map_mode(self, new_map_mode): 
        self.map_mode = new_map_mode
        self.shape_list = arcade.ShapeElementList()
        print(self.map_mode)
        
        if new_map_mode == 'none':
            arcade.start_render()
            self.text_list.append(['Welcome', window_width/2, window_height/2, arcade.color.BLACK, 20])
        elif ['Welcome', window_width/2, window_height/2, arcade.color.BLACK, 20] in self.text_list: 
            self.text_list.remove(['Welcome', window_width/2, window_height/2, arcade.color.BLACK, 20])
            #self.shape_list.append(shape)
            #arcade.finish_render()
            
        if new_map_mode == 'main': 
            point_list = []
            main_color_list = []
            max_element = np.amax(self.map)
            min_element = np.amin(self.map)
            color_step_0 = math.floor(125/(max_element))
            color_step_1 = math.floor(255/(max_element))
            color_step_2 = math.floor(170/(max_element))
            step_x = math.floor(map_width/size_x)
            step_y = math.floor(map_height/size_y)
            for x in range(0, size_x, 1): 
                for y in range(0, size_y, 1):
                    if self.map[x, y] > 0:
                        color_0 = 125 - color_step_0 * (self.map[x, y])
                        color_1 = 255 - color_step_1 * (self.map[x, y])
                        color_2 = 170 - color_step_2 * (self.map[x, y])
                    elif self.map[x, y] > -1: 
                        color_0 = 0
                        color_1 = 171
                        color_2 = 255
                    else: 
                        color_0 = 0
                        color_1 = 125
                        color_2 = 255
                    for i in range(4): 
                        main_color_list.append((color_0, color_1, color_2))
                    point_list.append((map_width_start + x * step_x, map_height_start + (y + 1) * step_y))
                    point_list.append((map_width_start + (x + 1) * step_x, map_height_start + (y + 1) * step_y))
                    point_list.append((map_width_start + (x + 1) * step_x, map_height_start + y * step_y))
                    point_list.append((map_width_start + x * step_x, map_height_start + y * step_y))           
            shape = arcade.create_rectangles_filled_with_colors(point_list, main_color_list)
            self.shape_list.append(shape)
            
        if new_map_mode == 'landmass':
            point_list = []
            main_color_list = []
            step_x = math.floor(map_width/size_x)
            step_y = math.floor(map_height/size_y)
            for x in range(0, size_x, 1): 
                for y in range(0, size_y, 1):
                    if self.map_landmass[x, y] > 0:
                        color_0 = 75
                        color_1 = 83
                        color_2 = 32
                    else: 
                        color_0 = 0
                        color_1 = 127
                        color_2 = 255
                    for i in range(4): 
                        main_color_list.append((color_0, color_1, color_2))  
                    point_list.append((map_width_start + x * step_x, map_height_start + (y + 1) * step_y))
                    point_list.append((map_width_start + (x + 1) * step_x, map_height_start + (y + 1) * step_y))
                    point_list.append((map_width_start + (x + 1) * step_x, map_height_start + y * step_y))
                    point_list.append((map_width_start + x * step_x, map_height_start + y * step_y))           
            shape = arcade.create_rectangles_filled_with_colors(point_list, main_color_list)
            self.shape_list.append(shape)            

class TextButton:
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.hover = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height
        self.hover_color = arcade.color.BLUE

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)
        if self.pressed:
            color = self.highlight_color
        elif self.hover: 
            color = self.hover_color
        else: 
            color = self.shadow_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y - self.height / 2, color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)

        if self.pressed:
            color = self.highlight_color
        elif self.hover: 
            color = self.hover_color
        else: 
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x - self.width / 2, self.center_y + self.height / 2, color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height
        arcade.draw_text(self.text, x, y, arcade.color.BLACK, font_size=self.font_size, width=self.width, align="center", anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        
    def on_hover(self): 
        self.hover = True 
        
    def on_unhover(self): 
        self.hover = False


def check_mouse_press_for_buttons(x, y, button_list):
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()

def check_mouse_release_for_buttons(x, y, button_list):
    for button in button_list:
        if button.pressed:
            button.on_release()
    
def check_mouse_hover_for_buttons(x, y, button_list):
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_hover()

def check_mouse_unhover_for_buttons(x, y, button_list):
    for button in button_list:
        if button.hover:
            button.on_unhover()

class MapModeUpdateButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text):
        super().__init__(center_x, center_y, 150, 30, text, 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function(self.text)

def makeNoiseMap(size_x, size_y, continent_number, roughness, scale):
    map = np.zeros((size_x, size_y))
    seedx = random.randint(-1, 1024)
    octave_number = int(2 ** roughness)
    for x in range(0, size_x, 1):
        for y in range(0, size_y, 1): 
            map[x, y] = int(noise.pnoise2(seedx + continent_number * y/size_y, continent_number * x/size_x, octaves = octave_number, repeaty = continent_number) * scale)
    roll_amount = random.randint(-1, size_x)
    map = np.roll(map, roll_amount, axis = 0)
    return map

def initialMap(size_x, size_y, continent_number): 
    sum = 0
    while sum == 0: 
        map = makeNoiseMap(size_x, size_y, continent_number, 5, 20)
        map_landmass = np.zeros((size_x, size_y))
        for x in range(0, size_x, 1): 
            for y in range(0, size_y, 1):
                if map[x, y] > 0:
                    map_landmass[x, y] = 1  
        sum = np.sum(map_landmass)
    return map, map_landmass
    
def map_land_only(size_x, size_y, map, map_landmass, base_height): 
    for x in range(0, size_x, 1): 
        for y in range(0, size_y, 1): 
            if map_landmass[x, y] < base_height: 
                map[x, y] = 0
    return map
    
def map_sea_only(size_x, size_y, map, map_landmass, base_height): 
    for x in range(0, size_x, 1): 
        for y in range(0, size_y, 1): 
            if map_landmass[x, y] > base_height: 
                map[x, y] = 0
    return map
    
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

# class PopulationMap: 
    # def __init__(self, name, size, continent_number, roughness, scale, type_desc, map, map_landmass):
        # self.name = name
        # self.continent_number = continent_number
        # self.type_desc = type_desc
        
                
#map, map_landmass = initialMap(size_x, size_y, continent_number)
#resource_magnesium = Resource('Magnesium', size_x, size_y, 8, 5, 5, 'sea_only', map, map_landmass)
#print(map)
#print(resource_magnesium.map)

# step_x, step_y = draw_map(map)

window = Main(window_width, window_height, window_title)
window.setup()
arcade.run()