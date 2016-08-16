# -*- coding: utf-8 -*-
import os, subprocess, sys

# .py file imports
from debug import debug

import release_version


#self.OPENVPN_FILEHASHS = {"openvpn-install-2.3.11-I601-x86_64.exe": {"libeay32.dll": "8a96ddc451110b84ef7bad7003222de593fa6b44757093b13076404b9d92b9de5050196885dbbdff0335cd527d0821f83d9ff3cb610ab7c5aa2ebc7c6afc7cbe", "openvpn.exe": "e94cb06e44a17d2e0a4d884cee2253d960b8a41dcd191340a3f5be12888c4936d8a8a60e5f13604fd8bbac66df7350d8773391e4432697a5b3b1a3d0662837e9", "openvpnserv.exe": "3c86a89a163c2f7d043f692883d51ff6e1c2bd77801fefcd4e5458bfd0473863223d8ebdcf573fdbe64753b0071e505e285ab08a52d4925a1b0a6ce24d80a7d7", "liblzo2-2.dll": "5de56ee903501e84a4f8f988c7deb6d24b34e5b2ff4cf51e9e80cdcbc5a4710639bd7f6e559fdd2df7ae29d83bf7c58c41e74c5c4f7ddab7faf15df0353d0b05", "openvpn-gui.exe": "3c8d174dcfb71b6ce750bc7460bd4f0ab6b4e0bba8305253658fc4e02fb74fa1d737ca9e290a64818bea48857ecfb66b7af720c673e3f2d9f7eba206799aae8f", "libpkcs11-helper-1.dll": "f1ac4d5eed3a97b8cd9c5b053c6f3ea8fc7e2b25d1a9adead3b8a198bee9dea7237c07dd2d2561aeebed62aac318d90b321b73729b81f00a03f10b45eda56480", "ssleay32.dll": "a9384fd0ded117e3c27f988ea35109e7843b929edf79473ad0e485b5d0285660676fd9b9c43458de007dd142aedf9fdea75a2a7bdb9b7b600edee392d18bf90e", "openssl.exe": "7c6699cf02f3b1d017b867855935019f2d50fe6b4d49c79de06a7e40663d29dd955a7f6bfb7836aa2e52dde4d817712b6e46650a2a10f5958a81338b4106be1b"}, "openvpn-install-2.3.11-I601-i686.exe": {"libeay32.dll": "592475e0b0286914d697f36fff8af7b3e265342787d945c7fe9e234a7cfbd84a13e757850fe7588a382a83c5f59e0046f91aed1736d4c06181d180e33aced806", "openvpn.exe": "dfbad890037291a534da7c534b49ec70ecc9a044ee0d8508654696819d88b5b4845b81b2e1aecd5475dc62e0d9a0d1c147524c70940a4e96c4e1530e257758d6", "openvpnserv.exe": "6dc640730a5724de687b805699e51595a1f08b16bc1596564b89cd580deee7478113a4296c3de677f96d4501f4f40a4e36d7d4c1f6993d4dbb7199b0e6edfa14", "liblzo2-2.dll": "31b744a57105d122d2150b5ab793620b73dbc28788be8484fa682e1cf6857f01102034e220b63d5709f6baa44b547df94e2c8aad6b5124b91e105e42d258e40b", "openvpn-gui.exe": "dab26e87d66d65e727733e16f3234585f44f8ebbf969c9fd20d4fc55a973820cecfb6218e1b5da98eecdae111473a839cab7b128687808676801bce25558c4c2", "libpkcs11-helper-1.dll": "bd7339e3911ab75ddf805555e0f59e65927f1539a5561b22456e25f3d1868fb42d89cd95eaa96c3335fef7d3ec2a21ff7c53f04961fedc5e374f43f4070df58c", "ssleay32.dll": "440cf92524e21e9dc1d92f45a8fbd566f0eeec597e0f52a235847879bdd4806ac219b592aaec9976620082b2d8d5690d432e1a45b0df035b18404453530855d9", "openssl.exe": "49d274c5f4ccddda28751a1a6271888c32188a192b9ad9c224832b51af0b474225d75c6ac51e61438b7a9f956b1ba78fef7a5392759a3d38fc4ddd1d7772e464"}}

def values(DEBUG):
	debug(9,"[openvpn.py] def values()",DEBUG,True)
	try:
		ARCH = get_arch(DEBUG)
		BUILT = "May 10 2016"
		LATEST = "2311"
		TIMESTAMP = 1462831200
		VERSION = "2.3.11"
		BUILT_V = "I601"
		
		SHA_512 = {
			"i686" : "b6c1e5d9dd80fd6515d9683044dae7cad13c4cb5ac5590be4116263b7cde25e0fef1163deb5a1f1ad646e5fdb84c286308fa8af288692b9c7d4e2b7dbff38bbe",
			"x86_64" : "a59284b98e80c1cd43cfe2f0aee2ebb9d18ca44ffb7035b5a4bb4cb9c2860039943798d4bb8860e065a56be0284f5f23b74eba6a5e17f05df87303ea019c42a3"
			}
			
		F_SIZES = {
			"i686": 1738368,
			"x86_64": 1837808
			}
			
		URLS = {
			"REM" : "https://%s/files/openvpn" % (release_version.org_data()["VCP_DOMAIN"]),
			"ALT" : "https://swupdate.openvpn.net/community/releases"
			}
		
		SETUP_FILENAME = "openvpn-install-%s-%s-%s.exe" % (VERSION,BUILT_V,ARCH)
		OPENVPN_DL_URL =  "%s/%s" % (URLS["REM"],SETUP_FILENAME)
		OPENVPN_DL_URL_ALT = "%s/%s" % (URLS["ALT"],SETUP_FILENAME)
		
		return {
				"ARCH":ARCH, "BUILT":BUILT, "LATEST":LATEST, "TIMESTAMP":TIMESTAMP, "VERSION":VERSION, "BUILT_V":BUILT_V, 
				"SHA_512":SHA_512, "F_SIZES":F_SIZES, "SETUP_FILENAME":SETUP_FILENAME,
				"URLS":URLS, "OPENVPN_DL_URL":OPENVPN_DL_URL, "OPENVPN_DL_URL_ALT":OPENVPN_DL_URL_ALT,
				}
	except:
		debug(1,"[openvpn.py] def values: failed",DEBUG,True)
		sys.exit()

def supported_platforms(DEBUG):
	debug(9,"[openvpn.py] def supported_platforms()",DEBUG,True)
	return [ "AMD64", "x86" ]

def get_arch(DEBUG):
	debug(9,"[openvpn.py] def get_arch()",DEBUG,True)
	data = os_platform(DEBUG)
	if data == "AMD64":
		ARCH = "x86_64"
	elif data == "x86":
		ARCH = "i686"
	else:
		sys.exit()
	debug(9,"[openvpn.py] def get_arch: ARCH = '%s'" % (ARCH),DEBUG,True)
	return ARCH

def os_platform(DEBUG):
	debug(9,"[openvpn.py] def os_platform()",DEBUG,True)
	true_platform = os.environ['PROCESSOR_ARCHITECTURE']
	try:
		true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
	except KeyError:
		pass
		#true_platform not assigned to if this does not exist
	if true_platform in supported_platforms(DEBUG):
		debug(9,"[openvpn.py] def os_platform: true_platform = '%s'" % (true_platform),DEBUG,True)
		return true_platform
	else:
		debug(1,"[openvpn.py] def os_platform: true_platform = '%s' NOT SUPPORTED" % (true_platform),DEBUG,True)
		sys.exit()

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
		
		if not OPENVPN_DIR == False and os.path.isdir(OPENVPN_DIR):
			OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
			if os.path.isfile(OPENVPN_EXE):
				return { "OPENVPN_DIR":OPENVPN_DIR,"OPENVPN_EXE":OPENVPN_EXE }
	except:
		debug(1,"[openvpn.py] def win_detect_openvpn: failed",DEBUG,True)
	debug(1,"[openvpn.py] def win_detect_openvpn: return False",DEBUG,True)
	return False

def win_detect_openvpn_version(DEBUG,OPENVPN_EXE):
	# returns True or False
	OVPN_LATEST = values(DEBUG)["LATEST"]
	OVPN_LATEST_BUILT = values(DEBUG)["BUILT"]
	OVPN_LATEST_BUILT_TIMESTAMP = values(DEBUG)["TIMESTAMP"]
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
	debug(1,"[openvpn.py] def win_detect_openvpn_version: return False",DEBUG,True)
	return False

def list_openvpn_files(DEBUG,OPENVPN_DIR,type):
	debug(1,"[openvpn.py] def list_openvpn_files()",DEBUG,True)
	try:
		dir = OPENVPN_DIR
		if os.path.exists(dir):
			content = os.listdir(dir)
			list = []
			for file in content:
				if file.endswith(type):
					list.append(file)
			if len(list) >= 1:
				debug(1,"[openvpn.py] def list_openvpn_files: dir '%s', files = '%s'" % (dir,len(list)),DEBUG,True)
				return list
		else:
			debug(1,"[openvpn.py] def list_openvpn_files: dir '%s' not found!" % (dir),DEBUG,True)
	except:
		debug(1,"[openvpn.py] def list_openvpn_files: failed",DEBUG,True)
	debug(1,"[openvpn.py] def list_openvpn_files: return False",DEBUG,True)
	return False


"""
def upgrade_openvpn(DEBUG):
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