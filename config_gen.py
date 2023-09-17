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
    config_filename = f"Router_Json_Models/{hostname}.json"
    try:
        with open(config_filename, 'r') as json_file:
            config_data = json.load(json_file)
            return config_data
    except FileNotFoundError:
        print(f"Jason file for {hostname} not found in Router_Json_Models directory.")
        sys.exit(1)

def generate_config(configs_json, template_name):
    '''Function to generate configurations using Jinja2 template'''
    template_loader = FileSystemLoader(searchpath="./Jinja_Templates")
    env = Environment(loader=template_loader)
    template = env.get_template(template_name)
    hostname = configs_json.get("hostname", "null")
    rendered_template = template.render(
        router=hostname,
        interfaces=configs_json.get("production_interfaces", {}),
        loopbacks=configs_json.get("loopback_interfaces", {}),
        bgp_peers=configs_json.get("BGP_PeerGoup", {}),
        router_id=configs_json.get("router_id", "null")
        )

    with open(f"Generated_Configs/{hostname}_config.conf", "a") as config_file:
        config_file.write(rendered_template)

    print(f"Configlet {hostname}.{template_name} generated successfully.")

def main():
    '''Main function to generate configs'''
    validate_usage()
    router_arg = sys.argv[1].lower()
    config_data = load_jsonfile(router_arg)
    device_role = config_data.get("device_role", "null")
    
    # Generate configurations for the specified router
    generate_config(configs_json=config_data, template_name="base_template.j2")
    generate_config(configs_json=config_data, template_name=f"{device_role}_template.j2")
    print(f"Configuration file {router_arg}_config.conf generated successfully. Saved in Generated_Configs folder")

main()




