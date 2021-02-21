from pprint import pprint
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

def send_show_command(device, commands):
    int_status = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                int_status[command] = output
        return int_status
    except (NetmikoTimeoutException,NetmikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":
    device = {
        "device_type": "cisco_ios",
        "ip": "172.20.254.7",
        "username": "admin",
        "password": "Ciscocisco777",
        "secret": "Ciscocisco777",
        "port": 22,
    }

    int_status = send_show_command(device, ["show interface status", "sh mac address-table | inc 400"])

### Findrestart_portport in 400 vlan ###
    list_connected_port_vlan400 = re.findall('Gi\w+/\w+/\w+' + '\D+' + 'connected' + '\s+400', int_status["show interface status"]) ### Parse str from show interface status
    port_list = []
    for full_list_port in list_connected_port_vlan400:
        a = re.search('Gi\w+/\w+/\w+', full_list_port)
        port_list.append(a.group())

###  Mac addres table for vlan 400 ###
    list_mac_addr_table = list(set(re.findall('Gi\w+/\w+/\w+', int_status["sh mac address-table | inc 400"])))

### Sort list. Find port whithout mac-address ###
    no_mac_address_port = []
    for sort_port_connected in port_list:
        if (sort_port_connected in list_mac_addr_table) != True:
                no_mac_address_port.append(sort_port_connected)

    print(no_mac_address_port)

### Restart port ####
    if no_mac_address_port:
        port_for_reset = ''
        for port in no_mac_address_port:
            port_for_restart = port
            restart_port = send_show_command(device, ['conf t', 'int' + port_for_reset, 'shutdown', 'no shutdown'])


    #pprint(restart_port, width=120)
    #pprint(list_mac_addr_table, width=120)
    #pprint(list_mac_addr_table, width=120)
