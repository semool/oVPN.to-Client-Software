from Tkinter import *
from infi.systray import SysTrayIcon
import Tkinter,tkMessageBox,Tkconstants,types,os,platform,sys,hashlib,random,base64,urllib,urllib2,time,datetime
import _winreg,zipfile
import subprocess
import threading
import win32com.client
import socket
from Crypto.Cipher import AES


BUILT="0.1.4"
STATE="_alpha"

try:
	if sys.argv[1] == "debug":
		DEBUG = True
except:
	DEBUG = True

DOMAIN = "vcp.ovpn.to"
PORT="443"
API="xxxapi.php"
#SSL="CE:4F:88:43:F8:6B:B6:60:C6:02:C7:AB:9C:A9:2F:15:3A:9F:F4:65:A3:20:D0:11:A1:27:74:B4:07:B9:54:6A"

class AppUI(Frame):

	def __init__(self, root):
		Frame.__init__(self, root, relief=SUNKEN, bd=2)
		self.root = root
		self.root.bind( '<Configure>', self.onFormEvent )
		self.root.protocol("WM_DELETE_WINDOW", lambda root=root: self.on_closing(root))
		self.self_vars()		
		self.frame = Frame(self.root,bg="#1a1a1a", width=self.screen_width, height=self.screen_height)
		self.frame.pack_propagate(0)		
		self.frame.pack()
		self.make_mini_menubar()
		self.check_preboot()
					
	def self_vars(self):
		self.debug_log = False
		self.OVPN_LATEST = 236
		self.OVPN_LATEST_BUILT = "Mar 19 2015"
		self.OVPN_LATEST_BUILT_TIMESTAMP = 1426719600
		self.OVPN_DL_URL = False		
		self.OVPN_WIN_DL_URL_x86 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.6-I003-i686.exe"
		self.OVPN_WIN_DLHASH_x86 = "97db2d5545c59a9984a1117bca0b578bbdcb1134a720ca4f342aba8b44bee508"
		self.OVPN_WIN_DL_URL_x64 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.6-I003-x86_64.exe"
		self.OVPN_WIN_DLHASH_x64 = "409011239096933ebc8e6c9dd44ac3050e43466104f4b296e7d175094643af02"

		self.MAIN_WINDOW_OPEN = True
		self.isSMALL_WINDOW = False
		self.SWITCH_SMALL_WINDOW = False
		self.SWITCH_FULL_WINDOW = False
		self.SWITCH_SYSTRAY = False
		self.INFO_WINDOW_ACTIVE = False
		self.isLOGGEDin = False
		self.menubar = False
		self.UPDATE_MENUBAR = False
		self.statusbar = False
		self.timer_statusbar_running = False
		self.timer_ovpn_ping_running = False
		self.timer_ovpn_reconnect_running = False
		self.timer_check_certdl_running = False
		self.timer_check_certdl_dots = ""
		self.statustext_from_before = False
		self.systraytext_from_before = False
		self.statusbar_text = StringVar()
		self.statusbar_freeze = False
		self.OVPN_CONNECTEDsystraytext = StringVar()
		self.SYSTRAYon = False
		self.screen_width = 320
		self.screen_height = 240
		self.USERID = False
		self.input_PH = False
		self.extract = False
		self.STATE_OVPN = False
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS = False
		self.WIN_TAP_DEVICE = False
		self.WIN_EXT_DEVICE = False
		self.OVPN_SERVER = list()
		self.OVPN_FAV_SERVER = False
		self.OVPN_AUTO_RECONNECT = True
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtime = False
		self.OVPN_CONNECTEDdistime = False
		self.OVPN_CONNECTEDtoIP = False
		self.OVPN_CONNECTEDtoIPbefore = False
		self.OVPN_THREADID = False
		self.OVPN_THREAD_STARTED = False
		self.OVPN_RECONNECT_NOW = False
		self.OVPN_PING = list()
		self.OVPN_isTESTING = False
		self.OVPN_PING_LAST = -1
		self.OVPN_PING_STAT = -1
		self.INTERFACES = False
		self.d0wns_dns = False
		self.DNS_SELECTED = False

	def errorquit(self,text):
		self.debug(text)
		tkMessageBox.showinfo("Error","%s" % (text))
		sys.exit()

	def msgwarn(self,text):
		self.debug(text)
		tkMessageBox.showinfo("Warning","%s" % (text))	

	def debug(self,text):
		if DEBUG: 
			localtime = time.asctime (time.localtime(time.time()))
			debugstring = "%s: %s"%(localtime,text)
			print(debugstring)
			if not self.debug_log == False:
				try: 
					dbg = open(self.debug_log,'a')
					dbg.write("%s\r\n" % (debugstring))
					dbg.close()
					return True
				except: 
					print("Write to %s failed"%(self.debug_log))
					return False


	def check_preboot(self):
		if self.pre0_detect_os():
			if self.win_pre1_check_app_dir():
				if self.win_pre2_check_profiles_win():
					if self.win_pre3_load_profile_dir_vars():
						if self.check_config_folders():
							self.debug(text="def check_preboot: if self.check_config_folders :True")
							self.preboot = False
							self.timer_preboot()
							self.make_statusbar()
							self.check_inet_connection()						
							self.receive_passphrase()
							self.update_idletasks()
							self.debug(text="We start looping!")
							return True
						else:
							self.form_enter_new_encryption_password()
							self.debug(text="We start looping too!")
							return True
							
							
	def removethis(self):
		self.frame.destroy()
		self.frame = Frame(self, width=self.screen_width, height=self.screen_height)
		self.frame.pack_propagate(0)
		self.frame.pack()		
		self.update_idletasks()
	
	
	def timer_preboot(self):
		if self.preboot == True:
			self.removethis()
			self.make_menubar()
			if self.gui_check_remotelogin():
				self.debug(text="def timer_preboot remotelogin OK")
				if self.timer_check_certdl_running == False: 
					self.isLOGGEDin = True				
				if self.extract:
					self.make_menubar()
					text = "Extraction well done!"
					self.statusbar_text.set(text)
					self.make_label(text=text) 
					return True
				return True
		else:
			#self.debug(text="def timer_preboot: looping!")
			self.root.after(1000,self.timer_preboot)

			
	def ask_passphrase(self):
		self.debug(text="def ask_passphrase")
		self.removethis()
		self.make_label(text="oVPN.to Client Authentication\n\n\nEnter your Passphrase")
		self.input_PH = Entry(self.frame,show="*")
		self.input_PH.bind('<Return>', lambda x: self.receive_userid())
		self.input_PH.pack()
		self.input_PH.focus()
		button = Button(self.frame, text="OK", command=self.receive_passphrase).pack()
		self.update_idletasks()
	

	def receive_passphrase(self):
		self.debug(text="def receive_passphrase")
		
		if not self.input_PH == False: 
			self.PH = self.input_PH.get().rstrip()
			
		if not self.USERID == False and not self.input_PH == False:
			if self.read_config():
				self.debug(text="def receive_passphrase :self.read_config")
				if self.compare_confighash():
					self.input_PH = False
					self.preboot = True
					self.debug(text="def receive_passphrase :True")
					self.statusbar_text.set("Passphrase Ok!")
					self.removethis()
					self.make_label(text="\n\n\nPlease wait!")
					return True
				else:
					os.remove(self.api_cfg)
					self.quit_text = "READ_CONFIG HASH ERROR"
					self.errorquit()
			else:
				self.ask_passphrase()					
		else:
			self.ask_passphrase()							

			
	def pre0_detect_os(self):
		self.self_vars()
		self.OS = sys.platform
		if self.OS == "win32":
			w32Reg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
			w32Key1 = _winreg.OpenKey(w32Reg, "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0", _winreg.KEY_READ)
			key1_value, type = _winreg.QueryValueEx(w32Key1,"Identifier")
			key1_value = key1_value.split()
			w32Key1.Close()
			if key1_value[0] == "Intel64": 
				self.OSARCH = "x86_64"
				self.OSBITS = "64"			
			elif key1_value[0] == "AMD64":
				self.OSARCH = "x86_64"
				self.OSBITS = "64"
			elif key1_value[0] == "x86" or key1_value[0] == "i686" or key1_value[0] == "i586":
				self.OSARCH = "x86"
				self.OSBITS = "32"
			else:
				self.errorquit(text = "Operating System not supported: %s %s" % (self.OS,key1_value[0]))
			
			if self.OSBITS == "32": 
				self.OVPN_DL_URL = self.OVPN_WIN_DL_URL_x86
				self.OVPN_DLHASH = self.OVPN_WIN_DLHASH_x86
			if self.OSBITS == "64": 
				self.OVPN_DL_URL = self.OVPN_WIN_DL_URL_x64
				self.OVPN_DLHASH = self.OVPN_WIN_DLHASH_x64
				
			if DEBUG: print("def pre0_detect_os: arch=%s bits=%s key=%s OS=%s" % (self.OSARCH,self.OSBITS,key1_value[0],self.OS))
			self.win_get_interfaces()
			self.win_detect_openvpn()			
			self.root.title("oVPN.to v"+BUILT+STATE+" "+self.OSARCH)
			return True
		elif OS == "linux2" :
			self.errorquit(text = "Operating System not supported: %s" % (self.OS))	
		elif OS == "darwin":
			self.errorquit(text = "Operating System not supported: %s" % (self.OS))
		else: 
			self.errorquit(text = "Operating System not supported: %s" % (self.OS))
	
	
	def win_pre1_check_app_dir(self):
		os_appdata = os.getenv('APPDATA')
		self.app_dir = "%s\ovpn" % (os_appdata)
		if not os.path.exists(self.app_dir):
			if DEBUG: print("win_pre1_check_app_dir %s not found, creating." % (self.app_dir))
			os.mkdir(self.app_dir)
		if os.path.exists(self.app_dir):
			self.debug(text="win_pre1_check_app_dir self.app_dir=%s :True" % (self.app_dir))
			return True
		else:
			self.errorquit(text = "def check_winapp_dir could not create app_dir: %s" % (self.app_dir))

			
	def win_pre2_check_profiles_win(self):
		self.debug(text="def win_pre2_check_profiles_win: %s" % (self.app_dir))
		self.profiles_unclean = os.listdir(self.app_dir)
		self.profiles = list()
		for profile in self.profiles_unclean:
			if profile.isdigit():
				self.profiles.append(profile)
				
		self.profiles_count = len(self.profiles)
		if DEBUG: print("_check_profiles_win profiles_count %s" % (self.profiles_count))
		
		if self.profiles_count == 0:
			if DEBUG: print("No profiles found")
			if self.USERID == False:
				self.debug(text="spawn popup userid = %s" % (self.USERID))
				self.form_ask_userid()				
				
		elif self.profiles_count == 1 and self.profiles[0] > 1:
			self.profile = self.profiles[0]
			self.USERID = self.profile
			return True
		elif self.profiles_count > 1:
			self.errorquit(text = "Multiple profiles not yet implemented.\nPlease empty or rename profile-folders to *.bak (non int)\n %s" % (self.app_dir))
		
		if DEBUG: 
			for profile in self.profiles:
				print("Profile: %s" % (profile))
			print("def check_profiles_win end")
		
			
	def win_pre3_load_profile_dir_vars(self):
		self.api_dir = "%s\\%s" % (self.app_dir,self.profile)
		self.bin_dir = "%s\\bin\\client\\dist" % (self.app_dir)
		self.lock_file = "%s\\lock.file" % (self.app_dir)
		
		self.debug_log = "%s\\cient_debug.log" % (self.api_dir)
		if DEBUG:
			try:
				dbg = open(self.debug_log,'wb')
				dbg.write("DEBUG_LOG START\r\n")
				dbg.close()
			except: 
				print("Delete %s failed"%(self.debug_log))
		
		self.api_cfg = "%s\\ovpnapi.conf" % (self.api_dir)
		self.vpn_dir = "%s\\openvpn" % (self.api_dir)
		self.prx_dir = "%s\\proxy" % (self.api_dir)
		
		self.stu_dir = "%s\\stunnel" % (self.api_dir)
		self.pfw_dir = "%s\\pfw" % (self.api_dir)
		
		self.vpn_cfg = "%s\\config" % (self.vpn_dir)
		self.zip_cfg = "%s\\confs.zip" % (self.vpn_dir)
		self.zip_crt = "%s\\certs.zip" % (self.vpn_dir)
		self.api_upd = "%s\\lastupdate.txt" % (self.vpn_dir)
		
#		if not self.win_firewall_start():
#			self.msgwarn("Could not start Windows Firewall!")
			
		
		self.taskbar_icon = "%s\\ico\\earth.png" % (self.bin_dir)
		self.root.iconbitmap(self.taskbar_icon)
		
		self.systray_icon_connected = "%s\\ico\\292.ico" % (self.bin_dir)
		self.systray_icon_disconnected = "%s\\ico\\263.ico" % (self.bin_dir)
		self.systray_icon_connect = "%s\\ico\\396.ico" % (self.bin_dir)
		self.systray_icon_hourglass = "%s\\ico\\205.ico" % (self.bin_dir)
		self.systray_icon_syncupdate = "%s\\ico\\266.ico" % (self.bin_dir)
		self.systray_icon_greenshield = "%s\\ico\\074.ico" % (self.bin_dir)
		
		if DEBUG: print("win_pre3_load_profile_dir_vars loaded")
		return True	

		
	def check_config_folders(self):
		#self.debug(text="def check_config_folders userid = %s" % (self.USERID))
		self.debug(text="def check_config_folders: userid found")
		if not os.path.exists(self.api_dir):
			if DEBUG: print("api_dir %s not found, creating." % (self.api_dir))
			os.mkdir(self.api_dir)
			
		if os.path.isfile(self.lock_file):
			if tkMessageBox.askyesno("Client is Locked!", "oVPN Client is already running or did not close cleanly.\n\nDo you really want to start?"):
				try:
					os.remove(self.lock_file)
				except:
					self.msgwarn("Could not remove lock file.\nFile itself locked because another oVPN Client instance running?")
					sys.exit()
			else:
				sys.exit()
			
		if not os.path.isfile(self.lock_file):
			self.LOCK = open(self.lock_file,'wb')
			self.LOCK.write("%s" % (self.get_now_unixtime()))
			
		if not os.path.exists(self.vpn_dir):
			if DEBUG: print("vpn_dir %s not found, creating." % (self.vpn_dir))
			os.mkdir(self.vpn_dir)

		if not os.path.exists(self.vpn_cfg):
			if DEBUG: print("vpn_cfg %s not found, creating." % (self.vpn_cfg))
			os.mkdir(self.vpn_cfg)			

		if not os.path.exists(self.prx_dir):
			if DEBUG: print("prx_dir %s not found, creating." % (self.prx_dir))
			os.mkdir(self.prx_dir)
			
		if not os.path.exists(self.stu_dir):
			if DEBUG: print("stu_dir %s not found, creating." % (self.stu_dir))
			os.mkdir(self.stu_dir)
			
		if not os.path.exists(self.pfw_dir):
			if DEBUG: print("pfw_dir %s not found, creating." % (self.pfw_dir))
			os.mkdir(self.pfw_dir)			
			
		if os.path.exists(self.api_dir) and os.path.exists(self.vpn_dir) and os.path.exists(self.vpn_cfg) \
		and os.path.exists(self.prx_dir) and os.path.exists(self.stu_dir) and os.path.exists(self.pfw_dir):
			if not os.path.isfile(self.api_upd):
				if DEBUG: print("writing lastupdate to %s" % (self.api_upd))
				cfg = open(self.api_upd,'w')
				cfg.write("0")
				cfg.close()
				
			if not os.path.isfile(self.api_upd):
				self.errorquit(text = "Creating FILE\n%s\nfailed!" % (self.api_upd))
				
			if os.path.isfile(self.api_cfg):
				self.debug(text="def check_config_folders :True")
				return True
			else:
				return False
		else:
			self.errorquit(text = "Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!" % (self.api_dir,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))

			
	def form_ask_userid(self):
		if DEBUG: print("def form_ask_userid")
		self.removethis()
		self.make_label(text = "oVPN.to Client\n\n\nPlease enter your oVPN.to User-ID Number:")
		self.input_userid = Entry(self.frame)
		self.input_userid.bind('<Return>', lambda x: self.receive_userid())
		self.input_userid.pack()
		self.input_userid.focus()
		Button(self.frame, text="OK", command=self.receive_userid).pack()

		
	def receive_userid(self):
		self.USERID = self.input_userid.get().rstrip()
		if self.check_userid_format():
			if DEBUG: print("def receive_userid userid = %s" % (self.USERID))
			if self.OS == "win32": 
				self.profile = self.USERID				
				self.win_pre3_load_profile_dir_vars()
				if self.check_config_folders() == False:
					self.form_enter_new_encryption_password()
					return True
		else: self.USERID = False	

		
	def form_enter_new_encryption_password(self):
		self.removethis()
		self.make_label(text="oVPN.to Client Setup\n\nPlease enter a passphrase to encrypt your API configuration.\n")
		self.make_label(text="\nNew passphrase:")
		self.input_PH1 = Entry(self.frame,show="*")
		self.input_PH1.pack()
		self.input_PH1.focus()
		self.make_label(text="\nRepeat your new passphrase:")
		self.input_PH2 = Entry(self.frame,show="*")
		self.input_PH2.bind('<Return>', lambda x: self.receive_new_passphrase())
		self.input_PH2.pack()
		# create a margin
		Label(self.frame).pack()
		Button(self.frame, text="Save Encryption Passphrase!", command=self.receive_new_passphrase).pack(ipadx=10, ipady=10)
		
		
	def receive_new_passphrase(self):
		self.PH1 = self.input_PH1.get().rstrip()
		self.PH2 = self.input_PH2.get().rstrip()
		if self.PH1 == self.PH2 and len(self.PH1) > 0:
			if DEBUG: print("passphrase accepted")
			self.form_enter_api_login()
		else:
			if DEBUG: print("passphrase mismatch")	
			self.form_enter_new_encryption_password()
			
			
	def form_enter_api_login(self):
		self.removethis()
		self.make_label(text="oVPN.to Client Setup\n\n\nEnter your oVPN.to API-Key:")
		self.input_apikey = Entry(self.frame,show="*")
		self.input_apikey.bind('<Return>', lambda x: self.write_new_config())
		self.input_apikey.pack()
		self.input_apikey.focus()
		
		Button(self.frame, text="Save API-Key!", command=self.write_new_config).pack()		

		
	def gui_check_remotelogin(self):
		self.removethis()
		#if DEBUG: print("check_remotelogin: userid=%s apikey=%s") % (self.USERID,self.APIKEY)
		
		Label(self.frame,text="oVPN.to Client %s\n\n\n" % (self.USERID)).pack()
		
		if self.curl_api_request(API_ACTION = "lastupdate"):
			#self.debug(text="self.curldata: %s" % (self.curldata))
			self.remote_lastupdate = self.curldata
			if self.check_last_server_update():
				text = "Updating oVPN Configurations..."
				self.statusbar_text.set(text)
				self.make_label(text = text)
				if self.curl_api_request(API_ACTION = "getconfigs"):
					text = "Updating oVPN Certificates......"
					self.statusbar_text.set(text)
					self.make_label(text = text)
					if self.curl_api_request(API_ACTION = "requestcerts"):
						self.make_label(text = "Please wait up to 5 minutes.")
						self.timer_check_certdl()
						return True
			else:
				self.make_label(text="Checking for oVPN Updates: Complete!")
				self.make_label(text="\n\nAlpha is not Beta!\nThanks for testing!")
				return True	
		else:
			self.msgwarn(text="Connection failed to https://vcp.ovpn.to!")

			
	def check_last_server_update(self):
		cfg = open(self.api_upd,'r')
		read_data = cfg.read()
		cfg.close()
		if read_data < self.remote_lastupdate:
			if DEBUG: print("our last update: %s") % (read_data)
			return True	
	
	
	def write_last_update(self):
		cfg = open(self.api_upd,'wb')
		cfg.write("%s" % (self.get_now_unixtime()))
		cfg.close()
		return True

		
	def get_now_unixtime(self):
		self.now_unixtime = int(time.time())
		return self.now_unixtime
		
		
	def extract_ovpn(self):
		z1file = zipfile.ZipFile(self.zip_cfg)
		z2file = zipfile.ZipFile(self.zip_crt)		
		z1file.extractall(self.vpn_cfg) 
		z2file.extractall(self.vpn_cfg)
		if self.write_last_update():
			self.statusbar_text.set("Certificates and Configs extracted.")
			return True

			
	def timer_check_certdl(self):
		self.timer_check_certdl_running = True
		self.curl_api_request(API_ACTION = "requestcerts")

		if not self.body == "ready":
			if len(self.timer_check_certdl_dots) > 4: self.timer_check_certdl_dots = ""
			self.timer_check_certdl_dots = "%s." % (self.timer_check_certdl_dots)
			text = "Updating oVPN Certificates%s" % (self.timer_check_certdl_dots)
			self.statusbar_text.set(text)
			self.root.after(3000,self.timer_check_certdl)
		if self.body == "ready":
			if self.curl_api_request(API_ACTION = "getcerts"):	
				self.body = False
				if self.extract_ovpn():
					self.removethis()
					#self.make_label(text = "oVPN.to Client %s\n\n\noVPN Server Update Complete!\nFiles saved to:\n%s\n%s\nFiles extracted to:\n%s" % (self.USERID,self.zip_cfg,self.zip_crt,self.vpn_cfg))
					self.extract = True
					self.make_menubar()
					self.isLOGGEDin = True
					self.timer_check_certdl_running = False
					return True
				else:
					self.make_label(text = "\noVPN Server Update Failed!")
					return False


	def check_inet_connection(self):
		s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = "vcp.ovpn.to"
		port = 443
				
		if not self.try_socket(host,port):
			text="1) Could not connect to vcp.ovpn.to\nTry setting firewall rule to access VCP!"
			#self.msgwarn(text=text)
			self.debug(text=text)
			self.win_firewall_add_rule_to_vcp(option="add")
			time.sleep(2)
			if not self.try_socket(host,port):
				text="2) Could not connect to vcp.ovpn.to\nRetry"
				#self.msgwarn(text=text)
				self.debug(text=text)
				time.sleep(2)
				if not self.try_socket(host,port):
					#text="3) Could not connect to vcp.ovpn.to\nTry setting firewall rule to allowing outbound connections to world!"
					#self.win_firewall_allow_outbound()
					text="3) Could not connect to vcp.ovpn.to\n"
					self.debug(text=text)
					self.msgwarn(text=text)			
					#time.sleep(8)
					

	def try_socket(self,host,port):		
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = s.connect_ex((host, port))
			s.close()			
		except:
			result = False
		if result == 0:
			return True
		return False
		
	def read_d0wns_dns(self):
		if not self.OVPN_PING_STAT >= 0:
			self.UPDATE_MENUBAR = True
			return True
		
		url = "https://dns.d0wn.biz/dns.txt"
		req = urllib2.Request(url)
		body = False
		try: 
			response = urllib2.urlopen(req)
			body = response.read()
			
		except:
			text = "URL TIMEOUT: %s" % (url)
			self.debug(text=text)
			self.msgwarn(text=text)
		if not body  == False:
			#self.debug("def read_d0wns_dns body = %s"%(body))		
			dnslist = body.split('\n')
			self.d0wns_dns = list()
			if len(dnslist) >= 1:
				for line in dnslist:
					content = line.split(',')
					#self.debug(text="len content = %s" % (len(content)))
					if len(content) >= 3:
						self.d0wns_dns.append(content)
				self.UPDATE_MENUBAR = True
				
			else:
				text="Error loading d0wn's DNS!"
			
	def curl_api_request(self,API_ACTION):
		self.APIURL = "https://%s:%s/%s" % (DOMAIN,PORT,API)
		self.API_ACTION = API_ACTION
		url = self.APIURL
		
		if self.API_ACTION == "lastupdate": 
			self.TO_CURL = "uid=%s&apikey=%s&action=%s" % (self.USERID,self.APIKEY,self.API_ACTION)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : self.API_ACTION }		
			
		if self.API_ACTION == "getconfigs": 
			if os.path.isfile(self.zip_cfg): os.remove(self.zip_cfg)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : self.API_ACTION, 'version' : '23x', 'type' : 'win' }	
			
		if self.API_ACTION == "requestcerts":			
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : self.API_ACTION }	
			
		if self.API_ACTION == "getcerts":
			if os.path.isfile(self.zip_crt): os.remove(self.zip_crt)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : self.API_ACTION }	
			
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		
		self.body = False
		try: 
			response = urllib2.urlopen(req)
			self.body = response.read()
			#self.debug("self.body = %s"%(self.body))
		except:
			text = text="API Connection Timeout to https://vcp.ovpn.to!"
			self.debug(text=text)
			self.msgwarn(text=text)
			
		if not self.body == False:
		
			if not self.body == "AUTHERROR":
				self.curldata = self.body.split(":")
				if self.curldata[0] == "AUTHOK":
					self.curldata = self.curldata[1]
					return True
			else:
				os.remove(self.api_cfg)
				self.errorquit("Invalid User-ID/API-Key. Encrypted API-Keyfile deleted.")
		
			if self.API_ACTION == "getconfigs":
				try:
					fp = open(self.zip_cfg, "wb")
					fp.write(self.body)
					fp.close()
					return True	
				except:
					return False
					
			elif self.API_ACTION == "getcerts": 
				try:			
					fp = open(self.zip_crt, "wb")
					fp.write(self.body)
					fp.close()
					return True
				except:
					return False					

			if self.API_ACTION == "requestcerts": 
				if self.body == "ready" or self.body == "wait" or self.body == "submitted":
					if DEBUG: print("self.body: %s") % (self.body)
					return True		
			
			
	def check_userid_format(self):
		if self.USERID.isdigit() and self.USERID > 1 and len(self.USERID) > 1:
			return True		

			
	def check_login_format(self):
		if self.check_userid_format():
			self.APIKEY = self.input_apikey.get().rstrip()
			if self.USERID.isdigit() and self.USERID > 1 and len(self.USERID) > 1:
				if self.APIKEY.isalnum() and len(self.APIKEY) == 128:
					return True				

					
	def load_decryption(self):
		self.debug(text="def load_decryption")
		if len(self.input_PH.get()) > 0: 
			self.aeskey = hashlib.sha256(self.input_PH.get().rstrip()).digest()
			return True

			
	def read_config(self):
		self.debug(text="def read_config")
		if not self.input_PH == False and self.load_decryption():
			cfg = open(self.api_cfg,'r')
			read_data = cfg.read()
			cfg.close()
			b64decode = base64.b64decode(read_data)
			configdata = b64decode.split(",")
			aesiv = base64.b64decode(configdata[0])
			b64config = base64.b64decode(configdata[1])
			crypt = AES.new(self.aeskey, AES.MODE_CBC, aesiv)
			self.apidata = crypt.decrypt(b64config).split(",")
			aesiv = False
			self.aeskey = False						
			if len(self.apidata) > 3:
				USERID = self.apidata[0].split("=")
				APIKEY = self.apidata[1].split("=")
				CFGSHA = self.apidata[2].split("=")
				if len(USERID) == 2 and USERID[1] > 1 and USERID[1].isdigit():					
					#self.debug(text="def read_config USERID = %s :True" % (USERID))
					self.debug(text="def read_config USERID = profile-folder :True" % (USERID))
					if len(APIKEY) == 2 and len(APIKEY[1]) == 128 and APIKEY[1].isalnum():						
						self.debug(text="def read_config APIKEY len = %s :True" % (len(APIKEY)))
						if len(CFGSHA) == 2 and len(CFGSHA[1]) == 64 and CFGSHA[1].isalnum():
							if not self.USERID == False and self.USERID == USERID[1]:
								self.APIKEY = APIKEY[1]
								self.USERID = int(USERID[1])
								self.CFGSHA = CFGSHA[1]
								#self.debug(text="def read_config CFGSHA = %s" % (self.CFGSHA))
								#self.debug(text="def read_config print self.apidata: %s" % (self.apidata))
								return True
							#else:
							#	self.debug(text="def read_config self.USERID = %s " % (self.USERID))
							#	self.debug(text="def read_config passphrase :True") 
			self.statusbar_text.set("Invalid Passphrase!")
			self.debug(text="def read_config passphrase :False")
			return False

			
	def write_new_config(self):
		if self.check_login_format():
			self.aeskeyhash = hashlib.sha256(self.PH1).digest()
			self.aesiv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
			self.make_confighash()			
			self.randint = random.randint(0,9)
			self.text2aes = "%s,CFGSHA=%s,AESPAD=%s" % (self.text2hash1,self.hash2aes,self.randint)
			self.text2aeslen = len(self.text2aes)
			self.targetpad = 64*64
			self.addpad = self.targetpad - self.text2aeslen
			self.padfill = 2
			self.paddata = self.randint
			while self.padfill <= self.addpad:
				self.randadd = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
				self.paddata = '%s%s' % (self.paddata,self.randadd)
				#if DEBUG: print("padfill=%s\npaddata=%s" % (self.padfill,self.paddata))
				self.padfill += 1
			self.text2aes = "%s%s" % (self.text2aes,self.paddata)
			self.text2aeslen = len(self.text2aes)
			#if DEBUG: print("text2aeslen=%s\n" % (self.text2aeslen))
			#if DEBUG: print("\n##############debug:text2aes=%s\ndebug:aesiv=%s\ndebug:len(self.text2aeslen)=%s\nself.addpad=%s" % (self.text2aes,self.aesiv,self.text2aeslen,self.addpad))
			self.crypt = AES.new(self.aeskeyhash, AES.MODE_CBC, self.aesiv)
			cipherd_data = base64.b64encode(self.crypt.encrypt(self.text2aes))
			data2file = "%s,%s" % (base64.b64encode(self.aesiv),cipherd_data)
			cfg = open(self.api_cfg,'wb')
			cipherd_data_b64 = base64.b64encode(data2file)
			cfg.write(cipherd_data_b64)
			cfg.close()
			self.aesiv = False
			self.aeskeyhash = False
			self.hash2aes = False
			self.text2aes = False
			self.paddata = False
			# check_preboot() will cause a warning if we don't remove the lock
			self.remove_lock()
			self.check_preboot()			

			
	def make_confighash(self):
		self.text2hash1 = "USERID=%s,APIKEY=%s" % (self.USERID,self.APIKEY)
		self.hash2aes = hashlib.sha256(self.text2hash1).hexdigest()
			
			
	def compare_confighash(self):
		self.make_confighash()
		if self.hash2aes == self.CFGSHA:
			self.debug(text="def compare_confighash :True")
			return True	

			
	def make_label(self,text):
		Label(self.frame,text=text).pack()
		self.update_idletasks()
			
		
	def dologout(self):
		if self.OVPN_CONNECTEDto == False and self.isLOGGEDin == True:
			self.isSMALL_WINDOW = False	
			self.screen_width = 320
			self.screen_height = 240
			self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
			self.removethis()
			self.statusbar.destroy()
			self.isLOGGEDin = False
			self.USERID = False
			self.debug(text="Logout")
			self.make_mini_menubar()
			self.LOCK.close()
			if self.SYSTRAYon == True:
				self.systray.shutdown()
			self.remove_lock()
			self.check_preboot()
		else:
			self.msgwarn(text="Disconnect first!")
		

	def load_ovpn_server(self):
		self.removethis()
		content = os.listdir(self.vpn_cfg)
		#self.debug(text="def load_ovpn_server: content = %s " % (content))
		self.OVPN_SERVER = list()
		for trash in content:
			if trash.endswith('.ovpn.to.ovpn'):
				trash = trash[:-5]
				self.OVPN_SERVER.append(trash)
				#self.debug(text="def: trash = %s " % (trash))
		self.OVPN_SERVER.sort()
			
		
	def openvpn(self,server):
		if self.STATE_OVPN == False:
			self.OVPN_AUTO_RECONNECT = True
			self.ovpn_server_UPPER = server
			self.ovpn_server_LOWER = server.lower()

			self.ovpn_server_config_file = "%s\%s.ovpn" % (self.vpn_cfg,self.ovpn_server_UPPER)
			for line in open(self.ovpn_server_config_file):
				if "remote " in line:
					print(line)
					try:
						self.OVPN_CONNECTEDtoIP = line.split()[1]
						self.OVPN_CONNECTEDtoPort = line.split()[2]
						#break
					except:
						self.errorquit(text="Could not read Servers Remote-IP:Port from config: %s" % (self.ovpn_server_config_file) )
				if "proto " in line:
					try:
						self.OVPN_CONNECTEDtoProtocol = line.split()[1]
					except:
						self.errorquit(text="Could not read Servers Protocol from config: %s" % (self.ovpn_server_config_file) )
			
			
			self.ovpn_sessionlog = "%s\ovpn.log" % (self.vpn_dir)
			self.ovpn_server_dir = "%s\%s" % (self.vpn_cfg,self.ovpn_server_LOWER)
			self.ovpn_cert_ca = "%s\%s.crt" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_tls_key = "%s\%s.key" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_cli_crt = "%s\client%s.crt" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_cli_key = "%s\client%s.key" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_string = "\"%s\" --config \"%s\" --ca \"%s\" --cert \"%s\" --key \"%s\" --tls-auth \"%s\" --log \"%s\" " % (self.OPENVPN_EXE,self.ovpn_server_config_file,self.ovpn_cert_ca,self.ovpn_cli_crt,self.ovpn_cli_key,self.ovpn_tls_key,self.ovpn_sessionlog)
			
			try:
				self.call_ovpn_srv = server
				threading.Thread(target=self.inThread_spawn_openvpn_process).start()
				self.OVPN_THREADID = threading.currentThread()
				self.debug(text="Started: oVPN %s on Thread: %s" %(server,self.OVPN_THREADID))
				#self.statusbar_text.set("oVPN connecting to %s ..." %(server))
				self.OVPN_THREAD_STARTED = True
			except:
				text="Error! Unable to start thread: oVPN %s "%(server)
				self.statusbar_freeze = 5000
				self.statusbar_text.set(text)
				self.msgwarn(text=text)
				self.debug(text=text)
				
			if self.OVPN_AUTO_RECONNECT == True:
				self.debug("def openvpn: self.OVPN_AUTO_RECONNECT == True")
				self.OVPN_RECONNECT_NOW = False
				threading.Thread(target=self.inThread_timer_openvpn_reconnect).start()
			else:
				self.debug("def openvpn: self.OVPN_AUTO_RECONNECT == False")
				
		else:
			self.debug(text="def openvpn: self.OVPN_THREADID = %s" % (self.OVPN_THREADID))
			#if tkMessageBox.askyesno("Change oVPN Server?", "oVPN is connected to: %s\n\nSwitch to oVPN Server: %s?"%(self.OVPN_CONNECTEDto,server)):
			self.debug(text="Change oVPN to %s" %(server))
			self.kill_openvpn()
			self.openvpn(server)
		self.UPDATE_MENUBAR = True
		

	def inThread_timer_ovpn_ping(self):
		
		if self.timer_ovpn_ping_running == False:
			self.OVPN_PING_STAT = -2			
			self.debug(text="def inThread_timer_ovpn_ping")
			self.timer_ovpn_ping_running = True
		
		if self.STATE_OVPN == True:
			
			if self.OVPN_PING_STAT > 0: 
				time.sleep(6)
			else:
				time.sleep(3)
			if self.OS == "win32": 
				ovpn_ping_cmd = "ping.exe -n 1 172.16.32.1"
				PING_PROC = False
				try: PING_PROC = subprocess.check_output("%s" % (ovpn_ping_cmd),shell=True)
				except:	pass
					
				try: OVPN_PING_out = PING_PROC.split('\r\n')[2].split()[4].split('=')[1][:-2] 
				except: OVPN_PING_out = -2
				
				pingsum = 0
				if OVPN_PING_out > 0:
					self.OVPN_PING.append(OVPN_PING_out)
					self.OVPN_PING_LAST = OVPN_PING_out
				if len(self.OVPN_PING) > 255:
					self.OVPN_PING.pop(0)
				if len(self.OVPN_PING) > 0:
					for ping in self.OVPN_PING:
						pingsum += int(ping)
					self.OVPN_PING_STAT = pingsum/len(self.OVPN_PING)
				#self.debug(text="ping = %s\n#############\nList len=%s\n%s\npingstat=%s"%(OVPN_PING_out,len(self.OVPN_PING),self.OVPN_PING,self.OVPN_PING_STAT))
				#self.debug("timer ovpn ping running threads: %s, ping=%s" % (threading.active_count(),OVPN_PING_out))
				
				threading.Thread(target=self.inThread_timer_ovpn_ping).start()
				return True
				
		elif self.STATE_OVPN == False:
			self.debug("leaving timer_ovpn_ping")
			self.OVPN_PING_STAT = -1
			self.OVPN_PING = list()
			self.timer_ovpn_ping_running = False

		
	def inThread_spawn_openvpn_process(self):
		self.debug(text="def inThread_spawn_openvpn_process")
		self.ovpn_proc_retcode = False
		self.STATE_OVPN = True
		self.OVPN_CONNECTEDto = self.call_ovpn_srv
		self.win_netsh_set_dns_ovpn()	
		self.OVPN_PING_STAT = -1
		self.OVPN_PING_LAST = -1
		self.debug(text="def call_openvpn self.OVPN_CONNECTEDto = %s" %(self.OVPN_CONNECTEDto))
		self.OVPN_CONNECTEDtime = self.get_now_unixtime()
		self.UPDATE_MENUBAR = True
		if not self.win_firewall_start():
			self.msgwarn("Could not start Windows Firewall!")
		self.win_firewall_modify_rule(option="add")
		self.ovpn_proc_retcode = subprocess.call("%s" % (self.ovpn_string),shell=True)
		self.win_firewall_modify_rule(option="delete")
		self.OVPN_CONNECTEDtoIPbefore = self.OVPN_CONNECTEDtoIP
		self.STATE_OVPN = False
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtoIP = False
		self.OVPN_THREADID = False
		self.OVPN_PING_STAT = -1
		self.OVPN_PING_LAST = -1
		self.OVPN_PING = list()
		self.debug(text="def call_openvpn self.ovpn_proc_retcode = %s" %(self.ovpn_proc_retcode))
		if self.OVPN_AUTO_RECONNECT == True:
			self.debug(text="def inThread_spawn_openvpn_process: auto-reconnect %s" %(self.call_ovpn_srv))
			self.OVPN_RECONNECT_NOW = True
		self.UPDATE_MENUBAR = True
		#if self.SYSTRAYon == True:
		#	self.systray.shutdown()
		#	self.SYSTRAYon = False
		
		
	def read_gateway_from_routes(self):
		self.debug(text="def read_ovpn_routes:")
		string = "route.exe print"
		self.OVPN_READ_ROUTES = subprocess.check_output("%s" % (string),shell=True)
		#self.debug(text="self.OVPN_READ_ROUTES = %s"%(self.OVPN_READ_ROUTES))
		split = self.OVPN_READ_ROUTES.split('\r\n')
		#self.debug(text="split=%s"%(split))
		for line in split:
			#self.debug(text="%s"%(line))
			if "%s"%(self.OVPN_CONNECTEDtoIPbefore) in line:
				#self.debug(text="def read_ovpn_routes: %s"%(line))
				self.GATEWAY_LOCAL = line.split()[2]
				self.debug(text="self.GATEWAY_LOCAL: %s"%(self.GATEWAY_LOCAL))

				
	def del_ovpn_routes(self):
		if not self.OVPN_CONNECTEDtoIPbefore == False:
			self.read_gateway_from_routes()
			if not self.GATEWAY_LOCAL == False:
				self.debug(text="def del_ovpn_routes")
				string1 = "route.exe DELETE %s MASK 255.255.255.255 %s" % (self.OVPN_CONNECTEDtoIPbefore,self.GATEWAY_LOCAL)
				string2 = "route.exe DELETE 0.0.0.0 MASK 128.0.0.0 172.16.32.1"
				string3 = "route.exe DELETE 128.0.0.0 MASK 128.0.0.0 172.16.32.1"
				try: 
					self.OVPN_DEL_ROUTES1 = subprocess.check_output("%s" % (string1),shell=True)
					self.OVPN_DEL_ROUTES2 = subprocess.check_output("%s" % (string2),shell=True)
					self.OVPN_DEL_ROUTES3 = subprocess.check_output("%s" % (string3),shell=True)
					#self.debug(text="self.OVPN_DEL_ROUTES: %s, %s, %s"%(self.OVPN_DEL_ROUTES1,self.OVPN_DEL_ROUTES2,self.OVPN_DEL_ROUTES3))
				except:
					self.debug(text="def del_ovpn_routes: failed")
					pass
			self.OVPN_CONNECTEDtoIPbefore = False
			self.GATEWAY_LOCAL = False
			
		
	def inThread_timer_openvpn_reconnect(self):
		#self.debug("def inThread_timer_openvpn_reconnect")
		time.sleep(3)		
		if self.OVPN_RECONNECT_NOW == True and self.OVPN_AUTO_RECONNECT == True and self.STATE_OVPN == False:
			self.openvpn(self.call_ovpn_srv)
			text = "oVPN process crashed and restarted."
			self.debug(text=text)
			return False
		elif self.STATE_OVPN == True:
			#self.debug(text="Watchdog: oVPN is running to %s %s" %(self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP))
			if self.timer_ovpn_ping_running == False: 
				self.debug("def inThread_timer_openvpn_reconnect starting ping timer")
				threading.Thread(target=self.inThread_timer_ovpn_ping).start()
			else:
				#self.debug("def inThread_timer_openvpn_reconnect: timer_ovpn_ping is running")
				pass
			threading.Thread(target=self.inThread_timer_openvpn_reconnect).start()
			time.sleep(3)
			return True

			
	def kill_openvpn(self):		
		self.OVPN_AUTO_RECONNECT = False		
		self.debug(text="def kill_openvpn")	
		string1 = "taskkill /im openvpn.exe"
		string2 = "taskkill /im openvpn.exe /f"
		try: 
			self.OVPN_KILL1 = subprocess.check_output("%s" % (string1),shell=True)
		except:
			try:
				self.OVPN_KILL2 = subprocess.check_output("%s" % (string2),shell=True)
			except:
				pass
		self.UPDATE_MENUBAR = True
		self.del_ovpn_routes()
		
		
	def win_netsh_set_dns_ovpn(self):
		if not self.GATEWAY_DNS == "172.16.32.1":
			self.debug(text="def win_netsh_set_dns_ovpn:")
			string1 = "netsh interface ip set dnsservers \"%s\" static 172.16.32.1 primary no" % (self.WIN_EXT_DEVICE)
			string2 = "netsh interface ip set dnsservers \"%s\" static 172.16.32.1 primary no" % (self.WIN_TAP_DEVICE)
			try: 
				read1 = subprocess.check_output("%s" % (string1),shell=True)
				read2 = subprocess.check_output("%s" % (string2),shell=True)
				self.debug(text=":true")
			except:
				self.debug(text="def win_netsh_set_dns_ovpn: setting dns failed:\n%s\n%s"%(string1,string2))

				
	def win_netsh_change_dns_server(self,dns_ipv4):
		self.debug(text="def win_netsh_change_dns_server:")
		string1 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_EXT_DEVICE,dns_ipv4)
		string2 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_TAP_DEVICE,dns_ipv4)
		try: 
			read1 = subprocess.check_output("%s" % (string1),shell=True)
			read2 = subprocess.check_output("%s" % (string2),shell=True)
			text = "oVPN DNS changed to %s" % (dns_ipv4)
			if dns_ipv4 == "172.16.32.1":
				text = "%s (Internal Randomized)" % (text)
			elif dns_ipv4 == "127.0.0.1":
				text = "%s (DNScrypt enabled)" % (text)
			else:
				text = "%s (direct connection)" % (text)
			self.statusbar_freeze = 5000
			self.statusbar_text.set(text)
			self.DNS_SELECTED = dns_ipv4
			self.UPDATE_MENUBAR = True
			self.debug(text=":true")
		except:
			self.debug(text="def win_netsh_change_dns_server: failed\n%s\n%s"%(string1,string2))
		
	
	def win_netsh_restore_dns_dhcp(self):
		os.system('netsh interface ip set dnsservers "%" dhcp'%(self.WIN_EXT_DEVICE))

		
	def win_netsh_restore_dns_from_backup(self):
		if not self.GATEWAY_DNS == "172.16.32.1":
			string = 'netsh interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS)
			read = False
			try: 
				read = subprocess.check_output("%s" % (string),shell=True)
			except:
				pass
			if not read == False:
				self.msgwarn(text="Primary DNS Server restored to: %s"%(self.GATEWAY_DNS))
			else:
				self.msgwarn(text="Error: Restoring your DNS Server to %s failed."%(self.GATEWAY_DNS))
			self.debug(text="def win_netsh_restore_dns_from_backup: %s"%(read))

			
	def win_netsh_read_dns_to_backup(self):
		string = "netsh interface ipv4 show dns"
		read = subprocess.check_output("%s" % (string),shell=True)
		read = read.strip().decode('utf-8','ignore')
		search = '"%s"' % (self.WIN_EXT_DEVICE)
		list = read.strip(' ').split('\r\n')
		i=0
		m=0
		t=0
		for line in list:
			#self.debug(text=line)
			if search in line:
				self.debug(text=line)
				self.debug(text="%s"%(i))
				m=i+1
			if i == m:
				if "DNS" in line:
					dns = line.strip().split(":")[1].lstrip()
					self.debug(text=line)
					self.debug(text=dns)
					check = dns.split(".")
					for n in check:
						x = int(n)
						if x >= 0 and x <= 255 and t <= 4:
							t+=1
						else: 
							t = 0
							break
			i+=1
		if t == 4: self.GATEWAY_DNS = dns
		else: self.GATEWAY_DNS = self.GATEWAY_LOCAL
		self.debug(text="self.GATEWAY_DNS = %s"%(self.GATEWAY_DNS))
			

#	def win_netsh_show_interfaces(self):
#		os.system('netsh interface ip show interfaces')
#
#	def win_netsh_show_dnsservers(self):
#		os.system('netsh interface ip show dnsservers')	
		
	def win_detect_openvpn(self):
		self.OPENVPN_EXE = False
		os_programfiles = "PROGRAMFILES PROGRAMFILES(x86) PROGRAMW6432"
		r = 0
		for getenv in os_programfiles.split():
			programfiles = os.getenv(getenv)
			file = "%s\\OpenVPN\\bin\\openvpn.exe" % (programfiles)
			if os.path.isfile(file): 
				self.debug(text="def win_detect_openvpn: %s" % (file))
				self.OPENVPN_EXE = file
				break
		
		if self.OPENVPN_EXE == False:
			self.errorquit(text="Could not find openvpn.exe")
		else:
			try:
				out, err = subprocess.Popen("\"%s\" --version" % (self.OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()		
			except:
				self.errorquit(text="Could not detect openVPN Version!")
				
			self.OVPN_VERSION = out.split('\r\n')[0].split( )[1].replace(".","")
			self.OVPN_BUILT = out.split('\r\n')[0].split("built on ",1)[1].split()
			if self.OVPN_VERSION >= self.OVPN_LATEST:
				if self.OVPN_BUILT == self.OVPN_LATEST_BUILT:
					return True
				else:
					built_mon = self.OVPN_BUILT[0]
					built_day = int(self.OVPN_BUILT[1])
					built_year = int(self.OVPN_BUILT[2])
					builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
					string_built_time = time.strptime(builtstr,"%b/%d/%Y")
					built_month_int = int(string_built_time.tm_mon)
					built_timestamp = int(time.mktime(datetime.datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					if built_timestamp >= self.OVPN_LATEST_BUILT_TIMESTAMP:				
						return True
					else:
						self.errorquit(text="Please update your openVPN Version!")
			else:
				self.errorquit(text="Please update your openVPN Version!")

				
#	def win_install_tap_adapter(self):
#		path = "C:\Program Files\TAP-Windows\bin\tapinstall.exe find *TAP"
#		pass
		
	def win_get_interfaces(self):		
		self.debug(text="def win_get_interfaces")
		wmi=win32com.client.GetObject('winmgmts:')
		adapters=wmi.InstancesOf('win32_networkadapter')
		self.INTERFACES = list()
		for adapter in adapters:
			for p in adapter.Properties_:
				if p.Name == "NetConnectionID" and not p.Value == None:
					INTERFACE=p.Value
					string = "%s"%(INTERFACE)
					#self.debug(text=string)
					self.INTERFACES.append(string)
		#self.debug(text="%s"%(self.INTERFACES))			
		if len(self.INTERFACES)	< 2:
			self.errorquit(text="Could not read your Network Interfaces!")
		
		string = "openvpn.exe --show-adapters"
		ADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		ADAPTERS = ADAPTERS.split('\r\n')
		self.debug(text="TAP ADAPTER = %s"%(ADAPTERS))
		for line in ADAPTERS:
			#self.debug(text="checking line = %s"%(line))
			for INTERFACE in self.INTERFACES:
				#self.debug(text="is IF %s listed as TAP?"%(INTERFACE))
				if line.startswith("'%s'"%(INTERFACE)):
					self.debug(text=INTERFACE+" is TAP ADAPTER")
					self.WIN_TAP_DEVICE = INTERFACE
					break
				elif line.startswith("Available TAP-WIN32 adapters"):
					#self.debug(text="ignoring tap line")
					pass
				elif len(line) < 16:
					#self.debug(text="ignoring line < 16")
					pass
				else:
					#self.debug(text="ignoring else")
					pass
					
		if self.WIN_TAP_DEVICE == False:
			self.errorquit(text="No openVPN TAP-Adapter found!")
		else:
			self.INTERFACES.remove(self.WIN_TAP_DEVICE)
			self.debug(text="remaining INTERFACES = %s"%(self.INTERFACES))
			if len(self.INTERFACES) > 1:
				window = Toplevel()
				window.title("Choose your External Network Adapter!")
				text = Label(window, text="Multiple network adapters found.\nPlease select your external network adapter (the one you use to connect to the Internet)!")
				text.pack()
				listbox = Listbox(window, width=64)
				def adapter_window_callback(window, listbox):
					self.WIN_EXT_DEVICE = listbox.get(ACTIVE)
					window.destroy()
				button = Button(window, text="OK", command=lambda: adapter_window_callback(window, listbox))
				for INTERFACE in self.INTERFACES:
					listbox.insert(END, INTERFACE)	
				listbox.pack()
				button.pack()
				# Put our window into the foreground
				window.transient(self.root)
				window.grab_set()
				# Block until the users closes the window
 				self.root.wait_window(window)
			elif len(self.INTERFACES) < 1:
				self.errorquit(text="No Network Adapter found!")
			else:
				self.WIN_EXT_DEVICE = self.INTERFACES[0]
				text = "External Interface = %s"%(self.WIN_EXT_DEVICE)
				#self.msgwarn(text=text)
				self.debug(text=text)
		self.win_netsh_read_dns_to_backup()

	

		
	def win_firewall_start(self):
		#self.pfw_bak = "%s\\pfw.%s.bak.wfw" % (self.pfw_dir,int(time.time()))
		#self.pfw_log = "%s\\pfw.%s.log" % (self.pfw_dir,int(time.time()))
		self.pfw_cmdlist = list()
		#self.pfw_cmdlist.append("advfirewall export %s" % (self.pfw_bak))
		#self.pfw_cmdlist.append("advfirewall reset")
		self.pfw_cmdlist.append("advfirewall set allprofiles state on")
		#self.pfw_cmdlist.append("advfirewall set currentprofile logging filename \"%s\"" % (self.pfw_log))
		self.pfw_cmdlist.append("advfirewall set privateprofile firewallpolicy blockinbound,blockoutbound")
		self.pfw_cmdlist.append("advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound")
		self.pfw_cmdlist.append("advfirewall set domainprofile firewallpolicy blockinbound,blockoutbound")
		return self.win_join_netsh_cmd()

		
	def win_firewall_add_rule_to_vcp(self,option):
		self.debug(text="def win_firewall_add_rule_to_vcp:")
		self.pfw_cmdlist = list()
		url = "https://vcp.ovpn.to"
		ips = list()
		ips.append("178.17.170.116")
		ips.append("172.16.32.1")
		port = 443
		protocol = "tcp"
		for ip in ips:
			rule_name = "Allow OUT to %s at %s to Port %s Protocol %s" % (url,ip,port,protocol)
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % \
					(option,rule_name,ip,port,protocol)
			self.pfw_cmdlist.append(rule_string)
			
		return self.win_join_netsh_cmd()	

		
	def win_firewall_allow_outbound(self):
		self.debug(text="def win_firewall_allow_outbound:")
		self.pfw_cmdlist = list()
		self.pfw_cmdlist.append("advfirewall set privateprofile firewallpolicy blockinbound,allowoutbound")
		#self.pfw_cmdlist.append('interface set interface "%s" DISABLED'%(self.WIN_EXT_DEVICE))	
		#self.pfw_cmdlist.append('interface set interface "%s" ENABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()

		
	def win_firewall_modify_rule(self,option):
		self.pfw_cmdlist = list()		
		rule_name = "Allow OUT oVPN-IP %s to Port %s Protocol %s" % (self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
		if option == "add":
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % (option,rule_name,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
		if option == "delete":
			rule_string = "advfirewall firewall %s rule name=\"%s\"" % (option,rule_name)
		self.debug(text="def pfw: %s"%(rule_string))
		self.pfw_cmdlist.append(rule_string)
		return self.win_join_netsh_cmd()
			
	
	def win_join_netsh_cmd(self):
		self.pfw_cmd = "netsh.exe"
		i=0
		for cmd in self.pfw_cmdlist:
			fullstring = "%s %s" % (self.pfw_cmd,cmd)			
			try: 
				response = subprocess.check_output("%s" % (fullstring),shell=True)
				self.debug(text="pfwOK: %s" % (fullstring))
				i+=1
			except:
				self.debug(text="pfwFAIL: %s" % (fullstring))
		
		if len(self.pfw_cmdlist) == i:
			return True


	def info_window(self):
		if self.INFO_WINDOW_ACTIVE == False:
			self.info_toplevel = Toplevel(self.root)
			self.info_toplevel.attributes("-toolwindow", True)
			self.info_toplevel.title('Information')
			self.info_toplevel.protocol("WM_DELETE_WINDOW", self.info_window)
			self.info_toplevel.focus_set()
			self.INFO_WINDOW_ACTIVE = True
			xlist = list()
			xlist.append("\nAny Credits and Cookies go to:\n")
			xlist.append("+ dns.d0wn.biz for hosting DNS!")
			xlist.append("+ bauerj for code submits!")
			xlist.append("+ NhatPG for windows icons!")
			xlist.append("+ [ this place is for sale! ]")
			for x in xlist:
				infolabel = Label(self.info_toplevel,text=x)
				infolabel.pack()
		else:
			self.info_toplevel.destroy()
			self.INFO_WINDOW_ACTIVE = False

			
	def make_mini_menubar(self):
		self.mini_menubar = Menu(self)
		menu = Menu(self.mini_menubar, tearoff=0)
		self.mini_menubar.add_cascade(label="?", menu=menu)
		menu.add_command(label="Info",command=self.info_window)
		self.master.config(menu=self.mini_menubar)
		
	
	def make_menubar(self):
		""" check if menubar exists and destroy """
		if not self.menubar == False:
			self.menubar.destroy()
		""" setup our Menubar """
		menubar = Menu(self.root)
		self.root.config(menu=menubar)
		""" create first Menu: oVPN """
		ovpnMenu = Menu(menubar)		
		menubar.add_cascade(label="oVPN", underline=0, menu=ovpnMenu)
		""" create oVPN->submenu: Server """
		ovpnserver_submenu = Menu(ovpnMenu)
		label='Server'		
		if self.STATE_OVPN == True:
			servershort = self.OVPN_CONNECTEDto[:3]
			label = "Server [ %s ]" % (servershort)
		ovpnMenu.add_cascade(label=label, menu=ovpnserver_submenu, underline=0)
		""" load oVPN Server into submenu: Server """
		self.load_ovpn_server()
		for menuserver in self.OVPN_SERVER:
			self.countrycode = menuserver[:2]
			servershort = menuserver[:3]
			if self.OVPN_CONNECTEDto == menuserver:
				servershort = "[ "+servershort+" ]"
				ovpnserver_submenu.add_command(label=servershort)
			else:
				servershort = menuserver[:3]
				ovpnserver_submenu.add_command(label=servershort,command=lambda menuserver=menuserver: self.openvpn(menuserver))
		
		""" following menu commands will only run if certain states match! """
		if self.STATE_OVPN == False and not self.OVPN_FAV_SERVER == False:
			""" this state called 'mmb00' is reached if disconnected and FAV_SERVER is set. """
			""" show a connect button to join connection to FAV_SERVER. not yet done *fixme* """
			ovpnMenu.add_command(label="Connect",command=self.openvpn)

		elif self.STATE_OVPN == True and self.OVPN_PING_STAT < 0:
			""" this state called 'mmb01' is reached after ovpn connection established, but ping_timer is waiting for ping to our internal vpn gateway and user did not use any menu entry function """
			ovpnMenu.add_command(label="Load DNS",command=self.read_d0wns_dns)
			ovpnMenu.add_separator()
			ovpnMenu.add_command(label="Disconnect",command=self.kill_openvpn)
			
		elif self.STATE_OVPN == True and self.OVPN_PING_STAT >= 0:
			""" this state called 'mmb02' is reached if ovpn connection established and ping_timer is pinging our internal vpn gateway successfully """
			""" we'll come here after user hits label="Load DNS" from previous state """
			""" so we should add 'self.UPDATE_MENUBAR = True' to any function listed in previous state """
			
			""" if user hit command=self.read_d0wns_dns from previous state, make DNS Server Menu """
			if not self.d0wns_dns == False:
				""" create submenu for DNS Server """
				dnsserver_submenu = Menu(ovpnMenu)
				label = "Select DNS"
				if not self.DNS_SELECTED == False:
					label = "DNS: %s" % (self.DNS_SELECTED)
				ovpnMenu.add_cascade(label=label, menu=dnsserver_submenu, underline=0)
				""" add our internal DNS first """
				dns_ipv4 = "172.16.32.1"
				dns_country = "oVPN"
				dns_hostname = "Internal Randomized through vLAN and DNScrypt"
				label = "%s: %s (%s)" % (dns_country,dns_ipv4,dns_hostname)
				dnsserver_submenu.add_command(label=label,command=lambda dns_ipv4=dns_ipv4: self.win_netsh_change_dns_server(dns_ipv4))
				#self.debug(text="def make_menubar: len self.d0wns_dns = %s" % (len(self.d0wns_dns)))
				""" make submenu for d0wns dns """
				d0wns_dnsserver_submenu = Menu(dnsserver_submenu)
				label = "DNS by d0wn.biz (directl connection from VPN-Srv to DNS)"
				dnsserver_submenu.add_cascade(label=label, menu=d0wns_dnsserver_submenu, underline=0)
				""" load d0wns dns into DNS menu """
				for line in self.d0wns_dns:
					#print line
					try:
						dns_hostname = line[0]
						dns_ipv4 = line[1]
						dns_country =  line[2]
						dns_cryptkey = line[3]
						dns_cryptname =  line[4]
						dns_crypt_ports = line[5].split(' ')
						label = "%s: %s (%s)" % (dns_country,dns_ipv4,dns_hostname)
						d0wns_dnsserver_submenu.add_command(label=label,command=lambda dns_ipv4=dns_ipv4: self.win_netsh_change_dns_server(dns_ipv4))
					except:
						break
					
				""" finally """
				ovpnMenu.add_separator()
				ovpnMenu.add_command(label="Disconnect",command=self.kill_openvpn)
		
		""" regardless of any state, show the ? info menu """
		infoMenu = Menu(menubar)
		menubar.add_cascade(label="?", underline=0, menu=infoMenu)
		infoMenu.add_command(label="Logout",command=self.dologout)
		infoMenu.add_command(label="Info",command=self.info_window)
		
		
	
	def make_statusbar(self):
		if not self.statusbar == False:
			self.statusbar.destroy()
			self.statusbar = False
		
		if self.isSMALL_WINDOW == False:
			self.statusbar = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self.statusbar_text,font=('Courier','12','normal'))	
			
		if self.isSMALL_WINDOW == True:
			self.statusbar = Label(self, bd=0, relief=SUNKEN, anchor=W, textvariable=self.statusbar_text,font=('Courier','10','normal'))
		
		if not self.statusbar == False:
			self.statusbar.pack(side=BOTTOM, fill=X)
			
		#self.statusbar_text.set("Statusbar-Text")
		if self.timer_statusbar_running == False: 
			self.timer_statusbar()

			
	def timer_statusbar(self):

		self.timer_statusbar_running = True
		text = False
		systraytext = False

		if not self.statusbar_freeze == False:
			self.root.after(self.statusbar_freeze,self.timer_statusbar)
			self.statusbar_freeze = False
			return True		
		
		if not self.isLOGGEDin == True:
			text = "Please enter your Passphrase!"
		else:
			if self.STATE_OVPN == False:
				text = "oVPN disconnected!"
				systraytext = text
				systrayicon = self.systray_icon_disconnected
				#self.SWITCH_SYSTRAY = True
			elif self.STATE_OVPN == True:
			
				if self.OVPN_PING_STAT == -1:								
					text = "oVPN is connecting to %s"%(self.OVPN_CONNECTEDto)
					systraytext = text
					systrayicon = self.systray_icon_connect
					#self.SWITCH_SYSTRAY = True
				elif self.OVPN_PING_STAT == -2:
					self.OVPN_isTESTING = True									
					text = "oVPN is testing connection to %s" % (self.OVPN_CONNECTEDto)
					systraytext = text
					systrayicon = self.systray_icon_hourglass					
					#self.SWITCH_SYSTRAY = True
				else:					
					if self.OVPN_isTESTING == True:
						self.OVPN_PING = list()
						self.OVPN_PING_STAT = self.OVPN_PING_LAST
						self.OVPN_isTESTING = False
					now = self.get_now_unixtime()
					connectedseconds = now - self.OVPN_CONNECTEDtime
					m, s = divmod(connectedseconds, 60)
					h, m = divmod(m, 60)
					self.OVPN_CONNECTEDtimetext = "%d:%02d:%02d"  % (h,m,s)
					systraytext = "oVPN is connected to %s"%(self.OVPN_CONNECTEDto)
					text = "oVPN is connected to %s (%s/%s ms)  [%s]"%(self.OVPN_CONNECTEDto,self.OVPN_PING_LAST,self.OVPN_PING_STAT,self.OVPN_CONNECTEDtimetext)
					systrayicon = self.systray_icon_connected
						
				if self.isSMALL_WINDOW == False:
					self.SWITCH_SMALL_WINDOW = True
				
		if self.SWITCH_SMALL_WINDOW == True and self.isSMALL_WINDOW == False:
			self.isSMALL_WINDOW = True
			self.screen_width = 480
			self.screen_height = 24
			self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
			self.removethis()			
			self.make_statusbar()			
			self.SWITCH_SMALL_WINDOW = False
			self.root.attributes("-toolwindow", False)
			
		elif self.SWITCH_FULL_WINDOW == True and self.isSMALL_WINDOW == True:
			self.isSMALL_WINDOW = False	
			self.screen_width = 320
			self.screen_height = 240
			self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
			self.removethis()			
			self.make_statusbar()
			self.SWITCH_FULL_WINDOW = False
			self.root.attributes("-toolwindow", False)
			
		if not self.systraytext_from_before == systraytext and not systraytext == False:
			if self.SYSTRAYon == True:
				self.systray.shutdown()			
			self.systraytext_from_before = systraytext
			menu_options = ((systraytext, systrayicon, self.defundef),)			
			self.systray = SysTrayIcon(systrayicon, systraytext, menu_options)
			self.systray.start()
			self.SYSTRAYon = True

		if not self.statustext_from_before == text and not text == False:
			self.statusbar_text.set(text)
			self.statustext_from_before = text
			#self.debug(text="timer_statusbar: running: text = %s" % (text))
			
		if self.isLOGGEDin and self.UPDATE_MENUBAR == True:
			self.make_menubar()
			self.UPDATE_MENUBAR = False
			
		self.root.after(1000,self.timer_statusbar)
		return True

		
	"""	
	def systray2mainwindow(self):
		if self.MAIN_WINDOW_OPEN == True:
			self.root.iconify()
			self.MAIN_WINDOW_OPEN = False
		elif self.MAIN_WINDOW_OPEN == False:
			self.root.show()
			self.MAIN_WINDOW_OPEN = True
	"""	

	
	def onFormEvent(self, event ):
		i = 0
		for key in dir( event ):			
			if not key.startswith( '_' ):
				#print '%s=%s' % ( key, getattr( event, key ) )
				if key == "width" and getattr( event, key ) < self.screen_width:
					i+=1
				if key == "height"  and getattr( event, key ) < self.screen_height:
					i+=1					
			if i == 2:
				self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
				#self.debug(text="def onFormEvent: root.geometry reset")
				#print '%s=%s' % ( key, getattr( event, key ) )
				i = 0
				break

				
	def remove_lock(self):
		if os.path.isfile(self.lock_file):
			self.LOCK.close()
			try:
				os.remove(self.lock_file)
			except:
				self.msgwarn(text="Could not delete lock file")
		else:
			self.msgwarn(text="Could not delete LOCK. File not found.")


	def on_closing(self,root):
		if self.STATE_OVPN == True:
			tkMessageBox.showwarning("Warning", "Quit blocked while oVPN is connected.\nDisconnect oVPN from %s first."%(self.OVPN_CONNECTEDto[:3]))
			return False
		elif tkMessageBox.askyesno("Quit", "Quit oVPN Client?"):
			self.win_netsh_restore_dns_from_backup()
			if tkMessageBox.askyesno("Keep Firewall Protection?", "Keep Firewall loaded and block OUT to Internet?"):
				if self.win_firewall_start():
					text="Firewall enabled!\nInternet is blocked!"
					self.debug(text=text)
					#self.msgwarn(text=text)
				else:
					text="Error. Could not start Firewall!"
					self.debug(text=text)
					self.msgwarn(text=text)
			else:
				if self.win_firewall_allow_outbound():
					text="Firewall rules unloaded.\nSettings restored."
					self.debug(text=text)
					#self.msgwarn(text=text)
				else:
					text="Error! Unloading Firewall failed."
					self.debug(text=text)					
					self.msgwarn(text=text)
			if self.SYSTRAYon == True:
				self.systray.shutdown()
			self.remove_lock()
			sys.exit()
		
		
	def defundef(self):
		pass
		

def main():
	root = Tk()
	root.screen_width = 320
	root.screen_height = 240	
	root.geometry("%sx%s"%(root.screen_width,root.screen_height))
	root.resizable(0,0)
	root.attributes("-toolwindow", False)
	root.overrideredirect(False)
	root.title("oVPN.to v"+BUILT+STATE)
	app = AppUI(root).pack()	
	root.mainloop()	
	print("Ending")
	sys.exit()
	


if __name__== '__main__':
	main()
