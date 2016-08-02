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

def gtk_trayicon_dpi():
	return
	# Patching libgtk-3-0.dll for 16px or 32px TrayIcon Output
	gtkfile = "%s\\libgtk-3-0.dll" % (os.getcwd())
	gtkfile16 = "%s\\libgtk-3-0-16.dll" % (os.getcwd())
	gtkfile32 = "%s\\libgtk-3-0-32.dll" % (os.getcwd())

	if os.path.exists(gtkfile) and sys.platform == "win32":
		pixel = "\x10"
		pixeldez = "16"
		RawKey = False
		offset_one = 0x3E4E2 # win32
		offset_two = 0x3D051 # win64

		# Get Windows DPI Scaling Factor from Registry (96 = 100%, 120 = 125%)
		# When reg key = False, use standard 16px output
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
					f.seek(offset_one)
					checkoffset = f.read(1)
					if checkoffset == "\x10" or checkoffset == "\x20":
						offset = offset_one
					else:
						f.seek(offset_two)
						checkoffset = f.read(1)
						if checkoffset == "\x10" or checkoffset == "\x20":
							offset = offset_two
					
			if not checkoffset == pixel:
				Patch = True
				if os.path.exists(gtkfile16) or os.path.exists(gtkfile32):
					Patch = False
				if pixel == "\x20":
					if os.path.exists(gtkfile32):
						print "Set TrayIcon Output Size to: %s pixel" % (pixeldez)
						shutil.move(gtkfile, gtkfile16)
						shutil.move(gtkfile32, gtkfile)
				if pixel == "\x10":
					if os.path.exists(gtkfile16):
						print "Set TrayIcon Output Size to: %s pixel" % (pixeldez)
						shutil.move(gtkfile, gtkfile32)
						shutil.move(gtkfile16, gtkfile) 
				if Patch == True:
					with open(gtkfile,'r+b') as f:
						print "Patch TrayIcon Output Size to: %s pixel" % (pixeldez)
						f.seek(offset)
						f.write(pixel)
		except:
			return False
	else:
		return False
	return True
	
	

