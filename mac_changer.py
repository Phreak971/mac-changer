#!/usr/bin/env python
 
import subprocess
import argparse
import re
import random

def randomWord():
    word = random.choice([chr(number) for number in range(97,103)])
    return word

def randomNum():
    return random.choice(range(0,10))

def randomAlphaNum():
    word = randomWord()
    number = randomNum()
    choices = [f'{word}{number}', f'{number}{word}']
    return random.choice(choices)

def get_mac_addr():
    mac_dict = [randomAlphaNum() for i in range(0,5)]
    mac_address = '00:' + ':'.join(mac_dict)
    return mac_address


def get_arguments():
    argument_parser = argparse.ArgumentParser(description='Change the MAC Address')
    argument_parser.add_argument('--interface', metavar='interface', default='eth0', type=str, help='Network Interface of which MacAddress is to be changed')
    argument_parser.add_argument('--mac_addr', metavar='mac_addr', type=str, help="New MacAddress")
    return argument_parser.parse_args()

def get_current_mac_addr(interface):
    res = subprocess.check_output(['ifconfig', interface])
    mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(res))
    if mac_addr:
        return mac_addr.group(0)
    else:
        print("Couldn't find the mac address")
        return None

def change_mac(interface, mac_addr): 
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    try:
        subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', mac_addr])
    except Exception as e:
        print(f"Error occurred changing mac address > {e}" )


def main():
    args = get_arguments()
    if args.mac_addr:
        new_mac_addr = args.mac_addr
    else:
        new_mac_addr = get_mac_addr()
    mac_addr = get_current_mac_addr(args.interface)
    if mac_addr:
        print(f"Your current mac address is {mac_addr}")
        print(f"Changing the Mac address to {new_mac_addr}")
        change_mac(args.interface, new_mac_addr)

    mac_addr = get_current_mac_addr(args.interface)
    if new_mac_addr == mac_addr: 
        print(f"MacAddress was succesfully changed to {mac_addr}")

if __name__ == "__main__":
    main()


