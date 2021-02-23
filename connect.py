#!/usr/bin/python3

from datetime import datetime
import logging
import yaml
from pprint import pprint
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
### Connect whith device and send show command ####
def send_show_command(device, commands):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received: {}'
    ip = device['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    int_status = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                int_status[command] = output
                logging.info(received_msg.format(datetime.now().time(), ip))
        return int_status
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

### Connect whith device and send conf t command ####

def send_conf_command(device, commands):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received: {}'
    ip = device['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                ssh.send_command(command)
                logging.info(received_msg.format(datetime.now().time(), ip))
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":

    show_command = ["show interface status", "sh mac address-table | inc 400"]
    start_time = datetime.now()
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level = logging.INFO)

    with open('device.yaml', 'r') as f:
        try:
            all_device = yaml.safe_load(f)
            for list_device in all_device:
                # for name_device in list_device.keys():
                for name_device, device in list_device.items():
                    int_status_result = send_show_command(device, show_command)

### Findrestart_portport in 400 vlan ###
                    list_connected_port_vlan400 = re.findall('Gi\w+/\w+/\w+' + '\D+' + 'connected' + '\s+400', int_status_result['show interface status'])

### Parse str from show interface status
                    port_list = []
                    for full_list_port in list_connected_port_vlan400:
                        a = re.search('Gi\w+/\w+/\w+', full_list_port)
                        port_list.append(a.group())

###  Mac addres table for vlan 400 ###
                    list_mac_addr_table = list(set(re.findall('Gi\w+/\w+/\w+', int_status_result["sh mac address-table | inc 400"])))

### Sort list. Find port whithout mac-address ###
                    no_mac_address_port = []
                    for sort_port_connected in port_list:
                        if (sort_port_connected in list_mac_addr_table) != True:
                           no_mac_address_port.append(sort_port_connected)

### Restart port ####
                    if no_mac_address_port:
                      port_for_reset = ''
                      for port in no_mac_address_port:
                           port_for_restart = port
                           restart_port = send_conf_command(device, ['int' + port_for_reset, 'shutdown', 'no shutdown'])
                        # pprint(port_for_reset, width=120)
                        # pprint(list_mac_addr_table, width=120)
                        # pprint(list_mac_addr_table, width=120)

        except yaml.YAMLError as exc:
            print(exc)

        print(datetime.now() - start_time)
        pprint(no_mac_address_port, width=120)
