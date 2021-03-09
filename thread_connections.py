from datetime import datetime
import yaml
import logging
from netmiko import Netmiko
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def yaml_import(file_config):                                      # Import file from yaml
    with open(file_config, 'r') as f:
        all_config_device = yaml.safe_load(f)
    return all_config_device

def conf_file(yaml_config):                                         # Create config list
    devices_config_list = []
    for device_dic in yaml_config['hosts']:
        devices_config_list.append(device_dic)
    return devices_config_list

def connect_and_send_command(host, command):                        # Connect to devices
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:{}'
    ip = host['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    net_connection = Netmiko(
        host=host['ip'],
        username=host['username'],
        password=host['password'],
        port=host['port'],
        device_type=host['type'],
        secret=host['secret']
    )
    with net_connection as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        logging.info(received_msg.format(datetime.now().time(), ip))
    return output

logging.getLogger('paramiko').setLevel(logging.WARNING)
logging.basicConfig(
format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
level=logging.INFO)

all_device = yaml_import('conf_device.yaml')
command ='show run'
connect_value = conf_file(all_device)

with ThreadPoolExecutor(max_workers=5) as executor:
    result = executor.map(connect_and_send_command, connect_value, repeat(command))
    for device, output in zip(connect_value, result):
        with open(f"{device['name']}", 'w+') as f:
            f.write(output)