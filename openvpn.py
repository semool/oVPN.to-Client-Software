# -*- coding: utf-8 -*-
import os, time, subprocess, sys
from datetime import datetime

# .py file imports
from debug import debug
from debug import devmode
import release_version
import hashings
import signtool


#self.OPENVPN_FILEHASHS = {"openvpn-install-2.3.11-I601-x86_64.exe": {"libeay32.dll": "8a96ddc451110b84ef7bad7003222de593fa6b44757093b13076404b9d92b9de5050196885dbbdff0335cd527d0821f83d9ff3cb610ab7c5aa2ebc7c6afc7cbe", "openvpn.exe": "e94cb06e44a17d2e0a4d884cee2253d960b8a41dcd191340a3f5be12888c4936d8a8a60e5f13604fd8bbac66df7350d8773391e4432697a5b3b1a3d0662837e9", "openvpnserv.exe": "3c86a89a163c2f7d043f692883d51ff6e1c2bd77801fefcd4e5458bfd0473863223d8ebdcf573fdbe64753b0071e505e285ab08a52d4925a1b0a6ce24d80a7d7", "liblzo2-2.dll": "5de56ee903501e84a4f8f988c7deb6d24b34e5b2ff4cf51e9e80cdcbc5a4710639bd7f6e559fdd2df7ae29d83bf7c58c41e74c5c4f7ddab7faf15df0353d0b05", "openvpn-gui.exe": "3c8d174dcfb71b6ce750bc7460bd4f0ab6b4e0bba8305253658fc4e02fb74fa1d737ca9e290a64818bea48857ecfb66b7af720c673e3f2d9f7eba206799aae8f", "libpkcs11-helper-1.dll": "f1ac4d5eed3a97b8cd9c5b053c6f3ea8fc7e2b25d1a9adead3b8a198bee9dea7237c07dd2d2561aeebed62aac318d90b321b73729b81f00a03f10b45eda56480", "ssleay32.dll": "a9384fd0ded117e3c27f988ea35109e7843b929edf79473ad0e485b5d0285660676fd9b9c43458de007dd142aedf9fdea75a2a7bdb9b7b600edee392d18bf90e", "openssl.exe": "7c6699cf02f3b1d017b867855935019f2d50fe6b4d49c79de06a7e40663d29dd955a7f6bfb7836aa2e52dde4d817712b6e46650a2a10f5958a81338b4106be1b"}, "openvpn-install-2.3.11-I601-i686.exe": {"libeay32.dll": "592475e0b0286914d697f36fff8af7b3e265342787d945c7fe9e234a7cfbd84a13e757850fe7588a382a83c5f59e0046f91aed1736d4c06181d180e33aced806", "openvpn.exe": "dfbad890037291a534da7c534b49ec70ecc9a044ee0d8508654696819d88b5b4845b81b2e1aecd5475dc62e0d9a0d1c147524c70940a4e96c4e1530e257758d6", "openvpnserv.exe": "6dc640730a5724de687b805699e51595a1f08b16bc1596564b89cd580deee7478113a4296c3de677f96d4501f4f40a4e36d7d4c1f6993d4dbb7199b0e6edfa14", "liblzo2-2.dll": "31b744a57105d122d2150b5ab793620b73dbc28788be8484fa682e1cf6857f01102034e220b63d5709f6baa44b547df94e2c8aad6b5124b91e105e42d258e40b", "openvpn-gui.exe": "dab26e87d66d65e727733e16f3234585f44f8ebbf969c9fd20d4fc55a973820cecfb6218e1b5da98eecdae111473a839cab7b128687808676801bce25558c4c2", "libpkcs11-helper-1.dll": "bd7339e3911ab75ddf805555e0f59e65927f1539a5561b22456e25f3d1868fb42d89cd95eaa96c3335fef7d3ec2a21ff7c53f04961fedc5e374f43f4070df58c", "ssleay32.dll": "440cf92524e21e9dc1d92f45a8fbd566f0eeec597e0f52a235847879bdd4806ac219b592aaec9976620082b2d8d5690d432e1a45b0df035b18404453530855d9", "openssl.exe": "49d274c5f4ccddda28751a1a6271888c32188a192b9ad9c224832b51af0b474225d75c6ac51e61438b7a9f956b1ba78fef7a5392759a3d38fc4ddd1d7772e464"}}

def values(DEBUG):
	debug(9,"[openvpn.py] def values()",DEBUG,True)
	try:
		ARCH = get_arch(DEBUG)
		BUILT = "Aug 23 2016"
		LATEST = "2312"
		TIMESTAMP = 1471903200
		VERSION = "2.3.12"
		BUILT_V = "I601"
		
		OPENVPN_FILEHASHS = {
							"openvpn-install-2.3.12-I601-x86_64.exe": {"libeay32.dll": "fdd2733eec8942c3257c57a96bd0bf5057347219d2038c50d149a379f5483e4e8d6145b80176de81855ef06151314dec6dc8c165c038f01a3af917d5098a67c6", "openvpn.exe": "6f41709c969c9264c001720b99a11597cfa6c9e82601c75707cf79e7b7ec80da034e4862b732fb9c9eb2c7dd39f815e3ce7619eb25d3c96f8cb21582f370df78", "openvpnserv.exe": "7bd2e8216977a44dabaaa5035841ce44bd7612c7a30396ee89be500a08e6d612486de17e53297a19474f1c4a38ea529d2870c45c91dd6a9f88ca0314857ec588", "liblzo2-2.dll": "ea9a4855d6cdd4faf16a8feedf17c0c8fcef300d82553b0928c2371ea7fd20eb23be3ae20c9e99f1ed2781a7dfbd7e45d85f9690bae83fc945ef0da2e61502fc", "openvpn-gui.exe": "ec31005c3552316e7de45c96a16234a169cb8988d34f42d95166ff0ff981321d984c4d81e32d0651cfd8ecfdfd30f084019b02cf296d8192168e221fc6fb0a3f", "libpkcs11-helper-1.dll": "84d709127c9f76844d47cf4a8ea531c2b334a8576b7bc0a761f490848794f3d72d077fe708e34bd3410b0cce7ca85f0681877c561b147290983c34ac28cebd80", "ssleay32.dll": "36218cf83f47d50ac7e21c84e937dc5c1aaccafe97353bf47f8a1a65d6f264afa9fd01de9cffa0d8d7c2387000678c82f2fad1a8e17d238d68bdad9964730e0d", "openssl.exe": "e123610f484f87b245ccad8fedfc4a7f2accd5d428509936ff52695f2da4f20f8e1d90a77bfcc5c158cb08d3dfaf9f791e049bfaad547399f85cea0fd83c9354"},
							"openvpn-install-2.3.12-I601-i686.exe": {"libeay32.dll": "e91b836cfbb2f425d3ea19e33bfcd8c476513fe1bf52e91492730291ef43238593959b470b5105ca3d876a1bfb15cc9e55880693048356a40c44dbc62d6b3d0e", "openvpn.exe": "003384b8402a8162b72897a65c6d76e6a6bbc4e62fc4c890e8410d51fb5651418cdb8c109c9264b5f1d26c2be40fa3c3e6f1461141c50be98d89ffdbf716926a", "openvpnserv.exe": "ca39ad042af6f40850b8e2e2c03f591459bc9228a17fe46c55c9f78c8c4419c957bf33d413e5b0e1be07224b7810fbbe9768fc48a2dd2da8f66eb936e4689664", "liblzo2-2.dll": "3c487a7baefe6f28e028147e02b30de149d920e3e136f5e4724ae69cb29d09f6e9881357d2a9f189f6dc6d8296888127891ac1a610c22c7da84028f5a7c5c938", "openvpn-gui.exe": "0006aa07334ac3c2f435faad054c08f00ba0dcb39809f50613fef0065fce6fa1dda973c0a01f4dc48e99cbd3034a414a84c9d4eb7762d770ae1033cd3ef4357e", "libpkcs11-helper-1.dll": "d3cd573a65e4a29db5f7f33ee5207400a55c06fcc0bc8bd388659ac3d7bc656b128dbd6939be6cc64bf4c054ff160edaa85e50c5247c446001f22d3212bcaa33", "ssleay32.dll": "86cb78444bf2a548d2f285318cdd064cec978b299c462e665a3c80e14a46bee03396c220bbdb7a62fef6bff15fc636bfc21934d1e06e78a0bc3d0b0a5b2dbf34", "openssl.exe": "aee5d0fb211b030ef48434b68445fdea3f9a865e8bd61e30ebbb9adeb98620b1dec2282fb4c2f3492e7645514677c794434853a0c04bbae9fce1291a5e1f8b93"}
							}
		
		SHA_512 = {
			"i686" : "44226c0a623c9c16e9590e212de1e728dc368757f00dc433eb1d586edf89fbfbe8e43d6300271b73b3d5751563fbec5b43eb9ce29d4ac9dbf2aff9571f19eecc",
			"x86_64" : "49fbc53570b9dfe0bc1e84905deffc440fddd2f1a6fbec801d34d4eec1262668eaf36a2397c289737f26b0ec033ce7cb601662ef35cb526b66688b71130819ad"
			}
			
		F_SIZES = {
			"i686": 1739400,
			"x86_64": 1837928
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
				"OPENVPN_FILEHASHS":OPENVPN_FILEHASHS
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
	if devmode() == True:
		debug(1,"[openvpn.py] def check_file_hashs: DEVMODE ! force signature check",DEBUG,True)
		return False
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
			debug(1,"[openvpn.py] filename = '%s' hashs = '%s'"%(filename,hashs),DEBUG,True)
		except:
			debug(1,"[openvpn.py] def check_file_hashs: filename/hashs failed",DEBUG,True)
			sys.exit()
		
		debug(2,"def check_file_hashs: hashs = '%s'" % (hashs),DEBUG,True)
		for file in content:
			if file.endswith(type):
				filepath = "%s\\%s" % (OPENVPN_DIR,file)
				hasha = hashings.hash_sha512_file(DEBUG,filepath)
				try:
					hashb = hashs[file]
				except:
					return False
				if hasha == hashb:
					debug(1,"[openvpn.py] def check_file_hashs: hash file = '%s' OK!" % (file),DEBUG,True)
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