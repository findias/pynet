import device
from pprint import pprint
import yaml
from netmiko import Netmiko
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def yaml_import(file_config):
    with open(file_config, 'r') as f:
        all_device = yaml.safe_load(f)
    return all_device

def connect_to_device(import_file, command):
    for host in import_file['hosts']:
        net_connection = Netmiko(
            host=host['ip'],
            username=host['username'],
            password=host['password'],
            port=host['port'],
            device_type=host['type'],
            secret=host['secret']
        )
        net_connection.enable()
        output = net_connection.send_command(command)
        # print(host['ip'])
        with open(f"{host['name']}" + "_tech-support.txt", 'w') as f:
             f.write(output)
    return output

# def thread_pool(function, connect, command):
#     with ThreadPoolExecutor(max_workers=3) as executor:
#         result = executor.map(function, connect, repeat(command))
#         for device, output in zip(connect, result):
#             print(device['ip'], output)

all_device = yaml_import('conf_device_cit.yaml')
command ='show run'
connect = connect_to_device(all_device, command)
####thread = thread_pool(connect_to_device, all_device, command)
# print(all_device)
