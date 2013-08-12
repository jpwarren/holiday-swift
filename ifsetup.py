#!/usr/bin/python
#
"""
Simple Wifi Tools - MooresCloud prototype implementation
module ifsetup - determines the name of the wireless interface

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '0.01-dev'
__license__ = 'MIT'

import subprocess

# All of this is going inline, so that when the module is loaded, this information is globally available.
# If the interface doesn't include 'wlan' in it, there will be trouble. But why would that happen?

try:
	result = subprocess.check_output(["ifconfig | grep wlan"], shell=True)
	if len(result) > 0:
		name = result.split()[0]
		if (name[-1] == ':'):
			name = name[0:-1]
	else:
		name = 'undefined'
except:
	name = 'undefined'

if __name__ == '__main__':
	print name