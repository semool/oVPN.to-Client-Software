
import os, sys, time
BOOTTIME = time.time()

SOURCEDIR="E:\\Persoenlich\\ovpn-client"

LOGLEVEL = 1
LOGLEVELS = [0,1,2,3]

DEBUGcount = 0
DEBUGfrombefore = False

def debug(level,text,istrue,bindir):
	if bindir == False:
		print "DEBUG: %s" % (text)
		return False
	cmddir = os.getcwd()
	if cmddir.endswith("system32"):
		if os.path.exists(SOURCEDIR):
			bindir=SOURCEDIR
		else:
			print "DEBUG: %s" % (text)
			return False

 
	logfile = "%s\\client_debug.log" % (bindir)
	global DEBUGcount
	global DEBUGfrombefore
	if not level in LOGLEVELS:
		return False
	elif not level <= LOGLEVEL:
		return False
	timefromboot = round(time.time() - BOOTTIME,3)
	debugstringsht = False
	debugstringsht1 = False
	debugstringsht2 = False
	if DEBUGcount > 0 and not DEBUGfrombefore == text:
		debugstringsht1 = "(%s):(d1) %s (repeat: %s)" % (timefromboot, DEBUGfrombefore,DEBUGcount)
		debugstringsht2 = "(%s):(d2) %s" % (timefromboot,text)
		if level > 0:
			print(debugstringsht1)
			print(debugstringsht2)
		DEBUGcount = 0
	elif DEBUGcount >= 4096 and DEBUGfrombefore == text:
		debugstringsht = "(%s):(d3) %s (repeated: %s e2)" % (timefromboot, DEBUGfrombefore,DEBUGcount)
		if level > 0:
			print("%s" % (debugstringsht))
		DEBUGcount = 0
	elif DEBUGfrombefore == text:
		DEBUGcount += 1
		return
	elif not DEBUGfrombefore == text:
		debugstringsht = "(%s):(d4) %s"%(timefromboot,text)
		if level > 0:
			print("%s" % (debugstringsht))
	DEBUGfrombefore = text
	if istrue == True:
		if not debugstringsht == False:
			write_debug(level,debugstringsht,timefromboot,logfile)
		if not debugstringsht1 == False:
			write_debug(level,debugstringsht1,timefromboot,logfile)
		if not debugstringsht2 == False:
			write_debug(level,debugstringsht2,timefromboot,logfile)

def write_debug(level,string,timefromboot,logfile):
	try:
		localtime = time.asctime(time.localtime(time.time()))
		debugstringlog = "%s (%s):(d5,%s) %s" % (localtime,timefromboot,level,string)
		dbg = open(logfile,'a')
		dbg.write("%s\n" % (debugstringlog))
		dbg.close()
	except:
		print("def write_debug: write to %s failed"%(DEBUGLOG))