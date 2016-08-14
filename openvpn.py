# -*- coding: utf-8 -*-
import os, subprocess
from debug import debug

def win_detect_openvpn(DEBUG,OPENVPN_EXE):
	# returns [ OPENVPN_DIR, OPENVPN_EXE ]
	try:
		debug(1,"[openvpn.py] def win_detect_openvpn()",DEBUG,True)
		if OPENVPN_EXE == False:
			debug(1,"[openvpn.py] def win_detect_openvpn: check programfiles",DEBUG,True)
			programfiles = [ "PROGRAMFILES", "PROGRAMFILES(x86)", "PROGRAMW6432" ]
			for getenv in programfiles:
				programfiles_dir = os.getenv(getenv)
				file = "%s\\OpenVPN\\bin\\openvpn.exe" % (programfiles_dir)
				if os.path.isfile(file):
					debug(1,"[openvpn.py] def win_detect_openvpn: '%s'" % (file),DEBUG,True)
					OPENVPN_DIR = "%s\\OpenVPN\\bin" % (programfiles_dir)
					break
		else:
			try:
				OPENVPN_DIR = OPENVPN_EXE.rsplit('\\', 1)[0]
			except:
				return False
		
		if OPENVPN_DIR == False:
			return False
		elif not os.path.isdir(OPENVPN_DIR):
			return False
		else:
			OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
			if not os.path.isfile(OPENVPN_EXE):
				return False
			else:
				return { "OPENVPN_DIR":OPENVPN_DIR,"OPENVPN_EXE":OPENVPN_EXE }
	except:
		debug(1,"[openvpn.py] def win_detect_openvpn: failed",DEBUG,True)
		return False

def win_detect_openvpn_version(DEBUG,OPENVPN_EXE,OVPN_LATEST,OVPN_LATEST_BUILT,OVPN_LATEST_BUILT_TIMESTAMP):
	debug(1,"[openvpn.py] def win_detect_openvpn_version()",DEBUG,True)
	if not os.path.isfile(OPENVPN_EXE):
		debug(1,"[openvpn.py] def win_detect_openvpn_version: OPENVPN_EXE not found",DEBUG,True)
		return False
	try:
		out, err = subprocess.Popen("\"%s\" --version" % (OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()
	except:
		#self.msgwarn(_("Could not detect openVPN Version!"),_("Error"))
		return False
	try:
		OVPN_VERSION = out.split('\r\n')[0].split( )[1].replace(".","")
		OVPN_BUILT = out.split('\r\n')[0].split("built on ",1)[1].split()
		OVPN_LATESTBUILT = OVPN_LATEST_BUILT.split()
		debug(1,"OVPN_VERSION = %s, OVPN_BUILT = %s, OVPN_LATESTBUILT = %s" % (OVPN_VERSION,OVPN_BUILT,OVPN_LATESTBUILT),DEBUG,True)
		if OVPN_VERSION >= OVPN_LATEST:
			debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_VERSION '%s' >= OVPN_LATEST '%s': True"%(OVPN_VERSION,OVPN_LATEST),DEBUG,True)
			if len(OVPN_BUILT) == 3 and len(OVPN_LATESTBUILT) == 3:
				STR1 = str(OVPN_BUILT[0]+OVPN_BUILT[1]+OVPN_BUILT[2])
				STR2 = str(OVPN_LATESTBUILT[0]+OVPN_LATESTBUILT[1]+OVPN_LATESTBUILT[2])
				if STR1 == STR2:
					debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_BUILT '%s' == OVPN_LATESTBUILT '%s': True"%(OVPN_BUILT,OVPN_LATESTBUILT),DEBUG,True)
					return True
				else:
					built_mon = OVPN_BUILT[0]
					built_day = int(OVPN_BUILT[1])
					built_year = int(OVPN_BUILT[2])
					builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
					string_built_time = time.strptime(builtstr,"%b/%d/%Y")
					built_month_int = int(string_built_time.tm_mon)
					built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					if built_timestamp > OVPN_LATEST_BUILT_TIMESTAMP:
						debug(1,"[openvpn.py] def win_detect_openvpn_version: built_timestamp '%s' > OVPN_LATEST_BUILT_TIMESTAMP '%s': True" % (built_timestamp,OVPN_LATEST_BUILT_TIMESTAMP),DEBUG,True)
						return True
		else:
			debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_VERSION '%s' too old"%(OVPN_VERSION),DEBUG,True)
	except:
		debug(1,"[openvpn.py] def win_detect_openvpn_version: failed",DEBUG,True)
	return False

"""
def upgrade_openvpn(DEBUG):
	pass

def list_openvpn_files(DEBUG,type):
	pass

def openvpn_filename_exe(self):
	pass

def openvpn_check_files(DEBUG,OPENVPN_DIR):
	pass

def openvpn_check_file_hashs(DEBUG,type):
	pass

def build_openvpn_dlurl(self):
	pass

def load_openvpnbin_from_remote(self):
	pass

def verify_openvpnbin_dl(self):
	pass

def win_install_openvpn(self):
	pass

def extract_ovpn(self):
	pass

def win_select_openvpn(self):
	pass

def win_detect_openvpn_version(self):
	pass

def find_signtool(self):
	pass

def signtool_verify(self,file):
	pass
"""