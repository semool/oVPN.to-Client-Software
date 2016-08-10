# -*- coding: utf-8 -*-
import hashlib, os, requests, subprocess, sys, struct, time, zipfile
from datetime import datetime as datetime
from ConfigParser import SafeConfigParser
# .py files imports

try:
	import debug
	import release_version
except:
	print "imports failed"

def CDEBUG(level,text,istrue,bindir):
	debug.debug(level,text,istrue,bindir)

try:
	
	CLIENTVERSION = "%s" % (release_version.version_data()["VERSION"])
	CLIENT_STRING = "%s %s" % (release_version.version_data()["NAME"],CLIENTVERSION)
	VCP_DOMAIN = release_version.org_data()["VCP_DOMAIN"]
	API_DOMAIN = release_version.org_data()["API_DOMAIN"]
	API_URL = "https://%s:%s/%s" % (API_DOMAIN,release_version.org_data()["API_PORT"],release_version.org_data()["API_POST"])
	print CLIENTVERSION
	print CLIENT_STRING
	print API_URL
	
	try:
		BITS = struct.calcsize("P") * 8
		if BITS == 32:
			import release_hard32
			BUILT_STRING = release_hard32.builtdate()
		elif BITS == 64:
			import release_hard64
			BUILT_STRING = release_hard64.builtdate()
		else:
			sys.exit()
	except: 
		BUILT_STRING = "(UNDEFINED)"
	print BUILT_STRING

except:
	print "import release_version failed"
	sys.exit()

class CMDLINE:
	def __init__(self):
		if self.self_vars():
			if self.read_options_file():
				if not self.USERID == False and not self.APIKEY == False:
					self.debug(1,"Read Options File: OK")
					if self.API_REQUEST("auth"):
						self.debug(1,"API Login OK!")
						self.check_certdl()
						self.debug(1,"sleeping 15 seconds before exit")
						time.sleep(15)
				else:
					self.debug(1,"def __init__: config file '%s' created, please edit and enter your login credentials!" % (self.OPT_FILE))

	def self_vars(self):
		self.DEBUG = False
		self.USERID = False
		self.APIKEY = False
		self.APIURL = API_URL
		self.LAST_CFG_UPDATE = 0
		
		self.OVPN_CONFIGVERSION = "23x"
		self.CONFIGVERSIONS = [ "23x", "23x46", "23x64" ]
		
		self.OVPN_CONFIGSOSTYPE = "win"
		self.CONFIGSOSTYPES = [ "win", "lin", "mac", "and" ]
		
		self.BIN_DIR = os.getcwd()
		self.OPT_FILE = "%s\\ovpn_client_cmd.conf" % (self.BIN_DIR)
		
		BIN1 = "%s\\ovpn_client_cmd.exe" % (self.BIN_DIR)
		BIN2 = "%s\\ovpn_client_cmd.py" % (self.BIN_DIR)
		
		self.CA_FILE = "%s\\cacert_ovpn.pem" % (self.BIN_DIR)
		self.CA_FIXED_HASH = "f37dff160dda454d432e5f0e0f30f8b20986b59daadabf2d261839de5dfd1e7d8a52ecae54bdd21c9fee9238628f9fff70c7e1a340481d14f3a1bdeea4a162e8"
		
		if not self.load_ca_cert():
			return False
		
		if os.path.exists(BIN1) or os.path.exists(BIN2):
			pass
		else:
			self.debug(1,"def init_dirs: binary not found")
			return False
		return True

	def hash_sha512_file(self,file):
		self.debug(1,"def hash_sha512_file()")
		if os.path.isfile(file):
			hasher = hashlib.sha512()
			fp = open(file, 'rb')
			with fp as afile:
				buf = afile.read()
				hasher.update(buf)
			fp.close()
			return hasher.hexdigest()

	def load_ca_cert(self):
		self.debug(1,"def load_ca_cert()")
		if os.path.isfile(self.CA_FILE):
			self.CA_FILE_HASH = self.hash_sha512_file(self.CA_FILE)
			if self.CA_FILE_HASH == self.CA_FIXED_HASH:
				try:
					os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(self.BIN_DIR, self.CA_FILE)
					return True
				except:
					self.debug(1,"Error:\nSSL Root Certificate for %s not loaded %s" % (VCP_DOMAIN,self.CA_FILE))
					return False
			else:
				self.debug(1,"Error:\nInvalid SSL Root Certificate for %s in:\n'%s'\nhash is:\n'%s'\nbut should be '%s'" % (VCP_DOMAIN,self.CA_FILE,self.CA_FILE_HASH,self.CA_FIXED_HASH))
				return False
		else:
			self.debug(1,"Error:\nSSL Root Certificate for %s not found in:\n'%s'!" % (VCP_DOMAIN,self.CA_FILE))
			return False

	def read_options_file(self):
		self.debug(1,"def read_options_file()")
		if os.path.isfile(self.OPT_FILE):
			try:
				parser = SafeConfigParser()
				parser.read(self.OPT_FILE)
				
				try:
					self.DEBUG = parser.getboolean('oVPN','debugmode')
					self.debug(1,BUILT_STRING)
				except:
					self.debug(1,"def read_options_file: self.DEBUG failed")
					#return False
				
				try:
					USERID = parser.get('oVPN','userid')
					if USERID == "False":
						self.USERID = False
					else:
						self.USERID = USERID
				except:
					self.debug(1,"def read_options_file: self.USERID failed")
					#return False
				
				try:
					APIKEY = parser.get('oVPN','apikey')
					if APIKEY == "False":
						self.APIKEY = False
					else:
						if len(APIKEY) == 128:
							self.APIKEY = APIKEY
						else:
							self.APIKEY = False
				except:
					self.debug(1,"def read_options_file: self.APIKEY failed")
					#return False
				
				try:
					LAST_CFG_UPDATE = parser.getint('oVPN','lastcfgupdate')
					if not LAST_CFG_UPDATE >= 0:
						self.LAST_CFG_UPDATE = 0
					else:
						self.LAST_CFG_UPDATE = LAST_CFG_UPDATE
					self.debug(1,"def read_options_file: self.LAST_CFG_UPDATE = '%s'" % (self.LAST_CFG_UPDATE))
				except:
					self.debug(1,"def read_options_file: self.LAST_CFG_UPDATE failed")
					#return False
				
				try:
					ocfgv = parser.get('oVPN','configversion')
					if ocfgv.lower() in self.CONFIGVERSIONS:
						self.OVPN_CONFIGVERSION = ocfgv.lower()
					else:
						self.OVPN_CONFIGVERSION = "23x"
				except:
					self.debug(1,"def read_options_file: self.OVPN_CONFIGVERSION failed")
					return False
				
				try:
					configsostype = parser.get('oVPN','configsostype')
					if configsostype.lower() in self.CONFIGSOSTYPES:
						self.OVPN_CONFIGSOSTYPE = configsostype.lower()
					else:
						self.OVPN_CONFIGSOSTYPE = "win"
					self.debug(1,"def read_options_file: self.OVPN_CONFIGSOSTYPE = '%s'"%(self.OVPN_CONFIGSOSTYPE))
				except:
					self.write_options_file()
					self.debug(1,"def read_options_file: self.OVPN_CONFIGSOSTYPE failed, please restart")
					return False
					
					
				if len(sys.argv) > 1:
					try:
						if sys.argv[1].lower() in self.CONFIGSOSTYPES:
							self.OVPN_CONFIGSOSTYPE = sys.argv[1].lower()
							self.LAST_CFG_UPDATE = 0
							self.debug(1,"def read_options_file: self.OVPN_CONFIGSOSTYPE overwritten from sys.argv[1] = '%s'"%(sys.argv[1].lower()))
					except:
						pass
					
					try:
						if sys.argv[2].lower() in self.CONFIGVERSIONS:
							self.OVPN_CONFIGVERSION = sys.argv[2].lower()
							self.debug(1,"def read_options_file: self.OVPN_CONFIGVERSION overwritten from sys.argv[2] = '%s'"%(sys.argv[2].lower()))
					except:
						pass
					
				
				try:
					print self.OVPN_CONFIGVERSION
					if self.OVPN_CONFIGVERSION == "23x":
						self.VPN_CFG = "%s\\configs\\%s\\ip4" % (self.BIN_DIR,self.OVPN_CONFIGSOSTYPE)
					elif self.OVPN_CONFIGVERSION == "23x46":
						self.VPN_CFG = "%s\\configs\\%s\\ip46" % (self.BIN_DIR,self.OVPN_CONFIGSOSTYPE)
					elif self.OVPN_CONFIGVERSION == "23x64":
						self.VPN_CFG = "%s\\configs\\%s\\ip64" % (self.BIN_DIR,self.OVPN_CONFIGSOSTYPE)
					else:
						return False
					
					self.debug(1,"def read_options_file: self.OVPN_CONFIGVERSION = '%s'" % (self.OVPN_CONFIGVERSION))
					
					self.ZIP_CFG = "%s\\configs\\%s_%s_confs.zip" % (self.BIN_DIR,self.OVPN_CONFIGSOSTYPE,self.OVPN_CONFIGVERSION)
					self.ZIP_CRT = "%s\\configs\\%s_%s_certs.zip" % (self.BIN_DIR,self.OVPN_CONFIGSOSTYPE,self.OVPN_CONFIGVERSION)
					
					self.debug(1,"self.ZIP_CFG = '%s', self.ZIP_CRT = '%s'"%(self.ZIP_CFG,self.ZIP_CRT))
					
				except:
					self.debug(1,"def read_options_file: self.OVPN_CONFIGVERSION failed")
					return False
				
				if not os.path.isdir("%s\\configs"%(self.BIN_DIR)):
					os.mkdir("%s\\configs"%(self.BIN_DIR))
				
				if not os.path.isdir("%s\\configs\\%s"%(self.BIN_DIR,self.OVPN_CONFIGSOSTYPE)):
					os.mkdir("%s\\configs\\%s"%(self.BIN_DIR,self.OVPN_CONFIGSOSTYPE))
					
				if not os.path.isdir(self.VPN_CFG):
					os.mkdir(self.VPN_CFG)
					self.debug(1,"def read_options_file: created DIR self.VPN_CFG = '%s'"%(self.VPN_CFG))
				
				self.debug(1,"def read_options_file: return True")
				return True
			except:
				self.debug(1,"def read_options_file: failed")
		else:
			# We have no config file here at first start, set right values
			try:
				cfg = open(self.OPT_FILE,'wb')
				parser = SafeConfigParser()
				parser.add_section('oVPN')
				parser.set('oVPN','debugmode','%s'%(self.DEBUG))
				parser.set('oVPN','userid','%s'%(self.USERID))
				parser.set('oVPN','apikey','%s'%(self.APIKEY))
				parser.set('oVPN','lastcfgupdate','%s'%(self.LAST_CFG_UPDATE))
				parser.set('oVPN','configversion','%s'%(self.OVPN_CONFIGVERSION))
				parser.set('oVPN','configsostype','%s'%(self.OVPN_CONFIGSOSTYPE))
				parser.write(cfg)
				cfg.close()
				return True
			except:
				self.debug(1,"def read_options_file: create failed")
				sys.exit()

	def write_options_file(self):
		try:
			cfg = open(self.OPT_FILE,'wb')
			parser = SafeConfigParser()
			parser.add_section('oVPN')
			parser.set('oVPN','debugmode','%s'%(self.DEBUG))
			parser.set('oVPN','userid','%s'%(self.USERID))
			parser.set('oVPN','apikey','%s'%(self.APIKEY))
			parser.set('oVPN','lastcfgupdate','%s'%(self.LAST_CFG_UPDATE))
			parser.set('oVPN','configversion','%s'%(self.OVPN_CONFIGVERSION))
			parser.set('oVPN','configsostype','%s'%(self.OVPN_CONFIGSOSTYPE))
			parser.write(cfg)
			cfg.close()
			return True
		except:
			self.debug(1,"def read_options_file: create failed")
			sys.exit()

	def API_REQUEST(self,API_ACTION):
		self.debug(1,"def API_REQUEST(%s)"%(API_ACTION))
		if self.APIKEY == False:
			self.debug(1,"def API_REQUEST: No API-Key!")
			return False
		
		if API_ACTION == "auth":
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
			
		if API_ACTION == "lastupdate":
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		if API_ACTION == "getconfigs":
			if os.path.isfile(self.ZIP_CFG): os.remove(self.ZIP_CFG)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION, 'version' : self.OVPN_CONFIGVERSION, 'type' : self.OVPN_CONFIGSOSTYPE }
		
		if API_ACTION == "requestcerts":
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		if API_ACTION == "getcerts":
			if os.path.isfile(self.ZIP_CRT): os.remove(self.ZIP_CRT)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		self.body = False
		
		self.debug(1,"def API_REQUEST: API_ACTION = %s" % (API_ACTION))
		try:
			headers = False
			try:
				version = release_version.version_data()["VERSION"]
				versionint = 0
				
				try:
					split = version.split(".")
					versionint = "%s%s%s" % (split[0],split[1],split[2])
				except:
					self.debug(1,"def API_REQUEST: version.split failed")
				
				if versionint > 0:
					version = versionint
				user_agent = "clientcmd/%s" % (version)
				headers = { 'User-Agent':user_agent }
			except:
				self.debug(1,"def API_REQUEST: construct user-agent failed")
			
			if headers == False:
				try:
					r = requests.post(url=self.APIURL,data=values)
				except:
					self.debug(1,"def API_REQUEST: post without headers failed")#
					return False
			else:
				try:
					r = requests.post(url=self.APIURL,data=values,headers=headers)
				except:
					self.debug(1,"def API_REQUEST: post with headers failed")
					return False
			
			if API_ACTION == "getconfigs" or API_ACTION == "getcerts":
				self.body = r.content
			else:
				self.body = r.text
			
			if self.body == "AUTHERROR":
				self.debug(1,"Invalid User-ID or API-Key or Account expired!")
				return False
			elif API_ACTION == "auth" and self.body == "AUTHOK:True":
				self.debug(1,"API Login OK!")
				return True
			
			if self.body.isalnum() and len(self.body) <= 128:
				self.debug(1,"def API_REQUEST: self.body = %s"%(self.body))
		
		except:
			self.debug(1,"API requests on: '%s' failed!" % (API_ACTION))
			return False
		
		if not self.body == False:
			
			if not self.body == "AUTHERROR":
				self.curldata = self.body.split(":")
				if self.curldata[0] == "AUTHOK":
					self.curldata = self.curldata[1]
					self.debug(1,"def API_REQUEST: self.curldata = '%s'" % (self.curldata))
					return True
			else:
				self.debug(1,"Invalid User-ID or API-Key or Account expired!")
				self.body = False
				self.timer_check_certdl_running = False
				return False
			
			if API_ACTION == "getconfigs":
				if os.path.isfile(self.ZIP_CFG):
					os.remove(self.ZIP_CFG)
				try:
					fp = open(self.ZIP_CFG, "wb")
					fp.write(self.body)
					fp.close()
					return True
				except:
					return False
			
			elif API_ACTION == "getcerts":
				if os.path.isfile(self.ZIP_CRT):
					os.remove(self.ZIP_CRT)
				try:
					fp = open(self.ZIP_CRT, "wb")
					fp.write(self.body)
					fp.close()
					return True
				except:
					return False
			
			if API_ACTION == "requestcerts":
				if self.body == "ready" or self.body == "wait" or self.body == "submitted":
					return True

	def check_last_server_update(self,remote_lastupdate):
		self.debug(1,"def check_last_server_update(): self.LAST_CFG_UPDATE = '%s', remote_lastupdate = '%s'" % (self.LAST_CFG_UPDATE,remote_lastupdate))
		if self.LAST_CFG_UPDATE < int(remote_lastupdate):
			self.remote_lastupdate = remote_lastupdate
			self.debug(1,"def check_last_server_update: requesting update")
			return True
		else:
			self.debug(1,"def check_last_server_update: no update")
			return False

	def check_certdl(self):
		try:
			self.debug(1,"def inThread_timer_check_certdl()")
			if self.API_REQUEST(API_ACTION = "lastupdate"):
				self.debug(1,"def inThread_timer_check_certdl: API_ACTION lastupdate")
				if self.check_last_server_update(self.curldata):
					if self.API_REQUEST(API_ACTION = "getconfigs"):
						if self.API_REQUEST(API_ACTION = "requestcerts"):
							self.API_COUNTDOWN = 180
							LAST_requestcerts = 0
							while not self.body == "ready":
								if self.API_COUNTDOWN <= 0:
									self.msgwarn("Update took too long...aborted!\nPlease retry in few minutes...","Error: Update Timeout")
									return False
								sleep = 0.5
								time.sleep(sleep)
								if LAST_requestcerts > 16:
									self.API_REQUEST(API_ACTION = "requestcerts")
									LAST_requestcerts = 0
								else:
									LAST_requestcerts += sleep
								self.API_COUNTDOWN -= sleep
							# final step to download certs
							if self.API_REQUEST(API_ACTION = "getcerts"):
								if self.extract_ovpn():
									return True
								else:
									self.msgwarn("Extraction failed!","Error: def inThread_timer_check_certdl")
							else:
								self.msgwarn("Failed to download certificates","Error: def inThread_timer_check_certdl")
							# finish downloading certs
						else:
							self.msgwarn("Failed to request certificates!","Error: def inThread_timer_check_certdl")
					else:
						self.msgwarn("Failed to download configurations!","Error: def inThread_timer_check_certdl")
				else:
					self.msgwarn("No update needed!","oVPN Update OK!")
					return True
			#else:
			#	self.msgwarn("oVPN Update failed","Error: def inThread_timer_check_certdl")
		except:
			self.msgwarn("Failed to check for updates!","Error: def inThread_timer_check_certdl")
		return False

	def delete_dir(self,path):
		try:
			self.debug(1,"def delete_dir()")
			string = 'rmdir /S /Q "%s"' % (path)
			self.debug(1,"def delete_dir: %s" % (string))
			subprocess.check_output("%s" % (string),shell=True)
		except:
			self.debug(1,"def delete_dir: failed")

	def extract_ovpn(self):
		self.debug(1,"def extract_ovpn()")
		try:
			if os.path.isfile(self.ZIP_CFG) and os.path.isfile(self.ZIP_CRT):
				z1file = zipfile.ZipFile(self.ZIP_CFG)
				z2file = zipfile.ZipFile(self.ZIP_CRT)
				if os.path.isdir(self.VPN_CFG):
					self.debug(1,"def extract_ovpn: os.path.isdir(%s)"%(self.VPN_CFG))
					self.delete_dir(self.VPN_CFG)
				if not os.path.isdir(self.VPN_CFG):
					try:
						os.mkdir(self.VPN_CFG)
						self.debug(1,"def extract_ovpn: os.mkdir(%s)"%(self.VPN_CFG))
					except:
						self.debug(1,"def extract_ovpn: %s not found, create failed."%(self.VPN_CFG))
				else:
					self.debug(1,"def extract_ovpn: DIR '%s' delete failed")
					
				try:
					z1file.extractall(self.VPN_CFG)
					z2file.extractall(self.VPN_CFG)
					if self.write_last_update():
						self.debug(1,"Certificates and Configs extracted to '%s'" % (self.VPN_CFG))
						return True
				except:
					self.debug(1,"Error on extracting Certificates and Configs!")
					return False
		except:
			self.debug(1,"def extract_ovpn: failed")

	def write_last_update(self):
		self.debug(1,"def write_last_update()")
		self.LAST_CFG_UPDATE = self.remote_lastupdate
		if self.write_options_file():
			return True

	def msgwarn(self,text,title):
		self.debug(1,text)

	def debug(self,level,text):
		try:
			istrue = self.DEBUG
		except:
			istrue = False
		
		try:
			bindir = self.BIN_DIR
		except:
			bindir = False
		CDEBUG(level,text,istrue,bindir)
		return

def app():
	CMDLINE()

if __name__ == "__main__":
	app()