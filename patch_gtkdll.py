
import os, shutil, struct
from _winreg import *
BITS = struct.calcsize("P") * 8


def patch_gtkdll():
	unsigned_dir = "includes\\DLL\\%s\\unsigned" % (BITS)
	gtkfile = "%s\\libgtk-3-0.dll" % (unsigned_dir)
	gtkfile32 = "%s\\libgtk-3-0-32.dll" % (unsigned_dir)
	gtkfile32tmp = "%s.tmp" % (gtkfile32)
	if os.path.exists(gtkfile):
		if BITS == 32:
			offset = 0x3E4E2 # win32
		if BITS == 64:
			offset = 0x3D051 # win64
		
		pixel_16 = "\x10"
		pixel_32 = "\x20"
		
		if os.path.exists(gtkfile32):
			print "delete alread patched file '%s' before patching" % (gtkfile32)
			return False
		
		try:
			with open(gtkfile,'r+b') as f1:
				f1.seek(offset)
				checkoffset = f1.read(1)
				f1.close()
				if checkoffset == pixel_16:
					shutil.copyfile(gtkfile, gtkfile32tmp)
			
			with open(gtkfile32tmp,'r+b') as f2:
				f2.seek(offset)
				checkoffset = f2.read(1)
				if checkoffset == pixel_16:
					print "write pixel to file '%s'"  % (gtkfile32tmp)
					f2.seek(offset)
					f2.write(pixel_32)
				f2.close()
			shutil.move(gtkfile32tmp, gtkfile32)
			print "move tmp file to '%s'"  % (gtkfile32)
		except:
			print "patch_gtkdll() failed"
	
	else:
		print "gtkfile '%s' not found" % (gtkfile)

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
			if pixel == 32 and not os.path.isfile(gtkfile16):
				if os.path.isfile(gtkfile):
					shutil.copyfile(gtkfile, gtkfile16)
				if os.path.isfile(gtkfile32):
					shutil.copyfile(gtkfile32, gtkfile)
					return True
			elif pixel == 16 and os.path.isfile(gtkfile16):
				shutil.copyfile(gtkfile16, gtkfile)
				return True
	except:
		print "select_gtkdll failed"


#patch_gtkdll()

select_gtkdll()