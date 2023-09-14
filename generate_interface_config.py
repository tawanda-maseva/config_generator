'''
Code has been updated such that makes use of Jinja2 templates

'''

import json
import sys
from jinja2 import Environment, FileSystemLoader

# Function to generate configurations using Jinja2 templates
def generate_config(router, interface_configs):
    template_loader = FileSystemLoader(searchpath="./")
    env = Environment(loader=template_loader)
    template = env.get_template("interface_template.j2")
    rendered_template = template.render(router=router, interfaces=interface_configs)

    with open(f"{router}_config.conf", "w") as config_file:
        config_file.write(rendered_template)

    print(f"Configuration file {router}_config.conf generated successfully.")

# Check if a router argument is provided
if len(sys.argv) != 2:
    print("Usage: python3 generate_config.py <router>")
    sys.exit(1)

router_arg = sys.argv[1]

# Load the corresponding JSON configuration
config_filename = f"{router_arg}_config.json"
try:
    with open(config_filename, 'r') as json_file:
        router_configs = json.load(json_file)
except FileNotFoundError:
    print(f"Configuration file for {router_arg} not found.")
    sys.exit(1)

# Generate configurations for the specified router
generate_config(router_arg.upper(), router_configs)

