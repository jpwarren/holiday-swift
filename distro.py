#!/usr/bin/python
#
"""
Simple Wifi Tools - MooresCloud prototype implementation
module distro - determines the LINUX distribution being used
Right now, choices are ARCH and DEBIAN, and that's it.

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '0.01-dev'
__license__ = 'MIT'

import os.path

# All of this is going inline, so that when the module is loaded, this information is globally available.
# distro.name is thename, distro.isarch and distro.isdeb are booleans

archpath = """/etc/arch-release"""
debpath = """/etc/debian_version"""

isarch = False
isdeb = False

if os.path.exists(archpath):
	name = 'ARCH'
	isarch = True
else:
	if os.path.exists(debpath):
		name = 'DEBIAN'
		isdeb = True
	else:
		name = 'undefined'

if __name__ == '__main__':
	print name, isarch, isdeb