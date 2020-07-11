import arcade
import numpy as np
import include.os
import include.update_map
import math

ui_config = {
    "window_width": 1500,
    "window_height": 800,
    "window_title": "Map",
    "font": "Arial",
    "font_size": 18
}

def init_params(config):
    ui_config["map_width"] = int(ui_config["window_width"]/5*4)
    ui_config["map_height"] = int(ui_config["window_height"]/4*3)
    
    ui_config["step_x"] = math.floor(ui_config["map_width"]/config["size_x"])
    ui_config["step_y"] = math.floor(ui_config["map_height"]/config["size_y"])
    ui_config["map_width"] = ui_config["step_x"]*config["size_x"]
    ui_config["map_height"] = ui_config["step_y"]*config["size_y"]

    ui_config["map_height_start"] = int((ui_config["window_height"] - ui_config["map_height"])/2)
    ui_config["map_height_end"] = int(ui_config["window_height"] - ui_config["map_height_start"])
    ui_config["map_width_start"] = int((ui_config["window_width"] - ui_config["map_width"])/2)
    ui_config["map_width_end"] = int(ui_config["window_width"] - ui_config["map_width_start"])

    ui_config["button_width"] = int(ui_config["window_width"]/10)
    ui_config["button_height"] = int(ui_config["window_width"]/50)
    ui_config["button_border_width"] = int(ui_config["window_width"]/1000)

    ui_config["left_button_column_width_centre"] = int(ui_config["window_width"]/20)
    ui_config["right_button_column_width_centre"] = ui_config["window_width"] - int(ui_config["window_width"]/20)
    
    ui_config["font_size"] = int(ui_config["window_width"]/100)

def make_button_column(button_list, json_button_list, button_width_centre):
    index = 0
    button_height_centre = ui_config["window_height"] - int(ui_config["window_height"]/8)
    button_height_step = ui_config["button_height"]
    print("button_height_step: ", button_height_step)
    for json_button in json_button_list:
        button = MapModeUpdateButton(button_width_centre, button_height_centre, json_button["function"], json_button["text"])
        button_height_centre -= button_height_step
        print("height_centre: ", button_height_centre)
        button_list.append(button)
    return button_list

def clear_button_column(button_list, button_width_centre):
    new_button_list = []
    for button in button_list:
        if button.width_centre != button_width_centre:
            new_button_list.append(button)
    return new_button_list
    
class ui(arcade.Window):
    def __init__(self, config):
        ui_config["window_width"] = config["screen_width"]
        ui_config["window_height"] = config["screen_height"]
        super().__init__(ui_config["window_width"], ui_config["window_height"], ui_config["window_title"])
        ui_config["window_width"], ui_config["window_height"] = self.get_size()
        init_params(config)
        arcade.set_background_color(arcade.color.WHITE)
        self.shape_list = None
        self.button_list = []
        self.text_list = []
        self.create_buttons()
        self.maps = {}
        
        make_button_column(self.button_list, self.button_list_mapmodes, ui_config["left_button_column_width_centre"])
        make_button_column(self.button_list, self.button_list_datachanges, ui_config["right_button_column_width_centre"])
        
        self.step_x = 0
        self.step_y = 0
        
        self.size_x = config['size_x']
        self.size_y = config['size_y']
        
        self.configurations = config
    
        self.state = "geography"

    def create_buttons(self):
        self.button_main = {
            "function": self.update_map_mode,
            "text": "main"
        }

        self.button_landmass = {
            "function": self.update_map_mode,
            "text": "landmass"
        }

        self.button_resource = {
            "function": self.update_button_list,
            "text": "resource"
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
        
        self.button_back = {
            "function": self.update_button_list,
            "text": "back"
        }
        self.button_list_resources = [self.button_back]
        self.button_list_mapmodes = [self.button_main, self.button_landmass, self.button_resource]
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
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)

    def draw_map(self, map, color_dict):
        point_list = []
        render_color_list = []
        # self.shape_list = arcade.ShapeElementList()
        step_x = math.floor(ui_config["map_width"]/self.size_x)
        step_y = math.floor(ui_config["map_height"]/self.size_y)
        for x in range(0, self.size_x, 1):
            for y in range(0, self.size_y, 1):
                color = color_dict[int(map[x, y])]
                for i in range(4): 
                    render_color_list.append(color)
                point_list.append((ui_config["map_width_start"] + x * step_x, ui_config["map_height_start"] + (y + 1) * step_y))
                point_list.append((ui_config["map_width_start"] + (x + 1) * step_x, ui_config["map_height_start"] + (y + 1) * step_y))
                point_list.append((ui_config["map_width_start"] + (x + 1) * step_x, ui_config["map_height_start"] + y * step_y))
                point_list.append((ui_config["map_width_start"] + x * step_x, ui_config["map_height_start"] + y * step_y))
        shape = arcade.create_rectangles_filled_with_colors(point_list, render_color_list)
        self.shape_list.append(shape)

    def update_map_mode(self, new_map_mode): 
        self.map_mode = new_map_mode
        print(self.map_mode)
        
        if new_map_mode == 'none':
            arcade.start_render()
            self.text_list.append(['Welcome', ui_config["window_width"]/2, ui_config["window_height"]/2, arcade.color.BLACK, ui_config["font_size"]])
        elif ['Welcome', ui_config["window_width"]/2, ui_config["window_height"]/2, arcade.color.BLACK, ui_config["font_size"]] in self.text_list: 
            self.text_list.remove(['Welcome', ui_config["window_width"]/2, ui_config["window_height"]/2, arcade.color.BLACK, ui_config["font_size"]])
        
        value_color_dict = {}
        
        if new_map_mode == 'main':
            max_element = int(np.amax(self.maps['main']))
            min_element = int(np.amin(self.maps['main']))
            color_step_0 = math.floor(125/(max_element))
            color_step_1 = math.floor(255/(max_element))
            color_step_2 = math.floor(170/(max_element))
            
            for altitude in range(min_element, max_element + 1, 1):
                if altitude > 0:
                    color_0 = 125 - color_step_0 * altitude
                    color_1 = 255 - color_step_1 * altitude
                    color_2 = 170 - color_step_2 * altitude
                elif altitude > -1:
                    color_0 = 0
                    color_1 = 171
                    color_2 = 255
                else:
                    color_0 = 0
                    color_1 = 125
                    color_2 = 255
                value_color_dict[altitude] = (color_0, color_1, color_2)
            
            self.draw_map(self.maps['main'], value_color_dict)
            
        if new_map_mode == 'landmass':
            max_element = int(np.amax(self.maps['main']))
            min_element = int(np.amin(self.maps['main']))
            
            for altitude in range(min_element, max_element + 1, 1):
                if altitude > 0:
                    color_0 = 75
                    color_1 = 83
                    color_2 = 32
                else:
                    color_0 = 0
                    color_1 = 127
                    color_2 = 255
                value_color_dict[altitude] = (color_0, color_1, color_2)
                
            self.draw_map(self.maps['landmass'], value_color_dict)
    
    def data_change(self, text):
        print(text)
        if text == 'load':
            self.maps = include.os.load(self.maps)
            self.update_map_mode('main')
        if text == 'save':
            include.os.save(self.maps)
        if text == 'new':
            self.maps = include.update_map.generate_map(self.configurations)
            self.update_map_mode('main')
    
    def update_button_list(self, text):
        print(text)
        if text == 'resource':
            self.button_list = clear_button_column(self.button_list, ui_config["left_button_column_width_centre"])
            self.button_list = make_button_column(self.button_list, self.button_list_resources, ui_config["left_button_column_width_centre"])
            self.state = "resource"
        if text == 'back':
            if self.state == "resource":
                self.button_list = clear_button_column(self.button_list, ui_config["left_button_column_width_centre"])
                self.button_list = make_button_column(self.button_list, self.button_list_mapmodes, ui_config["left_button_column_width_centre"])
    
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
        self.button_height = ui_config["button_height"]
        self.hover_color = (0, 255, 0)
        
    def draw(self):
        if self.pressed:
            self.face_color = self.highlight_color
        elif self.hover: 
            self.face_color = self.hover_color
        else: 
            self.face_color = self.shadow_color

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)

        if self.pressed:
            color = self.highlight_color
        elif self.hover: 
            color = self.hover_color
        else: 
            color = self.shadow_color

        # Bottom horizontal
        arcade.draw_line(int(self.center_x - self.width / 2), int(self.center_y - self.height / 2), int(self.center_x + self.width / 2), int(self.center_y - self.height / 2), color)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color)

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x - self.width / 2, self.center_y + self.height / 2, color)

        x = self.center_x
        y = self.center_y
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
        super().__init__(center_x, center_y, ui_config["button_width"], ui_config["button_height"], text, ui_config["font_size"], ui_config["font"])
        self.action_function = action_function
        self.width_centre = center_x

    def on_release(self):
        super().on_release()
        self.action_function(self.text)
