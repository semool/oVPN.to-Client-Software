# -*- coding: utf-8 -*-
import os, time, subprocess, sys, json
from datetime import datetime

# .py file imports
from debug import debug
from debug import devmode
import release_version
import hashings
import signtool
import shlex
import win32process

def values(DEBUG):
	debug(9,"[openvpn.py] def values()",DEBUG,True)
	try:
		ALLOWED_VERSIONS = [ "2312" ]
		ARCH = get_arch(DEBUG)
		BUILT = "Oct 3 2016"
		LATEST = "2312"
		TIMESTAMP = 1475445600
		VERSION = "2.3.12"
		BUILT_V = "I602"
		
		OPENVPN_FILEHASHS = {
								"openvpn-install-2.3.12-I602-i686.exe": {"libeay32.dll": "068083ce5c94430e5ea57e46969094526769fe14b08880a691ac097d57b29a4b6b6dafc2dbebb3bea499482371c5c427d01b2cef33ce50f5b98a5fadc03e54f8", "openvpn.exe": "13f8cf1dd0a9bc1d6cd7aeaf4ffd33c3021f6b028321dabf732ce2138faf1398921d8537a62f7d1846accb8c0f164e3652ba52a4e6e3a5788b9c6c1bd73c9a18", "openvpnserv.exe": "4893892a69cb569cd723aab1cbf8a66a294f4e0eb7b4fe9bcc3211e578b46c9adece4cfd8baeba8cb254b0f205b0608011d8c4f6d4b5e01e60f0ebc9d6933e1d", "liblzo2-2.dll": "98487bc4c6f6479358866dc8b7adfccce63c2df92ded4097a7fa7867fd2a3459be154e99bef671efaa55b59b77bedc0a9a86c69efb7548022b6b6fb499e400a5", "openvpn-gui.exe": "773fb28465bd2c473f3c08904a8523afed6bdc07721b470d73058c928c6c06eecbd3d291be49c36fea4d96adc6c50a1e22e9bbb6bd5128c61a62fa1bc2c8e484", "libpkcs11-helper-1.dll": "4f19a0aac0dcd7acbd1340351cb8bf810fed214965987ae1a0777aead5a4f3c402d2016c1cb0bfd450a50321b0bfa743c8d05634df5caca24340d1007aad411d", "ssleay32.dll": "b34616ea203867c437850b33c4c0af8d93df696cd82923526f897257b9cce61e0c62df5df96f11aa843e9aeaf62b59d45dc9b025548cb00de2b07e9e26652bbc", "openssl.exe": "a3ba2e16026ce42576f76ab97c0944295755b739bb3ba53cc39187017aaf352f02930a12b1645fde658e21ee4d27c5d2d96ee2cbf6f55140c7336dfd2eb9dc35"}, 
								"openvpn-install-2.3.12-I602-x86_64.exe": {"libeay32.dll": "9acbad57bdb0698d63e2fde83b3195f4ab3ee3142d4b8165d216ef4644bd25767c5ef6340b99b410ad16d374f81ad81eafeda0bea99ae8512a01947dd513a684", "openvpn.exe": "a1375d645cecebd96634efe65dda5391731c0667f94f2f08f4ed12aab5c6698a7401c0565a0f9d4767058d3eb1960ead7c987f04e4b689939c23486b66faac7b", "openvpnserv.exe": "31648f863af49ab0a1a3bd89cfb1ed52ec224c72803e8d3913025f696668502995ea593d991938781d659f40c2a327d503cb259cc5a3c6cd356b14e77482b1d7", "liblzo2-2.dll": "d405228a8123bb91da798a4a564d79a9635cdd1e87d881d619fc057300421d9cb672d37440c609a00a5004d981d6058a839ff9742d453850bcdd79b5f8c2947e", "openvpn-gui.exe": "077dee49370823c842833c4b12d411febec29403b1ead88bf365c215d7929eedbb16a685c71447d78bfaa5ca4a842f19bf0694bdf406db6714913012fe32def8", "libpkcs11-helper-1.dll": "6399762e061c692aac820dcd1406dff8c45fcd74ffbba1d59bb0a9f4a6d6b7f5dc777f0d620cdb3386a945992df0d2c61a74f12800189619c882f5d09bdf43b0", "ssleay32.dll": "de0dcb6dea2569dc4dc5f9b4a26014e583e9f2a7544f609b6fb41e101273b529ce16c3a313b601d9efdf27a6cb86cec6e83f7e7af0143b105c3c0a2986d5d4d6", "openssl.exe": "7e46409a1903a6a873b8e62487e0e47009b1cd53320023fadc2212e3eeff438d125174100308bf673062125def995729cb3521efc82e88c9ad8ae0f826049548"}, 
							}
		
		
		SHA_512 = {
			"i686" : "0d6503300d2b9c9a1cb3b4e0af24528227c6b1d0e72c7b99ef070177fcfa1b1711a2a718df615e5be89d20376fe955481232c39848c5434fd63cd591f9d9711c",
			"x86_64" : "988870a8e8277282b5fb064379594a5fd618456676ad06d1be74311754cb270c62e411aba78db6b7be08a9d31ea4e66b313373a9a461894d57f99efe870f94ca"
			}
			
		F_SIZES = {
			"i686": 1742632,
			"x86_64": 1840304
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
				"OPENVPN_FILEHASHS":OPENVPN_FILEHASHS,
				"ALLOWED_VERSIONS":ALLOWED_VERSIONS
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

def win_get_openvpn_version(DEBUG,OPENVPN_DIR):
	OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
	if not os.path.isfile(OPENVPN_EXE):
		debug(1,"[openvpn.py] def win_get_openvpn_version: OPENVPN_EXE not found",DEBUG,True)
		return False
	try:
		cmdstring = '"%s" --version' % (OPENVPN_EXE)
		cmdargs = shlex.split(cmdstring)
		p = subprocess.Popen(cmdargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags = win32process.CREATE_NO_WINDOW)
		out, err = p.communicate()
		rc = p.returncode
		OVPN_VERSION = out.decode('utf-8').split('\r\n')[0].split( )[1].replace(".","")
		OVPN_BUILT = out.decode('utf-8').split('\r\n')[0].split("built on ",1)[1].split()
		debug(1,"[openvpn.py] def win_get_openvpn_version: OVPN_VERSION = '%s', OVPN_BUILT = '%s'"%(OVPN_VERSION,OVPN_BUILT),DEBUG,True)
		return [ OVPN_VERSION, OVPN_BUILT ]
	except Exception as e:
		debug(1,"[openvpn.py] def win_get_openvpn_version: failed, exception = '%s'"%(e),DEBUG,True)
	return False

def win_detect_openvpn_version(DEBUG,OPENVPN_DIR):
	try:
		debug(1,"[openvpn.py] def win_detect_openvpn_version()",DEBUG,True)
		OVPN_LATEST = values(DEBUG)["LATEST"]
		OVPN_LATEST_BUILT = values(DEBUG)["BUILT"].split()
		OVPN_LATEST_BUILT_TIMESTAMP = values(DEBUG)["TIMESTAMP"]
		DATA = win_get_openvpn_version(DEBUG,OPENVPN_DIR)
		if not DATA == False:
			OVPN_VERSION = DATA[0]
			OVPN_BUILT = DATA[1]
		else:
			debug(1,"[openvpn.py] def win_detect_openvpn_version: failed, DATA == False",DEBUG,True)
			return False
		debug(1,"OVPN_VERSION = %s, OVPN_BUILT = %s, OVPN_LATEST_BUILT = %s" % (OVPN_VERSION,OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
		if OVPN_VERSION >= OVPN_LATEST:
			debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_VERSION '%s' >= OVPN_LATEST '%s': True"%(OVPN_VERSION,OVPN_LATEST),DEBUG,True)
			if len(OVPN_BUILT) == 3 and len(OVPN_LATEST_BUILT) == 3:
				STR1 = str(OVPN_BUILT[0]+OVPN_BUILT[1]+OVPN_BUILT[2])
				STR2 = str(OVPN_LATEST_BUILT[0]+OVPN_LATEST_BUILT[1]+OVPN_LATEST_BUILT[2])
				if STR1 == STR2:
					debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_BUILT '%s' == OVPN_LATEST_BUILT '%s': True"%(OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
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
				debug(1,"[openvpn.py] def list_openvpn_files: dir '%s', files = '%s', list = '%s'" % (dir,len(list),list),DEBUG,True)
				return list
		else:
			debug(1,"[openvpn.py] def list_openvpn_files: dir '%s' not found!" % (dir),DEBUG,True)
	except:
		debug(1,"[openvpn.py] def list_openvpn_files: failed",DEBUG,True)
	debug(1,"[openvpn.py] def list_openvpn_files: return False",DEBUG,True)
	return False

def check_files(DEBUG,OPENVPN_DIR):
	debug(1,"[openvpn.py] def check_files()",DEBUG,True)
	
	if check_file_hashs(DEBUG,OPENVPN_DIR,".exe") == True:
		if check_file_hashs(DEBUG,OPENVPN_DIR,".dll") == True:
			return True
	else:
		# openvpn.exe hash failed, search signtool
		if not signtool.find_signtool(DEBUG) == False:
			# check exe signatures
			files = list_openvpn_files(DEBUG,OPENVPN_DIR,".exe")
			if files == False:
				return False
			for file in files:
				filepath = "%s\\%s" % (OPENVPN_DIR,file)
				if not signtool.signtool_verify(DEBUG,filepath):
					return False
			# check dll signatures
			files = list_openvpn_files(DEBUG,OPENVPN_DIR,".dll")
			if files == False:
				return False
			for file in files:
				filepath = "%s\\%s" % (OPENVPN_DIR,file)
				if not signtool.signtool_verify(DEBUG,filepath):
					return False
			# all file signatures verified
			return True
	debug(1,"[openvpn.py] def check_files: failed",DEBUG,True)
	return False

def check_file_hashs(DEBUG,OPENVPN_DIR,type):
	debug(1,"[openvpn.py] def check_file_hashs(%s)"%(type),DEBUG,True)
	#if devmode() == True:
	#	debug(1,"[openvpn.py] def check_file_hashs: DEVMODE ! force signature check",DEBUG,True)
	#	return False
	types = [ ".exe", ".dll" ]
	if not type in types:
		debug(1,"[openvpn.py] def check_file_hashs: type '%s' invalid"%(type),DEBUG,True)
		return False
	try:
		content = list_openvpn_files(DEBUG,OPENVPN_DIR,type)
		if content == False:
			return False
		try:
			filename = values(DEBUG)["SETUP_FILENAME"]
			try:
				hashs = values(DEBUG)["OPENVPN_FILEHASHS"][filename]
			except:
				return False
			
		except:
			debug(2,"[openvpn.py] def check_file_hashs: filename/hashs failed",DEBUG,True)
			sys.exit()
		
		debug(2,"[openvpn.py] filename = '%s' hashs = '%s'"%(filename,hashs),DEBUG,True)
		for file in content:
			debug(2,"[openvpn.py] def check_file_hashs: file = '%s'" % (file),DEBUG,True)
			filepath = "%s\\%s" % (OPENVPN_DIR,file)
			hasha = hashings.hash_sha512_file(DEBUG,filepath)
			debug(2,"[openvpn.py] def check_file_hashs: hasha = '%s'" % (hasha),DEBUG,True)
			try:
				hashb = hashs[file]
			except:
				return False
			if hasha == hashb:
				debug(2,"[openvpn.py] def check_file_hashs: hash file = '%s' OK!" % (file),DEBUG,True)
			else:
				debug(1,"[openvpn.py] def check_file_hashs: hash file = '%s' failed" % (file),DEBUG,True)
				return False
		return True
	except:
		debug(1,"[openvpn.py] def check_file_hashs: failed",DEBUG,True)
		sys.exit()
		return False

"""
def upgrade_openvpn(DEBUG):
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