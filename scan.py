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

def scan_parse():
	"""scan_parse should be able to handle any format for the iwlist output data"""
	scanstr = """sudo iwlist %s scanning""" %  (ifsetup.name,)
	try:
		scanresult = subprocess.check_output([scanstr], shell=True)
	except:
		return []			# Failed scan, return nothing
	scanlist = scanresult.split('- Address: ')

	if len(scanlist) == 0:			# Nothing there?
		return []

	retlist = []
	for entry in scanlist:
		entry_ssid = ''
		entry_mode = ''
		entry_encryption = ''
		entry_method = []
		entry_signal = ''
		els = entry.split('\n')	# Break it into lines
		for ln in els:

			if ln.find('ESSID:') != -1:
				entry_ssid = ln.split('ESSID:')[1][1:-1]

			if ln.find('Mode:') != -1:
				entry_mode = ln.split('Mode:')[1]

			if ln.find('Encryption key:') != -1:
				entry_encryption = ln.split('Encryption key:')[1]

			if ln.find('IE:') != -1:
				newmethod = ln.split('IE:')[1]
				if newmethod.find('Unknown:') == -1:
					entry_method.append(newmethod[1:])

			if ln.find('Signal level=') != -1:
				entry_signal = ln.split('Signal level=')[1]
				#entry_signal = netlevel.split(' ')[0]

		# Only add real entries
		if len(entry_ssid) > 0:
			retlist.append({ "ssid": entry_ssid, "mode": entry_mode, "encryption": entry_encryption, "method": entry_method, "signal": entry_signal })

	return retlist

if __name__ == '__main__':
    result = scan_parse()
    print result
