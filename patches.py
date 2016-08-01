# -*- coding: utf-8 -*-
import os
import sys, shutil, struct
from _winreg import *

BITS = struct.calcsize("P") * 8

def select_gtkdll():
	gtkfile = "%s\\libgtk-3-0.dll" % (os.getcwd())
	gtkfile16 = "%s\\libgtk-3-0-16.dll" % (os.getcwd())
	gtkfile32 = "%s\\libgtk-3-0-32.dll" % (os.getcwd())
	try:
		Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
		RawKey = OpenKey(Registry, "Control Panel\Desktop")
	except:
		pass
	try:
		pixel = False
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
		
		if not pixel == False:
			print "pixel = '%s'" % (pixel)
			if pixel == 32 and not os.path.isfile(gtkfile16):
				print "pixel is 32 and no gtkfile16 found"
				if os.path.isfile(gtkfile):
					print "backup gtkfile to gtkfile16"
					shutil.copyfile(gtkfile, gtkfile16)
				if os.path.isfile(gtkfile32):
					print "found pre-patched gtkfile32, copy to gtkfile"
					shutil.copyfile(gtkfile32, gtkfile)
			elif pixel == 16 and os.path.isfile(gtkfile16):
				print "pixel is 16 and gtkfile16 exists, restore gtkfile16 to gtkfile"
				shutil.copyfile(gtkfile16, gtkfile)
		else:
			if os.path.isfile(gtkfile16):
				print "pixel is False and gtkfile16 exists, restore gtkfile16 to gtkfile"
				shutil.copyfile(gtkfile16, gtkfile)
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
	
	

