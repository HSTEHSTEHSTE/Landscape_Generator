import src.resource.resource as rs

# Resource config dictionary
resources = {
    "vibranium": {
        "vein_number": 1,
        "generation_method": "uniform",
        "land_or_sea_only": "land_only"
    }
}

# Give default value to each key for each resource
for resource in resources:
    if "vein_number" not in resources[resource]:
        resources[resource]["vein_number"] = 1
    if "generation_method" not in resources[resource]:
        resources[resource]["generation_method"] = "uniform"
    if "land_or_sea_only" not in resources[resource]:
        resources[resource]["land_or_sea_only"] = "any"

# Takes resource config dictionary
# Generates map with initial configuration of resource
def generate_resources(config, maps):
    resource_maps = {}
    for resource in resources:
        resources[resource] = rs.Resource(resources[resource], config, maps)