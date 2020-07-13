import src.resource.resource as rs

# Resource config dictionary
resource_dict = {
    "vibranium": {
        "vein_number": 100,
        "generation_method": "uniform",
        "land_or_sea_only": "land_only"
    }
}

# Give default value to each key for each resource
for resource in resource_dict:
    if "vein_number" not in resource_dict[resource]:
        resource_dict[resource]["vein_number"] = 1
    if "generation_method" not in resource_dict[resource]:
        resource_dict[resource]["generation_method"] = "uniform"
    if "land_or_sea_only" not in resource_dict[resource]:
        resource_dict[resource]["land_or_sea_only"] = "any"

# Takes resource config dictionary
# Generates map with initial configuration of resource
def generate_resources(config, maps):
    resource_maps = {}
    for resource_key in resource_dict:
        resource_dict[resource_key]["resource_object"] = rs.Resource(resource_dict[resource_key], config, maps)
    return resource_dict

# Takes current state
# Evolves selected resource        
def evolve_resource(config, maps, name):
    pass