#!/usr/bin/python
#
"""
Simple Wifi Tools - MooresCloud prototype implementation
module ssid - handles the SSID scans and setting

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '0.01-dev'
__license__ = 'MIT'

import subprocess, ifsetup, distro, time, json

def new_scan():
	"""new_scan gets all the data and formats it into a nice object to be sent somewhere"""
	scanstr = """sudo iwlist %s scanning""" %  (ifsetup.name,)
	scanresult = subprocess.check_output([scanstr], shell=True)
	scanlist = scanresult.split('\n')[1:-1]
	retlist = []
	for ln in scanlist:
		if ln.find('ESSID:') != -1:
			netname = ln.split('ESSID:')[1]
			netmethod = []
			#print netname[1:-1]
		if ln.find('Mode:') != -1:
			netmode = ln.split('Mode:')[1]
		if ln.find('Encryption key:') != -1:
			netsec = ln.split('Encryption key:')[1]
			#print netsec
		if ln.find('IE:') != -1:
			newmethod = ln.split('IE:')[1]
			#print "newmethod %s" % newmethod[1:]
			if newmethod.find('Unknown:') == -1:
				#print "appending"
				netmethod.append(newmethod[1:])
		if ln.find('Signal level=') != -1:
			netlevel = ln.split('Signal level=')[1]
			netlevel = netlevel.split(' ')[0]
			entry = { "ssid": netname[1:-1], "mode": netmode, "encryption": netsec, "method": netmethod, "signal": netlevel }
			retlist.append(entry)

	return json.dumps({"scan": retlist})

def scan():
	"""scan() will perform a scan of the wireless interface and return a list of the visible networks"""
	scanstr = """sudo iwlist %s scanning | grep -Po '".*?"' """ %  (ifsetup.name,)
	scanresult = subprocess.check_output([scanstr], shell=True)
	scanlist = scanresult.split('\n')[:-1]
	resultlist = []
	for ssid in scanlist:
		resultlist.append(ssid[1:-1])
	return resultlist

def join(ssid, password=''):
	"""join will attempt to join wifi network SSID using the given credential""" 
	if distro.isarch:
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
		time.sleep(3)	# Just to let things simmer down a bit
		dhcpcdstart = subprocess.check_output(["sudo", "dhcpcd", ifsetup.name])

		return result

	else:
		if distro.isdeb:
			interfaces_base = """auto lo

iface lo inet loopback
iface eth0 inet dhcp

auto wlan

iface wlan inet dhcp
"""
			interfaces_ssid = """	wpa-ssid: "%s"
""" % ssid
			interfaces_psk = """	wpa-psk: "%s"
""" % password
		interfaces_text = interfaces_base + interfaces_ssid + interfaces_psk

		# Ok go and overwrite the /etc/network/interfacess file (do we need privleges for this?)
		f = open("/etc/network/interfaces", "w")
		f.write(interfaces_text)
		f.close()

		# Now restart the networking. Theoretically this will all work seamlessly.
		result = subprocess.check_output(["sudo", "service", "networking", "--full-restart"])
		return result		

if __name__ == '__main__':
	#print scan()
	#print join("Optus 4G Wifi E589 4A23", "10634791")
    #print join("TTHS_2EB87D","8847A64F47")
    result = new_scan()
    print result
