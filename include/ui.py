from screeninfo import get_monitors

create_ui_function = None

# Takes initial maps, create ui function
# Returns ui instance

def create_ui_instance(maps, create_ui_function, config):
    return create_ui_function(maps, config, screen_config)
    
def choose_ui(config):
    config["screen_width"], config["screen_height"] = get_screen_resolutions()
    if config['ui'] == 'arcade':
        from src.ui.arcade import ui
        ui_object = ui.ui(config)
        ui_object.setup()
        return ui_object
    
    create_ui_function = ui.ui

def get_screen_resolutions():    
    screen = get_monitors()[0]
    return screen.width, screen.height