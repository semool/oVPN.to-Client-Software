# -*- coding: utf-8 -*-
import os
import sys, shutil, struct
from _winreg import *
from ctypes import *

BITS = struct.calcsize("P") * 8

def select_gtkdll():
	pixel = 16
	gtkfile = "%s\\libgtk-3-0.dll" % (os.getcwd())
	gtkfile16 = "%s\\libgtk-3-0-16.dll" % (os.getcwd())
	gtkfile32 = "%s\\libgtk-3-0-32.dll" % (os.getcwd())

	try:
		LOGPIXELSX = 88
		DC = windll.user32.GetDC(None)
		dpi = windll.gdi32.GetDeviceCaps(DC, LOGPIXELSX)
		windll.user32.ReleaseDC(None, DC)
		if dpi > 96:
			pixel = 32
		if dpi == 96:
			pixel = 16
		print "Get DPI from DC: %s" % dpi
	except:
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
							pixel = 32
						if value == 96:
							pixel = 16
						break
					i += 1
				print "Get DPI from REG: %s" % value
		except:
			pass

	try:
		print "pixel = '%s'" % (pixel)
		if pixel == 32:
			print "pixel is 32"
			if os.path.isfile(gtkfile32):
				print "gtkfile --> gtkfile16"
				shutil.move(gtkfile, gtkfile16)
				print "restore gtkfile32 --> gtkfile"
				shutil.move(gtkfile32, gtkfile)
			else:
				print "select_gtkdll not needed: gtkfile32 not found"
		if pixel == 16:
			print "pixel is 16"
			if os.path.isfile(gtkfile16):
				print "gtkfile --> gtkfile32"
				shutil.move(gtkfile, gtkfile32)
				print "gtkfile16 --> gtkfile"
				shutil.move(gtkfile16, gtkfile)
			else:
				print "select_gtkdll not needed: gtkfile16 not found"
	except:
		print "select_gtkdll failed"
