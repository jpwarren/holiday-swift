#!/usr/bin/python
#
"""
Simple Wifi Tools - MooresCloud prototype implementation
module swift - main module, handles RESTful interface 

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '0.01-dev'
__license__ = 'MIT'

import json
from bottle import Bottle, run, static_file, post, request
import ssid

app = Bottle()

class Swift():
	"""The Swift class will eventually handle all of the methods needed to manage WiFi networks"""

	def __init__(self,bottle):
		"""Must pass the instanced Bottle app object in order for the routes to insert correctly
		Those routes are instanced here, in a fancy function-within-a-function declaration"""
		if bottle == None:
			self.app = Bottle()
		else:
			self.app = bottle

		@self.app.get('/iotas/swift/scan')
		def scan():
			"""Scan the networks, return in a list of JSON tuples (network name, encryption status)"""
			scan_data = ssid.new_scan()
			return scan_data

		@self.app.put('/iotas/swift/join')
		def join():
			"""Join a network with the given name (SSID) and password"""

			# First we need to fish that information out of the JSON that was sent along with this
			d = request.body.read()
			if len(d) == 0:
				return json.dumps({"success": False})
			try:
				dj = json.loads(d)
			except:
				print "Bad JSON data, aborting..."
				return json.dumps({"success": False})
			if 'ssid' in dj:
				ssid_value = dj['ssid']
			else:
				print "Missing SSID"
				return json.dumps({"success": False})
			if 'password' in dj:
				passwd = dj['password']  # Salted, I hope
			else:
				print "Missing password"
				return json.dumps({"success": False})

			# And here we should be able to join the network maybe
			print "Joining %s" % ssid_value
			#ssid.join(ssid_value,password)
			return json.dumps({"success": True})

if __name__ == '__main__':

	# From here we can run a test if we like.
	# But mainly this is for integration into IoTAS as a module
	# So we won't normally use this entry point.

	sw = Swift(bottle=None)

	the_srv = 'wsgiref'  
	
	# Try to run on port 8011, if that fails, go to 8080
	try:
		sw.app.run(host='0.0.0.0', port=8011, debug=False, server=the_srv)
	except:
		print "No port available, exiting..."

