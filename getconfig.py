#! /usr/bin/python3

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime

import yaml
import netmiko

def send_show(device, show):
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(show)
        return result






if __name__ == "__main__":