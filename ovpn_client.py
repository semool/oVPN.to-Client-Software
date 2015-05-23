# -*- coding: utf-8 -*-
from Tkinter import *
from infi.systray import SysTrayIcon
from datetime import datetime as datetime
import Tkinter,tkMessageBox,Tkconstants,types,os,platform,sys,hashlib,random,base64,urllib,urllib2,time
import _winreg,zipfile,subprocess,threading,win32com.client,socket,random,struct
from Crypto.Cipher import AES
import gettext
import locale

BUILT="0.1.9b"
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
		self.init_localization()
		self.root = root
		self.root.bind( '<Configure>', self.onFormEvent )
		self.root.protocol("WM_DELETE_WINDOW", lambda root=root: self.on_closing(root))
		self.self_vars()		
		self.frame = Frame(self.root,bg="#1a1a1a", width=self.screen_width, height=self.screen_height)
		self.frame.pack_propagate(0)		
		self.frame.pack()
		self.make_mini_menubar()
		self.check_preboot(logout=False)
					
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
		#self.OVPN_FAV_SERVER = "BG1.ovpn.to"
		self.OVPN_AUTO_CONNECT_ON_START = False
		self.OVPN_AUTO_RECONNECT = True
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtime = False
		self.OVPN_CONNECTEDdistime = False
		self.OVPN_CONNECTEDtoIP = False
		self.OVPN_CONNECTEDtoIPbefore = False
		self.OVPN_GATEWAY_IP4 = "172.16.32.1"
		self.OVPN_THREADID = False
		self.OVPN_RECONNECT_NOW = False
		
		self.OVPN_PING = list()
		self.OVPN_isTESTING = False
		self.OVPN_PING_LAST = -1
		self.OVPN_PING_STAT = -1
		self.INTERFACES = False
		self.d0wns_dns = False
		self.DNS_SELECTED = False
		self.DNS_SELECTEDcountry = False
		self.DNS_COUNTRYLIST = False
		self.DNS_TEST_PORT=53
		self.DNS_TEST_TIMEOUT=1		
		self.DNS_DICT = {}
		self.DNS_TEST = {}
		self.DNS_PING = {}
		self.d0wns_DICT = {}
		self.d0wnsIP4s = list()
		self.d0wns_PING = False
		self.plaintext_passphrase = False
		self.save_passphrase = IntVar()
		
	def errorquit(self,text):
		self.debug(text)
		tkMessageBox.showinfo(_("Error"),"%s" % (text))
		sys.exit()

	def msgwarn(self,text):
		self.debug(text)
		tkMessageBox.showinfo(_("Warning"),"%s" % (text))	

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


	def check_preboot(self,logout):
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
							if self.plaintext_passphrase == False or logout == True:
								self.receive_passphrase()
							else:
								self.debug("def check_preboot: plaintext_passphrase loaded, try auto-login")
								self.input_PH = self.plaintext_passphrase
								if self.read_config():
									self.debug(text="def check_preboot: self.read_config() :True")
									if self.compare_confighash():
										self.plaintext_passphrase = False
										self.input_PH = False
										self.preboot = True
										self.debug(text="def check_preboot: self.compare_confighash() :True")
										self.statusbar_text.set("Passphrase Ok!")
										self.removethis()
										self.make_label(text="\n\n\nPlease wait!")
										return True
									else:
										try:
											os.remove(self.api_cfg)
											self.errorquit(text = "def check_preboot: self.compare_confighash() failed. CFG deleted.")
										except:
											self.errorquit(text = "def check_preboot: self.compare_confighash() failed. CFG delete failed.")
								else:
									try:
										os.remove(self.plaintext_passphrase_file)
										self.errorquit(text="Decryption with plaintext_passphrase failed. txt removed.")
									except:
										self.errorquit(text="Decryption with plaintext_passphrase failed. txt remove failed.")	
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
					text = _("Extraction well done!")
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
		self.make_label(text=_("oVPN.to Client Authentication\n\n\nEnter your Passphrase"))
		self.input_PH = Entry(self.frame,show="*")
		self.input_PH.pack()
		self.input_PH.focus()
		checkbox = Checkbutton(self.frame, text="Save passphrase", variable=self.save_passphrase)
		checkbox.pack()
		button = Button(self.frame, text="OK", command=self.receive_passphrase)
		button.pack()
	

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
					self.statusbar_text.set(_("Passphrase Ok!"))
					self.removethis()
					self.make_label(text=_("\n\n\nPlease wait!"))
					try:
						if self.save_passphrase.get():
							f = open(self.plaintext_passphrase_file,'w')
							f.write(self.PH)
							f.close()
					except:
						self.debug(text="def receive_passphrase: write plaintext_passphrase_file failed")
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
				self.errorquit(text = _("Operating System not supported: %s %s") % (self.OS,key1_value[0]))
			
			if self.OSBITS == "32": 
				self.OVPN_DL_URL = self.OVPN_WIN_DL_URL_x86
				self.OVPN_DLHASH = self.OVPN_WIN_DLHASH_x86
			if self.OSBITS == "64": 
				self.OVPN_DL_URL = self.OVPN_WIN_DL_URL_x64
				self.OVPN_DLHASH = self.OVPN_WIN_DLHASH_x64
				
			if DEBUG: print("def pre0_detect_os: arch=%s bits=%s key=%s OS=%s" % (self.OSARCH,self.OSBITS,key1_value[0],self.OS))
			self.win_get_interfaces()
			self.win_detect_openvpn()			
			self.root.title("oVPN v"+BUILT+STATE+" "+self.OSARCH)
			return True
		elif OS == "linux2" :
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))	
		elif OS == "darwin":
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))
		else: 
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))
	
	
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
			self.errorquit(text = _("Multiple profiles not yet implemented.\nPlease empty or rename profile-folders to *.bak (non int)\n %s") % (self.app_dir))
		
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
		
		self.dns_dir =  "%s\\dns" % (self.api_dir)
		self.dns_d0wntxt =  "%s\\dns.d0wn.biz.txt" % (self.dns_dir)
		self.dns_ung =  "%s\\ungefiltert" % (self.dns_dir)
		self.dns_ung_alphaindex =  "%s\\alphaindex.txt" % (self.dns_ung)
		
		self.plaintext_passphrase_file = "%s\\plaintext_passphrase.txt" % (self.api_dir)
		
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
		try:
			#self.debug(text="def check_config_folders userid = %s" % (self.USERID))
			self.debug(text="def check_config_folders: userid found")
			if not os.path.exists(self.api_dir):
				if DEBUG: print("api_dir %s not found, creating." % (self.api_dir))
				os.mkdir(self.api_dir)
				
			if os.path.isfile(self.lock_file):
				if tkMessageBox.askyesno(_("Client is Locked!"), _("oVPN Client is already running or did not close cleanly.\n\nDo you really want to start?")):
					try:
						os.remove(self.lock_file)
					except:
						self.msgwarn(_("Could not remove lock file.\nFile itself locked because another oVPN Client instance running?"))
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
			
			if not os.path.exists(self.dns_dir):
				os.mkdir(self.dns_dir)
				
			if not os.path.exists(self.dns_ung):
				os.mkdir(self.dns_ung)
				
			if os.path.isfile(self.plaintext_passphrase_file):
				self.debug(text="reading plaintext passphrase")
				fp = open(self.plaintext_passphrase_file,'r')
				ph = fp.read()
				fp.close()
				self.plaintext_passphrase = ph
				
			if os.path.exists(self.api_dir) and os.path.exists(self.vpn_dir) and os.path.exists(self.vpn_cfg) \
			and os.path.exists(self.prx_dir) and os.path.exists(self.stu_dir) and os.path.exists(self.pfw_dir):
				if not os.path.isfile(self.api_upd):
					if DEBUG: print("writing lastupdate to %s" % (self.api_upd))
					cfg = open(self.api_upd,'w')
					cfg.write("0")
					cfg.close()
					
				if not os.path.isfile(self.api_upd):
					self.errorquit(text = _("Creating FILE\n%s\nfailed!") % (self.api_upd))
					
				if os.path.isfile(self.api_cfg):
					self.debug(text="def check_config_folders :True")
					return True
				else:
					return False
			else:
				self.errorquit(text = _("Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!") % (self.api_dir,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))
		except:
			self.errorquit(text="def check_config_folders: failed")

			
	def form_ask_userid(self):
		if DEBUG: print("def form_ask_userid")
		self.removethis()
		self.make_label(text = _("oVPN.to Client\n\n\nPlease enter your oVPN.to User-ID Number:"))
		self.input_userid = Entry(self.frame)
		self.input_userid.pack()
		self.input_userid.focus()
		button = Button(self.frame, text="OK", command=self.receive_userid)
		button.pack()

		
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
		self.make_label(text=_("oVPN.to Client Setup\n\nPlease enter a passphrase to encrypt your API configuration.\n"))
		self.make_label(text="\n" + _("New passphrase:"))		
		self.input_PH1 = Entry(self.frame,show="*")
		self.input_PH1.pack()
		self.input_PH1.focus()
		self.make_label(text="\n" + _("Repeat your new passphrase:"))
		self.input_PH2 = Entry(self.frame,show="*")
		self.input_PH2.pack()
		# create a margin
		Label(self.frame).pack()
		Button(self.frame, text=_("Save Encryption Passphrase!"), command=self.receive_new_passphrase).pack(ipadx=10, ipady=10)
		
		
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
		self.make_label(text=_("oVPN.to Client Setup\n\n\nEnter your oVPN.to API-Key:"))
		self.input_apikey = Entry(self.frame,show="*")
		self.input_apikey.pack()
		self.input_apikey.focus()
		
		button = Button(self.frame, text=_("Save API-Key!"), command=self.write_new_config)
		button.pack()
		

		
	def gui_check_remotelogin(self):
		self.removethis()
		#if DEBUG: print("check_remotelogin: userid=%s apikey=%s") % (self.USERID,self.APIKEY)
		
		Label(self.frame,text=_("oVPN.to Client %s\n\n\n") % (self.USERID)).pack()
		
		if self.curl_api_request(API_ACTION = "lastupdate"):
			#self.debug(text="self.curldata: %s" % (self.curldata))
			self.remote_lastupdate = self.curldata
			if self.check_last_server_update():
				text = _("Updating oVPN Configurations...")
				self.statusbar_text.set(text)
				self.make_label(text = text)
				if self.curl_api_request(API_ACTION = "getconfigs"):
					text = _("Updating oVPN Certificates......")
					self.statusbar_text.set(text)
					self.make_label(text = text)
					if self.curl_api_request(API_ACTION = "requestcerts"):
						self.make_label(text = _("Please wait up to 5 minutes."))
						self.timer_check_certdl()
						return True
			else:
				self.make_label(text=_("Checking for oVPN Updates: Complete!"))
				self.make_label(text="\n\n" + _("Alpha is not Beta!\nThanks for testing!"))
				return True	
		else:
			self.msgwarn(text=_("Connection failed to https://vcp.ovpn.to!"))

			
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
		try:
			z1file = zipfile.ZipFile(self.zip_cfg)
			z2file = zipfile.ZipFile(self.zip_crt)		
			z1file.extractall(self.vpn_cfg) 
			z2file.extractall(self.vpn_cfg)
			if self.write_last_update():
				self.statusbar_text.set("Certificates and Configs extracted.")
				return True
		except:
			self.debug(text="def extract_ovpn: failed")

			
	def timer_check_certdl(self):
		self.timer_check_certdl_running = True
		self.curl_api_request(API_ACTION = "requestcerts")

		if not self.body == "ready":
			if len(self.timer_check_certdl_dots) > 4: self.timer_check_certdl_dots = ""
			self.timer_check_certdl_dots = "%s." % (self.timer_check_certdl_dots)
			text = _("Updating oVPN Certificates%s") % (self.timer_check_certdl_dots)
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
					self.make_label(text = "\n" + _("oVPN Server Update Failed!"))
					return False


	def check_inet_connection(self):
		s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = "vcp.ovpn.to"
		port = 443
				
		if not self.try_socket(host,port):
			text=_("1) Could not connect to vcp.ovpn.to\nTry setting firewall rule to access VCP!")
			#self.msgwarn(text=text)
			self.debug(text=text)
			self.win_firewall_add_rule_to_vcp(option="add")
			time.sleep(2)
			if not self.try_socket(host,port):
				text=_("2) Could not connect to vcp.ovpn.to\nRetry")
				#self.msgwarn(text=text)
				self.debug(text=text)
				time.sleep(2)
				if not self.try_socket(host,port):
					#text="3) Could not connect to vcp.ovpn.to\nTry setting firewall rule to allowing outbound connections to world!"
					#self.win_firewall_allow_outbound()
					text=_("3) Could not connect to vcp.ovpn.to\n")
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

		
	def read_ungefiltert_surfen_dns(self,countrycode,countryindexupdate):
		file = self.dns_ung_alphaindex
		if countrycode == None:			
				if countryindexupdate == True:
					try:
						if os.path.isfile(file):
							os.remove(file)
						self.DNS_COUNTRYLIST = False
					except:
						pass
				try:
					countryindex = open(file,'r')
					body = countryindex.read()
					countryindex.close()
					self.DNS_COUNTRYLIST = list()
					for line in body.split('\n'):
						if len(line) > 3:
							try:
								splitline = line.split('=',1)
								splitline[1] = base64.b64decode(splitline[1])
								splitline[1] = splitline[1].decode('utf8')
								self.DNS_COUNTRYLIST.append(splitline)
							except:
								self.debug(text="def rusd: read from file: append(splitline) = %s failed"%(splitline)) 
					self.debug(text="def rusd: read from file")
					self.UPDATE_MENUBAR = True
					return True
				except:
					pass
					self.debug(text="def rusd: read from file failed")
				
		if self.DNS_COUNTRYLIST == False:
			""" load countrylist from website """
			body = False
			urls = ["https://vcp.ovpn.to/files/dns/ungefiltert-surfen.de/mirror.html","https://vcp.ovpn.to/files/dns/ungefiltert-surfen.de/mirror.bak","http://www.ungefiltert-surfen.de/"]
			for url in urls:
				if not body == False:
					break
				try: 
					headers = { 'User-Agent' : 'oVPN.to Client - Loading Country List. Contact support@ovpn.to or join https://webirc.ovpn.to' }
					req = urllib2.Request(url, None, headers)				
					response = urllib2.urlopen(req)
					body = response.read()
					self.DNS_COUNTRYLIST = list()
					self.debug(text="def rusd: read dns countrylist from url %s"%(url))
				except:
					text = "URL TIMEOUT: %s" % (url)
					self.debug(text=text)
					#self.msgwarn(text=text)
			if not body  == False:
				#print body
				i=0
				if os.path.isfile(file):
					os.remove(file)
				for line in body.split('\n'):
					if line.startswith('<li><a href="/nameserver/') and line.endswith("</a></li>"):						
						try:
							thisline = line.decode('utf8','ignore')
							#thisline = line.decode('utf8')
							try:
								thisline = thisline.replace('<li><a href="/nameserver/','')
								thisline = thisline.replace('html">','')
								thisline = thisline.replace('</a></li>','')
								splitline = thisline.split('.',1)
								try:
									self.DNS_COUNTRYLIST.append(splitline)								
									try:
										#content = "%s=%s\n" % (,splitline[1])
										try:
											splitline[1] = splitline[1].encode('utf8')
										except:
											self.debug(text="def rusd: splitline encode utf8 failed")
										try:
											b64countryname = base64.b64encode(splitline[1])
											content = splitline[0]+'='+b64countryname+'\n'
											countrycode = splitline[0]
										except:
											self.debug(text="def rusd: splitline b64 encode failed")										
										try:
											fpindex = open(self.dns_ung_alphaindex, "a")
											try:
												fpindex.write(content)
												try:
													fpindex.close()
													#self.debug(text="def rusd: write content %s to file"%(content))
												except:
													self.debug(text="def rusd: fpindex close failed")
											except:			
												self.debug(text="def rusd: fpindex write content failed: content = %s"%(content))
										except:
											self.debug(text="def rusd: fpindex open failed")
									except:
										self.debug(text="def rusd: build content failed")									
								except:
									self.debug(text="def rusd: self.DNS_COUNTRYLIST.append(splitline) failed")
							except:								
								self.debug(text="def rusd: thisline replace failed")
						except:
							self.debug(text="def rusd: thisline failed")
					
				if len(self.DNS_COUNTRYLIST)> 0:
					self.debug(text="def rusd: self.DNS_COUNTRYLIST = %s"%(len(self.DNS_COUNTRYLIST)))
					self.UPDATE_MENUBAR = True
					self.statusbar_freeze = 2000
					self.statusbar_text.set("oVPN is loading %s DNS Country into Menu"%(len(self.DNS_COUNTRYLIST)))
					return True
				
		elif not self.DNS_COUNTRYLIST == False and not countrycode == None:
			""" we already loaded the full country list """
			""" now load dns from specific country """
			body = False
			try:
				self.debug(text="download dns for countrycode: %s"%(countrycode))
				headers = { 'User-Agent' : 'oVPN.to Client - Loading DNS from Country. Contact support@ovpn.to or join https://webirc.ovpn.to' }
				url = "http://www.ungefiltert-surfen.de/nameserver/%s.txt" % (countrycode)
				req = urllib2.Request(url)				
				response = urllib2.urlopen(req)
				body = response.read()				
			except:
				text = _("URL TIMEOUT: %s") % (url)
				self.debug(text=text)
				self.msgwarn(text=text)			
			if not body == False:
				#print body
				file = "%s\\%s.txt"%(self.dns_ung,countrycode)
				try:
					""" write countrycode dns to file and trigger UPDATE_MENUBAR """
					dns = open(file,'w')
					dns.write(body)
					dns.close()
					self.debug(text="dns for %s written to %s"%(countrycode,file))
					try:
						""" check if we have a dictionary and set empty list to clear cache """
						dnslist = self.DNS_DICT[countrycode]
						self.DNS_DICT[countrycode] = list()					
						pass
						#self.debug(text="dns cache cleared for %s"%(countrycode))
					except:
						pass
					try:
						self.read_ungefiltert_dns_file(file,countrycode)
						self.debug(text="def: rusd: self.read_ungefiltert_dns_file(file,%s) :True"%(countrycode))
					except:
						self.debug(text="def: rusd: self.read_ungefiltert_dns_file(file,%s) failed"%(countrycode))
					self.UPDATE_MENUBAR = True
					return True
				except:
					print("Write to %s failed"%(file))
					return False


	def DNStest(self,addr):
		try:
			try:
				domains = ["google","wikipedia","spiegel"]
				domain = random.choice(domains)
				if domain == "google":
					tlds = ["com","net","org"]
				elif domain == "wikipedia":
					tlds = ["com","net","org"]
				elif domain == "spiegel":
					tlds = ["info","net","de"]
				sub = "www"	
				tld = random.choice(tlds)
				dnshost = [sub,domain,tld]
				packet=struct.pack("!HHHHHH", 0x0001, 0x0100, 1, 0, 0, 0)
				for name in dnshost:
					query=struct.pack("!b"+str(len(name))+"s", len(name), name)
					packet=packet+query	
				packet=packet+struct.pack("!bHH",0,1,1)
				try:
					s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
					s.settimeout(self.DNS_TEST_TIMEOUT)
					# send DNS question to server
					sendcount=s.sendto(packet, 0, (addr,self.DNS_TEST_PORT))
					if sendcount <= 0:
						return False
					start = int(time.time() * 1000)
					try:
						recvdata=s.recvfrom(1024)
					except socket.error, e:
						return False
					try:
						end = int(time.time() * 1000)
						tdiff = end-start
						self.debug(text="def DNStest: DNS %s (%s) %s"%(addr,tdiff,dnshost))
						self.DNS_PING[addr] = tdiff
						#self.debug(text="def DNStest: DICT self.DNS_PING[%s] = %s"%(addr,self.DNS_PING[addr]))
						#self.statusbar_freeze = 100
						#self.statusbar_text.set(text)
						return True
					except:
						self.debug(text="def DNStest: calc failed")
				except:
					self.debug(text="def DNStest: socket socket failed")				
			except:
				self.debug(text="def DNStest: struct packet failed")
		except:
			self.debug(text="def DNStest: failed")
		
					
	def read_ungefiltert_dns_file(self,file,countrycode):
		try:
			dnslist = self.DNS_DICT[countrycode]
			random.shuffle(dnslist)
			self.dnslist = list()
			self.dnslist = dnslist[-8:]
			#self.debug(text="reloaded dnslist [%s] from cache self.DNS_DICT[%s]"%(countrycode,countrycode))
			try:
				if self.DNS_TEST[countrycode] == "DNStest" and len(self.dnslist) > 0:
					""" send query to every loaded dns and measure response time """
					responses = 0
					for trydns in self.dnslist:
						self.debug(text="spawn DNStest with addr %s from [%s]"%(trydns,countrycode))
						response = False
						try:							
							response = self.DNStest(trydns)
							if response == True:
								responses+=1
								self.debug(text="def read_ungefiltert_dns_file: self.DNStest(trydns) response = %s"%(response))
								self.debug(text="def read_ungefiltert_dns_file: self.DNS_PING[%s] = %s"%(trydns,self.DNS_PING[trydns]))
						except:
							self.debug(text="def read_ungefiltert_dns_file: self.DNStest(trydns) failed")				
					if responses > 0:
						self.DNS_TEST[countrycode] = False
						#self.UPDATE_MENUBAR = True
						self.debug(text="def read_ungefiltert_dns_file: responses = %s"%(responses))	
						return True
			except:
				pass
				#self.debug(text="def read_ungefiltert_dns_file: 'if self.DNS_TEST[countrycode] == DNStest' failed"%(countrycode))
		except:
			pass
			#self.debug(text="No DNS cache-DICT for [%s], try read from file."%(countrycode))
		try:
			if os.path.isfile(file):
				dns = open(file,'r')
				read_data = dns.read()
				dns.close()
				dnslist = list()
				i=0
				for line in read_data.split('\n'):
					if self.isValueIPv4(line):
						dnslist.append(line)
						i+=1
				if i > 0:
					self.DNS_DICT[countrycode] = dnslist
					#self.debug(text="def read_ungefiltert_dns_file: DNS IPs: %d countrycode %s"%(i,countrycode))
					""" randomize/shuffle loaded dns from file """
					random.shuffle(dnslist)
					self.dnslist = list()
					self.dnslist = dnslist[-8:]
					if len(self.dnslist) > 0:
						return True
					else:
						self.dnslist = ["Error reading DNS from cachefile"]
				else:
					return False
			else:
				""" maybe spawn def read_ungefiltert_surfen_dns with countrycode to update it """
				return False
		except:
			self.debug(text="def read_ungefiltert_dns_file: %s [%s] failed"%(file,countrycode))

			
	def update_d0wns_dns_from_url(self):
		if not self.OVPN_PING_STAT >= 0:
			self.UPDATE_MENUBAR = True
			return False

		urls = ["https://vcp.ovpn.to/files/dns/d0wns_dns.txt","https://dns.d0wn.biz/dns.txt"]
		for url in urls:
			try: 
				text = "try reading d0wns dns from url: %s" % (url)
				self.debug(text=text)			
				req = urllib2.Request(url)
				body = False		
				response = urllib2.urlopen(req)
				body = response.read()
			except:
				text = "URL TIMEOUT: %s" % (url)
				self.debug(text=text)
				self.msgwarn(text=text)
			if not body  == False:
				try:
					fp = open(self.dns_d0wntxt, "wb")
					fp.write(body)
					fp.close()
					try:
						self.read_d0wns_dns_from_file(update=False)
						return True
					except:
						self.debug(text="def update_d0wns_dns_from_url: try: self.read_d0wns_dns_from_file() failed")					
				except:
					pass
		return False
					
					
	def read_d0wns_dns_from_file(self,update):
		file = self.dns_d0wntxt
		if update == True:
			try:
				if os.path.isfile(file):
					os.remove(file)
				self.d0wns_DICT = {}
				self.d0wnsIP4s = list()
			except:
				pass
				self.debug(text="def read_d0wns_dns_from_file: force-update failed")
		try:
			self.d0wns_dns = self.d0wns_DICT["d0wnsdns"]
			try:
				if update == "DNStest":
					#self.debug(text="def read_d0wns_dns_from_file: DNStest")
					responses = 0
					for trydns in self.d0wnsIP4s:
						#self.debug(text="def read_d0wns_dns_from_file: DNStest %s"%(trydns))
						response = False
						try:
							response = self.DNStest(trydns)
							if response == True:
								responses+=1
								#self.debug(text="def read_d0wns_dns_from_file: self.DNStest(trydns) response = %s"%(response))
								#self.debug(text="def read_d0wns_dns_from_file: self.DNS_PING[%s] = %s"%(trydns,self.DNS_PING[trydns]))
						except:
							pass
							#self.debug(text="def read_d0wns_dns_from_file: self.DNStest(trydns) failed")				
					if responses > 0:
						self.UPDATE_MENUBAR = True
						#self.debug(text="def read_d0wns_dns_from_file: responses = %s"%(responses))	
						return True
			except:
				self.debug(text="def read_d0wns_dns_from_file: try: DICT try: DNStest failed")
					
			self.debug(text="def read_d0wns_dns_from_file: load from cache")
			self.UPDATE_MENUBAR = True
			return True
		except:
			pass
			self.debug(text="def read_d0wns_dns_from_file: no cache found, read from file")	
		try:
			if not os.path.isfile(file):
				try:
					self.update_d0wns_dns_from_url()
					return True
				except:
					self.debug(text="def read_d0wns_dns_from_file: try: self.update_d0wns_dns_from_url() failed")
			elif os.path.isfile(file):
				try:					
					dns = open(file,'r')
					body = dns.read()
					dns.close()
					dnslist = body.split('\n')
					self.d0wns_dns = list()
					i=0
					dnslist.pop(-1)
				except:
					self.debug(text="def read_d0wns_dns_from_file: open file failed")
				try:
					if len(dnslist) >= 1:
						self.d0wnsIP4s = list()
						for line in dnslist:
							content = line.split(',')
							""" check if our loaded content is valid """
							if len(content) >= 6:
								if content[0].startswith('ns') and content[0].endswith('.dns.d0wn.biz'):
									for value in content[0].split('.'):
										if not value.isalnum():
											break
									
									if self.isValueIPv4(content[1]):
										self.d0wnsIP4s.append(content[1])
										if content[2].isalnum() and len(content[3].split(':')) == 16:
											for hex in content[3].split(':'):
												if not hex.isalnum() or not len(hex) == 4:
													break
											
											if content[4] == "2.dnscrypt-cert.d0wn.biz":
												for port in content[5].split(' '):
													if not port.isdigit():
														break
											#self.debug(text="content %s\n:0,1,2,3,4,5 ok"%(content))
											self.d0wns_dns.append(content)
											self.UPDATE_MENUBAR = True
											i+=1
							else:
								self.debug(text="def read_d0wns_dns_from_file: ! line len(content) >= 6")
				except:
					self.debug(text="def read_d0wns_dns_from_file: check file content failed")
				""" we need a -1 here because d0wns dns.txt is auto-generated with trailing \n """
				if len(dnslist)-1 == len(self.d0wns_dns) and len(dnslist) >= 3:
					self.d0wns_DICT["d0wnsdns"] = self.d0wns_dns
					self.statusbar_freeze = 1000
					self.statusbar_text.set("oVPN is loading DNS Menu. Please wait...")
					#self.debug(text="TRUE len(dnslist) = %s len(self.d0wns_dns) = %s i = %s"%(len(dnslist)-1,len(self.d0wns_dns),i))
					return True
				else:
					self.debug(text="FALSE len(dnslist) = %s len(self.d0wns_dns) = %s i = %s"%(len(dnslist),len(self.d0wns_dns),i))
					self.debug(text="dnslist =\n%s"%(dnslist))
					self.debug(text="self.d0wns_dns =\n%s"%(self.d0wns_dns))
					""" """
					return False
		except:
			self.debug(text="def read_d0wns_dns_from_file: failed")
			

	def isValueIPv4(self,value):
		try:
			if len(value.split('.')) == 4:
				for n in value.split('.'):
					if n.isdigit():
						#self.debug(text="def isValueIPv4: n = %s"%(n))
						if not n >= 0 and not n <= 255:
							return False
				return True	
		except:
			return False
		
				
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
			text = text=_("API Connection Timeout to https://vcp.ovpn.to!")
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
				self.errorquit(_("Invalid User-ID/API-Key. Encrypted API-Keyfile deleted."))
		
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
		if self.plaintext_passphrase == False:
			try:
				if len(self.input_PH.get()) > 0: 
					self.aeskey = hashlib.sha256(self.input_PH.get().rstrip()).digest()
					return True
			except:
				return False
		else:
			try:
				if len(self.input_PH) > 0:
					self.aeskey = hashlib.sha256(self.input_PH.rstrip()).digest()
					return True
			except:
				return False

			
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
			self.statusbar_text.set(_("Invalid Passphrase!"))
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
			self.check_preboot(logout=False)			

			
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
			self.debug(text=_("Logout"))
			self.make_mini_menubar()
			self.LOCK.close()
			if self.SYSTRAYon == True:
				self.systray.shutdown()
			self.remove_lock()
			self.check_preboot(logout=True)
		else:
			self.msgwarn(text=_("Disconnect first!"))
		

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
						ip = line.split()[1]
						port = int(line.split()[2])
						if self.isValueIPv4(ip) and port > 0 and port < 65535:
							self.OVPN_CONNECTEDtoIP = ip
							self.OVPN_CONNECTEDtoPort = port
						#break
					except:
						self.errorquit(text=_("Could not read Servers Remote-IP:Port from config: %s") % (self.ovpn_server_config_file) )
				if "proto " in line:
					try:
						proto = line.split()[1]
						if proto.lower()  == "tcp" or proto.lower() == "udp":
							self.OVPN_CONNECTEDtoProtocol = proto
					except:
						self.errorquit(text=_("Could not read Servers Protocol from config: %s") % (self.ovpn_server_config_file) )
			
			
			self.ovpn_sessionlog = "%s\ovpn.log" % (self.vpn_dir)
			self.ovpn_server_dir = "%s\%s" % (self.vpn_cfg,self.ovpn_server_LOWER)
			self.ovpn_cert_ca = "%s\%s.crt" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_tls_key = "%s\%s.key" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_cli_crt = "%s\client%s.crt" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_cli_key = "%s\client%s.key" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_string = "\"%s\" --config \"%s\" --ca \"%s\" --cert \"%s\" --key \"%s\" --tls-auth \"%s\" --log \"%s\" " % (self.OPENVPN_EXE,self.ovpn_server_config_file,self.ovpn_cert_ca,self.ovpn_cli_crt,self.ovpn_cli_key,self.ovpn_tls_key,self.ovpn_sessionlog)
			
			try:
				self.call_ovpn_srv = server
				thread_spawn_openvpn_process = threading.Thread(target=self.inThread_spawn_openvpn_process)
				thread_spawn_openvpn_process.start()
				self.OVPN_THREADID = threading.currentThread()
				self.debug(text=_("Started: oVPN %s on Thread: %s") %(server,self.OVPN_THREADID))
			except:
				text=_("Error! Unable to start thread: oVPN %s ")%(server)
				self.statusbar_freeze = 6000
				self.statusbar_text.set(text)
				self.msgwarn(text=text)
				self.debug(text=text)
				
			if self.OVPN_AUTO_RECONNECT == True:
				self.debug("def openvpn: self.OVPN_AUTO_RECONNECT == True")
				self.OVPN_RECONNECT_NOW = False
				try:
					#threading.Thread(target=self.inThread_timer_openvpn_reconnect).start()
					thread_timer_openvpn_reconnect = threading.Thread(target=self.inThread_timer_openvpn_reconnect)
					thread_timer_openvpn_reconnect.start()
					self.OVPN_PING_TIMER_THREADID = threading.currentThread()
					self.debug(text="Started: self.inThread_timer_openvpn_reconnect() on Thread: %s" %(self.OVPN_PING_TIMER_THREADID))
					#self.statusbar_freeze = 500
					text = "oVPN Process Watchdog enabled."
					#self.statusbar_text.set(text)
					self.debug(text=text)
				except:
					self.statusbar_freeze = 6000
					text = "Could not start oVPN Watchdog"
					self.statusbar_text.set(text)
					self.debug(text=text)
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
			
			if self.OS == "win32":
				ovpn_ping_cmd = "ping.exe -n 1 172.16.32.1"
				PING_PROC = False
				try:
					PING_PROC = subprocess.check_output("%s" % (ovpn_ping_cmd),shell=True)
				except:
					self.debug(text="def inThread_timer_ovpn_ping: ping.exe failed")
					pass
					
				try:
					OVPN_PING_out = PING_PROC.split('\r\n')[2].split()[4].split('=')[1][:-2]
				except:
					self.debug(text="def inThread_timer_ovpn_ping: split ping failed, but normally not an issue while connection is testing")
					OVPN_PING_out = -2
				
				pingsum = 0
				if OVPN_PING_out > 0:
					self.OVPN_PING.append(OVPN_PING_out)
					self.OVPN_PING_LAST = OVPN_PING_out
				if len(self.OVPN_PING) > 360:
					self.OVPN_PING.pop(0)
				if len(self.OVPN_PING) > 0:
					for ping in self.OVPN_PING:
						pingsum += int(ping)
					self.OVPN_PING_STAT = pingsum/len(self.OVPN_PING)
				#self.debug(text="ping = %s\n#############\nList len=%s\n%s\npingstat=%s"%(OVPN_PING_out,len(self.OVPN_PING),self.OVPN_PING,self.OVPN_PING_STAT))
				if self.OVPN_PING_STAT >= 0:
					if self.OVPN_CONNECTEDtime > 60:
						time.sleep(10)
					else:
						time.sleep(3)
				else:
					time.sleep(1)
				try:
					pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
					pingthread.start()
					self.OVPN_PING_TIMER_THREADID = threading.currentThread()
					self.debug(text="done: rejoin def inThread_timer_ovpn_ping() %s: total threads: %s, ping=%s" %(self.OVPN_PING_TIMER_THREADID,threading.active_count(),OVPN_PING_out))	
					return True
				except:
					self.debug(text="rejoin def inThread_timer_ovpn_ping() failed")
				
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
			self.msgwarn(_("Could not start Windows Firewall!"))
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
		
		
	def read_gateway_from_routes(self):
		try:
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
		except:
			self.debug(text="def read_gateway_from_routes: failed")

				
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
		if not self.GATEWAY_DNS == self.OVPN_GATEWAY_IP4:
			self.debug(text="def win_netsh_set_dns_ovpn:")
			string1 = "netsh interface ip set dnsservers \"%s\" static 172.16.32.1 primary no" % (self.WIN_EXT_DEVICE)
			string2 = "netsh interface ip set dnsservers \"%s\" static 172.16.32.1 primary no" % (self.WIN_TAP_DEVICE)
			try: 
				read1 = subprocess.check_output("%s" % (string1),shell=True)
				read2 = subprocess.check_output("%s" % (string2),shell=True)
				self.debug(text=":true")
			except:
				self.debug(text="def win_netsh_set_dns_ovpn: setting dns failed:\n%s\n%s"%(string1,string2))

				
	def win_netsh_change_dns_server(self,dns_ipv4,countrycode):
		self.debug(text="def win_netsh_change_dns_server: %s %s"%(dns_ipv4,countrycode))
		string1 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_EXT_DEVICE,dns_ipv4)
		string2 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_TAP_DEVICE,dns_ipv4)
		try: 
			read1 = subprocess.check_output("%s" % (string1),shell=True)
			read2 = subprocess.check_output("%s" % (string2),shell=True)
			text = _("oVPN DNS changed to %s") % (dns_ipv4)
			if dns_ipv4 == False:
				dns_ipv4 = self.OVPN_GATEWAY_IP4
			if dns_ipv4 == self.OVPN_GATEWAY_IP4:
				text = "%s (Randomized)" % (text)
			elif dns_ipv4 == "127.0.0.1":
				text = _("%s (DNScrypt enabled)") % (text)
			else:
				text = _("%s (direct connection)") % (text)
			self.statusbar_freeze = 5000
			self.statusbar_text.set(text)
			self.DNS_SELECTED = dns_ipv4
			self.DNS_SELECTEDcountry = countrycode
			self.UPDATE_MENUBAR = True
			self.debug(text=":true")
		except:
			self.statusbar_freeze = 5000
			self.statusbar_text.set(_("oVPN DNS Change failed!"))		
			self.debug(text="def win_netsh_change_dns_server: failed\n%s\n%s"%(string1,string2))
		
	
	def win_netsh_restore_dns_dhcp(self):
		os.system('netsh interface ip set dnsservers "%" dhcp'%(self.WIN_EXT_DEVICE))

		
	def win_netsh_restore_dns_from_backup(self):
		if not self.GATEWAY_DNS == self.OVPN_GATEWAY_IP4:
			string = 'netsh interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS)
			read = False
			try: 
				read = subprocess.check_output("%s" % (string),shell=True)
			except:
				pass
			if not read == False:
				self.msgwarn(text=_("Primary DNS Server restored to: %s")%(self.GATEWAY_DNS))
			else:
				self.msgwarn(text=_("Error: Restoring your DNS Server to %s failed.")%(self.GATEWAY_DNS))
			self.debug(text="def win_netsh_restore_dns_from_backup: %s"%(read))

			
	def win_netsh_read_dns_to_backup(self):
		string = "netsh interface ipv4 show dns"
		read = subprocess.check_output("%s" % (string),shell=True)
		read = read.strip().decode('cp1258','ignore')
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
					if self.isValueIPv4(dns):
						self.GATEWAY_DNS = dns
						break
					else: 
						self.GATEWAY_DNS = self.GATEWAY_LOCAL
						break
			i+=1
		self.debug(text="self.GATEWAY_DNS = %s"%(self.GATEWAY_DNS))
			
		
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
			self.errorquit(text=_("Could not find openvpn.exe"))
		else:
			try:
				out, err = subprocess.Popen("\"%s\" --version" % (self.OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()		
			except:
				self.errorquit(text=_("Could not detect openVPN Version!"))
				
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
					built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					if built_timestamp >= self.OVPN_LATEST_BUILT_TIMESTAMP:				
						return True
					else:
						self.errorquit(text=_("Please update your openVPN Version!"))
			else:
				self.errorquit(text=_("Please update your openVPN Version!"))

	
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
			self.errorquit(text=_("Could not read your Network Interfaces!"))
		
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
				""" do not remove! maybe need for debug in future """
				#elif line.startswith("Available TAP-WIN32 adapters"):
				#	#self.debug(text="ignoring tap line")
				#	pass
				#elif len(line) < 16:
				#	#self.debug(text="ignoring line < 16")
				#	pass
				#else:
				#	#self.debug(text="ignoring else")
				#	pass
					
		if self.WIN_TAP_DEVICE == False:
			self.errorquit(text=_("No openVPN TAP-Adapter found!"))
		else:
			self.INTERFACES.remove(self.WIN_TAP_DEVICE)
			self.debug(text="remaining INTERFACES = %s"%(self.INTERFACES))
			if len(self.INTERFACES) > 1:
				window = Toplevel()
				window.title(_("Choose your External Network Adapter!"))
				text = Label(window, text=_("Multiple network adapters found.\nPlease select your external network adapter (the one you use to connect to the Internet)!"))
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
				self.errorquit(text=_("No Network Adapter found!"))
			else:
				self.WIN_EXT_DEVICE = self.INTERFACES[0]
				text = _("External Interface = %s")%(self.WIN_EXT_DEVICE)
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
		ips.append(self.OVPN_GATEWAY_IP4)
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
		#self.debug(text="def pfw: %s"%(rule_string))
		self.pfw_cmdlist.append(rule_string)
		return self.win_join_netsh_cmd()
			
	
	def win_join_netsh_cmd(self):
		self.pfw_cmd = "netsh.exe"
		i=0
		for cmd in self.pfw_cmdlist:
			fullstring = "%s %s" % (self.pfw_cmd,cmd)
			try: 
				exitcode = subprocess.call("%s" % (fullstring),shell=True)
				self.debug(text="pfwOK: %s: exitcode = %s" % (fullstring,exitcode))
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
			xlist.append("\n" + _("Any Credits and Cookies go to:") + "\n")
			xlist.append(_("+ d0wn for hosting DNS on dns.d0wn.biz!"))
			xlist.append(_("+ bauerj for code submits!"))
			xlist.append(_("+ dogpellet for DNStest() ideas!"))
			xlist.append(_("+ [ this place is for sale! ]"))
			xlist.append(_("+ ungefiltert-surfen.de for DNS Lists!"))
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
		menu.add_command(label=_("Info"),command=self.info_window)
		self.root.config(menu=self.mini_menubar)
		
	
	def make_menubar(self):
		""" check if menubar exists and destroy """
		if not self.menubar == False:
			self.menubar.destroy()
		""" setup our Menubar """
		menubar = Menu(self.root)		
		""" create first Menu: oVPN """
		ovpnMenu = Menu(menubar)		
		menubar.add_cascade(label="oVPN", underline=0, menu=ovpnMenu)
		""" create oVPN->submenu: Server """
		ovpnserver_submenu = Menu(ovpnMenu)
		label="Select oVPN Server"	
		if self.STATE_OVPN == True:
			servershort = self.OVPN_CONNECTEDto[:3]
			label = "Server [ %s ] %s (%s:%s)" % (servershort,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoProtocol.upper(),self.OVPN_CONNECTEDtoPort)
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
			try:
				""" this state called 'mmb00' is reached if disconnected and FAV_SERVER is set. """
				""" show a connect button to join connection to FAV_SERVER. not yet done *fixme* """
				ovpnMenu.add_command(label="FAV Connect: %s"%(self.OVPN_FAV_SERVER),command=lambda: self.openvpn(self.OVPN_FAV_SERVER))
			except:
				self.debug(text="def mmb: state called 'mmb00' failed")
		elif self.STATE_OVPN == True and self.OVPN_PING_STAT < 0:
			""" this state called 'mmb01' is reached after ovpn connection established, but ping_timer is waiting for ping to our internal vpn gateway and user did not use any menu entry function """
			try:
				self.DNS_SELECTEDcountry = "Randomized"
				dlabel = "Change DNS: %s" % (self.DNS_SELECTEDcountry)				
				self.DNS_SELECTED = self.OVPN_GATEWAY_IP4
				ovpnMenu.add_command(label=dlabel,command=lambda update=False: self.read_d0wns_dns_from_file(update=False))
				ovpnMenu.add_separator()
				ovpnMenu.add_command(label="Disconnect",command=self.kill_openvpn)
			except:
				self.debug(text="def mmb: state called 'mmb01' failed")
			
		elif self.STATE_OVPN == True and self.OVPN_PING_STAT >= 0:
			""" this state called 'mmb02' is reached if ovpn connection established and ping_timer is pinging our internal vpn gateway successfully """
			""" we'll come here after user hits label="Load DNS" from previous state """
			""" so we should add 'self.UPDATE_MENUBAR = True' to any function listed in previous state """
			
			""" if user hit command=self.read_d0wns_dns from previous state, make DNS Server Menu """
			if not self.d0wns_dns == False:
				""" create submenu for DNS Server """
				dnsserver_submenu = Menu(ovpnMenu)
				if self.DNS_SELECTEDcountry == False:
					label = "Randomized"
					self.DNS_SELECTEDcountry = label
					self.DNS_SELECTED = self.OVPN_GATEWAY_IP4
				if not self.DNS_SELECTED == False:
					if len(self.DNS_SELECTEDcountry) == 2:
						self.DNS_SELECTEDcountry.upper()
					label = "DNS: [%s] %s " % (self.DNS_SELECTEDcountry,self.DNS_SELECTED)
				ovpnMenu.add_cascade(label=label, menu=dnsserver_submenu, underline=0)
				""" add our internal DNS first """
				dns_ipv4 = self.OVPN_GATEWAY_IP4
				countrycode = "Randomized"
				label = "%s: %s" % (countrycode,dns_ipv4)
				dnsserver_submenu.add_command(label=label,command=lambda dns_ipv4=dns_ipv4,countrycode=countrycode: self.win_netsh_change_dns_server(dns_ipv4=dns_ipv4,countrycode=countrycode))
				#self.debug(text="def make_menubar: len self.d0wns_dns = %s" % (len(self.d0wns_dns)))
				""" make submenu for d0wns dns """
				d0wns_dnsserver_submenu = Menu(dnsserver_submenu)
				label = "DNS by d0wn.biz"
				dnsserver_submenu.add_cascade(label=label, menu=d0wns_dnsserver_submenu, underline=0)
				dlabel = "Update d0wns DNS from URL"
				d0wns_dnsserver_submenu.add_command(label=dlabel,command=lambda update=True: self.read_d0wns_dns_from_file(update=True))
				dlabel = "Check DNS Ping Response"
				update = "DNStest"
				d0wns_dnsserver_submenu.add_command(label=dlabel,command=lambda update=update: self.read_d0wns_dns_from_file(update=update))				
				d0wns_dnsserver_submenu.add_separator()				
				""" load d0wns dns into DNS menu """
				for line in self.d0wns_dns:
					#print line
					try:
						dns_hostname = line[0]
						dns_ipv4 = line[1]
						countrycode =  line[2]
						dns_cryptkey = line[3]
						dns_cryptname =  line[4]
						dns_crypt_ports = line[5].split(' ')
						dnsping = "n/a"
						try:
							dnsping = self.DNS_PING[dns_ipv4]
						except:
							pass
						label = "%s: %s (%s ms)" % (countrycode,dns_ipv4,dnsping)
						#self.debug("def mmb: create d0wn dns label %s"%(label))
						countrycode = countrycode
						d0wns_dnsserver_submenu.add_command(label=label,command=lambda dns_ipv4=dns_ipv4,countrycode=countrycode: self.win_netsh_change_dns_server(dns_ipv4=dns_ipv4,countrycode=countrycode))
						
					except:
						break
					
				""" make submenu for ungefiltert-surfen dns inside ovpn->dns menu """
				ungefiltert_dnsserver_submenu = Menu(dnsserver_submenu)
				label = "DNS by ungefiltert-surfen.de"
				dnsserver_submenu.add_cascade(label=label, menu=ungefiltert_dnsserver_submenu, underline=0)
				""" check if we have ungefiltert country list loaded """
				if self.DNS_COUNTRYLIST == False:
					""" offer button to load country list """
					label = "Load Country List"
					ungefiltert_dnsserver_submenu.add_command(label=label,command=lambda countrycode=None,countryindexupdate=None: self.read_ungefiltert_surfen_dns(countrycode=None,countryindexupdate=None))
				else:
					""" we have country index file, offer option to update country index """
					commandtext = "Update Index from URL"
					ungefiltert_dnsserver_submenu.add_command(label=commandtext,command=lambda countrycode=None,countryindexupdate=True: self.read_ungefiltert_surfen_dns(countrycode=None,countryindexupdate=True))
					ungefiltert_dnsserver_submenu.add_separator()				
					""" fill submenu with alphabet chars  """
					countrylist_len = len(self.DNS_COUNTRYLIST)
					if countrylist_len >= 1:
						self.DNS_COUNTRYLIST.sort()
						charlist = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
						charfrombefore = False
						""" loop through charlist """
						for checkchar in charlist:
							label = checkchar.upper()
							""" make alphabet submenu for ungefiltert-surfen dns """
							alphabet_ungefiltert_dnsserver_submenu = Menu(ungefiltert_dnsserver_submenu)
							""" loop every content in self.DNS_COUNTRYLIST """
							for content in self.DNS_COUNTRYLIST:	
								""" if first upper char from content[0] is checkchar from charlist """
								if content[0].upper()[:1] == label:
									#self.debug(text="content = %s"%(content))
									""" create alphabetic submenu """
									if not charfrombefore == label:
										#self.debug(text="make ungefiltert menu checkchar %s" % (label))
										charfrombefore = label
										ungefiltert_dnsserver_submenu.add_cascade(label=label, menu=alphabet_ungefiltert_dnsserver_submenu, underline=1)									
									countrycode = content[0].upper()
									
									if len(content) == 2:									
										countryname = content[1]
										try:
											countryname = countryname.decode('utf8')
										except:
											pass
										
									""" a hack to replace html chars in countryname """
									try:
										countryname = countryname.replace("&#x27;","'")
									except:
										self.debug(text="countryname replace failed %s" % (countryname))

									#self.debug(text="creating submenu content %s: %s %s"%(label,countrycode,countryname))
									""" fill country into alphabet checkchar submenu """
									countrycode = countrycode.lower()
									file = "%s\\%s.txt" % (self.dns_ung,countrycode.lower())
									if not os.path.isfile(file):
										""" offer download for country if we have no local cache file"""
										commandtext="-[%s] %s" %(countrycode.upper(),countryname)										
										alphabet_ungefiltert_dnsserver_submenu.add_command(label=commandtext,command=lambda countrycode=countrycode: self.read_ungefiltert_surfen_dns(countrycode=countrycode,countryindexupdate=None))
									else:							
										""" now create submenu in alphabet_ and load dns IP from csv into it """
										dnsip_alphabet_ungefiltert_dnsserver_submenu = Menu(alphabet_ungefiltert_dnsserver_submenu)
										try:
											dnscountincountry = len(self.DNS_DICT[countrycode])
										except:
											dnscountincountry = 0
										newlabel = "+[%s] %s (%s DNS)" %(countrycode.upper(),countryname,dnscountincountry)
										alphabet_ungefiltert_dnsserver_submenu.add_cascade(label=newlabel, menu=dnsip_alphabet_ungefiltert_dnsserver_submenu, underline=0)
										
										""" first entry is Update Country Option """
										commandtext="Update Country DNS from URL"
										#self.debug(text="adding menu entry '%s' for %s"%(commandtext,countrycode))
										dnsip_alphabet_ungefiltert_dnsserver_submenu.add_command(label=commandtext,command=lambda countrycode=countrycode: self.read_ungefiltert_surfen_dns(countrycode=countrycode,countryindexupdate=None))
										dlabel = "Random Reload from Cache"
										#dnsip_alphabet_ungefiltert_dnsserver_submenu.add_command(label=dlabel,command=lambda dns_ipv4=self.DNS_SELECTED,countrycode=False: self.win_netsh_change_dns_server(dns_ipv4=self.DNS_SELECTED,countrycode=False))
										dnsip_alphabet_ungefiltert_dnsserver_submenu.add_command(label=dlabel,command=lambda countrycode=countrycode: self.reload_ungefiltert_dns_cache(countrycode=countrycode))										
										dnsip_alphabet_ungefiltert_dnsserver_submenu.add_separator()
										""" now create entry for every dns-ip in dnslist """
										try:
											#self.debug(text="def make_menubar: self.read_ungefiltert_dns_file(%s,%s):"%(file,countrycode))
											if self.read_ungefiltert_dns_file(file,countrycode) == True:												
												for dns_ipv4 in self.dnslist:
													entry = "%s (n/a ms)" % (dns_ipv4)
													#self.debug(text="def mmb: rudf: dns_ipv4 = %s" % (dns_ipv4))
													try:
														#self.debug(text="def mmb: rudf: try: check if we have a DICT DNS_PING[%s]"%(dns_ipv4))
														try:
															dnsping = self.DNS_PING[dns_ipv4]
															#self.debug(text="def mmb: dnsping for %s = %s ms"%(dns_ipv4,dnsping))
															try:
																entry = "%s (%s ms)" % (dns_ipv4,dnsping)
																#self.debug(text="def mmb: create dnsip entry = %s" % (entry))													
															except:
																pass
																#self.debug(text="def mmb: building entry with ping failed for %s"%(dns_ipv4))
														except:
															pass
															#self.debug(text="def mmb: dnsping = self.DNS_PING[%s] = %s failed"%(dns_ipv4,self.DNS_PING[dns_ipv4]))
													except:
														pass
														#self.debug(text="def mmb: bad except: DICT DNS_PING[%s] :NX"%(dns_ipv4))	
													try:
														dnsip_alphabet_ungefiltert_dnsserver_submenu.add_command(label=entry,command=lambda dns_ipv4=dns_ipv4,countrycode=countrycode: self.win_netsh_change_dns_server(dns_ipv4=dns_ipv4,countrycode=countrycode))
													except:
														self.debug("def mmb: error adding dns ip into country menu")
											self.dnslist = list()
										except:
											self.debug(text="def mmb: try: if self.read_ungefiltert_dns_file(file,countrycode) failed")


				""" finally """
				ovpnMenu.add_separator()
				ovpnMenu.add_command(label=_("Disconnect"),command=self.kill_openvpn)
		
		""" regardless of any state, show the ? info menu """
		infoMenu = Menu(menubar)
		menubar.add_cascade(label="?", underline=0, menu=infoMenu)
		infoMenu.add_command(label=_("Logout"),command=self.dologout)
		infoMenu.add_command(label=_("Info"),command=self.info_window)
		
		self.root.config(menu=menubar)
		

	def reload_ungefiltert_dns_cache(self,countrycode):
		countrycode = countrycode
		self.debug(text="def reload_ungefiltert_dns_cache: %s"%(countrycode))
		try:			
			dnslist = self.DNS_DICT[countrycode]			
			self.DNS_TEST[countrycode] = "DNStest"
			self.debug(text="def reload_ungefiltert_dns_cache: %s cleared"%(countrycode))
			self.UPDATE_MENUBAR = True
		except:
			self.debug(text="def reload_ungefiltert_dns_cache: %s failed"%(countrycode))
		
	def make_statusbar(self):
		try:
			if not self.statusbar == False:
				self.statusbar.destroy()
				self.statusbar = False
				
			self.statusbar = Label(self, bd=1, relief=SUNKEN, anchor=W, textvariable=self.statusbar_text,font=('Courier','10','normal'))
			
			if not self.statusbar == False:
				self.statusbar.pack(side=BOTTOM, fill=X)
			
			if self.timer_statusbar_running == False:
				self.timer_statusbar()
		except:
			self.debug(text="def make_statusbar: failed")

			
	def timer_statusbar(self):
		self.timer_statusbar_running = True
		text = False
		systraytext = False
		
		if self.isLOGGEDin and self.UPDATE_MENUBAR == True:
			""" enable 2 lines and disable next try to debug menubar update """
			#self.UPDATE_MENUBAR = False
			#self.make_menubar()
			try:
				self.UPDATE_MENUBAR = False
				self.make_menubar()
				self.debug(text="def timer_statusbar: self.make_menubar() :True")
				#self.statusbar_freeze = 300
				#self.statusbar_text.set("oVPN Menu Updated")
			except:
				self.debug(text="def timer_statusbar: self.make_menubar() failed")
			

		if not self.statusbar_freeze == False:
			self.root.after(self.statusbar_freeze,self.timer_statusbar)
			self.statusbar_freeze = False
			return True
			
		if not self.isLOGGEDin == True:
			text = _("Please enter your Passphrase!")
		else:
			if self.STATE_OVPN == False:
				text = _("oVPN disconnected!")
				systraytext = text
				systrayicon = self.systray_icon_disconnected
				try:
					if self.OVPN_AUTO_CONNECT_ON_START == True and not self.OVPN_FAV_SERVER == False:
						self.openvpn(self.OVPN_FAV_SERVER)
						self.OVPN_AUTO_CONNECT_ON_START = False
				except:
					self.debug(text="def timer_statusbar: OVPN_AUTO_CONNECT_ON_START failed")
			elif self.STATE_OVPN == True:
			
				if self.OVPN_PING_STAT == -1:								
					text = _("oVPN is connecting to %s")%(self.OVPN_CONNECTEDto)
					systraytext = text
					systrayicon = self.systray_icon_connect
					self.debug(text=text)
				elif self.OVPN_PING_STAT == -2:
					self.OVPN_isTESTING = True									
					text = _("oVPN is testing connection to %s") % (self.OVPN_CONNECTEDto)
					systraytext = text
					systrayicon = self.systray_icon_hourglass
					self.debug(text=text)
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
					systraytext = _("oVPN is connected to %s")%(self.OVPN_CONNECTEDto)
					text = _("oVPN is connected to %s (%s/%s ms)  [%s]")%(self.OVPN_CONNECTEDto,self.OVPN_PING_LAST,self.OVPN_PING_STAT,self.OVPN_CONNECTEDtimetext)
					systrayicon = self.systray_icon_connected
						
				if self.isSMALL_WINDOW == False:
					self.SWITCH_SMALL_WINDOW = True
				
		if self.SWITCH_SMALL_WINDOW == True and self.isSMALL_WINDOW == False:
			self.isSMALL_WINDOW = True
			self.screen_width = 480
			self.screen_height = 24
			self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
			self.removethis()	
			self.SWITCH_SMALL_WINDOW = False
			#self.root.attributes("-toolwindow", False)
			
		elif self.SWITCH_FULL_WINDOW == True and self.isSMALL_WINDOW == True:
			self.isSMALL_WINDOW = False	
			self.screen_width = 320
			self.screen_height = 240
			self.root.geometry("%sx%s"%(self.screen_width,self.screen_height))
			self.removethis()			
			self.SWITCH_FULL_WINDOW = False
			#self.root.attributes("-toolwindow", False)
	
		if not self.systraytext_from_before == systraytext and not systraytext == False:
			if self.SYSTRAYon == True:
				try:
					self.systray.shutdown()
					self.SYSTRAYon = False
				except:
					self.debug(text="def timer_statusbar: self.systray.shutdown() failed")
			if self.SYSTRAYon == False:
				self.systraytext_from_before = systraytext
				menu_options = ((systraytext, systrayicon, self.defundef),)			
				self.systray = SysTrayIcon(systrayicon, systraytext, menu_options)
				try:
					self.systray.start()
					self.debug(text="def timer_statusbar: self.systray.start()")
					self.SYSTRAYon = True
				except:
					self.debug(text="def timer_statusbar: self.systray.start() failed")
					self.SYSTRAYon = False
		
		if not self.statustext_from_before == text:
			self.statusbar_text.set(text)
			self.statustext_from_before = text
			#self.debug(text="def timer_statusbar: running: text = %s" % (text))
			
		self.root.after(1000,self.timer_statusbar)
		return True
	

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
				self.msgwarn(text=_("Could not delete lock file"))
		else:
			self.msgwarn(text=_("Could not delete LOCK. File not found."))


	def on_closing(self,root):
		if self.STATE_OVPN == True:
			tkMessageBox.showwarning(_("Warning"), _("Quit blocked while oVPN is connected.\nDisconnect oVPN from %s first.")%(self.OVPN_CONNECTEDto[:3]))
			return False
		elif tkMessageBox.askyesno(_("Quit"), _("Quit oVPN Client?")):
			self.win_netsh_restore_dns_from_backup()
			if tkMessageBox.askyesno(_("Keep Firewall Protection?"), _("Keep Firewall loaded and block OUT to Internet?")):
				if self.win_firewall_start():
					text="Firewall enabled! Internet blocked!"
					self.debug(text=text)
					#self.msgwarn(text=text)
				else:
					text=_("Error. Could not start Firewall!")
					self.debug(text=text)
					self.msgwarn(text=text)
			else:
				if self.win_firewall_allow_outbound():
					text=_("Firewall rules unloaded.\nSettings restored.")
					self.debug(text=text)
					#self.msgwarn(text=text)
				else:
					text=_("Error! Unloading Firewall failed.")
					self.debug(text=text)					
					self.msgwarn(text=text)
			if self.SYSTRAYon == True:
				self.systray.shutdown()
			self.remove_lock()
			sys.exit()
		
		
	def defundef(self):
		pass

	def init_localization(self):
		loc = locale.getdefaultlocale()[0][0:2]
		filename = "locale/messages_%s.mo" % loc
		try:
			translation = gettext.GNUTranslations(open(filename, "rb"))
		except IOError:
			translation = gettext.NullTranslations()
			print("Language file for %s not found" % loc)
		
		translation.install() 
		

def main():
	root = Tk()
	root.screen_width = 320
	root.screen_height = 240	
	root.geometry("%sx%s"%(root.screen_width,root.screen_height))
	root.resizable(0,0)
	root.attributes("-toolwindow", False)
	root.overrideredirect(False)
	root.title("oVPN v"+BUILT+STATE)
	app = AppUI(root).pack()	
	root.mainloop()	
	print("Ending")
	sys.exit()
	


if __name__== '__main__':
	main()
