import arcade
import json
import numpy as np
import include.os

ui_config = {
    "window_width": 1500,
    "window_height": 800,
    "window_title": "Map",
    "font": "Arial",
    "font_size": 18
}
#todo: generate ui_config automatically by fetching window resolution

window_width = ui_config["window_width"]
window_height = ui_config["window_height"]
window_title = ui_config["window_title"]

map_width = int(window_width/5*4)
map_height = int(window_height/4*3)

map_height_start = (window_height - map_height)/2
map_height_end = window_height - map_height_start
map_width_start = (window_width - map_width)/2
map_width_end = window_width - map_width_start

button_width = int(window_width/10)
button_height = int(window_width/50)
font = ui_config["font"]
font_size = ui_config["font_size"]

left_button_column_width_centre = int(window_width/20)
right_button_column_width_centre = window_width - int(window_width/20)

def make_button_column(button_list, json_button_list, button_width_centre):
    index = 0
    button_height_centre = window_height - int(window_height/8)
    button_height_step = int(window_height/22)
    for json_button in json_button_list:
        button = MapModeUpdateButton(button_width_centre, button_height_centre, json_button["function"], json_button["text"])
        button_height_centre -= button_height_step
        button_list.append(button)
    return button_list
    
class ui(arcade.Window):
    
    map_mode = None
    
    def __init__(self):
        super().__init__(window_width, window_height, window_title)
        arcade.set_background_color(arcade.color.WHITE)
        self.shape_list = None
        self.button_list = []
        self.text_list = []
        self.create_buttons()
        
        make_button_column(self.button_list, self.button_list_mapmodes, left_button_column_width_centre)
        make_button_column(self.button_list, self.button_list_datachanges, right_button_column_width_centre)
        
        self.step_x = 0
        self.step_y = 0
    
    def create_buttons(self):
        self.button_main = {
            "function": self.update_map_mode,
            "text": "main"
        }

        self.button_landmass = {
            "function": self.update_map_mode,
            "text": "landmass"
        }

        self.button_new = {
            "function": self.data_change,
            "text": "new"
        }

        self.button_load = {
            "function": self.data_change,
            "text": "load"
        }

        self.button_save = {
            "function": self.data_change,
            "text": "save"
        }
        
        self.button_list_mapmodes = [self.button_main, self.button_landmass]
        self.button_list_datachanges = [self.button_new, self.button_load, self.button_save]
    
    def setup(self): 
        self.shape_list = arcade.ShapeElementList()
        self.update_map_mode('none')
        arcade.run()
        
    def on_draw(self):
        arcade.start_render()
        for button in self.button_list:
            button.draw()
        self.shape_list.draw()
        for text in self.text_list: 
            arcade.draw_text(text[0], text[1], text[2], text[3], text[4])

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""     
        check_mouse_unhover_for_buttons(x, y, self.button_list)
        check_mouse_hover_for_buttons(x, y, self.button_list)

    def on_mouse_press(self, x, y, button, modifiers):
        check_mouse_press_for_buttons(x, y, self.button_list)\

    def on_mouse_release(self, x, y, button, modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)\

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
    
    def data_change(self, text):
        pass
        
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
        super().__init__(center_x, center_y, button_width, button_height, text, font_size, font)
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function(self.text)
