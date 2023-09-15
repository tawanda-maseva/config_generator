'''
Main script for populating jinja2 templates and export as files.

'''

import json
import sys
from jinja2 import Environment, FileSystemLoader

# Function to generate configurations using Jinja2 template
def generate_config(router, configs):
    template_loader = FileSystemLoader(searchpath="./Jinja_Templates")
    env = Environment(loader=template_loader)
    template = env.get_template("config_template.j2")
    rendered_template = template.render(router=router, 
        interfaces=configs.get("production_interfaces", {}),
        bgp_peers=configs.get("BGP_PeerGoup", {}),
        router_id=configs.get("router_id", 0)
        )

    with open(f"Generated_Configs/{router}_config.conf", "w") as config_file:
        config_file.write(rendered_template)

    print(f"Configuration file {router}_config.conf generated successfully. Saved in /Generated_Configs folder")

# Check if a router argument is provided
if len(sys.argv) != 2:
    print("Usage: python3 config_gen.py <router>")
    sys.exit(1)

router_arg = sys.argv[1]

# Load the corresponding JSON configuration
config_filename = f"Router_Json_Models/{router_arg}_config.json"
try:
    with open(config_filename, 'r') as json_file:
        config_data = json.load(json_file)
except FileNotFoundError:
    print(f"Configuration file for {router_arg} not found.")
    sys.exit(1)

# Generate configurations for the specified router
generate_config(router_arg.upper(), config_data)



