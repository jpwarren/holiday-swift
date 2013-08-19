#!/usr/bin/python
#
"""
Simple Wifi Tools - MooresCloud prototype implementation
module join - handles joining wireless networks

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '0.01-dev'
__license__ = 'MIT'

import subprocess, ifsetup, distro, time, json, threading

def join_deb(ssid, password):
    """Attempt to join a wireless network using Debian (Raspberry Pi)
    Note that this completely rewrites /etc/network/interfaces,
    Which is a very rude thing to do, and we won't, in the longer run.
    We will likely need to parse the file and just make wifi-specific changes.
    Plus, it probably only works for WPA networks, not WEP. Probably."""

    interfaces_base = """auto lo
iface lo inet loopback
 
auto eth0
iface eth0 inet dhcp

auto wlan
iface wlan inet dhcp
"""
    interfaces_ssid = """   wpa-ssid: "%s" 
""" % ssid
    interfaces_psk = """    wpa-psk: "%s" 
""" % password
    interfaces_text = interfaces_base + interfaces_ssid + interfaces_psk

    # Ok go and overwrite the /etc/network/interfacess file (do we need privleges for this?)
    f = open("/etc/network/interfaces", "w")
    f.write(interfaces_text)
    f.close()

    # Now restart the networking. Theoretically this will all work seamlessly.
    result = subprocess.check_output(["sudo", "service", "networking", "--full-restart"])
    return result   


def join(ssid, password=''):
    """join will attempt to join wifi network SSID using the given credential
    These are done on separate threads so the web server doesn't time out on us.
    Because apparently it does.""" 
    if distro.isdeb:
        t1 = threading.Thread(target=join_deb, args = (ssid,password))
        t1.daemon = True
        t1.start()
        #result = join_deb(ssid,password)
        return True

    if distro.isarch:
        result = join_arch(ssid, password)
        return result

def join_arch(ssid, password):
    """Join an Arch Linux (Holiday) wireless network"""

    wpa_supplicant_base = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
fast_reauth=1
"""
    wpa_supplicant_network = """network={
priority=10
ssid="%s" """ % ssid
    if len(password) > 0:
        wpa_supplicant_network_rest = """
psk="%s" 
}
""" % password 
    else:
        wpa_supplicant_network_rest = """
key_mgmt=NONE 
}
"""
    wpa_supplicant_text = wpa_supplicant_base + wpa_supplicant_network + wpa_supplicant_network_rest

    # Ok go and overwrite the wpa_supplicant.conf file (do we need privleges for this?)
    f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
    f.write(wpa_supplicant_text)
    f.close()

    # Restart the wpa_supplicant process - somehow?
    result = subprocess.check_output(["sudo","wpa_cli","reconfigure"])
    #result = subprocess.check_output(["sudo","wpa_cli","reconfigure"])

    # kill dhcpcd, then restart it (DHCP only)
    try:
        dhcpkill = subprocess.check_output(["sudo", "killall", "dhcpcd"])
    except:
        print "Maybe dhcpcd isn't running"
    time.sleep(3)   # Just to let things simmer down a bit
    dhcpcdstart = subprocess.check_output(["sudo", "dhcpcd", ifsetup.name])

    return result

if __name__ == '__main__':
    while True:
        print "joining Terazzo Vecchio..."
        join('Terazzo Vecchio', 'DelNuovo')
        print "Joined."
        time.sleep(120)
        print "joining Moores4G"
        join('Moores4G', '10634791')
        print "Joined."
        time.sleep(120)