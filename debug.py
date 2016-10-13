# -*- coding: utf-8
import os, sys, time, locale
BOOTTIME = time.time()

LOGLEVEL = 1
LOGLEVELS = []

DEBUGcount = 0
DEBUGfrombefore = False

def devdir():
	dir = "E:\\Persoenlich\\ovpn-client"
	return dir

def getmode(MODE):
	if len(sys.argv) > 1:
		for arg in sys.argv:
			if arg == MODE:
				print("sys.argv %s" % MODE)
				return True
	return False

def devmode():
	return getmode("DEVMODE")


def debug(level,text,DEBUG,bindir):
	try:
		if bindir == False or level <= 0:
			print("DEBUG: %s" % (text))
			return False
		bindir = os.getcwd()
		if bindir.endswith("system32"):
			if os.path.exists(devdir()):
				bindir=devdir()
			else:
				print("DEBUG: %s" % (text))
				return False
		
		logfile = "%s\\client_debug.log" % (bindir)
		global DEBUGcount
		global DEBUGfrombefore
		
		if level > LOGLEVEL:
			if not level in LOGLEVELS:
				return False
		
		timefromboot = round(time.time() - BOOTTIME,3)
		tempdebuglist = list()
		if DEBUGcount > 0 and not DEBUGfrombefore == text:
			debugstringsht1 = "(%s):(d1) %s (repeat: %s)" % (timefromboot, DEBUGfrombefore,DEBUGcount)
			debugstringsht2 = "(%s):(d2) %s" % (timefromboot,text)
			tempdebuglist.append(debugstringsht1)
			tempdebuglist.append(debugstringsht2)
			DEBUGcount = 0
		elif DEBUGcount >= 4096 and DEBUGfrombefore == text:
			debugstringsht = "(%s):(d3) %s (repeated: %s e2)" % (timefromboot, DEBUGfrombefore,DEBUGcount)
			tempdebuglist.append(debugstringsht)
			DEBUGcount = 0
		elif DEBUGfrombefore == text:
			DEBUGcount += 1
			return
		elif not DEBUGfrombefore == text:
			debugstringsht = "(%s):(d4) %s"%(timefromboot,text)
			tempdebuglist.append(debugstringsht)
		DEBUGfrombefore = text
		if len(tempdebuglist) > 0:
			for entry in tempdebuglist:
				print(entry)
				if DEBUG == True:
					debug_cache(entry,'add')
					write_debug(level,entry,timefromboot,logfile)
	except Exception as e:
		print("[debug.py] debug failed, exception = '%s'" % (e))

def debug_cache(entry,query):
	global DEBUGcache
	
	try:
		cachesize = len(DEBUGcache)
	except Exception as e:
		print("creating debug cache")
		DEBUGcache = list()
		cachesize = 0
	
	if cachesize >= 4096:
		DEBUGcache.pop(0)
	
	if query == "add":
		DEBUGcache.append(entry)
		#print("added debug entry to cache")
	if query == "get":
		return DEBUGcache

def write_debug(level,string,timefromboot,logfile):
	try:
		localtime = time.asctime(time.localtime(time.time()))
		debugstringlog = "%s (%s):(d5,%s) %s" % (localtime,timefromboot,level,string)
		dbg = open(logfile,'a')
		dbg.write("%s\n" % (debugstringlog))
		dbg.close()
	except:
		print("def write_debug: write to %s failed"%(logfile))