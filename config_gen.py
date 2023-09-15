'''
Main script for populating jinja2 templates and export as files.

'''

import json
import sys
from jinja2 import Environment, FileSystemLoader

def validate_usage():
    '''Check if a router argument is provided and print help statement'''
    if len(sys.argv) != 2:
        print("Usage: python3 config_gen.py <router>")
        sys.exit(1)

def load_jsonfile(hostname):
    '''Load the corresponding JSON configuration of a given router/hostname'''
    config_filename = f"Router_Json_Models/{hostname}_config.json"
    try:
        with open(config_filename, 'r') as json_file:
            config_data = json.load(json_file)
            return config_data
    except FileNotFoundError:
        print(f"Configuration file for {router_arg} not found.")
        sys.exit(1)

def generate_config(router, configs):
    '''Function to generate configurations using Jinja2 template'''
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

def main():
    '''Main function to generate configs'''
    validate_usage()
    router_arg = sys.argv[1]

    # Generate configurations for the specified router
    config_data = load_jsonfile(router_arg)
    generate_config(router_arg.upper(), config_data)

main()




