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
    #for host in import_file['hosts']:
        net_connection = Netmiko(
            host=import_file['ip'],
            username=import_file['username'],
            password=import_file['password'],
            port=import_file['port'],
            device_type=import_file['type'],
            secret=import_file['secret']
        )
        net_connection.enable()
        output = net_connection.send_command(command)
        # print(host['ip'])
        with open(f"{host['name']}.txt", 'w') as f:
             f.write(output)
    return output


all_device = yaml_import('conf_device.yaml')
command ='show run'
# connect = connect_to_device(all_device, command)
# thread = thread_pool(connect_to_device, all_device, command)

# def thread_pool(function, connect, command):
for device in all_device['hosts']:
    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(connect_to_device, device, repeat(command))
        for device, output in zip(device, result):
            print(device['name'], output)
            print(device)