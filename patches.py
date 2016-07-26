# -*- coding: utf-8 -*-
import os
import sys
from _winreg import *

def gtk_trayicon_dpi():
	# Patching libgtk-3-0.dll for 16px or 32px TrayIcon Output
	# File Size win32 dll: 6453248
	# File Size win64 dll: 6675968
	gtkfile = "%s\\libgtk-3-0.dll" % (os.getcwd())
	if os.path.exists(gtkfile) and sys.platform == "win32":
		# Check filesize to detect 32 or 64bit dll
		offset = False
		filesize = os.path.getsize(gtkfile)
		if filesize == 6675968:
			offset = 0x3D051
			version = "win64"
		if filesize == 6453248:
			offset = 0x3E4E2
			version = "win32"
		# Get Windows DPI Scaling Factor from Registry (96 = 100%, 120 = 125%)
		# When reg key = False, use standard 16px output
		if not offset == False:
			print "Found: %s [%s]" % (gtkfile,version)
			pixel = "\x10"
			pixeldez = "16"
			RawKey = False
			try:
				Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
				RawKey = OpenKey(Registry, "Control Panel\Desktop")
			except:
				pass
			try:
				if not RawKey == False:
					i = 0
					while 1:
						name, value, type = EnumValue(RawKey, i)
						if name == "LogPixels":
							if value > 96:
								pixel = "\x20"
								pixeldez = "32"
							if value == 96:
								pass
							break
						i += 1
			except:
				pass
			
			# Patching
			try:
				with open(gtkfile,'r+b') as f:
						f.seek(offset)
						if not f.read(1) == pixel:
							print "Patch TrayIcon Output Size to: %s pixel" % (pixeldez)
							f.seek(offset)
							f.write(pixel)
			except:
				return False
		else:
			print "No compatible gtk-3-0.dll found"
	return True
