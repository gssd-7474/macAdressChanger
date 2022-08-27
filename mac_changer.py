#!/usr/bin/env python

import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC')
    parser.add_option('-m', '--mac', dest='macAdd', help='New Mac address value')
    (options, arguments)  = parser.parse_args()
    if not options.interface:
        parser.error("[-] please provide a inteface")
    elif not options.macAdd:
        parser.error("[-] please provide a mac address")
    return options

def change_mac(interface, macAdd):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", macAdd])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+]Changing Mac Adress for "+interface+" to "+macAdd)

def get_current_mcc_add(interface):
    ifconfig_check = subprocess.check_output(["ifconfig", interface])
    macADD_check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_check))
    if macADD_check:
        return macADD_check.group(0)
    else:
        print("[-]could not read mac address.")

options = get_args()

current_mac = get_current_mcc_add(options.interface)
print("[+]Current Mac: "+str(current_mac))

change_mac(options.interface, options.macAdd)
current_mac = get_current_mcc_add(options.interface)
if current_mac == options.macAdd:
    print("[+]Mac Address was successfully changed to: "+current_mac)
else:
    print("[-]Mac Address did not get changed")
