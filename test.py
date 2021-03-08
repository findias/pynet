import device
from pprint import pprint
import yaml
import netmiko
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def yaml_import(file_config):
    with open(file_config, 'r') as f:
        all_device = yaml.safe_load(f)
    return all_device

def devices_connections(import_device_file_all):
    device = {}
    for device_dict in import_device_file_all:
         device['device_type'] = device_dict['type']
    return device

def connect_send_command(devices, command):
    with netmiko.ConnectHandler(**devices) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        return result

all_device = yaml_import('conf_device.yaml')
command ='show run'
devices = devices_connections(all_device)
print(devices)

# connect = connect_to_device(all_device, command)
# thread = thread_pool(connect_to_device, all_device, command)

# def thread_pool(function, connect, command):


with ThreadPoolExecutor(max_workers=3) as executor:
    for devices in all_device['hosts']:

        print(devices)
        result = executor.map(connect_send_command, devices, repeat(command))
        for devices, output in zip(devices, result):
            print(device['name'], output)
            print(device)