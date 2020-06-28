create_ui_function = None

# Takes initial maps, create ui function
# Returns ui instance

def create_ui_instance(maps, create_ui_function, config):
    return create_ui_function(maps, config)
    
def choose_ui(config):
    if config['ui'] == 'arcade':
        from src.ui.arcade import ui
        ui_object = ui.ui()
        return ui_object
    
    create_ui_function = ui.ui