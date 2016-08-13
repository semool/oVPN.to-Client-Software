# -*- coding: utf-8 -*-
import os
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

"""
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

def upgrade_openvpn(self):
	pass

def load_openvpnbin_from_remote(self):
	pass

def verify_openvpnbin_dl(self):
	pass

def win_install_openvpn(self):
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