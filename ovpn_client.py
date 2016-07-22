# -*- coding: utf-8 -*-
"""
import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
"""
import os
import sys
from _winreg import *

# Patching libgtk-3-0.dll for 16px or 32px TrayIcon Output
# File Size win32 dll: 6453248
# File Size win64 dll: 6675968

bin_dir = os.getcwd()
gtkfile = "%s\\libgtk-3-0.dll" % (bin_dir)

if os.path.exists(gtkfile) and sys.platform == "win32":

	# Check filesize to detect 32 or 64bit dll
	offset = False
	filesize = os.path.getsize(gtkfile)
	if filesize == 6675968:
		offset = 0x3D051
		version = "win64"
	if filesize == 6453248:
		offset = 0x3E4E2
		version = "win32"

	if not offset == False:

		print "Found: %s [%s]" % (gtkfile,version)

		# Get Windows DPI Scaling Factor from Registry (96 = 100%, 120 = 125%)
		# When reg key = False, use standard 16px output
		pixel = "\x10"
		pixeldez = "16"
		RawKey = False
		try:
			Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
			RawKey = OpenKey(Registry, "Control Panel\Desktop")
		except:
			pass
		try:
			if not RawKey == False:
				i = 0
				while 1:
					name, value, type = EnumValue(RawKey, i)
					if name == "LogPixels":
						if value > 96:
							pixel = "\x20"
							pixeldez = "32"
						if value == 96:
							pass
						break
					i += 1
		except:
			pass

		# Patching
		with open(gtkfile,'r+b') as f:
				f.seek(offset)
				if not f.read(1) == pixel:
					print "Patch TrayIcon Output Size to: %s pixel" % (pixeldez)
					f.seek(offset)
					f.write(pixel)

	else:
		print "No compatible gtk-3-0.dll found"

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, GObject, Gio

from datetime import datetime as datetime
import base64
import gettext
import locale
import types
import platform
import hashlib
import random
import time
import zipfile
import subprocess
import threading
import socket
import requests
import json
#import gc
from ConfigParser import SafeConfigParser

CLIENTVERSION="v0.5.7-gtk3"
CLIENT_STRING="oVPN.to Client %s" % (CLIENTVERSION)

ABOUT_TEXT = """Credits and Cookies go to...
+ ... all our customers! We can not exist without you!
+ ... d0wn for hosting DNS on dns.d0wn.biz!
+ ... bauerj for code submits!
+ ... semool for gtk3 fork!
+ ... dogpellet for DNStest() ideas!
+ ... ungefiltert-surfen.de for WorldWide DNS!
+ ... famfamfam.com for flag and silk icons!

Need Help?

Join https://webirc.ovpn.to into Channel #help !
"""

DOMAIN = "vcp.ovpn.to"
PORT="443"
API="xxxapi.php"

class Systray:
	def __init__(self):
		self.self_vars()
		self.tray = Gtk.StatusIcon()
		traysize = self.tray.get_size()
		self.debug(1,"TrayIcon Output Size: %s pixel" % (traysize))
		self.tray.connect('size-changed', self.statusicon_size_changed)
		self.tray.set_from_stock(Gtk.STOCK_EXECUTE)
		self.tray.set_tooltip_markup(CLIENT_STRING)
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.connect('activate', self.on_left_click)
		self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		self.window.connect("delete-event", Gtk.main_quit)
		self.init_localization(None)
		if self.preboot():
			self.init_theme()
			if self.UPDATEOVPNONSTART == True:
				if self.check_inet_connection() == True:
					self.check_remote_update()
				else:
					self.msgwarn(_("Could not connect to %s") % (DOMAIN),_("Update failed!"))
			thread = threading.Thread(target=self.systray_timer)
			thread.daemon = True
			thread.start()
			self.win_firewall_analyze()
		else:
			sys.exit()

	def self_vars(self):
		self.APIURL = "https://%s:%s/%s" % (DOMAIN,PORT,API)
		self.LOGLEVEL = 1
		self.LOGLEVELS = [1,2,3,49]
		self.OS = sys.platform
		self.INIT_FIRST_UPDATE = True
		self.SAVE_APIKEY_INFILE = False
		self.MAINWINDOW_OPEN = False
		self.MAINWINDOW_HIDE = False
		self.SETTINGSWINDOW_OPEN = False
		self.ENABLE_MAINWINDOW_SORTING = True
		self.APP_LANGUAGE = "en"
		self.LANG_FONT_CHANGE = False
		self.APP_FONT_SIZE = "9"
		self.APP_FONT_SIZE_AVAIABLE = [ "6", "7", "8", "9", "10", "11", "12", "13" ]
		self.APP_THEME = "Adwaita"
		self.INSTALLED_THEMES = [ "ms-windows", "Adwaita", "Adwaita-dark", "Greybird" ]
		self.ICONS_THEME = "standard"
		self.ICONS_THEME_frombefore = self.ICONS_THEME
		self.INSTALLED_ICONS = [ "standard", "classic", "classic2", "shield_bluesync", "experimental", "private" ]
		self.INSTALLED_LANGUAGES = [ "en", "de", "es" ]
		self.ACCWINDOW_OPEN = False
		self.DEBUG = True
		self.DEBUGfrombefore = False
		self.DEBUGcount = 0
		self.debug_write_thread_running = False
		self.BOOTTIME = time.time()
		self.debug_log = False
		self.OVPN_LATEST = 2311
		self.OVPN_LATEST_BUILT = "May 10 2016"
		self.OVPN_LATEST_BUILT_TIMESTAMP = 1462831200
		
		self.OPENVPN_REM_URL = "https://%s/files/openvpn" % (DOMAIN)
		self.OPENVPN_ALT_URL = "https://swupdate.openvpn.net/community/releases"
		self.OPENVPN_VERSION = "2.3.11"
		self.OPENVPN_BUILT_V = "I601"
		self.OPENVPN_FILEHASHS = {"openvpn-install-2.3.11-I601-x86_64.exe": {"libeay32.dll": "8a96ddc451110b84ef7bad7003222de593fa6b44757093b13076404b9d92b9de5050196885dbbdff0335cd527d0821f83d9ff3cb610ab7c5aa2ebc7c6afc7cbe", "openvpn.exe": "e94cb06e44a17d2e0a4d884cee2253d960b8a41dcd191340a3f5be12888c4936d8a8a60e5f13604fd8bbac66df7350d8773391e4432697a5b3b1a3d0662837e9", "openvpnserv.exe": "3c86a89a163c2f7d043f692883d51ff6e1c2bd77801fefcd4e5458bfd0473863223d8ebdcf573fdbe64753b0071e505e285ab08a52d4925a1b0a6ce24d80a7d7", "liblzo2-2.dll": "5de56ee903501e84a4f8f988c7deb6d24b34e5b2ff4cf51e9e80cdcbc5a4710639bd7f6e559fdd2df7ae29d83bf7c58c41e74c5c4f7ddab7faf15df0353d0b05", "openvpn-gui.exe": "3c8d174dcfb71b6ce750bc7460bd4f0ab6b4e0bba8305253658fc4e02fb74fa1d737ca9e290a64818bea48857ecfb66b7af720c673e3f2d9f7eba206799aae8f", "libpkcs11-helper-1.dll": "f1ac4d5eed3a97b8cd9c5b053c6f3ea8fc7e2b25d1a9adead3b8a198bee9dea7237c07dd2d2561aeebed62aac318d90b321b73729b81f00a03f10b45eda56480", "ssleay32.dll": "a9384fd0ded117e3c27f988ea35109e7843b929edf79473ad0e485b5d0285660676fd9b9c43458de007dd142aedf9fdea75a2a7bdb9b7b600edee392d18bf90e", "openssl.exe": "7c6699cf02f3b1d017b867855935019f2d50fe6b4d49c79de06a7e40663d29dd955a7f6bfb7836aa2e52dde4d817712b6e46650a2a10f5958a81338b4106be1b"}, "openvpn-install-2.3.11-I601-i686.exe": {"libeay32.dll": "592475e0b0286914d697f36fff8af7b3e265342787d945c7fe9e234a7cfbd84a13e757850fe7588a382a83c5f59e0046f91aed1736d4c06181d180e33aced806", "openvpn.exe": "dfbad890037291a534da7c534b49ec70ecc9a044ee0d8508654696819d88b5b4845b81b2e1aecd5475dc62e0d9a0d1c147524c70940a4e96c4e1530e257758d6", "openvpnserv.exe": "6dc640730a5724de687b805699e51595a1f08b16bc1596564b89cd580deee7478113a4296c3de677f96d4501f4f40a4e36d7d4c1f6993d4dbb7199b0e6edfa14", "liblzo2-2.dll": "31b744a57105d122d2150b5ab793620b73dbc28788be8484fa682e1cf6857f01102034e220b63d5709f6baa44b547df94e2c8aad6b5124b91e105e42d258e40b", "openvpn-gui.exe": "dab26e87d66d65e727733e16f3234585f44f8ebbf969c9fd20d4fc55a973820cecfb6218e1b5da98eecdae111473a839cab7b128687808676801bce25558c4c2", "libpkcs11-helper-1.dll": "bd7339e3911ab75ddf805555e0f59e65927f1539a5561b22456e25f3d1868fb42d89cd95eaa96c3335fef7d3ec2a21ff7c53f04961fedc5e374f43f4070df58c", "ssleay32.dll": "440cf92524e21e9dc1d92f45a8fbd566f0eeec597e0f52a235847879bdd4806ac219b592aaec9976620082b2d8d5690d432e1a45b0df035b18404453530855d9", "openssl.exe": "49d274c5f4ccddda28751a1a6271888c32188a192b9ad9c224832b51af0b474225d75c6ac51e61438b7a9f956b1ba78fef7a5392759a3d38fc4ddd1d7772e464"}}
		self.CHECK_FILEHASHS = True
		
		self.OVPN_WIN_DL_URL_x86 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.11-I601-i686.exe"
		self.OVPN_WIN_SHA512_x86 = "b6c1e5d9dd80fd6515d9683044dae7cad13c4cb5ac5590be4116263b7cde25e0fef1163deb5a1f1ad646e5fdb84c286308fa8af288692b9c7d4e2b7dbff38bbe"
		self.OVPN_WIN_DL_URL_x64 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.11-I601-x86_64.exe"
		self.OVPN_WIN_SHA512_x64 = "a59284b98e80c1cd43cfe2f0aee2ebb9d18ca44ffb7035b5a4bb4cb9c2860039943798d4bb8860e065a56be0284f5f23b74eba6a5e17f05df87303ea019c42a3"
		
		self.timer_load_remote_data_running = False
		self.timer_ovpn_ping_running = False
		self.timer_check_certdl_running = False
		self.statusbartext_from_before = False
		self.statusbar_text = False
		self.systraytext_from_before = False
		self.systrayicon_from_before = False
		self.stop_systray_timer = False
		self.stop_systray_timer2 = False
		self.systray_timer_running = False
		self.systray_timer2_running = False
		self.inThread_jump_server_running = False
		self.USERID = False
		self.STATE_OVPN = False
		self.STATE_CERTDL = False
		self.LAST_CFG_UPDATE = 0
		self.LAST_CHECK_MYIP = 0
		self.NEXT_PING_EXEC = 0
		self.LAST_CHECK_INET_FALSE = 0
		self.LAST_MSGWARN_WINDOW = 0
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS1 = False
		self.GATEWAY_DNS2 = False
		self.WIN_TAP_DEVICE = False
		self.WIN_TAP_DEVS = list()
		self.TAP_BLOCKOUTBOUND = False
		self.win_firewall_tap_blockoutbound_running = False
		self.WIN_EXT_DEVICE = False
		self.WIN_EXT_DHCP = False
		self.NO_WIN_FIREWALL = False
		self.NO_DNS_CHANGE = False
		self.MYDNS = {}
		self.NETSH_CMDLIST = list()
		self.ROUTE_CMDLIST = list()
		self.API_DIR = False
		self.OPENVPN_EXE = False
		self.OPENVPN_SILENT_SETUP = False
		
		self.OVPN_SERVER = list()
		self.OVPN_FAV_SERVER = False
		self.OVPN_AUTO_CONNECT_ON_START = False
		self.OVPN_CALL_SRV = False
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtime = False
		self.OVPN_CONNECTEDseconds = 0
		self.OVPN_CONNECTEDtoIP = False
		self.GATEWAY_OVPN_IP4A = "172.16.32.1"
		self.GATEWAY_OVPN_IP4B = "172.16.48.1"
		self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4A
		self.OVPN_THREADID = False
		self.OVPN_CONFIGVERSION = "23x"
		self.OPENVPN_DIR = False
		
		self.OVPN_PING = list()
		self.OVPN_isTESTING = False
		self.OVPN_PING_LAST = -1
		self.OVPN_PING_STAT = 0
		self.OVPN_PING_DEAD_COUNT = 0
		self.OVPN_PING_EVERY = "15,30"
		self.INTERFACES = False
		
		self.d0wns_DNS = {}
		
		
		import flags_b64
		self.FLAGS_B64 = flags_b64.flagsb64()
		print "len(self.FLAGS_B64) = '%s'" % (len(self.FLAGS_B64))
		self.COUNTRYNAMES = {
			'BG':'Bulgaria','CA':'Canada','CH':'Swiss','DE':'Germany','FR':'France','HU':'Hungary','IS':'Iceland','LT':'Lithuania','MD':'Moldova','NL':'Netherlands','RO':'Romania','SE':'Sweden','UA':'Ukraine','UK':'United Kingdom','US':'U.S.A.',
			}
		self.FLAG_CACHE_PIXBUF = {}
		self.ICON_CACHE_PIXBUF = {}
		#self.IDLE_TIME = 0
		self.systray_menu = False
		self.WINDOW_QUIT_OPEN = False
		self.WINDOW_ABOUT_OPEN = False
		
		self.OVPN_SERVER_INFO = {}
		self.OVPN_SRV_DATA = {}
		self.LAST_OVPN_SRV_DATA_UPDATE = 0
		self.OVPN_ACC_DATA = {}
		self.OVPN_ACC_DATAfrombefore = False
		self.LAST_OVPN_ACC_DATA_UPDATE = 0
		self.UPDATEOVPNONSTART = False
		self.APIKEY = False
		self.LOAD_DATA_EVERY = 900
		self.LOAD_ACCDATA = False
		self.LOAD_SRVDATA = False
		self.SRV_LIGHT_WIDTH = "490"
		self.SRV_LIGHT_HEIGHT = "830"
		self.SRV_WIDTH = "910"
		self.SRV_HEIGHT = "830"
		self.SRV_LIGHT_WIDTH_DEFAULT = self.SRV_LIGHT_WIDTH
		self.SRV_LIGHT_HEIGHT_DEFAULT = self.SRV_LIGHT_HEIGHT
		self.SRV_WIDTH_DEFAULT = self.SRV_WIDTH
		self.SRV_HEIGHT_DEFAULT = self.SRV_HEIGHT
		self.WIN_RESET_EXT_DEVICE = False
		self.WIN_FIREWALL_STARTED = False
		self.WIN_FIREWALL_ADDED_RULE_TO_VCP = False
		self.WIN_BACKUP_FIREWALL = False
		self.WIN_RESET_FIREWALL = False
		self.WIN_DONT_ASK_FW_EXIT = False
		self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = True
		self.WIN_DISABLE_EXT_IF_ON_DISCO = False
		self.WIN_DNS_CHANGED = False
		self.LAST_FAILED_CHECKFILE = False
		self.CA_FIXED_HASH = "f37dff160dda454d432e5f0e0f30f8b20986b59daadabf2d261839de5dfd1e7d8a52ecae54bdd21c9fee9238628f9fff70c7e1a340481d14f3a1bdeea4a162e8"
		self.DISABLE_SRV_WINDOW = False
		self.DISABLE_ACC_WINDOW = False
		self.DISABLE_QUIT_ENTRY = True
		self.OVERWRITE_TRAYICON = False
		self.MOUSE_IN_TRAY = 0
		self.UPDATE_SWITCH = False
		self.isWRITING_OPTFILE = False
		self.WHITELIST_PUBLIC_PROFILE = {
			"Intern 01) oVPN Connection Check": {"ip":self.GATEWAY_OVPN_IP4A,"port":"80","proto":"tcp"},
			"Intern 02) https://vcp.ovpn.to": {"ip":self.GATEWAY_OVPN_IP4A,"port":"443","proto":"tcp"},
			"Intern 03) IRC": {"ip":self.GATEWAY_OVPN_IP4A,"port":"6697","proto":"tcp"},
			"Intern 04) DNS": {"ip":self.GATEWAY_OVPN_IP4A,"port":"53","proto":"tcp"},
			"Intern 05) DNS": {"ip":self.GATEWAY_OVPN_IP4A,"port":"53","proto":"udp"},
			"Intern 06) SSH": {"ip":self.GATEWAY_OVPN_IP4A,"port":"22","proto":"tcp"},
			"Intern 07) SOCKS": {"ip":self.GATEWAY_OVPN_IP4A,"port":"1080","proto":"tcp"},
			"Intern 08) HTTP": {"ip":self.GATEWAY_OVPN_IP4A,"port":"3128","proto":"tcp"},
			"Intern 09) SOCKS Random": {"ip":self.GATEWAY_OVPN_IP4A,"port":"1081","proto":"tcp"},
			"Intern 10) HTTP Random": {"ip":self.GATEWAY_OVPN_IP4A,"port":"3129","proto":"tcp"},
			"Intern 11) STUNNEL HTTP": {"ip":self.GATEWAY_OVPN_IP4A,"port":"8081","proto":"tcp"},
			"Intern 12) STUNNEL SOCKS": {"ip":self.GATEWAY_OVPN_IP4A,"port":"8080","proto":"tcp"},
			"Intern 13) TOR SOCKS": {"ip":self.GATEWAY_OVPN_IP4A,"port":"9100","proto":"tcp"},
			"Intern 14) JABBER client": {"ip":self.GATEWAY_OVPN_IP4A,"port":"5222","proto":"tcp"},
			"Intern 15) JABBER transfer": {"ip":self.GATEWAY_OVPN_IP4A,"port":"5000","proto":"tcp"},
			"Intern 16) AnoMail IMAPs": {"ip":self.GATEWAY_OVPN_IP4A,"port":"993","proto":"tcp"},
			"Intern 17) AnoMail POP3s": {"ip":self.GATEWAY_OVPN_IP4A,"port":"995","proto":"tcp"},
			"Intern 18) AnoMail SMTPs": {"ip":self.GATEWAY_OVPN_IP4A,"port":"587","proto":"tcp"},
			"Intern 19) ZNC": {"ip":self.GATEWAY_OVPN_IP4A,"port":"6444","proto":"tcp"},
			"Intern 20) dnscrypt": {"ip":self.GATEWAY_OVPN_IP4A,"port":"5353","proto":"tcp"},
			"Intern 21) dnscrypt": {"ip":self.GATEWAY_OVPN_IP4A,"port":"5353","proto":"udp"},
			"Intern 22) nntp-50001 Binary SSL user=ovpn,pass=free": {"ip":self.GATEWAY_OVPN_IP4A,"port":"50001","proto":"tcp"},
			"Intern 23) nntp-50002 Binary SSL user=ovpn,pass=free": {"ip":self.GATEWAY_OVPN_IP4A,"port":"50002","proto":"tcp"}
		}

	def preboot(self):
		self.debug(1,"def preboot()")
		self.self_vars()
		if self.OS == "win32":
				if self.win_pre1_check_app_dir():
					if self.win_pre2_check_profiles_win():
						if self.win_pre3_load_profile_dir_vars():
							if self.check_config_folders():
								if self.read_options_file():
									if self.read_interfaces():
										if self.write_options_file():
											return True
		elif OS == "linux2" :
			self.errorquit(text=_("Operating System not supported: %s") % (self.OS))
		elif OS == "darwin":
			self.errorquit(text=_("Operating System not supported: %s") % (self.OS))
		else: 
			self.errorquit(text=_("Operating System not supported: %s") % (self.OS))

	def win_pre1_check_app_dir(self):
		self.debug(1,"def win_pre1_check_app_dir()")
		os_appdata = os.getenv('APPDATA')
		if os.path.exists("appdata"):
			print "alternative folder found"
			self.bin_dir = os.getcwd()
			self.app_dir = "%s\\appdata\\ovpn" % (self.bin_dir)
		else:
			self.app_dir = "%s\\ovpn" % (os_appdata)
			self.bin_dir = "%s\\bin\\client\\dist" % (self.app_dir)
		if not os.path.exists(self.app_dir):
			if self.DEBUG: print("win_pre1_check_app_dir %s not found, creating." % (self.app_dir))
			os.mkdir(self.app_dir)
		if os.path.exists(self.app_dir):
			self.debug(1,"win_pre1_check_app_dir self.app_dir=%s :True" % (self.app_dir))
			return True
		else:
			self.errorquit(text = _("Could not create app_dir: %s") % (self.app_dir))

	def list_profiles(self):
		self.debug(1,"def list_profiles()")
		self.profiles_unclean = os.listdir(self.app_dir)
		self.PROFILES = list()
		for profile in self.profiles_unclean:
			if profile.isdigit():
				self.PROFILES.append(profile)
		self.PROFILES_COUNT = len(self.PROFILES)
		self.debug(1,"def list_profiles: profiles_count %s" % (self.PROFILES_COUNT))
		
	def win_pre2_check_profiles_win(self):
		self.debug(1,"def win_pre2_check_profiles_win()")
		self.list_profiles()
		if self.PROFILES_COUNT == 0:
			self.debug(1,"No profiles found")
			if self.USERID == False:
				self.debug(1,"spawn popup userid = %s" % (self.USERID))
				self.debug(1,"def win_pre2_check_profiles_win: L:308")
				self.form_ask_userid()
				self.debug(1,"def win_pre2_check_profiles_win: L:309")
				if not self.USERID == False and not self.APIKEY == False:
					self.debug(1,"def win_pre2_check_profiles_win: L:310")
					return True
		elif self.PROFILES_COUNT == 1 and self.PROFILES[0] > 1:
			self.USERID = self.PROFILES[0]
			return True
		elif self.PROFILES_COUNT > 1:
			if not self.select_userid() == True:
				self.errorquit(text=_("Select User-ID failed!"))
			return True

	def win_pre3_load_profile_dir_vars(self):
		self.debug(1,"def win_pre3_load_profile_dir_vars()")
		self.API_DIR = "%s\\%s" % (self.app_dir,self.USERID)
		self.debug_log = "%s\\client_debug.log" % (self.API_DIR)
		if os.path.isfile(self.debug_log):
			try:
				os.remove(self.debug_log)
			except:
				pass
		self.lock_file = "%s\\lock.file" % (self.app_dir)
		self.opt_file = "%s\\options.cfg" % (self.API_DIR)
		self.api_cfg = "%s\\ovpnapi.conf" % (self.API_DIR)
		if os.path.isfile(self.api_cfg):
			os.remove(self.api_cfg)
		self.vpn_dir = "%s\\openvpn" % (self.API_DIR)
		self.prx_dir = "%s\\proxy" % (self.API_DIR)
		self.stu_dir = "%s\\stunnel" % (self.API_DIR)
		self.pfw_dir = "%s\\pfw" % (self.API_DIR)
		self.pfw_bak = "%s\\pfw.%s.bak.wfw" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_private_log = "%s\\pfw.private.%s.log" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_public_log = "%s\\pfw.public.%s.log" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_domain_log = "%s\\pfw.domain.%s.log" % (self.pfw_dir,self.BOOTTIME)
		
		self.VPN_CFG = "%s\\config" % (self.vpn_dir)
		self.VPN_CFGip4 = "%s\\ip4" % (self.VPN_CFG)
		self.VPN_CFGip46 = "%s\\ip46" % (self.VPN_CFG)
		self.VPN_CFGip64 = "%s\\ip64" % (self.VPN_CFG)
		
		self.zip_cfg = "%s\\confs.zip" % (self.vpn_dir)
		self.zip_crt = "%s\\certs.zip" % (self.vpn_dir)
		self.api_upd = "%s\\lastupdate.txt" % (self.vpn_dir)
		if os.path.isfile(self.api_upd):
			os.remove(self.api_upd)
		
		self.dns_dir =  "%s\\dns" % (self.bin_dir)
		self.dns_d0wntxt =  "%s\\dns.txt" % (self.dns_dir)
		#self.dns_ung =  "%s\\ungefiltert" % (self.dns_dir)
		#self.dns_ung_alphaindex =  "%s\\alphaindex.txt" % (self.dns_ung)
		
		if self.load_icons() == False:
			return False

		self.CA_FILE = "%s\\cacert_ovpn.pem" % (self.bin_dir)
		if not self.load_ca_cert():
			return False
		
		self.WINDIR = os.getenv('WINDIR')
		if os.path.isdir(self.WINDIR):
			self.WIN_NETSH_EXE = "%s\\system32\\netsh.exe" % (self.WINDIR)
			self.WIN_ROUTE_EXE = "%s\\system32\\route.exe" % (self.WINDIR)
			self.WIN_IPCONFIG_EXE = "%s\\system32\\ipconfig.exe" % (self.WINDIR)
			self.WIN_TASKKILL_EXE = "%s\\system32\\taskkill.exe" % (self.WINDIR)
		else:
			self.errorquit(text=_("Error: '%s' not found!") % (self.WINDIR))
		
		if not os.path.isfile(self.WIN_NETSH_EXE):
			self.errorquit(text=_("Error: '%s' not found!") % (self.WIN_NETSH_EXE))
		
		if not os.path.isfile(self.WIN_ROUTE_EXE):
			self.errorquit(text=_("Error: '%s' not found!") % (self.WIN_ROUTE_EXE))
		
		if not os.path.isfile(self.WIN_IPCONFIG_EXE):
			self.errorquit(text=_("Error: '%s' not found!") % (self.WIN_IPCONFIG_EXE))
		
		if not os.path.isfile(self.WIN_TASKKILL_EXE):
			self.errorquit(text=_("Error: '%s' not found!") % (self.WIN_TASKKILL_EXE))
		
		self.debug(1,"win_pre3_load_profile_dir_vars loaded")
		return True

	def load_icons(self):
		self.debug(1,"def load_icons()")
		# called from: 
		"""
			def win_pre3_load_profile_dir_vars()
			def read_options_file()
			def cb_icons_switcher_changed()
		"""
		self.app_icon = self.decode_icon("app_icon")

		if self.ICONS_THEME == "standard":
			self.systray_icon_connected = self.app_icon
			self.systray_icon_connect = self.decode_icon("connect")
			self.systray_icon_testing = self.decode_icon("testing")
			self.systray_icon_disconnected = self.decode_icon("disconnect1")
			self.systray_icon_disconnected_traymenu = self.decode_icon("disconnect1_menu")
			self.systray_icon_syncupdate1 = self.decode_icon("sync_2a")
			self.systray_icon_syncupdate2 = self.decode_icon("sync_2b")
			self.systray_icon_syncupdate3 = self.decode_icon("sync_2c")
		
		elif self.ICONS_THEME == "classic":
			self.systray_icon_connected = self.decode_icon("connected_classic")
			self.systray_icon_connect = self.decode_icon("connect")
			self.systray_icon_testing = self.decode_icon("testing")
			self.systray_icon_disconnected = self.decode_icon("disconnect1")
			self.systray_icon_disconnected_traymenu = self.decode_icon("disconnect1_menu")
			self.systray_icon_syncupdate1 = self.decode_icon("sync_1a")
			self.systray_icon_syncupdate2 = self.decode_icon("sync_1b")
			self.systray_icon_syncupdate3 = self.decode_icon("sync_1c")
		
		elif self.ICONS_THEME == "classic2":
			self.systray_icon_connected = self.decode_icon("connected_classic")
			self.systray_icon_connect = self.decode_icon("connect")
			self.systray_icon_testing = self.decode_icon("testing")
			self.systray_icon_disconnected = self.decode_icon("disconnect2")
			self.systray_icon_disconnected_traymenu = self.decode_icon("disconnect1_menu")
			self.systray_icon_syncupdate1 = self.decode_icon("sync_1a")
			self.systray_icon_syncupdate2 = self.decode_icon("sync_1b")
			self.systray_icon_syncupdate3 = self.decode_icon("sync_1c")
		
		elif self.ICONS_THEME == "shield_bluesync":
			self.systray_icon_connected = self.app_icon
			self.systray_icon_connect = self.decode_icon("connect")
			self.systray_icon_testing = self.decode_icon("testing")
			self.systray_icon_disconnected = self.decode_icon("disconnect1")
			self.systray_icon_disconnected_traymenu = self.decode_icon("disconnect1_menu")
			self.systray_icon_syncupdate1 = self.decode_icon("sync_1a")
			self.systray_icon_syncupdate2 = self.decode_icon("sync_1b")
			self.systray_icon_syncupdate3 = self.decode_icon("sync_1c")
		
		elif self.ICONS_THEME == "experimental":
			self.systray_icon_connected = self.app_icon
			self.systray_icon_connect = self.decode_icon("connect")
			self.systray_icon_testing = self.decode_icon("testing")
			self.systray_icon_disconnected = self.decode_icon("disconnect3")
			self.systray_icon_disconnected_traymenu = self.decode_icon("disconnect3_menu")
			self.systray_icon_syncupdate1 = self.decode_icon("sync_2a")
			self.systray_icon_syncupdate2 = self.decode_icon("sync_2b")
			self.systray_icon_syncupdate3 = self.decode_icon("sync_2c")
		
		elif self.ICONS_THEME == "private":
			self.ico_dir_theme = "%s\\ico\\private" % (self.bin_dir)
			if os.path.isdir(self.ico_dir_theme):
				systray_icon_connected = "%s\\connected.ico" % (self.ico_dir_theme)
				systray_icon_connect = "%s\\connect.ico" % (self.ico_dir_theme)
				systray_icon_testing = "%s\\testing.ico" % (self.ico_dir_theme)
				systray_icon_disconnected = "%s\\disconnect.ico" % (self.ico_dir_theme)
				systray_icon_disconnected_traymenu = "%s\\disconnect_menu.ico" % (self.ico_dir_theme)
				systray_icon_syncupdate1 = "%s\\sync_1.ico" % (self.ico_dir_theme)
				systray_icon_syncupdate2 = "%s\\sync_2.ico" % (self.ico_dir_theme)
				systray_icon_syncupdate3 = "%s\\sync_3.ico" % (self.ico_dir_theme)
				checkfiles = [systray_icon_connected,systray_icon_connect,systray_icon_testing,systray_icon_disconnected,systray_icon_disconnected_traymenu,systray_icon_syncupdate1,systray_icon_syncupdate2,systray_icon_syncupdate3]

				missing_file = list()
				for file in checkfiles:
					if not os.path.isfile(file):
						missing_file.append(file.rsplit("\\", 1)[1])
						self.debug(1,"def load_icons: file '%s' not found" %(file))

				if missing_file:
					self.msgwarn(_("Private Icon(s) not found in:\n%s\n\nMissing Icons:\n%s") % (self.ico_dir_theme,missing_file),_("Error: Icon"))
					return False
				else:
					self.systray_icon_connected = systray_icon_connected
					self.systray_icon_connect = systray_icon_connect
					self.systray_icon_testing = systray_icon_testing
					self.systray_icon_disconnected = systray_icon_disconnected
					self.systray_icon_disconnected_traymenu = systray_icon_disconnected_traymenu
					self.systray_icon_syncupdate1 = systray_icon_syncupdate1
					self.systray_icon_syncupdate2 = systray_icon_syncupdate2
					self.systray_icon_syncupdate3 = systray_icon_syncupdate3
			else:
				#self.debug(1,"def load_icons(), private icon dir not found: '%s'" % (self.ico_dir_theme))
				self.msgwarn(_("Private Icon Dir not found:\n%s") % (self.ico_dir_theme),_("Error: Icon Dir"))
				return False

		self.systrayicon_from_before = False
		return True

	def check_config_folders(self):
		self.debug(1,"def check_config_folders()")
		try:
			#self.debug(1,"def check_config_folders userid = %s" % (self.USERID))
			self.debug(1,"def check_config_folders: userid found")
			if not os.path.exists(self.API_DIR):
				if self.DEBUG: print("api_dir %s not found, creating." % (self.API_DIR))
				os.mkdir(self.API_DIR)
			if os.path.isfile(self.lock_file):
				try:
					os.remove(self.lock_file)
				except:
					self.errorquit(text=_("Could not remove lock file.\nFile itself locked because another oVPN Client instance running?"))
			if not os.path.isfile(self.lock_file):
				self.LOCK = open(self.lock_file,'wb')
				self.LOCK.write("%s" % (int(time.time())))
			if not os.path.exists(self.vpn_dir):
				if self.DEBUG: print("vpn_dir %s not found, creating." % (self.vpn_dir))
				os.mkdir(self.vpn_dir)
			if not os.path.exists(self.VPN_CFG):
				if self.DEBUG: print("vpn_cfg %s not found, creating." % (self.VPN_CFG))
				os.mkdir(self.VPN_CFG)
			if not os.path.exists(self.VPN_CFGip4):
				if self.DEBUG: print("vpn_cfgip4 %s not found, creating." % (self.VPN_CFGip4))
				os.mkdir(self.VPN_CFGip4)
			if not os.path.exists(self.VPN_CFGip46):
				if self.DEBUG: print("vpn_cfgip46 %s not found, creating." % (self.VPN_CFGip46))
				os.mkdir(self.VPN_CFGip46)
			if not os.path.exists(self.VPN_CFGip64):
				if self.DEBUG: print("vpn_cfgip64 %s not found, creating." % (self.VPN_CFGip64))
				os.mkdir(self.VPN_CFGip64)
			if not os.path.exists(self.prx_dir):
				if self.DEBUG: print("prx_dir %s not found, creating." % (self.prx_dir))
				os.mkdir(self.prx_dir)
			if not os.path.exists(self.stu_dir):
				if self.DEBUG: print("stu_dir %s not found, creating." % (self.stu_dir))
				os.mkdir(self.stu_dir)
			if not os.path.exists(self.pfw_dir):
				if self.DEBUG: print("pfw_dir %s not found, creating." % (self.pfw_dir))
				os.mkdir(self.pfw_dir)
			if not os.path.exists(self.dns_dir):
				os.mkdir(self.dns_dir)
			#if not os.path.exists(self.dns_ung):
			#	os.mkdir(self.dns_ung)
			if not self.build_openvpn_dlurl():
				return False
			if os.path.exists(self.API_DIR) and os.path.exists(self.vpn_dir) and os.path.exists(self.VPN_CFG) \
			and os.path.exists(self.prx_dir) and os.path.exists(self.stu_dir) and os.path.exists(self.pfw_dir):
				return True
			else:
				self.errorquit(text=_("Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!") % (self.API_DIR,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))
		except:
			self.errorquit(text=_("Creating config Folders failed"))

	def read_options_file(self):
		self.debug(1,"def read_options_file()")
		if os.path.isfile(self.opt_file):
			try:
				parser = SafeConfigParser()
				parser.read(self.opt_file)
				
				try:
					APIKEY = parser.get('oVPN','apikey')
					if APIKEY == "False" and not self.APIKEY == False:
						pass
					elif APIKEY == "False":
						self.APIKEY = False
					else:
						self.SAVE_APIKEY_INFILE = True
						self.APIKEY = APIKEY
				except:
					pass
				
				try:
					self.DEBUG = parser.getboolean('oVPN','debugmode')
				except:
					pass
				
				try:
					APPLANG = parser.get('oVPN','applanguage')
					self.debug(1,"APPLANG = parser.get(oVPN,'%s') " % (APPLANG))
					if APPLANG in self.INSTALLED_LANGUAGES:
						self.debug(1,"APPLANG '%s' in self.INSTALLED_LANGUAGES" % (APPLANG))
						if self.init_localization(APPLANG) == True:
							if self.APP_LANGUAGE == APPLANG:
								self.debug(1,"NEW self.APP_LANGUAGE = '%s'" % (self.APP_LANGUAGE))
					else:
						self.debug(1,"self.APP_LANGUAGE = '%s'" % (self.APP_LANGUAGE))
				except:
					self.debug(1,"self.APP_LANGUAGE FAILED")
				
				try:
					self.LAST_CFG_UPDATE = parser.get('oVPN','lastcfgupdate')
					if not self.LAST_CFG_UPDATE >= 0:
						self.LAST_CFG_UPDATE = 0
				except:
					pass
				
				try:
					self.OVPN_FAV_SERVER = parser.get('oVPN','favserver')
					if self.OVPN_FAV_SERVER == "False": 
						self.OVPN_FAV_SERVER = False
					self.debug(1,"self.OVPN_FAV_SERVER = '%s'" % (self.OVPN_FAV_SERVER))
				except:
					pass
				
				try:
					self.OVPN_AUTO_CONNECT_ON_START = parser.getboolean('oVPN','autoconnect')
					if not self.OVPN_FAV_SERVER == False and self.OVPN_AUTO_CONNECT_ON_START == False:
						self.OVPN_AUTO_CONNECT_ON_START = True
					self.debug(1,"self.OVPN_AUTO_CONNECT_ON_START = '%s'" % (self.OVPN_AUTO_CONNECT_ON_START))
				except:
					pass
				
				try:
					self.WIN_EXT_DEVICE = parser.get('oVPN','winextdevice')
					if self.WIN_EXT_DEVICE == "False": 
						self.WIN_EXT_DEVICE = False
					self.debug(1,"self.WIN_TAP_DEVICE = '%s'" % (self.WIN_EXT_DEVICE))
				except:
					pass
				
				try:
					self.WIN_TAP_DEVICE = parser.get('oVPN','wintapdevice')
					if self.WIN_TAP_DEVICE == "False": 
						self.WIN_TAP_DEVICE = False
					self.debug(1,"self.WIN_TAP_DEVICE = '%s'" % (self.WIN_TAP_DEVICE))
				except:
					pass
				
				try:
					self.OPENVPN_EXE = parser.get('oVPN','openvpnexe')
					if self.OPENVPN_EXE == "False":
						self.OPENVPN_EXE = False
				except:
					pass
				
				try:
					self.UPDATEOVPNONSTART = parser.getboolean('oVPN','updateovpnonstart')
					self.debug(1,"self.UPDATEOVPNONSTART = '%s'" % (self.UPDATEOVPNONSTART))
				except:
					pass
				
				try:
					ocfgv = parser.get('oVPN','configversion')
					if ocfgv == "23x" or ocfgv == "23x46" or ocfgv == "23x64":
					
						self.OVPN_CONFIGVERSION = ocfgv
					else:
						self.OVPN_CONFIGVERSION = "23x"
					
					if self.OVPN_CONFIGVERSION == "23x":
						self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4A
						self.VPN_CFG = self.VPN_CFGip4
					elif self.OVPN_CONFIGVERSION == "23x46":
						self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4B
						self.VPN_CFG = self.VPN_CFGip46
					elif self.OVPN_CONFIGVERSION == "23x64":
						self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4B
						self.VPN_CFG = self.VPN_CFGip64
					
					self.debug(1,"self.OVPN_CONFIGVERSION = '%s'" % (self.OVPN_CONFIGVERSION))
				except:
					pass
				
				try:
					self.WIN_RESET_FIREWALL = parser.getboolean('oVPN','winresetfirewall')
					self.debug(1,"self.WIN_RESET_FIREWALL = '%s'" % (self.WIN_RESET_FIREWALL))
				except:
					pass
				
				try:
					self.WIN_BACKUP_FIREWALL = parser.getboolean('oVPN','winbackupfirewall')
					self.debug(1,"self.WIN_BACKUP_FIREWALL = '%s'" % (self.WIN_RESET_FIREWALL))
				except:
					pass
				
				try:
					self.NO_WIN_FIREWALL = parser.getboolean('oVPN','nowinfirewall')
					self.debug(1,"self.NO_WIN_FIREWALL = '%s'" % (self.NO_WIN_FIREWALL))
				except:
					pass
				
				try:
					self.WIN_DONT_ASK_FW_EXIT = parser.getboolean('oVPN','winnoaskfwonexit')
					self.debug(1,"self.WIN_DONT_ASK_FW_EXIT = '%s'" % (self.WIN_DONT_ASK_FW_EXIT))
				except:
					pass
				
				try:
					self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = parser.getboolean('oVPN','winfwblockonexit')
					self.debug(1,"self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = '%s'" % (self.WIN_ALWAYS_BLOCK_FW_ON_EXIT))
				except:
					pass

				try:
					self.WIN_DISABLE_EXT_IF_ON_DISCO = parser.getboolean('oVPN','windisableextifondisco')
					self.debug(1,"self.WIN_DISABLE_EXT_IF_ON_DISCO = '%s'" % (self.WIN_DISABLE_EXT_IF_ON_DISCO))
				except:
					pass
				
				
				try:
					self.TAP_BLOCKOUTBOUND = parser.getboolean('oVPN','wintapblockoutbound')
					self.debug(1,"self.TAP_BLOCKOUTBOUND = '%s'" % (self.TAP_BLOCKOUTBOUND))
				except:
					pass
				
				try:
					self.NO_DNS_CHANGE = parser.getboolean('oVPN','nodnschange')
					self.debug(1,"self.NO_DNS_CHANGE = '%s'" % (self.NO_DNS_CHANGE))
				except:
					pass

				try:
					self.LOAD_DATA_EVERY = parser.getint('oVPN','loaddataevery')
					if self.LOAD_DATA_EVERY <= 60:
						self.LOAD_DATA_EVERY = 66
					self.debug(1,"self.LOAD_DATA_EVERY = '%s'" % (self.LOAD_DATA_EVERY))
				except:
					pass
					
				try:
					self.LOAD_ACCDATA = parser.getboolean('oVPN','loadaccinfo')
					self.debug(1,"self.LOAD_ACCDATA = '%s'" % (self.LOAD_ACCDATA))
				except:
					pass
				
				try:
					self.LOAD_SRVDATA = parser.getboolean('oVPN','serverviewextend')
					self.debug(1,"self.LOAD_SRVDATA = '%s'" % (self.LOAD_SRVDATA))
				except:
					pass
				
				try:
					SRV_LIGHT_WIDTH = parser.getint('oVPN','serverviewlightwidth')
					SRV_LIGHT_HEIGHT = parser.getint('oVPN','serverviewlightheight')
					SRV_WIDTH = parser.getint('oVPN','serverviewextendwidth')
					SRV_HEIGHT = parser.getint('oVPN','serverviewextendheight')
					if SRV_LIGHT_WIDTH >= 1 and SRV_LIGHT_HEIGHT >= 1 and SRV_WIDTH >= 1 and SRV_HEIGHT >= 1:
						self.SRV_LIGHT_WIDTH = SRV_LIGHT_WIDTH
						self.SRV_LIGHT_HEIGHT = SRV_LIGHT_HEIGHT
						self.SRV_WIDTH = SRV_WIDTH
						self.SRV_HEIGHT = SRV_HEIGHT
						self.debug(1,"self.SRV_LIGHT_WIDTH,self.SRV_LIGHT_HEIGHT = '%sx%s'" % (self.SRV_LIGHT_WIDTH,self.SRV_LIGHT_HEIGHT))
						self.debug(1,"self.SRV_WIDTH,self.SRV_HEIGHT Window Size = '%sx%s'" % (self.SRV_WIDTH,self.SRV_HEIGHT))
				except:
					pass
				
				try:
					self.APP_THEME = parser.get('oVPN','theme')
					self.debug(1,"self.APP_THEME = '%s'" % (self.APP_THEME))
				except:
					pass
				
				try:
					self.ICONS_THEME = parser.get('oVPN','icons')
					self.load_icons()
					self.debug(1,"self.ICONS_THEME = '%s'" % (self.ICONS_THEME))
				except:
					pass
				
				try:
					self.APP_FONT_SIZE = parser.get('oVPN','font')
					self.debug(1,"self.APP_FONT_SIZE = '%s'" % (self.APP_FONT_SIZE))
				except:
					pass
				
				try:
					self.DISABLE_QUIT_ENTRY = parser.getboolean('oVPN','disablequitentry')
					self.debug(1,"self.DISABLE_QUIT_ENTRY '%s'" % (self.DISABLE_QUIT_ENTRY))
				except:
					pass
					
				
				
				try:
					self.MYDNS = json.loads(parser.get('oVPN','mydns'))
					self.debug(1,"def read_options_file: len(self.MYDNS) == '%s'"%(len(self.MYDNS)))
					self.debug(1,"def read_options_file: self.MYDNS == '%s'"%(self.MYDNS))
				except:
					self.debug(1,"def read_options_file: self.MYDNS = json.loads failed")
					self.MYDNS = {}
				
				return True
			
			except:
				self.msgwarn(_("Read config file failed!"),_("Error: def read_options_file"))
				try:
					os.remove(self.opt_file)
				except:
					pass
		
		else:
			try:
				cfg = open(self.opt_file,'wb')
				parser = SafeConfigParser()
				parser.add_section('oVPN')
				parser.set('oVPN','debugmode','False')
				parser.set('oVPN','applanguage',self.APP_LANGUAGE)
				parser.set('oVPN','passphrase','False')
				parser.set('oVPN','lastcfgupdate','0')
				parser.set('oVPN','autoconnect','False')
				parser.set('oVPN','favserver','False')
				parser.set('oVPN','winextdevice','False')
				parser.set('oVPN','wintapdevice','False')
				parser.set('oVPN','openvpnexe','False')
				parser.set('oVPN','updateovpnonstart','False')
				parser.set('oVPN','configversion','23x')
				parser.set('oVPN','serverviewextend','False')
				parser.set('oVPN','serverviewlightwidth','%s' % (self.SRV_LIGHT_WIDTH_DEFAULT))
				parser.set('oVPN','serverviewlightheight','%s' % (self.SRV_LIGHT_HEIGHT_DEFAULT))
				parser.set('oVPN','serverviewextendwidth','%s' % (self.SRV_WIDTH_DEFAULT))
				parser.set('oVPN','serverviewextendheight','%s' % (self.SRV_HEIGHT_DEFAULT))
				parser.set('oVPN','theme','ms-windows')
				parser.set('oVPN','icons','standard')
				parser.set('oVPN','winresetfirewall','False')
				parser.set('oVPN','winbackupfirewall','False')
				parser.set('oVPN','nowinfirewall','False')
				parser.set('oVPN','nodnschange','False')
				parser.set('oVPN','winnoaskfwonexit','False')
				parser.set('oVPN','winfwblockonexit','True')
				parser.set('oVPN','windisableextifondisco','False')
				parser.set('oVPN','wintapblockoutbound','False')
				parser.set('oVPN','loadaccinfo','False')
				parser.set('oVPN','loaddataevery','900')
				parser.set('oVPN','disablequitentry','True')
				parser.set('oVPN','mydns','False')
				parser.write(cfg)
				cfg.close()
				return True
			except:
				self.debug(1,"def read_options_file: create failed")

	def write_options_file(self):
		if self.isWRITING_OPTFILE == True:
			self.debug(1,"self.isWRITING_OPTFILE == True")
			return False
		self.isWRITING_OPTFILE = True
		self.debug(1,"def write_options_file()")
		try:
			if not self.APIKEY == False:
				if self.SAVE_APIKEY_INFILE == True:
					APIKEY = self.APIKEY
				else:
					APIKEY = False
			else:
				APIKEY = False
			cfg = open(self.opt_file,'wb')
			parser = SafeConfigParser()
			parser.add_section('oVPN')
			parser.set('oVPN','apikey','%s'%(APIKEY))
			parser.set('oVPN','debugmode','%s'%(self.DEBUG))
			parser.set('oVPN','applanguage','%s'%(self.APP_LANGUAGE))
			parser.set('oVPN','lastcfgupdate','%s'%(self.LAST_CFG_UPDATE))
			parser.set('oVPN','autoconnect','%s'%(self.OVPN_AUTO_CONNECT_ON_START))
			parser.set('oVPN','favserver','%s'%(self.OVPN_FAV_SERVER))
			parser.set('oVPN','winextdevice','%s'%(self.WIN_EXT_DEVICE))
			parser.set('oVPN','wintapdevice','%s'%(self.WIN_TAP_DEVICE))
			parser.set('oVPN','openvpnexe','%s'%(self.OPENVPN_EXE))
			parser.set('oVPN','updateovpnonstart','%s'%(self.UPDATEOVPNONSTART))
			parser.set('oVPN','configversion','%s'%(self.OVPN_CONFIGVERSION))
			parser.set('oVPN','serverviewextend','%s'%(self.LOAD_SRVDATA))
			parser.set('oVPN','serverviewlightwidth','%s'%(self.SRV_LIGHT_WIDTH))
			parser.set('oVPN','serverviewlightheight','%s'%(self.SRV_LIGHT_HEIGHT))
			parser.set('oVPN','serverviewextendwidth','%s'%(self.SRV_WIDTH))
			parser.set('oVPN','serverviewextendheight','%s'%(self.SRV_HEIGHT))
			parser.set('oVPN','theme','%s'%(self.APP_THEME))
			parser.set('oVPN','icons','%s'%(self.ICONS_THEME))
			parser.set('oVPN','font','%s'%(self.APP_FONT_SIZE))
			parser.set('oVPN','winresetfirewall','%s'%(self.WIN_RESET_FIREWALL))
			parser.set('oVPN','winbackupfirewall','%s'%(self.WIN_BACKUP_FIREWALL))
			parser.set('oVPN','nowinfirewall','%s'%(self.NO_WIN_FIREWALL))
			parser.set('oVPN','nodnschange','%s'%(self.NO_DNS_CHANGE))
			parser.set('oVPN','winnoaskfwonexit','%s'%(self.WIN_DONT_ASK_FW_EXIT))
			parser.set('oVPN','winfwblockonexit','%s'%(self.WIN_ALWAYS_BLOCK_FW_ON_EXIT))
			parser.set('oVPN','windisableextifondisco','%s'%(self.WIN_DISABLE_EXT_IF_ON_DISCO))
			parser.set('oVPN','wintapblockoutbound','%s'%(self.TAP_BLOCKOUTBOUND))
			parser.set('oVPN','loadaccinfo','%s'%(self.LOAD_ACCDATA))
			parser.set('oVPN','loaddataevery','%s'%(self.LOAD_DATA_EVERY))
			parser.set('oVPN','disablequitentry','%s'%(self.DISABLE_QUIT_ENTRY))
			parser.set('oVPN','mydns','%s'%(json.dumps(self.MYDNS, ensure_ascii=True)))
			parser.write(cfg)
			cfg.close()
			self.isWRITING_OPTFILE = False
			return True
		except:
			self.debug(1,"def write_options_file: failed")
		self.isWRITING_OPTFILE = False

	def read_interfaces(self):
		self.debug(1,"def read_interfaces()")
		if self.OS == "win32":
			if self.WIN_RESET_EXT_DEVICE == False:
				if self.win_read_interfaces():
					if self.win_firewall_export_on_start():
						if self.win_netsh_read_dns_to_backup():
							if self.read_gateway_from_routes():
								return True
							else:
								i = 0
								while not self.read_gateway_from_routes():
									if i > 5:
										return False
									time.sleep(5)
									i += 1
								return True
			else:
				self.win_netsh_restore_dns_from_backup()
				self.WIN_RESET_EXT_DEVICE = False
				if self.win_read_interfaces():
					if self.win_firewall_export_on_start():
						if self.win_netsh_read_dns_to_backup():
							if self.read_gateway_from_routes():
								return True

	def win_read_interfaces(self):
		self.debug(1,"def win_read_interfaces()")
		self.win_detect_openvpn()
		self.INTERFACES = list()
		string = "netsh.exe interface show interface"
		ADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		ADAPTERS = ADAPTERS.split('\r\n')
		LANG = "undef"

		# language read hint
		if ADAPTERS[1].endswith("nsefladenavn"):
			LANG = "DK"
		elif ADAPTERS[1].endswith("Schnittstellenname"):
			LANG = "DE"
		elif ADAPTERS[1].endswith("Interface Name"):
			LANG = "EN"
		else:
			self.errorquit(text=_("Error reading your Interfaces from netsh.exe. Contact support@ovpn.to with Error-ID:\nADAPTERS[1]=(%s)\n") % (ADAPTERS[1]))

		self.debug(1,"def win_read_interfaces: LANG = %s" % (LANG))
		for line in ADAPTERS:
			self.debug(1,"%s"%(line))
			interface = line.split()
			try:
				if LANG == "DK":
					if interface[1].startswith("Forbindelsen"):
						interface = interface[5:]
					elif interface[1].startswith("Afbrudt"):
						interface = interface[3:]
				elif LANG == "DE" or LANG == "EN":
					interface = interface[3:]
				else:
					interface = interface[3:]
				ilen = len(interface)
				if ilen > 1:
					nface = None
					for iface in interface:
						if not nface == None:
							nface = nface+" %s" % (iface)
							self.debug(1,"%s"%(nface))
						else:
							nface = iface
					interface = nface
				else:
					interface = interface[0]
				self.INTERFACES.append(interface)
			except:
				pass
		self.INTERFACES.pop(0)
		self.debug(1,"INTERFACES: %s"%(self.INTERFACES))
		if len(self.INTERFACES)	< 2:
			self.errorquit(text=_("Could not read your Network Interfaces! Please install OpenVPN or check if your TAP-Adapter is really enabled and driver installed."))
		string = '"%s" --show-adapters' % (self.OPENVPN_EXE)
		TAPADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		TAPADAPTERS = TAPADAPTERS.split('\r\n')
		self.debug(1,"TAP ADAPTERS bp = %s"%(TAPADAPTERS))
		TAPADAPTERS.pop(0)
		self.debug(1,"TAP ADAPTERS ap = %s"%(TAPADAPTERS))
		self.WIN_TAP_DEVS = list()
		for line in TAPADAPTERS:
			self.debug(10,"checking line = %s"%(line))
			for INTERFACE in self.INTERFACES:
				#if len(line) >= 1: self.debug(1,"is IF: '%s' listed as TAP in line '%s'?"%(INTERFACE,line))
				if line.startswith("'%s' {"%(INTERFACE)) and len(line) >= 1:
					self.debug(1,"Found TAP ADAPTER: '%s'" % (INTERFACE))
					self.INTERFACES.remove(INTERFACE)
					self.WIN_TAP_DEVS.append(INTERFACE)
					break
				""" do not remove! maybe need for debug in future """
				#elif line.startswith("Available TAP-WIN32 adapters"):
				#	#self.debug(1,"ignoring tap line")
				#	pass
				#elif len(line) < 16:
				#	#self.debug(1,"ignoring line < 16")
				#	pass
				#else:
				#	#self.debug(1,"ignoring else")
				#	pass
		self.debug(1,"self.WIN_TAP_DEVS = '%s' len=%s" % (self.WIN_TAP_DEVS,len(self.WIN_TAP_DEVS)))
		if self.WIN_TAP_DEVICE in self.WIN_TAP_DEVS:
			self.debug(1,"Found self.WIN_TAP_DEVICE '%s' in self.WIN_TAP_DEVS '%s'" % (self.WIN_TAP_DEVICE,self.WIN_TAP_DEVS))
		if len(self.WIN_TAP_DEVS) == 0:
			self.errorquit(text=_("No OpenVPN TAP-Windows Adapter found!"))
		elif len(self.WIN_TAP_DEVS) == 1 or self.WIN_TAP_DEVS[0] == self.WIN_TAP_DEVICE:
			self.WIN_TAP_DEVICE = self.WIN_TAP_DEVS[0]
			self.debug(1,"Selected self.WIN_TAP_DEVICE = %s" % (self.WIN_TAP_DEVICE))
		else:
			self.debug(1,"self.WIN_TAP_DEVS (query) = '%s'" % (self.WIN_TAP_DEVS))
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
			dialogWindow.set_position(Gtk.WindowPosition.CENTER)
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			text = _("Multiple TAPs found!\n\nPlease select your TAP Adapter!")
			dialogWindow.set_title(text)
			dialogWindow.set_markup(text)
			dialogBox = dialogWindow.get_content_area()
			liststore = Gtk.ListStore(str)
			combobox = Gtk.ComboBoxText.new()
			combobox.pack_start(cell, True)
			for INTERFACE in self.WIN_TAP_DEVS:
				self.debug(1,"add tap interface '%s' to combobox" % (INTERFACE))
				combobox.append_text(INTERFACE)
			combobox.connect('changed',self.cb_tap_interface_selector_changed)
			dialogBox.pack_start(combobox,False,False,0)
			dialogWindow.show_all()
			dialogWindow.run()
			dialogWindow.destroy()
		if self.WIN_TAP_DEVICE == False:
			self.errorquit(text=_("No OpenVPN TAP-Adapter found!\nPlease install openVPN!\nURL1: %s\nURL2: %s") % (self.OPENVPN_DL_URL,self.OPENVPN_DL_URL_ALT))
		else:
			badchars = ["%","&","$"]
			for char in badchars:
				if char in self.WIN_TAP_DEVICE:
					self.errorquit(text=_("Invalid characters in '%s'") % char)
			self.debug(1,"Selected TAP: '%s'" % (self.WIN_TAP_DEVICE))
			self.win_enable_tap_interface()
			self.debug(1,"remaining INTERFACES = %s (cfg: %s)"%(self.INTERFACES,self.WIN_EXT_DEVICE))
			if len(self.INTERFACES) > 1:
				if not self.WIN_EXT_DEVICE == False and self.WIN_EXT_DEVICE in self.INTERFACES:
					self.debug(1,"loaded self.WIN_EXT_DEVICE %s from options file"%(self.WIN_EXT_DEVICE))
					return True
				else:
					dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
					dialogWindow.set_position(Gtk.WindowPosition.CENTER)
					dialogWindow.set_transient_for(self.window)
					try:
						dialogWindow.set_icon_from_pixbuf(self.app_icon)
					except:
						pass
					text = _("Choose your External Network Adapter!")
					dialogWindow.set_title(text)
					dialogWindow.set_markup(text)
					dialogBox = dialogWindow.get_content_area()
					combobox = Gtk.ComboBoxText.new()
					for INTERFACE in self.INTERFACES:
						self.debug(1,"add interface %s to combobox" % (INTERFACE))
						combobox.append_text(INTERFACE)
					combobox.connect('changed',self.cb_interface_selector_changed)
					dialogBox.pack_start(combobox,False,False,0)
					dialogWindow.show_all()
					self.debug(1,"open interface selector")
					dialogWindow.run()
					self.debug(1,"close interface selector")
					dialogWindow.destroy()
					if not self.WIN_EXT_DEVICE == False:
						return True
			elif len(self.INTERFACES) < 1:
				self.errorquit(text=_("No Network Adapter found!"))
			else:
				self.WIN_EXT_DEVICE = self.INTERFACES[0]
				self.debug(1,"External Interface = %s"%(self.WIN_EXT_DEVICE))
				return True

	def select_userid(self):
		self.debug(1,"def select_userid()")
		dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
		dialogWindow.set_position(Gtk.WindowPosition.CENTER)
		dialogWindow.set_transient_for(self.window)
		try:
			dialogWindow.set_icon_from_pixbuf(self.app_icon)
		except:
			pass
		text = _("Please select your User-ID!")
		dialogWindow.set_title(text)
		dialogWindow.set_markup(text)
		dialogBox = dialogWindow.get_content_area()
		liststore = Gtk.ListStore(str)
		combobox = Gtk.ComboBoxText.new()
		for userid in self.PROFILES:
			self.debug(1,"add userid '%s' to combobox" % (userid))
			combobox.append_text(userid)
		combobox.connect('changed',self.cb_select_userid)
		dialogBox.pack_start(combobox,False,False,0)
		dialogWindow.show_all()
		self.debug(1,"open userid selector")
		dialogWindow.run()
		self.debug(1,"close userid interface selector")
		dialogWindow.destroy()
		if self.USERID > 1 and os.path.isdir("%s\\%s" % (self.app_dir,self.USERID)):
			return True


	def on_right_click_mainwindow(self, treeview, event):
		self.debug(1,"def on_right_click_mainwindow()")
		#self.IDLE_TIME = 0
		self.destroy_systray_menu()
		# get selection, also when treeview is sorted by a row
		servername = False
		pthinfo = self.treeview.get_path_at_pos(int(event.x), int(event.y))
		if pthinfo is not None:
			tree_selection = self.treeview.get_selection()
			(model, pathlist) = tree_selection.get_selected_rows()
			for path in pathlist:
				tree_iter = model.get_iter(path)
				servername = model.get_value(tree_iter,2)
		else:
			return False
		if servername:
			if event.button == 1:
				self.debug(1,"mainwindow left click (%s)" % (servername))
			elif event.button == 3:
				self.make_context_menu_servertab(servername)
				self.debug(1,"mainwindow right click (%s)" % (servername))

	def make_context_menu_servertab(self,servername):
		self.debug(1,"def make_context_menu_servertab: %s" % (servername))
		context_menu_servertab = Gtk.Menu()
		self.context_menu_servertab = context_menu_servertab
		
		if self.OVPN_CONNECTEDto == servername:
			disconnect = Gtk.MenuItem(_("Disconnect %s")%(self.OVPN_CONNECTEDto))
			context_menu_servertab.append(disconnect)
			disconnect.connect('button-release-event', self.cb_kill_openvpn)
		else:
			connect = Gtk.MenuItem(_("Connect to %s")%(servername))
			context_menu_servertab.append(connect)
			connect.connect('button-release-event',self.cb_jump_openvpn,servername)
		
		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)
		
		if self.OVPN_FAV_SERVER == servername:
			delfavorite = Gtk.MenuItem(_("Remove AutoConnect: %s")%(servername))
			delfavorite.connect('button-release-event',self.cb_del_ovpn_favorite_server,servername)
			context_menu_servertab.append(delfavorite)
		else:
			setfavorite = Gtk.MenuItem(_("Set AutoConnect: %s")%(servername))
			setfavorite.connect('button-release-event',self.cb_set_ovpn_favorite_server,servername)
			context_menu_servertab.append(setfavorite)
		
		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)
		
		self.make_context_menu_servertab_d0wns_dnsmenu(servername)
		
		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)
		
		if self.DISABLE_SRV_WINDOW == False:
			try:
				if self.LOAD_SRVDATA == True:
					opt = _("[enabled]")
				else:
					opt = _("[disabled]")
				extserverview = Gtk.MenuItem(_("Load Server Information %s") %(opt))
				extserverview.connect('button-release-event', self.cb_extserverview)
				context_menu_servertab.append(extserverview)
			except:
				self.debug(1,"def make_context_menu_servertab: extserverview failed")
			
			try:
				if self.LOAD_SRVDATA == True:
					WIDTH = self.SRV_WIDTH
					HEIGHT = self.SRV_HEIGHT
				else:
					WIDTH = self.SRV_LIGHT_WIDTH
					HEIGHT = self.SRV_LIGHT_HEIGHT
				extserverviewsize = Gtk.MenuItem(_("Set Server-View Size [%sx%s]") %(int(WIDTH),int(HEIGHT)))
				extserverviewsize.connect('button-release-event', self.cb_extserverview_size)
				context_menu_servertab.append(extserverviewsize)
			except:
				self.debug(1,"def make_context_menu_servertab: extserverviewsize failed")
				
			try:
				loaddataevery = Gtk.MenuItem(_("Update every: %s seconds") %(self.LOAD_DATA_EVERY))
				loaddataevery.connect('button-release-event', self.cb_set_loaddataevery)
				context_menu_servertab.append(loaddataevery)
			except:
				self.debug(1,"def make_context_menu_servertab: loaddataevery failed")

		context_menu_servertab.show_all()
		context_menu_servertab.popup(None, None, None, 3, int(time.time()), 0)
		self.debug(1,"def make_context_menu_servertab: return")
		return

	def make_context_menu_servertab_d0wns_dnsmenu(self,servername):
		try:
			self.debug(1,"def make_context_menu_servertab_d0wns_dnsmenu: servername = '%s'" % (servername))
			if len(self.d0wns_DNS) == 0:
				self.read_d0wns_dns()
			
			dnsmenu = Gtk.Menu()
			dnsm = Gtk.MenuItem(_("Change DNS"))
			dnsm.set_submenu(dnsmenu)
			self.dnsmenu = dnsmenu
			
			try:
				self.debug(1,"mydns debug 1.1")
				pridns = self.MYDNS[servername]["primary"]["ip4"]
				self.debug(1,"mydns debug 1.2")
				priname = self.MYDNS[servername]["primary"]["dnsname"]
				self.debug(1,"mydns debug 1.3")
				string = "Primary DNS: %s (%s)" % (priname,pridns)
				self.debug(1,"mydns debug 1.4")
				pridnsm = Gtk.MenuItem(string)
				self.debug(1,"mydns debug 1.5")
				cbdata = {servername:{"primary":{"ip4":pridns,"dnsname":priname}}}
				self.debug(1,"mydns debug 1.6")
				pridnsm.connect('button-release-event',self.cb_del_dns,cbdata)
				self.debug(1,"mydns debug 1.7")
				self.context_menu_servertab.append(pridnsm)
				self.debug(1,"mydns debug 1.8")
			except:
				self.debug(1,"mydns debug 1.9")
				pridns = False
			
			try:
				self.debug(1,"mydns debug 2.1")
				secdns = self.MYDNS[servername]["secondary"]["ip4"]
				self.debug(1,"mydns debug 2.2")
				secname = self.MYDNS[servername]["secondary"]["dnsname"]
				self.debug(1,"mydns debug 2.3")
				string = "Secondary DNS: %s (%s)" % (secname,secdns)
				self.debug(1,"mydns debug 2.4")
				secdnsm = Gtk.MenuItem(string)
				self.debug(1,"mydns debug 2.5")
				cbdata = {servername:{"secondary":{"ip4":secdns,"dnsname":secname}}}
				self.debug(1,"mydns debug 2.6")
				secdnsm.connect('button-release-event',self.cb_del_dns,cbdata)
				self.debug(1,"mydns debug 2.7")
				self.context_menu_servertab.append(secdnsm)
				self.debug(1,"mydns debug 2.8")
			except:
				self.debug(1,"mydns debug 2.9")
				secdns = False
			
			for name,value in sorted(self.d0wns_DNS.iteritems()):
				try:
					dnsip4 = value['ip4']
					countrycode = self.d0wns_DNS[name]['countrycode']
					dnssubmenu = Gtk.Menu()
					self.dnssubmenu = dnssubmenu
					dnssubmtext = "%s (%s)" % (name,dnsip4)
					dnssubm = Gtk.ImageMenuItem(dnssubmtext)
					dnssubm.set_submenu(dnssubmenu)
					img = Gtk.Image()
					imgfile = self.decode_flag(countrycode)
					img.set_from_pixbuf(imgfile)
					dnssubm.set_always_show_image(True)
					dnssubm.set_image(img)
					dnsmenu.append(dnssubm)
					
					cbdata = {servername:{"primary":{"ip4":dnsip4,"dnsname":name}}}
					if pridns == dnsip4:
						string = "Primary DNS '%s' @ %s" % (pridns,servername)
						setpridns = Gtk.MenuItem(string)
						setpridns.connect('button-release-event',self.cb_del_dns,cbdata)
					else:
						setpridns = Gtk.MenuItem(_("Set Primary DNS"))
						setpridns.connect('button-release-event',self.cb_set_dns,cbdata)
					dnssubmenu.append(setpridns)
					
					cbdata = {servername:{"secondary":{"ip4":dnsip4,"dnsname":name}}}
					if secdns == dnsip4:
						string = "Secondary DNS '%s' @ %s" % (secdns,servername)
						setsecdns = Gtk.MenuItem(string)
						setsecdns.connect('button-release-event',self.cb_del_dns,cbdata)
					else:
						setsecdns = Gtk.MenuItem(_("Set Secondary DNS"))
						setsecdns.connect('button-release-event',self.cb_set_dns,cbdata)
					dnssubmenu.append(setsecdns)
				except:
					self.debug(1,"def make_context_menu_servertab_d0wns_dnsmenu: dnsmenu.append(dnssubm) '%s' failed "%(countrycode))
				
			dnsm.show_all()
			self.context_menu_servertab.append(dnsm)
		except:
			self.debug(1,"def make_context_menu_servertab_d0wns_dnsmenu: failed!")

	def systray_timer2(self):
		self.debug(10,"def systray_timer2()")
		self.systray_timer2_running = True
		if self.stop_systray_timer2 == True:
			self.systray_timer2_running = False
			return False
		
		if not self.systray_menu == False:
			self.check_hide_popup()
		
		try:
			if self.LAST_MSGWARN_WINDOW > 0 and (int(time.time())-self.LAST_MSGWARN_WINDOW) > 9:
				GLib.idle_add(self.msgwarn_window.destroy)
				self.LAST_MSGWARN_WINDOW = 0
		except:
			pass
		
		if self.UPDATE_SWITCH == True and self.SETTINGSWINDOW_OPEN == True:
			self.debug(1,"def systray_timer2: UPDATE_SWITCH")
			
			# Language changed
			if self.LANG_FONT_CHANGE == True:
				try:
					self.settingsnotebook.remove(self.nbpage0)
					self.settingsnotebook.remove(self.nbpage1)
					self.settingsnotebook.remove(self.nbpage2)
				except:
					pass
				try:
					self.settingsnotebook.remove(self.nbpage3)
				except:
					pass
				try:
					self.show_hide_security_window()
					self.show_hide_options_window()
					self.show_hide_updates_window()
					self.settingswindow.show_all()
					self.settingsnotebook.set_current_page(1)
				except:
					pass
				self.LANG_FONT_CHANGE = False
			
			if self.state_openvpn() == True:
				self.switch_fw.set_sensitive(False)
				self.switch_fwblockonexit.set_sensitive(False)
				self.switch_fwdontaskonexit.set_sensitive(False)
				self.switch_fwresetonconnect.set_sensitive(False)
				self.switch_fwbackupmode.set_sensitive(False)
				self.switch_nodns.set_sensitive(False)
				self.button_switch_network_adapter.set_sensitive(False)
				try:
					self.settingsnotebook.remove(self.nbpage3)
				except:
					pass
			elif self.NO_WIN_FIREWALL == True:
				self.switch_fwblockonexit.set_sensitive(False)
				self.switch_fwdontaskonexit.set_sensitive(False)
				self.switch_fwresetonconnect.set_sensitive(False)
				self.switch_fwbackupmode.set_sensitive(False)
				self.switch_tapblockoutbound.set_sensitive(False)
			else:
				self.switch_fw.set_sensitive(True)
				self.switch_fwblockonexit.set_sensitive(True)
				self.switch_fwdontaskonexit.set_sensitive(True)
				self.switch_fwresetonconnect.set_sensitive(True)
				self.switch_fwbackupmode.set_sensitive(True)
				self.switch_nodns.set_sensitive(True)
				self.button_switch_network_adapter.set_sensitive(True)
				try:
					self.show_hide_backup_window()
					self.settingswindow.show_all()
				except:
					pass
			
			# def settings_firewall_switch_nofw()
			if self.NO_WIN_FIREWALL == True:
				self.switch_fw.set_active(False)
				try:
					self.settingsnotebook.remove(self.nbpage3)
				except:
					pass
			else:
				self.switch_fw.set_active(True)
			
			# def settings_firewall_switch_tapblockoutbound()
			if self.TAP_BLOCKOUTBOUND == True:
				self.switch_tapblockoutbound.set_active(True)
			else:
				self.switch_tapblockoutbound.set_active(False)
			
			# def settings_firewall_switch_fwblockonexit()
			if self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
				self.switch_fwblockonexit.set_active(True)
			else:
				self.switch_fwblockonexit.set_active(False)
			
			# def settings_firewall_switch_fwdontaskonexit()
			if self.WIN_DONT_ASK_FW_EXIT == True:
				self.switch_fwdontaskonexit.set_active(True)
			else:
				self.switch_fwdontaskonexit.set_active(False)
			
			# def settings_firewall_switch_fwresetonconnect()
			if self.WIN_RESET_FIREWALL == True:
				self.switch_fwresetonconnect.set_active(True)
			else:
				self.switch_fwresetonconnect.set_active(False)
			
			# def settings_firewall_switch_fwbackupmode()
			if self.WIN_BACKUP_FIREWALL == True:
				self.switch_fwbackupmode.set_active(True)
			else:
				self.switch_fwbackupmode.set_active(False)
			
			# def settings_network_switch_nodns()
			if self.NO_DNS_CHANGE == True:
				self.switch_nodns.set_active(False)
			else:
				self.switch_nodns.set_active(True)
			
			# settings_network_switch_disableextifondisco
			if self.WIN_DISABLE_EXT_IF_ON_DISCO == True:
				self.switch_disableextifondisco.set_active(True)
			else:
				self.switch_disableextifondisco.set_active(False)
			
			# settings_options_switch_updateovpnonstart
			if self.UPDATEOVPNONSTART == True:
				self.switch_updateovpnonstart.set_active(True)
			else:
				self.switch_updateovpnonstart.set_active(False)
			
			# settings_options_switch_accinfo
			if self.LOAD_ACCDATA == True:
				self.switch_accinfo.set_active(True)
			else:
				self.switch_accinfo.set_active(False)
			
			# settings_options_switch_srvinfo
			if self.LOAD_SRVDATA == True:
				self.switch_srvinfo.set_active(True)
			else:
				self.switch_srvinfo.set_active(False)
			
			# settings_options_switch_debugmode
			if self.DEBUG == True:
				self.switch_debugmode.set_active(True)
			else:
				self.switch_debugmode.set_active(False)
			
			# settings_options_button_ipv6
			if self.OVPN_CONFIGVERSION == "23x":
				self.button_title.set_label(_("Current: IPv4 Entry Server with Exit to IPv4 (standard)"))
				self.button_ipmode.set_label(_("Use IPv4 Entry Server with Exits to IPv4 + IPv6"))
			elif self.OVPN_CONFIGVERSION == "23x46":
				self.button_title.set_label(_("Current: IPv4 Entry Server with Exits to IPv4 + IPv6"))
				self.button_ipmode.set_label(_("Use IPv4 Entry Server with Exit to IPv4 (standard)"))
			
			# settings_options_combobox_icons
			if self.ICONS_THEME == "standard":
				active_item = 0
			if self.ICONS_THEME == "classic":
				active_item = 1
			if self.ICONS_THEME == "classic2":
				active_item = 2
			if self.ICONS_THEME == "shield_bluesync":
				active_item = 3
			if self.ICONS_THEME == "experimental":
				active_item = 4
			if self.ICONS_THEME == "private":
				active_item = 5
			self.combobox_icons.set_active(active_item)
			
			# resize settings window
			self.settingswindow.resize(1,1)
			
			# end switches update
			self.UPDATE_SWITCH = False
		else:
			self.UPDATE_SWITCH = False
		
		systraytext = False
		if self.timer_check_certdl_running == True:
			if not self.STATE_CERTDL == False:
				if self.STATE_CERTDL == "lastupdate":
					systraytext = _("Checking for Updates!")
					systrayicon = self.systray_icon_syncupdate1
				elif self.STATE_CERTDL == "getconfigs":
					systraytext = _("Downloading Configurations...")
					systrayicon = self.systray_icon_syncupdate2
				elif self.STATE_CERTDL == "requestcerts":
					systraytext = _("Requesting Certificates...")
					systrayicon = self.systray_icon_syncupdate1
				elif self.STATE_CERTDL == "wait":
						systraytext = _("Please wait... Certificates requested from backend! (%s)") % (self.API_COUNTER)
						if not self.OVERWRITE_TRAYICON == False:
							systrayicon = self.OVERWRITE_TRAYICON
						elif self.STATUS_ICON_BLINK%2==0:
							systrayicon = self.systray_icon_syncupdate1
						else:
							systrayicon = self.systray_icon_syncupdate2
				elif self.STATE_CERTDL == "getcerts":
					systraytext = _("Downloading Certificates...")
					systrayicon = self.systray_icon_syncupdate1
				elif self.STATE_CERTDL == "extract":
					systraytext = _("Extracting Configs and Certs...")
					systrayicon = self.systray_icon_syncupdate2
				statusbar_text = systraytext
				
		elif self.state_openvpn() == False and self.OVERWRITE_TRAYICON == False:
			systraytext = _("Disconnected! Have a nice and anonymous day!")
			statusbar_text = systraytext
			systrayicon = self.systray_icon_disconnected
			try:
				if len(self.OVPN_SERVER) == 0 and self.INIT_FIRST_UPDATE == True:
					self.INIT_FIRST_UPDATE = False
					self.load_ovpn_server()
					if len(self.OVPN_SERVER) == 0:
						self.debug(1,"zero server found, initiate first update")
						self.check_remote_update()
				elif len(self.OVPN_SERVER) > 0 and self.INIT_FIRST_UPDATE == True:
					self.INIT_FIRST_UPDATE = False
				elif self.OVPN_AUTO_CONNECT_ON_START == True and not self.OVPN_FAV_SERVER == False:
					self.OVPN_AUTO_CONNECT_ON_START = False
					self.debug(1,"def systray_timer: self.OVPN_AUTO_CONNECT_ON_START: self.OVPN_FAV_SERVER = '%s'" % (self.OVPN_FAV_SERVER))
					self.cb_jump_openvpn(0,0,self.OVPN_FAV_SERVER)
				
			except:
				self.debug(1,"def timer_statusbar: OVPN_AUTO_CONNECT_ON_START failed")
		elif self.inThread_jump_server_running == True and self.OVERWRITE_TRAYICON == True:
			systraytext = _("Connecting to %s") % (self.OVPN_CALL_SRV)
			systrayicon = self.systray_icon_connect
			statusbar_text = systraytext
			self.debug(1,"def systray_timer: cstate = '%s'" % (systraytext))
		elif self.state_openvpn() == True:
			connectedseconds = int(time.time()) - self.OVPN_CONNECTEDtime
			self.OVPN_CONNECTEDseconds = connectedseconds
			if self.OVPN_PING_STAT == -2:
				self.OVPN_isTESTING = True
				systraytext = _("Testing connection to %s") % (self.OVPN_CONNECTEDto)
				systrayicon = self.systray_icon_testing
				statusbar_text = systraytext
				self.debug(1,"def systray_timer: cstate = '%s'" % (systraytext))
			elif self.OVPN_PING_LAST == -2 and self.OVPN_PING_DEAD_COUNT > 3:
				systraytext = _("Connection to %s unstable or failed!") % (self.OVPN_CONNECTEDto)
				systrayicon = self.systray_icon_testing
				statusbar_text = systraytext
				self.debug(1,"def systray_timer: cstate = '%s'" % (systraytext))
			elif self.OVPN_PING_STAT > 0:
				try:
					if self.OVPN_isTESTING == True:
						self.OVPN_PING = list()
						self.OVPN_PING_STAT = self.OVPN_PING_LAST
						self.OVPN_isTESTING = False
					m, s = divmod(connectedseconds, 60)
					h, m = divmod(m, 60)
					d, h = divmod(h, 24)
					if self.OVPN_CONNECTEDseconds >= 0:
						connectedtime_text = "%d:%02d:%02d:%02d" % (d,h,m,s)
					statusbar_text = _("Connected to %s [%s]:%s (%s) [ %s ] (%s / %s ms)") % (self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper(),connectedtime_text,self.OVPN_PING_LAST,self.OVPN_PING_STAT)
					# systraytext Windows only shows the first 64 characters
					systraytext = "%s [%s]:%s (%s) [%s] %sms" % (self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper(),connectedtime_text,self.OVPN_PING_LAST)
					#statusbar_text = systraytext
					systrayicon = self.systray_icon_connected
				except:
					self.debug(1,"def systray_timer: systraytext failed")

		try:
			# traytext
			if not self.systraytext_from_before == systraytext and not systraytext == False:
				self.systraytext_from_before = systraytext
				self.tray.set_tooltip_markup(systraytext)
			
			# trayicon
			if not self.systrayicon_from_before == systrayicon:
				self.systrayicon_from_before = systrayicon
				if self.APP_THEME == "private":
					self.tray.set_from_file(systrayicon)
				else:
					self.tray.set_from_pixbuf(systrayicon)
			
			# statusbar
			if self.MAINWINDOW_OPEN == True:
				if not self.statusbartext_from_before == statusbar_text:
					self.set_statusbar_text(statusbar_text)
					self.statusbartext_from_before = statusbar_text
		except:
			pass

		try:
			if self.timer_load_remote_data_running == False:
				thread = threading.Thread(target=self.load_remote_data)
				thread.daemon = True
				thread.start()
		except:
			self.debug(1,"def systray_timer2: thread target=self.load_remote_data failed")

		self.systray_timer2_running = False
		
		"""
		if self.IDLE_TIME > 300:
			
			if len(self.FLAG_CACHE_PIXBUF) >= 1:
				self.FLAG_CACHE_PIXBUF = {}
				for entry in self.FLAG_CACHE_PIXBUF:
					del entry
					gc.collect()
				self.debug(1,"def systray_timer2: CLEAR self.FLAG_CACHE_PIXBUF")
			
			if len(self.ICON_CACHE_PIXBUF) > 1:
				self.ICON_CACHE_PIXBUF = {}
				for entry in self.ICON_CACHE_PIXBUF:
					del entry
					gc.collect()
				self.debug(1,"def systray_timer2: CLEAR self.ICON_CACHE_PIXBUF")
		else:
			self.IDLE_TIME += 0.5
			#self.debug(1,"self.IDLE_TIME = %s" % (self.IDLE_TIME))
		"""
		
		self.debug(19,"def systray_timer2() return")
		return

	def systray_timer(self):
		#self.debug(19,"def systray_timer()")
		if self.stop_systray_timer == True:
			return False
		if self.systray_timer2_running == False:
			self.debug(19,"def systray_timer: GLib.idle_add(self.systray_timer2)")
			GLib.idle_add(self.systray_timer2)
		time.sleep(0.5)
		thread = threading.Thread(target=self.systray_timer)
		thread.daemon = True
		thread.start()
		return

	def on_right_click(self, widget, event, event_time):
		self.debug(1,"def on_right_click()")
		#self.IDLE_TIME = 0
		if not self.systray_menu == False:
			self.destroy_systray_menu()
		else:
			self.make_systray_menu(event)

	def on_left_click(self, widget):
		self.debug(1,"def on_left_click()")
		#self.IDLE_TIME = 0
		if not self.systray_menu == False:
			self.destroy_systray_menu()
		else:
			if self.MAINWINDOW_OPEN == False:
				try:
					self.load_ovpn_server()
					if len(self.OVPN_SERVER) > 0:
						event = Gtk.get_current_event_time()
						self.show_mainwindow(widget, event)
				except:
					self.debug(1,"def show_mainwindow() on_left_click failed")
			else:
				if self.mainwindow.get_property("visible") == False:
					self.debug(1,"def on_left_click: unhide Mainwindow")
					self.MAINWINDOW_HIDE = False
					self.mainwindow.show()
				else:
					self.debug(1,"def on_left_click: hide Mainwindow")
					self.mainwindow.hide()
					self.MAINWINDOW_HIDE = True
					return True

	def make_systray_menu(self, event):
		self.debug(1,"def make_systray_menu()")
		try:
			self.systray_menu = Gtk.Menu()
			if self.LOGLEVEL > 1:
				self.MOUSE_IN_TRAY = time.time() + 30
			else:
				self.MOUSE_IN_TRAY = time.time() + 3
			
			try:
				self.load_ovpn_server()
			except:
				self.debug(1,"def make_systray_menu: self.load_ovpn_server() failed")
			
			try:
				self.make_systray_server_menu()
			except:
				self.debug(1,"def make_systray_menu: self.make_systray_server_menu() failed")
			
			try:
				self.make_systray_openvpn_menu()
			except:
				self.debug(1,"def make_systray_menu: self.make_systray_openvpn_menu() failed")
			
			try:
				self.make_systray_bottom_menu()
			except:
				self.debug(1,"def make_systray_menu: self.make_systray_bottom_menu() failed")
			
			self.systray_menu.connect('enter-notify-event', self.systray_notify_event_enter,"systray_menu")
			self.systray_menu.show_all()
			self.systray_menu.popup(None, None, None, event, 0, 0)
		except:
			self.destroy_systray_menu()
			self.debug(1,"def make_systray_menu: failed")

	def make_systray_server_menu(self):
		self.debug(1,"def make_systray_server_menu()")
		if len(self.OVPN_SERVER) > 0:
			try:
				countrycodefrombefore = 0
				for servername in self.OVPN_SERVER:
					servershort = servername[:3]
					
					textstring = "%s [%s]:%s (%s)" % (servershort,self.OVPN_SERVER_INFO[servershort][0],self.OVPN_SERVER_INFO[servershort][1],self.OVPN_SERVER_INFO[servershort][2])
					countrycode = servershort[:2].lower()
					#print "string = %s, countrycode = %s" % (textstring,countrycode)
					
					if not countrycodefrombefore == countrycode:
						# create countrygroup menu
						countrycodefrombefore = countrycode
						cgmenu = Gtk.Menu()
						cgmenu.connect('enter-notify-event', self.systray_notify_event_enter,"sub_cgmenu")
						cgmenu.connect('leave-notify-event', self.systray_notify_event_leave,"sub_cgmenu")
						self.cgmenu = cgmenu
						try:
							countryname = self.COUNTRYNAMES[countrycode.upper()]
						except:
							countryname = countrycode.upper()
						
						try:
							cgm = Gtk.ImageMenuItem(countryname)
							img = Gtk.Image()
							try:
								imgfile = self.decode_flag(countrycode)
								img.set_from_pixbuf(imgfile)
								cgm.set_always_show_image(True)
								cgm.set_image(img)
								cgm.set_submenu(cgmenu)
								self.systray_menu.append(cgm)
							except:
								self.debug(1,"def make_systray_server_menu: countrycode = '%s' failed" % (countrycode))
								self.destroy_systray_menu()
						except:
							self.destroy_systray_menu()
							self.debug(1,"def make_systray_server_menu: flagimg group1 failed")
					
					if self.OVPN_CONNECTEDto == servername:
						textstring = servershort+_(" [ disconnect ]")
						serveritem = Gtk.ImageMenuItem(textstring)
						serveritem.connect('button-release-event', self.cb_kill_openvpn)
					else:
						serveritem = Gtk.ImageMenuItem(textstring)
						serveritem.connect('button-release-event', self.cb_jump_openvpn, servername)
					
					img = Gtk.Image()
					imgfile = self.decode_flag(countrycode)
					img.set_from_pixbuf(imgfile)
					serveritem.set_always_show_image(True)
					serveritem.set_image(img)
					cgmenu.append(serveritem)

			except:
				self.destroy_systray_menu()
				self.debug(1,"def make_systray_server_menu: failed")

	def make_systray_openvpn_menu(self):
		self.debug(1,"def make_systray_openvpn_menu()")
		if self.state_openvpn() == True:
			try:
				sep = Gtk.SeparatorMenuItem()
				servershort = self.OVPN_CONNECTEDto[:3]
				textstring = '%s @ [%s]:%s (%s)' % (servershort,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper())
				disconnect = Gtk.ImageMenuItem(textstring)
				img = Gtk.Image()
				if self.APP_THEME == "private":
					img.set_from_file(self.systray_icon_disconnected_traymenu)
				else:
					img.set_from_pixbuf(self.systray_icon_disconnected_traymenu)
				disconnect.set_always_show_image(True)
				disconnect.set_image(img)
				self.systray_menu.append(sep)
				self.systray_menu.append(disconnect)
				disconnect.connect('button-release-event', self.cb_kill_openvpn)
			except:
				self.debug(1,"def make_systray_openvpn_menu: failed")

	def make_systray_bottom_menu(self):
		self.debug(1,"def make_systray_bottom_menu()")
		
		sep = Gtk.SeparatorMenuItem()
		self.systray_menu.append(sep)
		
		try:
			accwindowentry = False
			if self.ACCWINDOW_OPEN == True:
				accwindowentry = Gtk.MenuItem(_("Close Account"))
			else:
				if self.LOAD_ACCDATA == True and not self.APIKEY == False:
					accwindowentry = Gtk.MenuItem(_("Account"))
			if accwindowentry:
				self.systray_menu.append(accwindowentry)
				accwindowentry.connect('button-release-event', self.show_accwindow)
				accwindowentry.connect('leave-notify-event', self.systray_notify_event_leave,"accwindowentry")
		except:
			self.debug(1,"def make_systray_bottom_menu: accwindowentry failed")
		
		try:
			if self.SETTINGSWINDOW_OPEN == True:
				settwindowentry = Gtk.MenuItem(_("Close Settings"))
			else:
				settwindowentry = Gtk.MenuItem(_("Settings"))
			self.systray_menu.append(settwindowentry)
			settwindowentry.connect('button-release-event', self.show_settingswindow)
			settwindowentry.connect('leave-notify-event', self.systray_notify_event_leave,"settwindowentry")
		except:
			self.debug(1,"def make_systray_bottom_menu: settwindowentry failed")
		
		if self.DISABLE_QUIT_ENTRY == True and self.state_openvpn() == True:
			pass
		else:
			try:
				sep = Gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)
				about = Gtk.MenuItem(_("About"))
				self.systray_menu.append(about)
				about.connect('button-release-event', self.show_about_dialog)
				about.connect('leave-notify-event', self.systray_notify_event_leave,"about")
			except:
				self.debug(1,"def make_systray_bottom_menu: about failed")
			
			# add quit item
			quit = Gtk.MenuItem(_("Quit"))
			if self.state_openvpn() == True:
				quit.set_sensitive(False)
			self.systray_menu.append(quit)
			quit.connect('button-release-event', self.on_closing)
			quit.connect('leave-notify-event', self.systray_notify_event_leave,"quit")

	def systray_notify_event_leave(self, widget, event, data = None):
		self.debug(10,"def systray_notify_event_leave() data = '%s'" % (data))
		self.MOUSE_IN_TRAY = time.time() + 1

	def systray_notify_event_enter(self, widget, event, data = None):
		self.debug(10,"def systray_notify_event_enter() data = '%s'" % (data))
		self.MOUSE_IN_TRAY = time.time() + 30

	def check_hide_popup(self):
		self.debug(10,"def check_hide_popup()")
		if self.MOUSE_IN_TRAY < time.time():
			self.destroy_systray_menu()

	def check_remote_update(self):
		self.debug(1,"def check_remote_update()")
		if self.timer_check_certdl_running == False:
			self.debug(1,"def check_remote_update: check_inet_connection() == True")
			try:
				thread_certdl = threading.Thread(name='certdl',target=self.inThread_timer_check_certdl)
				thread_certdl.daemon = True
				thread_certdl.start()
				threadid_certdl = threading.currentThread()
				self.debug(1,"def check_remote_update threadid_certdl = %s" %(threadid_certdl))
				return True
			except:
				self.debug(1,"starting thread_certdl failed")
		return False

	def inThread_timer_check_certdl(self):
		self.debug(1,"def inThread_timer_check_certdl()")
		try:
			self.timer_check_certdl_running = True
			try:
				self.load_ovpn_server()
				if len(self.OVPN_SERVER) == 0:
					self.reset_last_update()
			except:
				self.debug(1,"def inThread_timer_check_certdl: self.load_ovpn_server() failed")
			self.debug(1,"def inThread_timer_check_certdl()")
			self.STATE_CERTDL = "lastupdate"
			if self.API_REQUEST(API_ACTION = "lastupdate"):
				self.debug(1,"def inThread_timer_check_certdl: API_ACTION lastupdate")
				if self.check_last_server_update(self.curldata):
					self.STATE_CERTDL = "getconfigs"
					if self.API_REQUEST(API_ACTION = "getconfigs"):
						self.STATE_CERTDL = "requestcerts"
						if self.API_REQUEST(API_ACTION = "requestcerts"):
							self.STATUS_ICON_BLINK = 0
							self.STATE_CERTDL = "wait"
							self.API_COUNTER = 120
							LAST_requestcerts = 0
							while not self.body == "ready":
								if self.API_COUNTER <= 0:
									self.timer_check_certdl_running = False
									self.msgwarn(_("Update took too long...aborted!\nPlease retry in few minutes..."),_("Error: Update Timeout"))
									return False
								time.sleep(0.5)
								if LAST_requestcerts > 6:
									self.OVERWRITE_TRAYICON = self.systray_icon_syncupdate3
									self.API_REQUEST(API_ACTION = "requestcerts")
									self.OVERWRITE_TRAYICON = False
									LAST_requestcerts = 0
								else:
									LAST_requestcerts += 1
								self.STATUS_ICON_BLINK += 1
								self.API_COUNTER -= 1
							# final step to download certs
							self.STATE_CERTDL = "getcerts"
							if self.API_REQUEST(API_ACTION = "getcerts"):
								self.STATE_CERTDL = "extract"
								if self.extract_ovpn():
									self.timer_check_certdl_running = False
									self.msgwarn(_("Certificates and Configs updated!"),_("oVPN Update OK!"))
									return True
								else:
									self.msgwarn(_("Extraction failed!"),_("Error: def inThread_timer_check_certdl"))
							else:
								self.msgwarn(_("Failed to download certificates"),_("Error: def inThread_timer_check_certdl"))
							# finish downloading certs
						else:
							self.msgwarn(_("Failed to request certificates!"),_("Error: def inThread_timer_check_certdl"))
					else:
						self.msgwarn(_("Failed to download configurations!"),_("Error: def inThread_timer_check_certdl"))
				else:
					self.timer_check_certdl_running = False
					self.msgwarn(_("No update needed!"),_("oVPN Update OK!"))
					return True
			#else:
			#	self.msgwarn(_("oVPN Update failed"),_("Error: def inThread_timer_check_certdl"))
		except:
			self.msgwarn(_("Failed to check for updates!"),_("Error: def inThread_timer_check_certdl"))
		self.timer_check_certdl_running = False
		return False

	def update_mwls(self):
		self.debug(1,"def update_mwls()")
		liststore = self.serverliststore
		debugupdate_mwls = False
		t1 = time.time()
		for row in liststore:
			server = row[2]
			if server in self.OVPN_SERVER:
				if debugupdate_mwls: self.debug(1,"def update_mwls: server '%s'" % (server))
				servershort = server[:3].upper()
				if row[2] == server:
					value = False
					iter = liststore.get_iter_first()
					while iter != None and liststore.get_value(iter,2) != server:
						iter = liststore.iter_next(iter)
					value = liststore.get_value(iter,2)
					cellnumber = 0
					row_changed = 0
					while cellnumber <= 24:
						oldvalue = row[cellnumber]
						try:
							serverip4  = str(self.OVPN_SERVER_INFO[servershort][0])
							serverport = str(self.OVPN_SERVER_INFO[servershort][1])
							serverproto = str(self.OVPN_SERVER_INFO[servershort][2])
							servercipher = str(self.OVPN_SERVER_INFO[servershort][3])
							try:
								servermtu = str(self.OVPN_SERVER_INFO[servershort][4])
							except:
								servermtu = str(1500)
							if cellnumber == 0:
								if self.LOAD_SRVDATA == True and len(self.OVPN_SRV_DATA) >= 1:
									try:
										serverstatus = self.OVPN_SRV_DATA[servershort]["status"]
										if server == self.OVPN_CONNECTEDto:
											statusimg = self.decode_icon("shield_go")
										elif server == self.OVPN_FAV_SERVER:
											statusimg = self.decode_icon("star")
										elif serverstatus == "0":
											statusimg = self.decode_icon("bullet_red")
										elif serverstatus == "1":
											statusimg = self.decode_icon("bullet_green")
										elif serverstatus == "2":
											statusimg = self.decode_icon("bullet_white")
									except:
										self.debug(1,"def update_mwls: self.OVPN_SRV_DATA[%s]['status'] not found" % (servershort))
										break
								else:
									if server == self.OVPN_CONNECTEDto:
										statusimg = self.decode_icon("shield_go")
									elif server == self.OVPN_FAV_SERVER:
										statusimg = self.decode_icon("star")
									else:
										statusimg = self.decode_icon("bullet_white")
								try:
									liststore.set_value(iter,cellnumber,statusimg)
									row_changed += 1
								except:
									self.debug(1,"self.serverliststore.append: statusimg '%s'" % (server))
								
							elif cellnumber == 1:
								pass
							
							elif cellnumber == 2:
								pass
							
							elif cellnumber == 3 and not row[cellnumber] == serverip4:
								liststore.set_value(iter,cellnumber,serverip4)
								row_changed += 1
								if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' serverip4" % (server))
							
							elif cellnumber == 5 and not row[cellnumber] == serverport:
								liststore.set_value(iter,cellnumber,serverport)
								row_changed += 1
								if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' serverport" % (server))
							
							elif cellnumber == 6 and not row[cellnumber] == serverproto:
								liststore.set_value(iter,cellnumber,serverproto)
								row_changed += 1
								if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' serverproto" % (server))
							
							elif cellnumber == 7 and not row[cellnumber] == servermtu:
								liststore.set_value(iter,cellnumber,servermtu)
								row_changed += 1
								if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' servermtu" % (server))
							
							elif cellnumber == 8 and not row[cellnumber] == servercipher:
								liststore.set_value(iter,cellnumber,servercipher)
								row_changed += 1
								if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' servercipher" % (server))
							elif cellnumber == 25:
								pass
							elif cellnumber == 26:
								pass
							elif self.LOAD_SRVDATA == True and len(self.OVPN_SRV_DATA) >= 1:
								try:
									vlanip4 = str(self.OVPN_SRV_DATA[servershort]["vlanip4"])
									vlanip6 = str(self.OVPN_SRV_DATA[servershort]["vlanip6"])
									live = str(self.OVPN_SRV_DATA[servershort]["traffic"]["live"])
									uplink = str(self.OVPN_SRV_DATA[servershort]["traffic"]["uplink"])
									cpuinfo = str(self.OVPN_SRV_DATA[servershort]["info"]["cpu"])
									raminfo = str(self.OVPN_SRV_DATA[servershort]["info"]["ram"])
									hddinfo = str(self.OVPN_SRV_DATA[servershort]["info"]["hdd"])
									traffic = str(self.OVPN_SRV_DATA[servershort]["traffic"]["eth0"])
									cpuload = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-load"])
									cpuovpn = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-ovpn"])
									cpusshd = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-sshd"])
									cpusock = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-sock"])
									cpuhttp = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-http"])
									cputinc = str(self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-tinc"])
									ping4 = str(self.OVPN_SRV_DATA[servershort]["pings"]["ipv4"])
									ping6 = str(self.OVPN_SRV_DATA[servershort]["pings"]["ipv6"])
									serverip6 = str(self.OVPN_SRV_DATA[servershort]["extip6"])
									
									if cellnumber == 4 and not row[cellnumber] == serverip6:
										liststore.set_value(iter,cellnumber,serverip6)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' serverip6" % (server))
										
									elif cellnumber == 9 and not row[cellnumber] == live:
										liststore.set_value(iter,cellnumber,live)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' live" % (server))
									
									elif cellnumber == 10 and not row[cellnumber] == uplink:
										liststore.set_value(iter,cellnumber,uplink)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' uplink" % (server))
									
									elif cellnumber == 11 and not row[cellnumber] == vlanip4:
										liststore.set_value(iter,cellnumber,vlanip4)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' vlanip4" % (server))
									
									elif cellnumber == 12 and not row[cellnumber] == vlanip6:
										liststore.set_value(iter,cellnumber,vlanip6)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' vlanip6" % (server))
									
									elif cellnumber == 13 and not row[cellnumber] == cpuinfo:
										liststore.set_value(iter,cellnumber,cpuinfo)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpuinfo" % (server))
									
									elif cellnumber == 14 and not row[cellnumber] == raminfo:
										liststore.set_value(iter,cellnumber,raminfo)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' raminfo" % (server))
									
									elif cellnumber == 15 and not row[cellnumber] == hddinfo:
										liststore.set_value(iter,cellnumber,hddinfo)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' hddinfo" % (server))
									
									elif cellnumber == 16 and not row[cellnumber] == traffic:
										liststore.set_value(iter,cellnumber,traffic)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' traffic" % (server))
									
									elif cellnumber == 17 and not row[cellnumber] == cpuload:
										liststore.set_value(iter,cellnumber,cpuload)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpuload" % (server))
									
									elif cellnumber == 18 and not row[cellnumber] == cpuovpn:
										liststore.set_value(iter,cellnumber,cpuovpn)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpuovpn" % (server))
									
									elif cellnumber == 19 and not row[cellnumber] == cpusshd:
										liststore.set_value(iter,cellnumber,cpusshd)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpusshd" % (server))
									
									elif cellnumber == 20 and not row[cellnumber] == cpusock:
										liststore.set_value(iter,cellnumber,cpusock)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpusock" % (server))
									
									elif cellnumber == 21 and not row[cellnumber] == cpuhttp:
										liststore.set_value(iter,cellnumber,cpuhttp)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cpuhttp" % (server))
									
									elif cellnumber == 22 and not row[cellnumber] == cputinc:
										liststore.set_value(iter,cellnumber,cputinc)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' cputinc" % (server))
									
									elif cellnumber == 23 and not row[cellnumber] == ping4:
										liststore.set_value(iter,cellnumber,ping4)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' ping4" % (server))
									
									elif cellnumber == 24 and not row[cellnumber] == ping6:
										liststore.set_value(iter,cellnumber,ping6)
										row_changed += 1
										if debugupdate_mwls: self.debug(1,"def update_mwls: updated server '%s' ping6" % (server))
								
								except:
									pass
									# we may fail silently for private servers
									#self.debug(11,"def update_mwls: extended values '%s' failed" % (server))
						except:
							self.debug(1,"def update_mwls: #0 failed ")
						cellnumber += 1
						# end while cellnumber
					if row_changed >= 1:
						path = liststore.get_path(iter)
						liststore.row_changed(path,iter)
						self.debug(10,"def update_mwls: row_changed server '%s'" % (server))
		self.debug(1,"def update_mwls: return %s ms" % (int((time.time()-t1)*1000)))
		return

	def call_redraw_mainwindow(self):
		self.debug(1,"def call_redraw_mainwindow()")
		if self.MAINWINDOW_OPEN == True and self.MAINWINDOW_HIDE == False:
			self.statusbartext_from_before = False
			try:
				GLib.idle_add(self.update_mwls)
			except:
				self.debug(1,"def call_redraw_mainwindow: try #1 failed")

	def show_mainwindow(self,widget,event):
		self.debug(1,"def show_mainwindow()")
		self.destroy_systray_menu()
		self.reset_load_remote_timer()
		self.statusbartext_from_before = False
		if self.MAINWINDOW_OPEN == False:
			self.load_ovpn_server()
			try:
				self.mainwindow = Gtk.Window(Gtk.WindowType.TOPLEVEL)
				self.mainwindow.set_position(Gtk.WindowPosition.CENTER)
				self.mainwindow.connect("destroy",self.cb_destroy_mainwindow)
				self.mainwindow.connect("key-release-event",self.cb_reset_load_remote_timer)
				self.mainwindow.set_title(_("oVPN Server - %s") % (CLIENT_STRING))
				try:
					self.mainwindow.set_icon_from_pixbuf(self.app_icon)
				except:
					pass
				self.mainwindow_ovpn_server()
				self.mainwindow.show_all()
				self.MAINWINDOW_OPEN = True
				return True
			except:
				self.MAINWINDOW_OPEN = False
				self.debug(1,"def show_mainwindow: mainwindow failed")
				return False
		else:
			self.destroy_mainwindow()

	def cell_sort(self, treemodel, iter1, iter2, user_data):
		try:
			self.debug(1,"def cell_sort()")
			sort_column, _ = treemodel.get_sort_column_id()
			iter1 = treemodel.get_value(iter1, sort_column)
			iter2 = treemodel.get_value(iter2, sort_column)
			if float(iter1) < float(iter2):
				return -1
			elif float(iter1) == float(iter2):
				return 0
			else:
				return 1
		except:
			pass

	def cell_sort_traffic(self, treemodel, iter1, iter2, user_data):
		try:
			self.debug(1,"def cell_sort_traffic()")
			sort_column, _ = treemodel.get_sort_column_id()
			data1 = treemodel.get_value(iter1, sort_column)
			data2 = treemodel.get_value(iter2, sort_column)
			if data1 == "-1":
				data1 = "0 GB"
			if data2 == "-1":
				data2 = "0 GB"
			
			iter1 = data1.split(" ")
			number1 = float(iter1[0])
			byte1 = iter1[1]
			if byte1 == "TiB":
				number1 = number1 * 1024
			
			iter2 = data2.split(" ")
			number2 = float(iter2[0])
			byte2 = iter2[1]
			if byte2 == "TiB":
				number2 = number2 * 1024
			
			if float(number1) < float(number2):
				return -1
			elif float(number1) == float(number2):
				return 0
			else:
				return 1
		except:
			pass

	def mainwindow_ovpn_server(self):
		self.debug(1,"def mainwindow_ovpn_server: go")
		self.mainwindow_vbox = Gtk.VBox(False,1)
		self.mainwindow.add(self.mainwindow_vbox)
		
		if self.OVPN_CONFIGVERSION == "23x":
			mode = "IPv4"
		elif self.OVPN_CONFIGVERSION == "23x46":
			mode = "IPv4 + IPv6"
		elif self.OVPN_CONFIGVERSION == "23x64":
			mode = "IPv6 + IPv4"
		self.debug(1,"def mainwindow_ovpn_server: go0")
		label = Gtk.Label(_("oVPN Server [ %s ]") % (mode))
		
		self.debug(1,"def mainwindow_ovpn_server: go1")
		try:
			self.serverliststore = Gtk.ListStore(GdkPixbuf.Pixbuf,GdkPixbuf.Pixbuf,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,GdkPixbuf.Pixbuf)
			self.debug(1,"def mainwindow_ovpn_server: go2")
		except:
			self.debug(1,"def mainwindow_ovpn_server: server-window failed")
		
		self.debug(1,"def mainwindow_ovpn_server: go3")
		self.treeview = Gtk.TreeView(self.serverliststore)
		self.treeview.connect("button-release-event",self.on_right_click_mainwindow)
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.scrolledwindow.set_size_request(64,48)
		self.debug(1,"def mainwindow_ovpn_server: go4")
		self.scrolledwindow.add(self.treeview)
		self.mainwindow_vbox.pack_start(self.scrolledwindow,True,True,0)
		
		try:
			self.debug(1,"def fill_mainwindow_with_server: go2.1")
			cell = Gtk.CellRendererPixbuf()
			column = Gtk.TreeViewColumn(' ',cell, pixbuf=0)
			self.treeview.append_column(column)
			self.debug(1,"def fill_mainwindow_with_server: go2.2")
			cell = Gtk.CellRendererPixbuf()
			column = Gtk.TreeViewColumn(' ',cell, pixbuf=1)
			column.set_fixed_width(30)
			self.treeview.append_column(column)
			self.debug(1,"def fill_mainwindow_with_server: go2.3")
		except:
			self.debug(1,"cell = Gtk.CellRendererPixbuf failed")
		
		## cell 0 == statusicon
		## cell 1 == flagicon
		cellnumber = 2 #	2		3			4		5			6		7			8			9		10			11				12				13			14		15			16		17			18			19			20			21			22			23			24			25
		cellnames = [ " Server ", " IPv4 ", " IPv6 ", " Port ", " Proto ", " MTU ", " Cipher ", " Mbps ", " Link ", " VLAN IPv4 ", " VLAN IPv6 ", " Processor ", " RAM ", " HDD ", " Traffic ", " Load ", " oVPN % ", " oSSH % ", " SOCK % ", " HTTP % ", " TINC % ", " PING4 ", " PING6 ", " Short " ]
		for cellname in cellnames:
			align=0.5
			if cellnumber in [ 9, 23, 24 ]:
				align=1
			if cellnumber in [ 3, 4, 11, 12, 13, 16 ]:
				align=0
			cell = Gtk.CellRendererText(xalign=align)
			column = Gtk.TreeViewColumn(cellname, cell, text=cellnumber)
			
			if self.ENABLE_MAINWINDOW_SORTING == True:
				if cellnumber in [ 2, 5, 6, 7, 9, 10, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 ]:
					column.set_sort_column_id(cellnumber)
					# Add sort function for str cells
					if not cellnumber in [ 2, 6, 16, 25 ]: # sortable but text str, cannot convert to float, 16: Traffic needs own sort_func
						self.serverliststore.set_sort_func(cellnumber, self.cell_sort, None)
					if cellnumber in [ 16 ]:
						self.serverliststore.set_sort_func(cellnumber, self.cell_sort_traffic, None)
			# Hide colums in light server view
			if self.LOAD_SRVDATA == False:
				if cellnumber in [ 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 ]:
					column.set_visible(False)
			self.treeview.append_column(column)
			cellnumber = cellnumber + 1
		
		cell = Gtk.CellRendererPixbuf()
		column = Gtk.TreeViewColumn(' ',cell, pixbuf=26)
		column.set_fixed_width(30)
		if self.LOAD_SRVDATA == False:
			column.set_visible(False)
		self.treeview.append_column(column)
		
		self.debug(1,"def fill_mainwindow_with_server: go2.4")
		GLib.idle_add(self.fill_mainwindow_with_server)
		GLib.idle_add(self.update_mwls)
		self.debug(1,"def fill_mainwindow_with_server: go2.5")
		
		# statusbar
		self.statusbar_text = Gtk.Label()
		self.mainwindow_vbox.pack_start(self.statusbar_text,False,False,0)
		self.mainwindow_vbox.show_all()
		self.debug(1,"def fill_mainwindow_with_server: go2.6")
		
		if self.LOAD_SRVDATA == True:
			WIDTH = self.SRV_WIDTH
			HEIGHT = self.SRV_HEIGHT
			self.mainwindow.resize(int(WIDTH),int(HEIGHT))
		else:
			WIDTH = self.SRV_LIGHT_WIDTH
			HEIGHT = self.SRV_LIGHT_HEIGHT
			self.mainwindow.resize(int(WIDTH),int(HEIGHT))
		return

	def fill_mainwindow_with_server(self):
		for server in self.OVPN_SERVER:
			try:
				countrycode = server[:2].lower()
				servershort = server[:3].upper()
				statusimg = self.decode_icon("bullet_white")
				countryimg = self.decode_flag(countrycode)
				serverip4  = self.OVPN_SERVER_INFO[servershort][0]
				serverport = self.OVPN_SERVER_INFO[servershort][1]
				serverproto = self.OVPN_SERVER_INFO[servershort][2]
				servercipher = self.OVPN_SERVER_INFO[servershort][3]
				try:
					servermtu = self.OVPN_SERVER_INFO[servershort][4]
				except:
					servermtu = 1500
				self.serverliststore.append([statusimg,countryimg,str(server),str(serverip4),str("-1"),str(serverport),str(serverproto),str(servermtu),str(servercipher),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str("-1"),str(servershort),countryimg])
			except:
				self.debug(1,"def fill_mainwindow_with_server: server '%s' failed" % (server))

	def destroy_mainwindow(self):
		self.debug(1,"def destroy_mainwindow()")
		GLib.idle_add(self.mainwindow.destroy)
		#self.mainwindow.destroy()
		self.MAINWINDOW_OPEN = False
		self.MAINWINDOW_HIDE = False
		self.statusbar_text = False
		self.debug(1,"def destroy_mainwindow")

	def call_redraw_accwindow(self):
		self.debug(1,"def call_redraw_accwindow()")
		if self.ACCWINDOW_OPEN == True:
			try:
				self.accwindow.remove(self.accwindow_accinfo_vbox)
				self.accwindow_accinfo()
				self.debug(1,"def call_redraw_accwindow: True")
			except:
				self.debug(1,"def call_redraw_accwindow: False")

	def show_accwindow(self,widget,event):
		self.debug(1,"def show_accwindow()")
		self.destroy_systray_menu()
		if self.ACCWINDOW_OPEN == False:
			try:
				self.accwindow = Gtk.Window(Gtk.WindowType.TOPLEVEL)
				self.accwindow.set_position(Gtk.WindowPosition.CENTER)
				self.accwindow.connect("destroy",self.cb_destroy_accwindow)
				self.accwindow.connect("key-release-event",self.cb_reset_load_remote_timer)
				self.accwindow.set_title(_("oVPN Account - %s") % (CLIENT_STRING))
				try:
					self.accwindow.set_icon_from_pixbuf(self.app_icon)
				except:
					pass
				self.accwindow.set_default_size(370,480)
				self.accwindow_accinfo()
				self.ACCWINDOW_OPEN = True
				self.reset_load_remote_timer()
				return True
			except:
				self.ACCWINDOW_OPEN = False
				self.debug(1,"def show_accwindow: accwindow failed")
				return False
		else:
			self.destroy_accwindow()

	def accwindow_accinfo(self):
		self.debug(1,"def accwindow_accinfo()")
		self.accwindow_accinfo_vbox = Gtk.VBox(False,0)
		self.accwindow.add(self.accwindow_accinfo_vbox)
		if len(self.OVPN_ACC_DATA) == 0:
			if self.LOAD_ACCDATA == False:
				text = _("Settings -> Updates: 'Load Account Info' [disabled]")
			else:
				text = _("No data loaded! Retry in few seconds...")
			entry = Gtk.Entry()
			entry.set_max_length(64)
			entry.set_editable(0)
			entry.set_text(text)
			self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
		elif len(self.OVPN_ACC_DATA) > 0:
			try:
				self.debug(10,"def accwindow_accinfo: try get values")
				for key, value in sorted(self.OVPN_ACC_DATA.iteritems()):
					#print key
					value1 = False
					if key == "001":
						head = "User-ID"
					elif key == "002":
						head = "Service"
						if int(value) == ((2**31)-1):
							value1 = "Lifetime"
						else:
							value1 = datetime.fromtimestamp(int(value)).strftime('%d %b %Y %H:%M:%S UTC+1')
					elif key == "003":
						head = "Balance EUR"
						value1 = round(int(value),0) / 100
					elif key == "004":
						head = "Saved Days"
					elif key == "005":
						head = "Last Login"
						value1 = datetime.fromtimestamp(int(value)).strftime('%d %b %Y %H:%M:%S UTC+1')
					elif key == "006":
						head = "Login Count"
					elif key == "007":
						head = "Login Fail Count"
					elif key == "008":
						head = "Last Failed Login"
						value1 = datetime.fromtimestamp(int(value)).strftime('%d %b %Y %H:%M:%S UTC+1')
					elif key == "009":
						head = "eMail verified"
					elif key == "010":
						head = "Last eMail sent"
					elif key == "020":
						head = "Last Update Request"
						value1 = datetime.fromtimestamp(int(value)).strftime('%d %b %Y %H:%M:%S UTC+1')
					elif key == "022":
						head = "API Counter WIN"
					elif key == "021":
						head = "API Counter LIN"
					elif key == "023":
						head = "API Counter MAC"
					elif key == "024":
						head = "API Counter AND"
					elif key == "030":
						head = "IPv6 enabled"
					elif key == "999":
						for coin,addr in sorted(value.iteritems()):
							try:
								text = "%s: '%s'" % (coin.upper(),addr)
								#print text
								entry = Gtk.Entry()
								entry.set_max_length(128)
								entry.set_editable(0)
								entry.set_text(text)
								self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
							except:
								self.debug(1,"def accwindow_accinfo: coin '%s' failed" % (coin))
						break
					else:
						head = key
					if value1 == False:
						value1 = value
					text = "%s: %s" % (head,value1)
					self.debug(10,"def accwindow_accinfo: key [%s] = '%s' value = '%s'" % (key,head,value))
					try:
						entry = Gtk.Entry()
						entry.set_max_length(128)
						entry.set_editable(0)
						entry.set_text(text)
						self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
					except:
						self.debug(1,"def accwindow_accinfo: accdata vbox.pack_start entry failed!")
			except:
				self.debug(1,"def accwindow_accinfo: self.OVPN_ACC_DATA failed")
		self.accwindow.show_all()
		return

	def destroy_accwindow(self):
		self.debug(1,"def destroy_accwindow()")
		GLib.idle_add(self.accwindow.destroy)
		self.ACCWINDOW_OPEN = False
		self.debug(1,"def destroy_accwindow")

	def show_settingswindow(self,widget,event):
		self.destroy_systray_menu()
		if self.SETTINGSWINDOW_OPEN == False:
			try:
				self.settingswindow = Gtk.Window(Gtk.WindowType.TOPLEVEL)
				self.settingswindow.set_position(Gtk.WindowPosition.CENTER)
				self.settingswindow.connect("destroy",self.cb_destroy_settingswindow)
				self.settingswindow.set_title(_("oVPN Settings - %s") % (CLIENT_STRING))
				try:
					self.settingswindow.set_icon_from_pixbuf(self.app_icon)
				except:
					pass
				self.settingsnotebook = Gtk.Notebook()
				self.settingswindow.add(self.settingsnotebook)
				
				self.show_hide_security_window()
				self.show_hide_options_window()
				self.show_hide_updates_window()
				
				self.UPDATE_SWITCH = True
				self.settingswindow.show_all()
				self.SETTINGSWINDOW_OPEN = True
				return True
			except:
				self.SETTINGSWINDOW_OPEN = False
				self.debug(1,"def show_settingswindow: settingswindow failed")
				return False
		else:
			self.destroy_settingswindow()

	def show_hide_security_window(self):
		try:
			self.nbpage0 = Gtk.VBox(False,spacing=2)
			self.nbpage0.set_border_width(8)
			self.nbpage0.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_firewall_switch_nofw(self.nbpage0)
			self.settings_firewall_switch_fwblockonexit(self.nbpage0)
			self.settings_firewall_switch_fwdontaskonexit(self.nbpage0)
			self.settings_firewall_switch_tapblockoutbound(self.nbpage0)
			self.settings_firewall_switch_fwresetonconnect(self.nbpage0)
			self.settings_firewall_switch_fwbackupmode(self.nbpage0)
			self.settings_network_switch_nodns(self.nbpage0)
			self.settings_network_switch_disableextifondisco(self.nbpage0)
			self.settingsnotebook.append_page(self.nbpage0, Gtk.Label(_(" Security ")))
		except:
			self.debug(1,"def show_settingswindow: nbpage0 failed")

	def show_hide_options_window(self):
		try:
			self.nbpage1 = Gtk.VBox(False,spacing=2)
			self.nbpage1.set_border_width(8)
			self.nbpage1.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_options_switch_updateovpnonstart(self.nbpage1)
			self.settings_options_switch_accinfo(self.nbpage1)
			self.settings_options_switch_srvinfo(self.nbpage1)
			self.settings_options_switch_disablequit(self.nbpage1)
			self.settings_options_switch_debugmode(self.nbpage1)

			##
			self.nbpage1_h1 = Gtk.HBox(False, spacing=2)
			self.nbpage1_h1.pack_start(Gtk.Label(label=""),False,False,0)

			self.nbpage1_h1_v1 = Gtk.VBox(False, spacing=0)
			self.nbpage1_h1_v1.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_options_combobox_theme(self.nbpage1_h1_v1)
			
			self.nbpage1_h1_v2 = Gtk.VBox(False, spacing=0)
			self.nbpage1_h1_v2.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_options_combobox_icons(self.nbpage1_h1_v2)

			self.nbpage1_h1.add(self.nbpage1_h1_v1)
			self.nbpage1_h1.add(self.nbpage1_h1_v2)
			self.nbpage1.add(self.nbpage1_h1)
			##

			##
			self.nbpage1_h2 = Gtk.HBox(False, spacing=2)
			self.nbpage1_h2.pack_start(Gtk.Label(label=""),False,False,0)

			self.nbpage1_h2_v1 = Gtk.VBox(False, spacing=0)
			self.nbpage1_h2_v1.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_options_combobox_fontsize(self.nbpage1_h2_v1)
			
			self.nbpage1_h2_v2 = Gtk.VBox(False, spacing=0)
			self.nbpage1_h2_v2.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_options_combobox_language(self.nbpage1_h2_v2)

			self.nbpage1_h2.add(self.nbpage1_h2_v1)
			self.nbpage1_h2.add(self.nbpage1_h2_v2)
			self.nbpage1.add(self.nbpage1_h2)
			##

			self.settingsnotebook.append_page(self.nbpage1, Gtk.Label(_(" Options ")))
		except:
			self.debug(1,"def show_settingswindow: nbpage1 failed")

	def show_hide_updates_window(self):
		try:
			self.nbpage2 = Gtk.VBox(False,spacing=2)
			self.nbpage2.set_border_width(8)
			self.nbpage2.pack_start(Gtk.Label(label=""),False,False,0)
			self.settings_updates_button_normalconf(self.nbpage2)
			self.settings_updates_button_forceconf(self.nbpage2)
			self.settings_options_button_ipv6(self.nbpage2)
			self.settings_options_button_networkadapter(self.nbpage2)
			self.settings_updates_button_apireset(self.nbpage2)
			self.settingsnotebook.append_page(self.nbpage2, Gtk.Label(_(" Updates ")))
		except:
			self.debug(1,"def show_settingswindow: nbpage2 failed")

	def show_hide_backup_window(self):
		try:
			self.load_firewall_backups()
			if len(self.FIREWALL_BACKUPS) > 0 and self.NO_WIN_FIREWALL == False and self.state_openvpn() == False:
				self.nbpage3 = Gtk.VBox(False,spacing=2)
				self.nbpage3.set_border_width(8)
				self.nbpage3.pack_start(Gtk.Label(label=_("Restore Firewall Backups\n")),False,False,0)
				self.settings_firewall_switch_backuprestore(self.nbpage3)
				self.settingsnotebook.append_page(self.nbpage3, Gtk.Label(_(" Backups ")))
		except:
			self.debug(1,"def show_hide_backup_window: nbpage3 failed")

	def settings_firewall_switch_nofw(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_fw = switch
			checkbox_title = Gtk.Label(label=_("Use Windows Firewall (default: ON) "))
			if self.NO_WIN_FIREWALL == True:
				switch.set_active(False)
			else:
				switch.set_active(True)
			switch.connect("notify::state", self.cb_settings_firewall_switch_nofw)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_nofw: failed")

	def cb_settings_firewall_switch_nofw(self,switch,gparam):
		if self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_nofw()")
		if switch.get_active():
			self.NO_WIN_FIREWALL = False
			self.WIN_DONT_ASK_FW_EXIT = True
		else:
			self.NO_WIN_FIREWALL = True
		self.write_options_file()
		self.ask_loadorunload_fw()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_tapblockoutbound(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_tapblockoutbound = switch
			checkbox_title = Gtk.Label(label=_("TAP-Adapter block outbound (default: OFF)"))
			if self.TAP_BLOCKOUTBOUND == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_firewall_switch_tapblockoutbound)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_tapblockoutbound: failed")

	def cb_settings_firewall_switch_tapblockoutbound(self,switch,gparam):
		if self.NO_WIN_FIREWALL == True or self.inThread_jump_server_running == True or self.win_firewall_tap_blockoutbound_running == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_tapblockoutbound()")
		if switch.get_active():
			self.TAP_BLOCKOUTBOUND = True
		else:
			self.TAP_BLOCKOUTBOUND = False
		thread = threading.Thread(target=self.win_firewall_tap_blockoutbound)
		thread.daemon = True
		thread.start()
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_fwblockonexit(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_fwblockonexit = switch
			checkbox_title = Gtk.Label(label=_("Block Internet on Disconnect or Quit (default: ON)"))
			if self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_firewall_switch_fwblockonexit)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_fwblockonexit: failed")

	def cb_settings_firewall_switch_fwblockonexit(self,switch,gparam):
		if self.NO_WIN_FIREWALL == True or self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_fwblockonexit()")
		if switch.get_active():
			self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = True
		else:
			self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = False
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_fwdontaskonexit(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_fwdontaskonexit = switch
			checkbox_title = Gtk.Label(label=_("Disable FW question on Quit (default: OFF)"))
			if self.WIN_DONT_ASK_FW_EXIT == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_firewall_switch_fwdontaskonexit)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_fwblockonexit: failed")

	def cb_settings_firewall_switch_fwdontaskonexit(self,switch,gparam):
		if self.NO_WIN_FIREWALL == True or self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_fwdontaskonexit()")
		if switch.get_active():
			self.WIN_DONT_ASK_FW_EXIT = True
		else:
			self.WIN_DONT_ASK_FW_EXIT = False
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_fwresetonconnect(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_fwresetonconnect = switch
			checkbox_title = Gtk.Label(label=_("Clear Rules on Connect (default: OFF)"))
			if self.WIN_RESET_FIREWALL == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_firewall_switch_fwresetonconnect)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_fwresetonconnect: failed")

	def cb_settings_firewall_switch_fwresetonconnect(self,switch,gparam):
		if self.NO_WIN_FIREWALL == True or self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_fwresetonconnect()")
		if switch.get_active():
			self.WIN_RESET_FIREWALL = True
			if not self.win_firewall_export_on_start():
				self.msgwarn(_("Could not export Windows Firewall Backup!"),_("Error: Windows Firewall Backup failed"))
		else:
			self.WIN_RESET_FIREWALL = False
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_fwbackupmode(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_fwbackupmode = switch
			checkbox_title = Gtk.Label(label=_("Backup on Start / Restore on Quit (default: OFF)"))
			if self.WIN_BACKUP_FIREWALL == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_firewall_switch_fwbackupmode)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_firewall_switch_fwbackupmode: failed")

	def cb_settings_firewall_switch_fwbackupmode(self,switch,gparam):
		if self.NO_WIN_FIREWALL == True or self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_settings_firewall_switch_fwbackupmode()")
		if switch.get_active():
			self.WIN_BACKUP_FIREWALL = True
			if not self.win_firewall_export_on_start():
				self.msgwarn(_("Could not export Windows Firewall Backup!"),_("Error: Windows Firewall Backup failed"))
		else:
			self.WIN_BACKUP_FIREWALL = False
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_network_switch_nodns(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_nodns = switch
			checkbox_title = Gtk.Label(label=_("DNS Leak Protection (default: ON)"))
			if self.NO_DNS_CHANGE == True:
				switch.set_active(False)
			else:
				switch.set_active(True)
			switch.connect("notify::state", self.cb_switch_nodns)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_network_switch_nodns: failed")

	def cb_switch_nodns(self,switch,gparam):
		if self.state_openvpn() == True:
			self.UPDATE_SWITCH = True
			return
		self.debug(1,"def cb_switch_nodns()")
		if switch.get_active():
			self.NO_DNS_CHANGE = False
			self.read_d0wns_dns()
		else:
			self.NO_DNS_CHANGE = True
			self.win_netsh_restore_dns_from_backup()
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_network_switch_disableextifondisco(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_disableextifondisco = switch
			checkbox_title = Gtk.Label(label=_("Disable '%s' on Disconnect (default: OFF)")%(self.WIN_EXT_DEVICE))
			if self.WIN_DISABLE_EXT_IF_ON_DISCO == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_network_switch_disableextifondisco)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_network_switch_disableextifondisco: failed")

	def cb_settings_network_switch_disableextifondisco(self,switch,gparam):
		self.debug(1,"def cb_settings_network_switch_disableextifondisco()")
		if switch.get_active():
			self.WIN_DISABLE_EXT_IF_ON_DISCO = True
			if self.state_openvpn() == False:
				self.win_disable_ext_interface()
		else:
			self.WIN_DISABLE_EXT_IF_ON_DISCO = False
			if self.state_openvpn() == False:
				self.win_enable_ext_interface()
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_firewall_switch_backuprestore(self, page):
		for file in self.FIREWALL_BACKUPS:
			button = Gtk.Button(label=("%s")%(file))
			button.connect('clicked', self.cb_settings_firewall_switch_backuprestore, file)
			page.pack_start(button,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)

	def cb_settings_firewall_switch_backuprestore(self, file):
		GLib.idle_add(self.cb_restore_firewallbackup, file)

	def settings_options_switch_updateovpnonstart(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_updateovpnonstart = switch
			checkbox_title = Gtk.Label(label=_("Update Configs on Start (default: OFF)"))
			if self.UPDATEOVPNONSTART == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_switch_updateovpnonstart)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_switch_updateovpnonstart: failed")

	def cb_switch_updateovpnonstart(self,switch,gparam):
		self.debug(1,"def cb_switch_updateovpnonstart()")
		if switch.get_active():
			self.UPDATEOVPNONSTART = True
		else:
			self.UPDATEOVPNONSTART = False
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_options_switch_accinfo(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_accinfo = switch
			checkbox_title = Gtk.Label(label=_("Load Account Info (default: OFF)"))
			if self.LOAD_ACCDATA == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_switch_accinfo)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_switch_accinfo: failed")

	def cb_switch_accinfo(self,switch,gparam):
		self.debug(1,"def cb_switch_accinfo()")
		if switch.get_active():
			self.LOAD_ACCDATA = True
		else:
			self.LOAD_ACCDATA = False
		reopen = False
		if self.ACCWINDOW_OPEN == True:
			reopen = True
		if self.LOAD_ACCDATA == True:
			self.LOAD_ACCDATA = True
			self.LAST_OVPN_ACC_DATA_UPDATE = 0
			self.OVPN_ACC_DATA = {}
		self.write_options_file()
		if reopen == True:
			GLib.idle_add(self.call_redraw_accwindow)
		self.UPDATE_SWITCH = True

	def settings_options_switch_srvinfo(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_srvinfo = switch
			checkbox_title = Gtk.Label(label=_("Load Server Info (default: OFF)"))
			if self.LOAD_SRVDATA == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_switch_srvinfo)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_switch_srvinfo: failed")

	def cb_switch_srvinfo(self,switch,gparam):
		self.debug(1,"def cb_switch_srvinfo()")
		if switch.get_active():
			self.LOAD_SRVDATA = True
		else:
			self.LOAD_SRVDATA = False
		reopen = False
		if self.MAINWINDOW_OPEN == True:
			reopen = True
		if self.LOAD_SRVDATA == True:
			self.LOAD_SRVDATA = True
			self.LAST_OVPN_SRV_DATA_UPDATE = 0
			self.OVPN_SRV_DATA = {}
		self.write_options_file()
		if reopen == True:
			GLib.idle_add(self.mainwindow.remove,self.mainwindow_vbox)
			GLib.idle_add(self.mainwindow_ovpn_server)
		self.UPDATE_SWITCH = True

	def settings_options_switch_debugmode(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_debugmode = switch
			checkbox_title = Gtk.Label(label=_("Debug Mode (default: OFF)"))
			if self.DEBUG == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_switch_debugmode)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_switch_debugmode: failed")

	def cb_switch_debugmode(self,switch,gparam):
		self.debug(1,"def cb_switch_debugmode()")
		if switch.get_active():
			self.msgwarn(_("Logfile:\n'%s'") % (self.debug_log),_("Debug Mode Enabled"))
		else:
			self.DEBUG = False
			if os.path.isfile(self.debug_log):
				os.remove(self.debug_log)
		self.write_options_file()
		self.UPDATE_SWITCH = True

	def settings_options_button_networkadapter(self,page):
		button = Gtk.Button(label=_("Select Network Adapter"))
		self.button_switch_network_adapter = button
		button.connect('clicked', self.cb_settings_options_button_networkadapter)
		page.pack_start(button,False,False,0)
		page.pack_start(Gtk.Label(label=""),False,False,0)
		
	def cb_settings_options_button_networkadapter(self,event):
		GLib.idle_add(self.cb_resetextif)

	def settings_options_button_ipv6(self,page):
		if self.OVPN_CONFIGVERSION == "23x":
			button_title = Gtk.Label(label=_("Current: IPv4 Entry Server with Exit to IPv4 (standard)"))
			button = Gtk.Button(label=_("Use IPv4 Entry Server with Exits to IPv4 + IPv6"))
			button.connect('clicked', self.cb_settings_options_button_ipv6)
		elif self.OVPN_CONFIGVERSION  == "23x46":
			button_title = Gtk.Label(label=_("Current: IPv4 Entry Server with Exits to IPv4 + IPv6"))
			button = Gtk.Button(label=_("Use IPv4 Entry Server with Exit to IPv4 (standard)"))
			button.connect('clicked', self.cb_settings_options_button_ipv6)
		self.button_ipmode = button
		self.button_title = button_title
		page.pack_start(button_title,False,False,0)
		page.pack_start(button,False,False,0)
		page.pack_start(Gtk.Label(label=""),False,False,0)

	def cb_settings_options_button_ipv6(self,event):
		if not self.OVPN_CONFIGVERSION == "23x":
			GLib.idle_add(self.cb_change_ipmode1)
		if not self.OVPN_CONFIGVERSION  == "23x46":
			GLib.idle_add(self.cb_change_ipmode2)
		"""
		 *** fixme need isValueIPv6 first! ***
		if not self.OVPN_CONFIGVERSION == "23x64":
			GLib.idle_add(self.cb_change_ipmode3)
		"""

	def settings_options_combobox_theme(self,page):
		try:
			self.debug(1,"def settings_options_combobox_theme()")
			combobox_title = Gtk.Label(label=_("Change App Theme"))
			combobox = Gtk.ComboBoxText.new()
			for theme in self.INSTALLED_THEMES:
				combobox.append_text(theme)
			if self.APP_THEME == "ms-windows":
				active_item = 0
			if self.APP_THEME == "Adwaita":
				active_item = 1
			if self.APP_THEME == "Adwaita-dark":
				active_item = 2
			if self.APP_THEME == "Greybird":
				active_item = 3
			combobox.set_active(active_item)
			combobox.connect('changed',self.cb_theme_switcher_changed)
			page.pack_start(combobox_title,False,False,0)
			page.pack_start(combobox,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_combobox_theme: failed")

	def cb_theme_switcher_changed(self, combobox):
		self.debug(1,"def cb_theme_switcher_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.APP_THEME = combobox.get_active_text()
			get_settings = Gtk.Settings.get_default()
			get_settings.set_property("gtk-theme-name", self.APP_THEME)
			self.write_options_file()
			self.UPDATE_SWITCH = True
			self.debug(1,"def cb_theme_switcher_changed: selected Theme = '%s'" % (self.APP_THEME))
		return

	def settings_options_combobox_icons(self,page):
		try:
			self.debug(1,"def settings_options_combobox_icons()")
			combobox_title = Gtk.Label(label=_("Change App Icons"))
			combobox = Gtk.ComboBoxText.new()
			self.combobox_icons = combobox
			for icons in self.INSTALLED_ICONS:
				combobox.append_text(icons)
			if self.ICONS_THEME == "standard":
				active_item = 0
			if self.ICONS_THEME == "classic":
				active_item = 1
			if self.ICONS_THEME == "classic2":
				active_item = 2
			if self.ICONS_THEME == "shield_bluesync":
				active_item = 3
			if self.ICONS_THEME == "experimental":
				active_item = 4
			if self.ICONS_THEME == "private":
				active_item = 5
			combobox.set_active(active_item)
			combobox.connect('changed',self.cb_icons_switcher_changed)
			page.pack_start(combobox_title,False,False,0)
			page.pack_start(combobox,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_combobox_icons: failed")

	def cb_icons_switcher_changed(self, combobox):
		self.debug(1,"def cb_icons_switcher_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.ICONS_THEME_frombefore = self.ICONS_THEME
			self.ICONS_THEME = combobox.get_active_text()
			if self.load_icons():
				self.write_options_file()
				self.debug(1,"def cb_icons_switcher_changed: selected Icons = '%s'" % (self.ICONS_THEME))
				self.ICON_CACHE_PIXBUF = {}
			else:
				self.debug(1,"def cb_icons_switcher_changed: failed icon theme = '%s', revert to '%s'" % (self.ICONS_THEME,self.ICONS_THEME_frombefore))
				self.ICONS_THEME = self.ICONS_THEME_frombefore
			self.UPDATE_SWITCH = True
		return

	def settings_options_combobox_fontsize(self,page):
		try:
			self.debug(1,"def settings_options_combobox_fontsize()")
			combobox_title = Gtk.Label(label=_("Change App Font Size"))
			combobox = Gtk.ComboBoxText.new()
			for size in self.APP_FONT_SIZE_AVAIABLE:
				combobox.append_text(size)
			if self.APP_FONT_SIZE == "6":
				active_item = 0
			if self.APP_FONT_SIZE == "7":
				active_item = 1
			if self.APP_FONT_SIZE == "8":
				active_item = 2
			if self.APP_FONT_SIZE == "9":
				active_item = 3
			if self.APP_FONT_SIZE == "10":
				active_item = 4
			if self.APP_FONT_SIZE == "11":
				active_item = 5
			if self.APP_FONT_SIZE == "12":
				active_item = 6
			if self.APP_FONT_SIZE == "13":
				active_item = 7
			combobox.set_active(active_item)
			combobox.connect('changed',self.cb_settings_options_combobox_fontsize)
			page.pack_start(combobox_title,False,False,0)
			page.pack_start(combobox,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_combobox_theme: failed")

	def cb_settings_options_combobox_fontsize(self, combobox):
		self.debug(1,"def cb_settings_options_combobox_fontsize()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.APP_FONT_SIZE = combobox.get_active_text()
			get_settings = Gtk.Settings.get_default()
			get_settings.set_property("gtk-font-name", self.APP_FONT_SIZE)
			self.write_options_file()
			self.UPDATE_SWITCH = True
			self.LANG_FONT_CHANGE = True
			self.debug(1,"def cb_settings_options_combobox_fontsize: selected Size = '%s'" % (self.APP_FONT_SIZE))
		return

	def settings_options_combobox_language(self,page):
		try:
			i=0; 
			self.debug(1,"def settings_options_combobox_theme()")
			combobox_title = Gtk.Label(label=_("Change App Language"))
			combobox = Gtk.ComboBoxText.new()
			for lang in self.INSTALLED_LANGUAGES:
				combobox.append_text(lang)
			if self.APP_LANGUAGE == "en":
				active_item = 0
			if self.APP_LANGUAGE == "de":
				active_item = 1
			if self.APP_LANGUAGE == "es":
				active_item = 2
			if self.APP_LANGUAGE == "nl":
				active_item = 3
			combobox.set_active(active_item)
			combobox.connect('changed',self.cb_settings_options_combobox_language)
			page.pack_start(combobox_title,False,False,0)
			page.pack_start(combobox,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
			self.debug(1,"def settings_options_combobox_language()")
		except:
			self.debug(1,"def settings_options_combobox_language: failed")
			
	def cb_settings_options_combobox_language(self, combobox):
		self.debug(1,"def cb_settings_options_combobox_language()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.APP_LANGUAGE = combobox.get_active_text()
			self.write_options_file()
			self.UPDATE_SWITCH = True
			self.LANG_FONT_CHANGE = True
			if self.init_localization(self.APP_LANGUAGE) == True:
				self.debug(1,"def cb_settings_options_combobox_language: selected lang = '%s'" % (self.APP_LANGUAGE))
		return

	def settings_options_switch_disablequit(self,page):
		try:
			switch = Gtk.Switch()
			self.switch_disablequit = switch
			checkbox_title = Gtk.Label(label=_("Disable About and Quit on Connection (default: ON)"))
			if self.DISABLE_QUIT_ENTRY == True:
				switch.set_active(True)
			else:
				switch.set_active(False)
			switch.connect("notify::state", self.cb_settings_options_switch_disablequit)
			page.pack_start(checkbox_title,False,False,0)
			page.pack_start(switch,False,False,0)
			page.pack_start(Gtk.Label(label=""),False,False,0)
		except:
			self.debug(1,"def settings_options_switch_disablequit: failed")

	def cb_settings_options_switch_disablequit(self,switch,gparam ):
		self.debug(1,"def cb_settings_options_switch_disablequit()")
		if switch.get_active():
			self.DISABLE_QUIT_ENTRY = True
		else:
			self.DISABLE_QUIT_ENTRY = False
		self.write_options_file()

	def settings_updates_button_normalconf(self,page):
		button = Gtk.Button(label=_("Normal Config Update"))
		button.connect('clicked', self.cb_settings_updates_button_normalconf)
		page.pack_start(button,False,False,0)
		page.pack_start(Gtk.Label(label=""),False,False,0)

	def cb_settings_updates_button_normalconf(self,event):
		self.cb_check_normal_update()

	def settings_updates_button_forceconf(self,page):
		button = Gtk.Button(label=_("Forced Config Update"))
		button.connect('clicked', self.cb_settings_updates_button_forceconf)
		page.pack_start(button,False,False,0)
		page.pack_start(Gtk.Label(label=""),False,False,0)

	def cb_settings_updates_button_forceconf(self,event):
		GLib.idle_add(self.cb_force_update)

	def settings_updates_button_apireset(self,page):
		button = Gtk.Button(label=_("Reset API-Login"))
		button.connect('clicked', self.cb_settings_updates_button_apireset)
		page.pack_start(button,False,False,0)
		page.pack_start(Gtk.Label(label=""),False,False,0)
		
	def cb_settings_updates_button_apireset(self,event):
		GLib.idle_add(self.dialog_apikey)

	def destroy_settingswindow(self):
		self.debug(1,"def destroy_settingswindow()")
		GLib.idle_add(self.settingswindow.destroy)
		self.SETTINGSWINDOW_OPEN = False
		self.debug(1,"def destroy_settingswindow")

	def cb_destroy_settingswindow(self,event):
		self.debug(1,"def cb_destroy_settingswindow")
		self.SETTINGSWINDOW_OPEN = False

	def cb_destroy_mainwindow(self,event):
		self.debug(1,"def cb_destroy_mainwindow")
		self.MAINWINDOW_OPEN = False
		self.MAINWINDOW_HIDE = False

	def cb_destroy_accwindow(self,event):
		self.debug(1,"def cb_destroy_accwindow")
		self.ACCWINDOW_OPEN = False

	def cb_del_dns(self,widget,event,data):
		if event.button == 1:
			self.debug(1,"def cb_del_dns()")
			self.destroy_context_menu_servertab()
			print "def cb_del_dns: cbdata = '%s'" % (data)
			for name,value in data.iteritems():
				try:
					if value["primary"]["ip4"] == self.MYDNS[name]["primary"]["ip4"]:
						try:
							if self.isValueIPv4(self.MYDNS[name]["secondary"]["ip4"]):
								self.MYDNS[name]["primary"] = self.MYDNS[name]["secondary"]
								self.MYDNS[name]["secondary"] = {}
						except:
							self.MYDNS[name]["primary"] = {}
				except:
					pass
				
				try:
					if value["secondary"]["ip4"] == self.MYDNS[name]["secondary"]["ip4"]:
						self.MYDNS[name]["secondary"] = {}
				except:
					pass
			self.write_options_file()
			if self.OVPN_CONNECTEDto == name:
				self.debug(1,"def cb_set_dns: self.OVPN_CONNECTEDto = %s , name = %s" % (self.OVPN_CONNECTEDto,name))
				self.win_netsh_set_dns_ovpn()
			return True

	def cb_set_dns(self,widget,event,data):
		if event.button == 1:
			self.debug(1,"def cb_set_dns()")
			self.destroy_context_menu_servertab()
			for name,value in data.iteritems():
				self.debug(1,"def cb_set_dns: name '%s' value: '%s'" % (name,value))
				try:
					newpridns = value["primary"]["ip4"]
					if self.isValueIPv4(newpridns):
						print " set primary dns"
						try:
							print 'try: if newpridns == self.MYDNS[name]["secondary"]["ip4"]'
							if newpridns == self.MYDNS[name]["secondary"]["ip4"]:
								self.MYDNS[name]["secondary"] = {}
								self.debug('self.MYDNS[name]["secondary"] = {}')
						except:
							print "except1a"
				except:
					print "except1b"
				
				try:
					newsecdns = value["secondary"]["ip4"]
					if self.isValueIPv4(newsecdns):
						print " set secondary dns"
						try:
							print 'try: if newsecdns == self.MYDNS[name]["primary"]["ip4"]'
							if newsecdns == self.MYDNS[name]["primary"]["ip4"]:
								return False
						except:
							print "except2a"
				except:
					print "except2b"
				
				try:
					self.MYDNS[name].update(value)
				except:
					self.MYDNS[name] = value
				self.write_options_file()
				if self.OVPN_CONNECTEDto == name:
					self.debug(1,"def cb_set_dns: self.OVPN_CONNECTEDto = %s , name = %s" % (self.OVPN_CONNECTEDto,name))
					self.win_netsh_set_dns_ovpn()
					return True

	def destroy_context_menu_servertab(self):
		self.debug(1,"def destroy_context_menu_servertab()")
		try:
			self.dnssubmenu.hide()
			self.debug(1,"def destroy_context_menu_servertab: 0x0001")
		except:
			pass
		try:
			self.dnsmenu.hide()
			self.debug(1,"def destroy_context_menu_servertab: 0x0002")
		except:
			pass
		try:
			self.context_menu_servertab.hide()
			self.debug(1,"def destroy_context_menu_servertab: 0x0003")
		except:
			pass

	def destroy_systray_menu(self):
		self.debug(2,"def destroy_systray_menu()")
		try:
			GLib.idle_add(self.systray_menu.destroy)
			self.systray_menu = False
			self.MOUSE_IN_TRAY = 0
			self.debug(2,"def destroy_systray_menu: true")
		except:
			self.debug(1,"def destroy_systray_menu: failed")
			self.systray_menu = False

	def set_statusbar_text(self,text):
		self.debug(9,"def set_statusbar_text()")
		try:
			if not self.statusbar_text == False:
				GLib.idle_add(self.statusbar_text.set_label,text)
		except:
			self.debug(1,"def set_statusbar_text: text = '%s' failed" % (text))

	def cb_set_ovpn_favorite_server(self,widget,event,server):
		if event.button == 1:
			self.destroy_context_menu_servertab()
			self.debug(1,"def cb_set_ovpn_favorite_server()")
			try:
				self.OVPN_FAV_SERVER = server
				#self.OVPN_AUTO_CONNECT_ON_START = True
				self.write_options_file()
				self.call_redraw_mainwindow()
				return True
			except:
				self.debug(1,"def cb_set_ovpn_favorite_server: failed")

	def cb_del_ovpn_favorite_server(self,widget,event,server):
		if event.button == 1:
			self.destroy_context_menu_servertab()
			self.debug(1,"def cb_del_ovpn_favorite_server()")
			try:
				self.OVPN_FAV_SERVER = False
				self.OVPN_AUTO_CONNECT_ON_START = False
				self.write_options_file()
				self.call_redraw_mainwindow()
				return True
			except:
				self.debug(1,"def cb_del_ovpn_favorite_server: failed")

	def cb_reset_load_remote_timer(self,widget,event):
		if event.keyval == Gdk.KEY_F5:
			self.call_redraw_mainwindow()
			self.debug(1,"def cb_reset_load_remote_timer == F5")
			self.reset_load_remote_timer()
		
	def reset_load_remote_timer(self):
		
		if self.LOAD_SRVDATA == True and self.MAINWINDOW_OPEN == True:
			if self.LAST_OVPN_SRV_DATA_UPDATE > 0 and self.LAST_OVPN_SRV_DATA_UPDATE < time.time()-60:
				self.LAST_OVPN_SRV_DATA_UPDATE = 0
				self.debug(1,"reset_load_remote_timer: SRV")
		if self.LOAD_ACCDATA == True and self.ACCWINDOW_OPEN == True:
			if self.LAST_OVPN_ACC_DATA_UPDATE > 0 and self.LAST_OVPN_ACC_DATA_UPDATE < time.time()-60:
				self.LAST_OVPN_ACC_DATA_UPDATE = 0
				self.debug(1,"reset_load_remote_timer: ACC")

	def cb_redraw_mainwindow_vbox(self,widget,event):
		if event.button == 1:
			self.debug(1,"def cb_redraw_mainwindow_vbox()")
			self.destroy_context_menu_servertab()
			self.reset_load_remote_timer()

	def cb_kill_openvpn(self,widget,event):
		if event.button == 1:
			self.destroy_context_menu_servertab()
			self.destroy_systray_menu()
			self.debug(1,"def cb_kill_openvpn()")
			self.OVPN_AUTO_CONNECT_ON_START = False
			self.debug(1,"def cb_kill_openvpn")
			killthread = threading.Thread(target=self.inThread_kill_openvpn)
			killthread.daemon = True
			killthread.start()

	def inThread_kill_openvpn(self):
		self.debug(1,"def inThread_kill_openvpn()")
		self.kill_openvpn()

	def cb_jump_openvpn(self,widget,event,server):
		if (widget == 0 and event == 0) or event.button == 1:
			self.OVPN_CALL_SRV = server
			self.debug(1,"def cb_jump_openvpn(%s)"%(server))
			self.destroy_systray_menu()
			self.destroy_context_menu_servertab()
			self.debug(1,"def cb_jump_openvpn: %s" % (server))
			jumpthread = threading.Thread(target=lambda server=server: self.inThread_jump_server(server))
			jumpthread.daemon = True
			jumpthread.start()

	def inThread_jump_server(self,server):
		self.debug(1,"def inThread_jump_server()")
		if self.inThread_jump_server_running == True:
			self.debug(1,"def inThread_jump_server: running ! return")
			return
		else:
			self.inThread_jump_server_running = True
			self.OVERWRITE_TRAYICON = True
			self.UPDATE_SWITCH = True
			self.debug(1,"def inThread_jump_server: server %s" % (server))
			if self.state_openvpn() == True:
				self.kill_openvpn()
			while not self.OVPN_THREADID == False:
				self.debug(1,"def cb_jump_openvpn: sleep while self.OVPN_THREADID not == False")
				time.sleep(1)
			self.call_openvpn(server)
			self.debug(1,"def inThread_jump_server: exit")

	def kill_openvpn(self):
		self.debug(1,"def kill_openvpn()")
		if self.state_openvpn() == False:
			return False
		if self.timer_check_certdl_running == True:
			self.msgwarn(_("Update is running."),_("Please wait!"))
			return False
		self.debug(1,"def kill_openvpn")
		try:
			self.del_ovpn_routes()
		except:
			pass
		try:
			if os.path.isfile(self.WIN_TASKKILL_EXE):
				ovpn_exe = self.OPENVPN_EXE.split("\\")[-1]
				string = '"%s" /F /IM %s' % (self.WIN_TASKKILL_EXE,ovpn_exe)
				exitcode = subprocess.check_call("%s" % (string),shell=True)
				self.debug(1,"def kill_openvpn: exitcode = %s" % (exitcode))
		except:
			self.debug(1,"def kill_openvpn: failed!")
			self.reset_ovpn_values_disconnected()

	def call_openvpn(self,server):
		self.debug(1,"def call_openvpn()")
		try:
			thread_openvpn = threading.Thread(target=lambda server=server: self.openvpn(server))
			thread_openvpn.start()
			self.debug(1,"def call_openvpn: thread_openvpn.start()")
		except:
			self.debug(1,"def call_openvpn: thread self.openvpn(server) failed")
			return False
		return True

	def state_openvpn(self):
		if self.STATE_OVPN == False and self.inThread_jump_server_running == False:
			return False
		if self.STATE_OVPN == True or self.inThread_jump_server_running == True:
			return True

	def openvpn(self,server):
		self.debug(1,"def openvpn()")
		while self.timer_check_certdl_running == True:
			self.debug(1,"def openvpn: sleep while timer_check_certdl_running")
			time.sleep(1)
		self.debug(1,"def openvpn: server = '%s'" % (server))
		if self.state_openvpn() == False:
			self.ovpn_server_UPPER = server
			self.ovpn_server_LOWER = server.lower()
			self.ovpn_server_config_file = "%s\\%s.ovpn" % (self.VPN_CFG,self.ovpn_server_UPPER)
			if os.path.isfile(self.ovpn_server_config_file):
				for line in open(self.ovpn_server_config_file):
					if "remote " in line:
						print(line)
						try:
							ip = line.split()[1]
							port = int(line.split()[2])
							# *** fixme *** need ipv6 check here
							if self.isValueIPv4(ip) and port > 0 and port < 65535:
								self.OVPN_CONNECTEDtoIP = ip
								self.OVPN_CONNECTEDtoPort = port
							#break
						except:
							self.debug(1,"Could not read Servers Remote-IP:Port from config: %s" % (self.ovpn_server_config_file))
							return False
					if "proto " in line:
						try:
							proto = line.split()[1]
							if proto.lower()  == "tcp" or proto.lower() == "udp":
								self.OVPN_CONNECTEDtoProtocol = proto
						except:
							self.debug(1,"Could not read Servers Protocol from config: %s" % (self.ovpn_server_config_file))
							return False
			else:
				self.debug(1,"Error: Server Config not found: '%s'" % (self.ovpn_server_config_file))
				return False
			self.ovpn_sessionlog = "%s\\ovpn.log" % (self.vpn_dir)
			self.ovpn_server_dir = "%s\\%s" % (self.VPN_CFG,self.ovpn_server_LOWER)
			self.ovpn_cert_ca = "%s\\%s.crt" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_tls_key = "%s\\%s.key" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_cli_crt = "%s\\client%s.crt" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_cli_key = "%s\\client%s.key" % (self.ovpn_server_dir,self.USERID)
			if not os.path.isdir(self.ovpn_server_dir) or \
				not os.path.isfile(self.ovpn_cert_ca) or \
				not os.path.isfile(self.ovpn_tls_key) or \
				not os.path.isfile(self.ovpn_cli_crt) or \
				not os.path.isfile(self.ovpn_cli_key):
					self.msgwarn(_("Files missing: '%s'") % (self.ovpn_server_dir),_("Error: Certs not found!"))
					self.reset_ovpn_values_disconnected()
					return False
			try:
				ovpn_string = '"%s" --config "%s" --ca "%s" --cert "%s" --key "%s" --tls-auth "%s" --dev-node "%s"' % (self.OPENVPN_EXE,self.ovpn_server_config_file,self.ovpn_cert_ca,self.ovpn_cli_crt,self.ovpn_cli_key,self.ovpn_tls_key,self.WIN_TAP_DEVICE)
				if self.DEBUG == True:
					self.ovpn_string = '%s --log "%s"' % (ovpn_string,self.ovpn_sessionlog)
				else:
					self.ovpn_string = ovpn_string
				thread_spawn_openvpn_process = threading.Thread(target=self.inThread_spawn_openvpn_process)
				thread_spawn_openvpn_process.start()
				self.OVPN_THREADID = threading.currentThread()
				self.debug(1,"Started: oVPN %s on Thread: %s" % (server,self.OVPN_THREADID))
			except:
				self.debug(1,"Error: Unable to start thread: oVPN %s " % (server))
				self.reset_ovpn_values_disconnected()
				return False
		else:
			self.debug(1,"def openvpn: self.OVPN_THREADID = %s" % (self.OVPN_THREADID))

	def inThread_spawn_openvpn_process(self):
		self.debug(1,"def inThread_spawn_openvpn_process")
		exitcode = False
		self.win_enable_tap_interface()
		if not self.openvpn_check_files():
			self.reset_ovpn_values_disconnected()
			return False
		if not self.win_firewall_start():
			self.msgwarn(_("Could not start Windows Firewall!"),_("Error: def inThread_spawn_openvpn_process"))
			self.reset_ovpn_values_disconnected()
			return False
		self.win_firewall_modify_rule(option="add")
		self.win_clear_ipv6()
		self.OVPN_CONNECTEDtime = int(time.time())
		self.OVPN_CONNECTEDto = self.OVPN_CALL_SRV
		self.OVPN_PING_STAT = -1
		self.OVPN_PING_LAST = -1
		self.NEXT_PING_EXEC = 0
		self.reset_load_remote_timer()
		self.OVERWRITE_TRAYICON = False
		self.STATE_OVPN = True
		if self.timer_ovpn_ping_running == False:
			self.debug(1,"def inThread_spawn_openvpn_process: self.inThread_timer_ovpn_ping")
			pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
			pingthread.daemon = True
			pingthread.start()
		if self.TAP_BLOCKOUTBOUND == True:
			self.win_firewall_tap_blockoutbound()
		self.win_netsh_set_dns_ovpn()
		self.call_redraw_mainwindow()
		self.inThread_jump_server_running = False
		self.win_enable_ext_interface()
		try:
			exitcode = subprocess.check_call("%s" % (self.ovpn_string),shell=True,stdout=None,stderr=None)
		except:
			self.debug(1,"def inThread_spawn_openvpn_process: exited")
		self.win_disable_ext_interface()
		self.reset_ovpn_values_disconnected()
		self.call_redraw_mainwindow()
		return

	def reset_ovpn_values_disconnected(self):
		try:
			self.win_firewall_modify_rule(option="delete")
		except:
			self.debug(1,"def inThread_spawn_openvpn_process: self.win_firewall_modify_rule option=delete failed!")
		self.win_clear_ipv6()
		self.debug(1,"def reset_ovpn_values_after()")
		self.STATE_OVPN = False
		self.inThread_jump_server_running = False
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtoIP = False
		self.OVPN_CONNECTEDtime = 0
		self.OVPN_CONNECTEDseconds = 0
		self.OVPN_THREADID = False
		self.OVPN_PING_STAT = 0
		self.OVPN_PING_LAST = 0
		self.OVPN_PING = list()
		self.UPDATE_SWITCH = True
		try:
			if os.path.isfile(self.ovpn_sessionlog):
				os.remove(self.ovpn_sessionlog)
		except:
			pass

	def inThread_timer_ovpn_ping(self):
		self.debug(10,"def inThread_timer_ovpn_ping()")
		if self.timer_ovpn_ping_running == False:
			self.OVPN_PING_STAT = -2
			self.timer_ovpn_ping_running = True
			self.debug(1,"def inThread_timer_ovpn_ping: start")
		
		if self.state_openvpn() == False:
			self.OVPN_PING_STAT = -1
			self.OVPN_PING = list()
			self.timer_ovpn_ping_running = False
			self.debug(1,"def inThread_timer_ovpn_ping: leaving")
			return
		
		elif self.STATE_OVPN == True:
			try:
				try:
					if self.NEXT_PING_EXEC < int(time.time()) and self.OVPN_CONNECTEDseconds > 5:
						PING = self.get_ovpn_ping()
						if PING > 0 and PING < 1:
							PING = round(PING,3)
						elif PING > 1:
							PING = int(PING)
						if PING > 0 and self.check_myip() == True:
							randint = random.randint(15,30)
							self.NEXT_PING_EXEC = int(time.time())+randint
							pingsum = 0
							if PING > 0:
								self.OVPN_PING.append(PING)
							if len(self.OVPN_PING) > 16:
								self.OVPN_PING.pop(0)
							if len(self.OVPN_PING) > 0:
								for pingi in self.OVPN_PING:
									pingsum += int(pingi)
								self.OVPN_PING_STAT = pingsum/len(self.OVPN_PING)
							self.OVPN_PING_LAST = PING
							self.OVPN_PING_DEAD_COUNT = 0
							self.debug(3,"def inThread_timer_ovpn_ping: %s ms, next in %s s"%(PING,randint))
						else:
							self.set_ovpn_ping_dead()
				except:
					self.set_ovpn_ping_dead()
			except:
				self.set_ovpn_ping_dead()
				self.debug(1,"def inThread_timer_ovpn_ping: failed")
			time.sleep(0.5)
			try:
				pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
				pingthread.daemon = True
				pingthread.start()
				return True
			except:
				self.debug(1,"rejoin def inThread_timer_ovpn_ping() failed")

	def set_ovpn_ping_dead(self):
		self.OVPN_PING_LAST = -2
		self.NEXT_PING_EXEC = int(time.time())+5
		self.OVPN_PING_DEAD_COUNT += 1

	def get_ovpn_ping(self):
		self.debug(3,"def get_ovpn_ping()")
		try:
			ai_list = socket.getaddrinfo(self.GATEWAY_OVPN_IP4A,"443",socket.AF_UNSPEC,socket.SOCK_STREAM)
			for (family, socktype, proto, canon, sockaddr) in ai_list:
				try:
					t1 = time.time()
					s = socket.socket(family, socktype)
					s.connect(sockaddr)
					t2 = time.time()
					s.close()
					PING = (t2-t1)*1000
					if PING > 3000:
						PING = -2
					self.debug(3,"def get_ovpn_ping: %s ms" % (PING))
					return PING
				except:
					self.OVPN_PING_LAST = -2
					return -2
		except:
			self.debug(1,"def get_ovpn_ping: failed")

	def read_gateway_from_routes(self):
		self.debug(1,"def read_gateway_from_routes()")
		try:
			output = self.win_return_route_cmd('print')
			for line in output:
				split = line.split()
				try:
					if split[0] == "0.0.0.0" and split[1] == "0.0.0.0":
						self.GATEWAY_LOCAL = split[2]
						self.debug(1,"def read_gateway_from_routes: self.GATEWAY_LOCAL #1: %s" % (self.GATEWAY_LOCAL))
						return True
				except:
					pass
					self.debug(8,"def read_gateway_from_routes: #1 failed")
				try:
					if self.OVPN_CONNECTEDtoIP in line:
						self.debug(1,"def read_ovpn_routes: self.OVPN_CONNECTEDtoIP in line '%s'" % (line))
						self.GATEWAY_LOCAL = line.split()[2]
						self.debug(1,"self.GATEWAY_LOCAL #2: %s" % (self.GATEWAY_LOCAL))
						return True
				except:
					pass
					self.debug(8,"def read_gateway_from_routes: #2 failed")
			if self.GATEWAY_LOCAL == False:
				self.debug(1,"def read_gateway_from_routes: failed")
				return False
		except:
			self.debug(1,"def read_gateway_from_routes: failed")

	def del_ovpn_routes(self):
		self.debug(1,"def del_ovpn_routes()")
		try:
			if self.read_gateway_from_routes():
				if not self.GATEWAY_LOCAL == False:
					self.ROUTE_CMDLIST.append("DELETE %s MASK 255.255.255.255 %s" % (self.OVPN_CONNECTEDtoIP,self.GATEWAY_LOCAL))
					self.ROUTE_CMDLIST.append("DELETE 0.0.0.0 MASK 128.0.0.0 %s" % (self.GATEWAY_OVPN_IP4))
					self.ROUTE_CMDLIST.append("DELETE 128.0.0.0 MASK 128.0.0.0 %s" % (self.GATEWAY_OVPN_IP4))
					return self.win_join_route_cmd()
		except:
			self.debug(1,"def del_ovpn_routes: failed")

	def win_clear_ipv6(self):
		self.debug(1,"def win_clear_ipv6()")
		self.win_clear_ipv6_dns()
		self.win_clear_ipv6_addr()
		self.win_clear_ipv6_routes()

	def win_clear_ipv6_dns(self):
		self.debug(1,"def win_clear_ipv6_dns()")
		try:
			netshcmd = 'interface ipv6 show dnsservers "%s"' % (self.WIN_TAP_DEVICE)
			netsh_output = self.win_return_netsh_cmd(netshcmd)
			for line in netsh_output:
				#print line
				if " fd48:8bea:68a5:" in line:
					#print line
					ipv6addr = line.split("    ")[2]
					#print ipv6addr
					if ipv6addr.startswith("fd48:8bea:68a5:"):
						string = 'netsh.exe interface ipv6 delete dnsservers "%s" "%s"' % (self.WIN_TAP_DEVICE,ipv6addr)
						try:
							cmd = subprocess.check_output("%s" % (string),shell=True)
							self.debug(1,"def win_clear_ipv6_dns: removed %s '%s'" % (ipv6addr,string))
						except subprocess.CalledProcessError as e:
							self.debug(1,"def win_clear_ipv6_dns: %s %s failed '%s': %s" % (ipv6addr,self.WIN_TAP_DEVICE,string,e.output))
						except:
							self.debug(1,"def win_clear_ipv6_dns: %s %s failed '%s'" % (ipv6addr,self.WIN_TAP_DEVICE,string))
		except:
			self.debug(1,"def win_clear_ipv6_dns: failed")

	def win_clear_ipv6_addr(self):
		self.debug(1,"def win_clear_ipv6_addr()")
		try:
			try:
				netshcmd = 'interface ipv6 show addresses "%s"' % (self.WIN_TAP_DEVICE)
				netsh_output = self.win_return_netsh_cmd(netshcmd)
				try:
					for line in netsh_output:
						if " fd48:8bea:68a5:" in line or " fe80:" in line:
							self.debug(1,"def win_clear_ipv6_addr: found: line = '%s'" % (line))
							if not "%" in line:
								ipv6addr = line.split()[1]
								netshcmd = 'interface ipv6 delete address address="%s" interface="%s" store=active' % (ipv6addr,self.WIN_TAP_DEVICE)
								self.NETSH_CMDLIST.append(netshcmd)
					if len(self.NETSH_CMDLIST) > 0:
						self.win_join_netsh_cmd()
				except:
					self.debug(1,"def win_clear_ipv6_addr: failed #2")
			except:
				self.debug(1,"def win_clear_ipv6_addr: failed #1")
		except:
			self.debug(1,"def win_clear_ipv6_addr: failed")

	def win_clear_ipv6_routes(self):
		self.debug(1,"def win_clear_ipv6_routes()")
		try:
			netshcmd = 'interface ipv6 show route'
			netsh_output = self.win_return_netsh_cmd(netshcmd)
			for line in netsh_output:
				if " fd48:8bea:68a5:" in line or " fe80:" in line:
					self.debug(1,"def win_clear_ipv6_routes: found: line = '%s'" % (line))
					ipv6 = line.split()[3]
					output = self.win_return_route_cmd("DELETE %s" % (ipv6))
					self.debug(1,"def win_clear_ipv6_routes: %s %s" % (ipv6,output))
		except:
			self.debug(1,"def win_clear_ipv6_routes: failed")

	def win_netsh_set_dns_ovpn(self):
		self.debug(1,"def win_netsh_set_dns_ovpn()")
		if self.NO_DNS_CHANGE == True:
			self.debug(1,"def win_netsh_set_dns_ovpn: self.NO_DNS_CHANGE")
			return True
		if self.check_dns_is_whitelisted() == True:
			return True
		servername = self.OVPN_CONNECTEDto
		self.debug(1,"def win_netsh_set_dns_ovpn: servername = '%s'" % (servername))
		try:
			pridns = self.MYDNS[servername]["primary"]["ip4"]
			self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_EXT_DEVICE,pridns))
			self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_TAP_DEVICE,pridns))
			try:
				secdns = self.MYDNS[servername]["secondary"]["ip4"]
				self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no' % (self.WIN_EXT_DEVICE,secdns))
				self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no' % (self.WIN_TAP_DEVICE,secdns))
			except:
				self.debug(1,"def win_netsh_set_dns_ovpn: secdns not found")
		except:
			self.debug(1,"def win_netsh_set_dns_ovpn: pridns not found")
			if len(self.NETSH_CMDLIST) == 0:
				if self.GATEWAY_DNS1 == "127.0.0.1":
					setdns = "127.0.0.1"
				else:
					setdns = self.GATEWAY_OVPN_IP4A
				self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_EXT_DEVICE,setdns))
				self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_TAP_DEVICE,setdns))
		if self.win_join_netsh_cmd() == True:
			self.WIN_DNS_CHANGED = True
			return True
		else:
			self.debug(1,"def win_netsh_set_dns_ovpn: failed!")

	def win_netsh_restore_dns_from_backup(self):
		self.debug(1,"def win_netsh_restore_dns_from_backup()")
		try:
			if self.NO_DNS_CHANGE == True:
				return True
			if self.WIN_DNS_CHANGED == False:
				return True
			if self.check_dns_is_whitelisted() == True:
				return True
			try:
				if self.WIN_EXT_DHCP == True:
					self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" dhcp' % (self.WIN_EXT_DEVICE))
					if self.win_join_netsh_cmd():
						self.debug(1,"DNS restored to DHCP.")
						return True
					else:
						return False
			except:
				self.debug(1,"def win_netsh_restore_dns_from_backup: restore DHCP on IF: '%s' failed " % (self.WIN_EXT_DEVICE))
			
			try:
				if not self.GATEWAY_DNS1 == self.GATEWAY_OVPN_IP4A:
					self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS1))
					if self.win_join_netsh_cmd():
						self.debug(1,"Primary DNS restored to: %s"%(self.GATEWAY_DNS1))
						if self.GATEWAY_DNS2 == False:
							return True
						else:
							self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS2))
							if self.win_join_netsh_cmd():
								self.debug(1,"Secondary DNS restored to %s" % (self.GATEWAY_DNS2))
								return True
							else:
								self.msgwarn(_("Error: Restore Secondary DNS to %s failed.") % (self.GATEWAY_DNS2),_("Error: DNS restore 2nd"))
								return False
					else:
						self.msgwarn(_("Error: Restore Primary DNS to %s failed.") % (self.GATEWAY_DNS1),_("Error: DNS restore 1st"))
						return False
				else:
					self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" dhcp' % (self.WIN_EXT_DEVICE))
					if self.win_join_netsh_cmd():
						self.debug(1,"DNS restored to DHCP")
						return True
					else:
						return False
			except:
				self.debug(1,"def win_netsh_restore_dns_from_backup: Restore DNS failed")
		except:
			self.debug(1,"def win_netsh_restore_dns_from_backup: failed")

	def win_netsh_read_dns_to_backup(self):
		self.debug(1,"def win_netsh_read_dns_to_backup()")
		self.read_d0wns_dns()
		
		if self.NO_DNS_CHANGE == True:
			return True
		try:
			netshcmd = 'interface ipv4 show dns'
			netsh_output = self.win_return_netsh_cmd(netshcmd)
			search = '"%s"' % (self.WIN_EXT_DEVICE)
			i, m1, m2, t = 0, 0, 0 ,0
			self.debug(1,"def win_netsh_read_dns_to_backup: search = %s" % (search))
			for line in netsh_output:
				if search in line:
					self.debug(1,"found: %s in %s line %s" % (search,line,i))
					m1=i+1
				
				if i == m1:
					if "DHCP" in line:
						self.WIN_EXT_DHCP = True
						return True
					if "DNS" in line:
						m2=i+1
						try:
							dns1 = line.strip().split(":")[1].lstrip()
							if self.isValueIPv4(dns1):
								self.GATEWAY_DNS1 = dns1
								self.debug(1,"1st DNS '%s' IF: %s backuped" % (dns1,search))
						except:
							self.debug(1,"def win_netsh_read_dns_to_backup: 1st DNS failed read on line '%s' search '%s'" % (line,search))
				
				if i == m2:
					try:
						dns2 = line.strip()
						if self.isValueIPv4(dns2):
								self.GATEWAY_DNS2 = dns2
								self.debug(1,"2nd DNS '%s' IF: %s backuped" % (dns2,search))
								break
					except:
						self.debug(1,"def win_netsh_read_dns_to_backup: 2nd DNS failed read on line '%s' search '%s'" % (line,search))
				
				i+=1
			self.debug(1,"def win_netsh_read_dns_to_backup: self.GATEWAY_DNS1 = %s + self.GATEWAY_DNS2 = %s"%(self.GATEWAY_DNS1,self.GATEWAY_DNS2))
			if not self.GATEWAY_DNS1 == False:
				return True
			else:
				self.WIN_EXT_DHCP = True
				return True
		except:
			self.errorquit(text=_("def win_netsh_read_dns_to_backup: failed!"))

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

	def hash_sha256_file(self,file):
		self.debug(1,"def hash_sha256_file()")
		if os.path.isfile(file):
			hasher = hashlib.sha256()
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
					os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), self.CA_FILE)
					return True
				except:
					self.msgwarn(_("Error:\nSSL Root Certificate for %s not loaded %s") % (DOMAIN,self.CA_FILE),_("Error: SSL CA Cert #1"))
					return False
			else:
				self.msgwarn(_("Error:\nInvalid SSL Root Certificate for %s in:\n'%s'\nhash is:\n'%s'\nbut should be '%s'") % (DOMAIN,self.CA_FILE,self.CA_FILE_HASH,self.CA_FIXED_HASH),_("Error: SSL CA Cert #2"))
				return False
		else:
			self.msgwarn(_("Error:\nSSL Root Certificate for %s not found in:\n'%s'!") % (DOMAIN,self.CA_FILE),_("Error: SSL CA Cert #3"))
			return False

	def win_firewall_start(self):
		self.debug(1,"def win_firewall_start()")
		if self.NO_WIN_FIREWALL == True:
			return True
		if self.NO_DNS_CHANGE == False:
			self.win_ipconfig_flushdns()
		if self.WIN_RESET_FIREWALL == True:
			self.NETSH_CMDLIST.append("advfirewall reset")
		#self.NETSH_CMDLIST.append("advfirewall set privateprofile logging filename \"%s\"" % (self.pfw_private_log))
		#self.NETSH_CMDLIST.append("advfirewall set publicprofile logging filename \"%s\"" % (self.pfw_public_log))
		#self.NETSH_CMDLIST.append("advfirewall set domainprofile logging filename \"%s\"" % (self.pfw_domain_log))
		self.NETSH_CMDLIST.append("advfirewall set allprofiles state on")
		self.NETSH_CMDLIST.append("advfirewall set privateprofile firewallpolicy blockinbound,blockoutbound")
		self.NETSH_CMDLIST.append("advfirewall set domainprofile firewallpolicy blockinbound,blockoutbound")
		if self.TAP_BLOCKOUTBOUND == True:
			opt = "blockoutbound"
		else:
			opt = "allowoutbound"
		self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,%s" % (opt))
		if self.win_join_netsh_cmd():
			self.WIN_FIREWALL_STARTED = True
			return True

	def win_firewall_tap_blockoutbound(self):
		self.win_firewall_tap_blockoutbound_running = True
		self.debug(1,"def win_firewall_tap_blockoutbound()")
		try:
			if self.NO_WIN_FIREWALL == True:
				self.win_firewall_tap_blockoutbound_running = False
				return
			if self.TAP_BLOCKOUTBOUND == True:
				self.win_firewall_whitelist_ovpn_on_tap(option="delete")
				self.win_firewall_whitelist_ovpn_on_tap(option="add")
				self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,blockoutbound")
			else:
				self.win_firewall_whitelist_ovpn_on_tap(option="delete")
				self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound")		
			self.win_join_netsh_cmd()
			self.debug(1,"Block outbound on TAP!\n\nAllow Whitelist to Internal oVPN Services\n\n'%s'\n\nSee all Rules:\n Windows Firewall with Advanced Security\n --> Outgoing Rules" % (self.WHITELIST_PUBLIC_PROFILE))
		except:
			self.debug(1,"def win_firewall_tap_blockoutbound: failed!")
		self.win_firewall_tap_blockoutbound_running = False

	def win_firewall_allowout(self):
		self.debug(1,"def win_firewall_allowout()")
		if self.NO_WIN_FIREWALL == True:
			return True	
		self.NETSH_CMDLIST.append("advfirewall set allprofiles state on")
		self.NETSH_CMDLIST.append("advfirewall set privateprofile firewallpolicy blockinbound,allowoutbound")
		self.NETSH_CMDLIST.append("advfirewall set domainprofile firewallpolicy blockinbound,allowoutbound")
		self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound")
		if self.win_join_netsh_cmd():
			self.WIN_FIREWALL_STARTED = True
			return True

	def win_firewall_block_on_exit(self):
		self.debug(1,"def win_firewall_block_on_exit()")
		if self.NO_WIN_FIREWALL == True:
			return True
		self.NETSH_CMDLIST.append("advfirewall set allprofiles state on")
		self.NETSH_CMDLIST.append("advfirewall set privateprofile firewallpolicy blockinbound,blockoutbound")
		self.NETSH_CMDLIST.append("advfirewall set domainprofile firewallpolicy blockinbound,blockoutbound")
		self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,blockoutbound")
		return self.win_join_netsh_cmd()

	def win_firewall_whitelist_ovpn_on_tap(self,option):
		self.debug(1,"def win_firewall_whitelist_ovpn_on_tap()")
		if self.NO_WIN_FIREWALL == True:
			self.debug(1,"def win_firewall_whitelist_ovpn_on_tap: self.NO_WIN_FIREWALL == True")
			return True
		if option == "add":
			actionstring = "action=allow"
		elif option == "delete":
			actionstring = ""
		for entry,value in self.WHITELIST_PUBLIC_PROFILE.iteritems():
			ip = value["ip"]
			port = value["port"]
			protocol = value["proto"]
			
			rule_name = "(oVPN) Allow OUT on TAP: %s %s:%s %s" % (entry,ip,port,protocol)
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=public dir=out %s" % (option,rule_name,ip,port,protocol,actionstring)
			self.NETSH_CMDLIST.append(rule_string)
			self.debug(1,"Whitelist: %s %s %s %s" % (entry,ip,port,protocol))
		self.win_join_netsh_cmd()
		return True

	def win_firewall_add_rule_to_vcp(self,option):
		self.debug(1,"def win_firewall_add_rule_to_vcp()")
		if self.NO_WIN_FIREWALL == True:
			return True
		self.debug(1,"def win_firewall_add_rule_to_vcp()")
		if option == "add":
			actionstring = "action=allow"
		elif option == "delete":
			actionstring = ""
		url = "https://%s" % (DOMAIN)
		ips = ["178.17.170.116",self.GATEWAY_OVPN_IP4A]
		port = 443
		protocol = "tcp"
		for ip in ips:
			rule_name = "(oVPN) Allow OUT on EXT: %s %s:%s %s" % (url,ip,port,protocol)
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out %s" % (option,rule_name,ip,port,protocol,actionstring)
			self.NETSH_CMDLIST.append(rule_string)
		if self.win_join_netsh_cmd():
			self.WIN_FIREWALL_ADDED_RULE_TO_VCP = True
			return True

	def win_firewall_export_on_start(self):
		self.debug(1,"def win_firewall_export_on_start()")
		if self.NO_WIN_FIREWALL == True:
			return True
		if self.WIN_BACKUP_FIREWALL == False:
			return True
		self.debug(1,"def win_firewall_export_on_start()")
		if os.path.isfile(self.pfw_bak):
			os.remove(self.pfw_bak)
		self.NETSH_CMDLIST.append('advfirewall export "%s"' % (self.pfw_bak))
		return self.win_join_netsh_cmd()

	def win_firewall_restore_on_exit(self):
		self.debug(1,"def win_firewall_restore_on_exit()")
		if self.NO_WIN_FIREWALL == True:
			return True
		if self.WIN_BACKUP_FIREWALL == False:
			return True
		if self.WIN_FIREWALL_STARTED == True:
			self.debug(1,"def win_firewall_restore_on_exit()")
			self.NETSH_CMDLIST.append("advfirewall reset")
			if os.path.isfile(self.pfw_bak):
				self.NETSH_CMDLIST.append('advfirewall import "%s"' % (self.pfw_bak))
			return self.win_join_netsh_cmd()

	def win_enable_tap_interface(self):
		self.debug(1,"def win_enable_tap_interface()")
		self.NETSH_CMDLIST.append('interface set interface "%s" ENABLED'%(self.WIN_TAP_DEVICE))
		return self.win_join_netsh_cmd()

	def win_disable_ext_interface(self):
		self.debug(1,"def win_disable_ext_interface()")
		if self.WIN_DISABLE_EXT_IF_ON_DISCO == True:
			self.NETSH_CMDLIST.append('interface set interface "%s" DISABLED'%(self.WIN_EXT_DEVICE))
			return self.win_join_netsh_cmd()

	def win_enable_ext_interface(self):
		self.debug(1,"def win_enable_ext_interface()")
		self.NETSH_CMDLIST.append('interface set interface "%s" ENABLED'%(self.WIN_EXT_DEVICE))
		self.win_join_netsh_cmd()

	def win_firewall_analyze(self):
		return
		netshcmd = "advfirewall firewall show rule name=all"
		netsh_output = self.win_return_netsh_cmd(netshcmd)
		for line in netsh_output:
			line1 = line.split(":")[-1].lstrip()
			for entry in [ "pidgin","firefox","chrome","icq","skype","commander","github" ]:
				if entry in line1.lower():
					self.debug(1,"def win_firewall_dumprules: '%s'" % (line1))

	def win_firewall_modify_rule(self,option):
		try:
			self.debug(1,"def win_firewall_modify_rule()")
			if self.NO_WIN_FIREWALL == True:
				return True
			rule_name = "Allow OUT oVPN-IP %s to Port %s Protocol %s" % (self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
			if option == "add":
				rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % (option,rule_name,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
			if option == "delete":
				rule_string = "advfirewall firewall %s rule name=\"%s\"" % (option,rule_name)
			#self.debug(1,"def pfw: %s"%(rule_string))
			self.NETSH_CMDLIST.append(rule_string)
			return self.win_join_netsh_cmd()
		except:
			self.debug(1,"def win_firewall_modify_rule: option = '%s' failed" %(option))

	def win_return_netsh_cmd(self,cmd):
		self.debug(1,"def win_return_netsh_cmd()")
		if os.path.isfile(self.WIN_NETSH_EXE):
			netshcmd = '%s %s' % (self.WIN_NETSH_EXE,cmd)
			try: 
				read = subprocess.check_output('%s' % (netshcmd),shell=True)
				output = read.strip().decode('cp1258','ignore').strip(' ').split('\r\n')
				self.debug(5,"def win_return_netsh_cmd: output = '%s'" % (output))
				return output
			except:
				self.debug(1,"def win_return_netsh_cmd: '%s' failed" % (netshcmd))
		else:
			self.errorquit(text=_("Error: netsh.exe not found!"))

	def win_join_netsh_cmd(self):
		self.debug(1,"def win_join_netsh_cmd()")
		if os.path.isfile(self.WIN_NETSH_EXE):
			i=0
			for cmd in self.NETSH_CMDLIST:
				netshcmd = '"%s" %s' % (self.WIN_NETSH_EXE,cmd)
				try: 
					exitcode = subprocess.call('%s' % (netshcmd),shell=True)
					if exitcode == 0:
						self.debug(1,"netshOK: '%s': exitcode = %s" % (netshcmd,exitcode))
						i+=1
					else:
						self.debug(1,"netshERROR: '%s': exitcode = %s" % (netshcmd,exitcode))
				except:
					self.debug(1,"def win_join_netsh_cmd: '%s' failed" % (netshcmd))
			if len(self.NETSH_CMDLIST) == i:
				self.NETSH_CMDLIST = list()
				return True
			else:
				self.NETSH_CMDLIST = list()
				return False
		else:
			self.errorquit(text=_("Error: netsh.exe not found!"))

	def win_return_route_cmd(self,cmd):
		self.debug(1,"def win_return_route_cmd()")
		if os.path.isfile(self.WIN_ROUTE_EXE):
			routecmd = '"%s" %s' % (self.WIN_ROUTE_EXE,cmd)
			try: 
				read = subprocess.check_output('%s' % (routecmd),shell=True)
				output = read.strip().decode('cp1258','ignore').strip(' ').split('\r\n')
				self.debug(5,"def win_return_route_cmd: output = '%s'" % (output))
				return output
			except:
				self.debug(1,"def win_return_route_cmd: '%s' failed" % (routecmd))
				return False
		else:
			self.errorquit(text=_("Error: route.exe not found!"))

	def win_join_route_cmd(self):
		self.debug(1,"def win_join_route_cmd()")
		if os.path.isfile(self.WIN_ROUTE_EXE):
			i=0
			for cmd in self.ROUTE_CMDLIST:
				routecmd = '"%s" %s' % (self.WIN_ROUTE_EXE,cmd)
				try: 
					exitcode = subprocess.call('%s' % (routecmd),shell=True)
					if exitcode == 0:
						self.debug(1,"routeOK: '%s': exitcode = %s" % (routecmd,exitcode))
						i+=1
					else:
						self.debug(1,"routeERROR: '%s': exitcode = %s" % (routecmd,exitcode))
				except:
					self.debug(1,"def win_join_route_cmd: '%s' failed" % (routecmd))
			if len(self.ROUTE_CMDLIST) == i:
				self.ROUTE_CMDLIST = list()
				return True
			else:
				self.ROUTE_CMDLIST = list()
				return False
		else:
			self.errorquit(text=_("Error: route.exe not found!"))

	def win_ipconfig_flushdns(self):
		self.debug(1,"def win_ipconfig_flushdns()")
		if os.path.isfile(self.WIN_IPCONFIG_EXE):
			try: 
				cmdstring = '"%s" /flushdns' % (self.WIN_IPCONFIG_EXE)
				exitcode = subprocess.call("%s" % (cmdstring),shell=True)
				if exitcode == 0:
					self.debug(1,"%s: exitcode = %s" % (cmdstring,exitcode))
					return True
				else:
					self.debug(1,"%s: exitcode = %s" % (cmdstring,exitcode))
			except:
				self.debug(1,"def win_join_ipconfig_cmd: '%s' failed" % (cmdstring))
		else:
			self.errorquit(text=_("ipconfig.exe not found!"))

	def win_ipconfig_displaydns(self):
		self.debug(1,"def win_ipconfig_displaydns()")
		if os.path.isfile(self.WIN_IPCONFIG_EXE):
			try: 
				cmdstring = '"%s" /displaydns' % (self.WIN_IPCONFIG_EXE)
				out = subprocess.check_output("%s" % (cmdstring),shell=True)
				return out
			except:
				self.debug(1,"def win_ipconfig_displaydns: failed" % (cmdstring))
		else:
			self.errorquit(text=_("ipconfig.exe not found!"))

	def isValueIPv4(self,value):
		#self.debug(99,"def isValueIPv4()")
		try:
			if len(value.split('.')) == 4:
				for n in value.split('.'):
					if n.isdigit():
						self.debug(50,"def isValueIPv4: n = %s"%(n))
						if not n >= 0 and not n <= 255:
							return False
				return True
		except:
			return False

	# *** fixme ***
	def isValueIPv6(self,value):
		self.debug(1,"def isValueIPv6()")
		return True

	def form_ask_userid(self):
		self.debug(1,"def form_ask_userid()")
		try:
			self.dialog_form_ask_userid.destroy()
		except:
			pass
		try:
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL)
			dialogWindow.set_position(Gtk.WindowPosition.CENTER)
			self.dialog_form_ask_userid = dialogWindow
			try:
				dialogWindow.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			dialogWindow.set_transient_for(self.window)
			dialogWindow.set_title(_("oVPN.to Setup"))
			dialogWindow.set_markup(_("Enter your oVPN.to Details"))
			dialogBox = dialogWindow.get_content_area()
			useridEntry = Gtk.Entry()
			if self.USERID == False:
				useridEntry.set_visibility(True)
				useridEntry.set_max_length(9)
				useridEntry.set_size_request(200,24)
				useridLabel = Gtk.Label(label=_("User-ID:"))
				dialogBox.pack_start(useridLabel,False,False,0)
				dialogBox.pack_start(useridEntry,False,False,0)
			else:
				useridLabel1 = Gtk.Label(label=_("User-ID:"))
				useridLabel2 = Gtk.Label(label=" %s"%(self.USERID))
				dialogBox.pack_start(useridLabel1,False,False,0)
				dialogBox.pack_start(useridLabel2,False,False,0)
			apikeyEntry = Gtk.Entry()
			apikeyEntry.set_visibility(False)
			apikeyEntry.set_max_length(128)
			apikeyEntry.set_invisible_char("*")
			apikeyEntry.set_size_request(200,24)
			apikeyLabel = Gtk.Label(label=_("API-Key:"))
			dialogBox.pack_start(apikeyLabel,False,False,0)
			dialogBox.pack_start(apikeyEntry,False,False,0)
			
			checkbox = Gtk.Switch()
			checkbox_title = Gtk.Label(label=_("Save Passphrase in File?"))
			checkbox.set_active(False)
			dialogBox.pack_start(checkbox_title,False,False,0)
			dialogBox.pack_start(checkbox,False,False,0)
			
			dialogWindow.show_all()
			dialogWindow.connect("response", self.response_dialog_apilogin, useridEntry, apikeyEntry, checkbox)
			dialogWindow.connect("close", self.response_dialog_apilogin, None, None, None)
			dialogWindow.run()
		except:
			self.debug(1,"def form_ask_userid: Failed")

	def response_dialog_apilogin(self, dialog, response_id, useridEntry, apikeyEntry, checkbox):
		self.debug(1,"response_dialog_apilogin()")
		if response_id == Gtk.ResponseType.CANCEL:
			self.debug(1,"def response_dialog_apilogin: response_id == Gtk.ResponseType.CANCEL")
			dialog.destroy()
			return
		elif response_id == Gtk.ResponseType.OK:
			self.debug(1,"def response_dialog_apilogin: Gtk.ResponseType.OK self.USERID = '%s'"%(self.USERID))
			if self.USERID == False:
				userid = useridEntry.get_text().rstrip()
			else:
				userid = self.USERID
			apikey = apikeyEntry.get_text().rstrip()
			self.debug(1,"def response_dialog_apilogin: Gtk.ResponseType.OK userid = '%s'"%(userid))
			if userid.isdigit() and userid > 1 and (len(apikey) == 0 or (len(apikey) == 128 and apikey.isalnum())) and (self.USERID == False or self.USERID == userid):
				dialog.destroy()
				saveph = checkbox.get_active()
				if saveph == True:
					self.SAVE_APIKEY_INFILE = True
				else:
					self.SAVE_APIKEY_INFILE = False
				if self.USERID == False:
					self.debug(1,"def response_dialog_apilogin: self.USERID == False")
					api_dir = "%s\\%s" % (self.app_dir,userid)
					if not os.path.isdir(api_dir):
						os.mkdir(api_dir)
						if os.path.isdir(api_dir):
							self.API_DIR = api_dir
							self.USERID = userid
							self.APIKEY = apikey
							self.debug(1,"def response_dialog_apilogin: return True #1")
							return True
				elif not self.API_DIR == False and os.path.isdir(self.API_DIR):
					if len(apikey) == 0:
						self.APIKEY = False
					else:
						self.APIKEY = apikey
					if not self.write_options_file() == True:
						self.APIKEY = False
						return False
					self.INIT_FIRST_UPDATE = True
					self.debug(1,"def response_dialog_apilogin: return True #2")
					return True
		elif dialog:
			dialog.destroy()

	def dialog_apikey(self):
		self.debug(1,"def dialog_apikey()")
		self.form_ask_userid()
		if not self.APIKEY == False:
			self.debug(1,"def dialog_apikey: self.APIKEY '-NOT_FALSE-'")
			self.UPDATE_SWITCH = True
			
	def cb_interface_selector_changed(self, combobox):
		self.debug(1,"def cb_interface_selector_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_EXT_DEVICE = model[index][0]
			self.debug(1,"def cb_interface_selector_changed: selected IF = '%s'" % (self.WIN_EXT_DEVICE))
		return

	def cb_select_userid(self, combobox):
		self.debug(1,"def cb_select_userid()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1 and model[index][0].isdigit() and model[index][0] > 1:
			self.USERID = model[index][0]
			self.debug(1,"def cb_select_userid: selected USERID = '%s'" % (self.USERID))
		return

	def cb_tap_interface_selector_changed(self, combobox):
		self.debug(1,"def cb_tap_interface_selector_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_TAP_DEVICE = model[index][0]
			self.debug(1,"def cb_tap_interface_selector_changed: selected tap IF = '%s'" % (self.WIN_TAP_DEVICE))
		return

	def check_last_server_update(self,remote_lastupdate):
		self.debug(1,"def check_last_server_update()")
		if self.LAST_CFG_UPDATE < remote_lastupdate:
			self.remote_lastupdate = remote_lastupdate
			self.debug(1,"def check_last_server_update: requesting update")
			return True
		else:
			self.debug(1,"def check_last_server_update: no update")
			return False

	def write_last_update(self):
		self.debug(1,"def write_last_update()")
		self.LAST_CFG_UPDATE = self.remote_lastupdate
		if self.write_options_file():
			return True

	def reset_last_update(self):
		self.debug(1,"def reset_last_update()")
		self.LAST_CFG_UPDATE = 0
		if self.write_options_file():
			return True

	def cb_check_normal_update(self):
		self.debug(1,"def cb_check_normal_update()")
		if self.check_inet_connection() == False:
			self.msgwarn(_("Could not connect to %s") % (DOMAIN),_("Error: Update failed"))
			return False
		if self.check_remote_update():
			self.debug(1,"def cb_check_normal_update: self.check_remote_update() == True")
			return True

	def cb_force_update(self):
		self.debug(1,"def cb_force_update()")
		if self.check_inet_connection() == False:
			self.msgwarn(_("Could not connect to %s") % (DOMAIN),_("Error: Update failed"))
			return False
		if self.reset_last_update() == True:
			self.debug(1,"def cb_force_update: self.reset_last_update")
			self.cb_check_normal_update()

	def cb_resetextif(self):
		self.debug(1,"def cb_resetextif()")
		self.WIN_EXT_DEVICE = False
		self.WIN_TAP_DEVICE = False
		self.WIN_RESET_EXT_DEVICE = True
		self.read_interfaces()
		self.write_options_file()

	def cb_extserverview(self,widget,event):
		if event.button == 1:
			self.debug(1,"def cb_extserverview()")
			reopen = False
			if self.MAINWINDOW_OPEN == True:
				reopen = True
				GLib.idle_add(self.mainwindow.remove,self.mainwindow_vbox)
			if self.LOAD_SRVDATA == False:
				self.LOAD_SRVDATA = True
				self.LAST_OVPN_SRV_DATA_UPDATE = 0
				self.OVPN_SRV_DATA = {}
			else:
				self.LOAD_SRVDATA = False
			self.write_options_file()
			if reopen == True:
				GLib.idle_add(self.mainwindow_ovpn_server)
	
	def cb_extserverview_size(self,widget,event):
		if event.button == 1:
			self.debug(1,"def cb_extserverview_size()")
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL)
			dialogWindow.set_position(Gtk.WindowPosition.CENTER)
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			text = _("Server Window Size")
			dialogWindow.set_title(text)
			dialogWindow.set_markup(text)
			dialogBox = dialogWindow.get_content_area()
			widthLabel = Gtk.Label(label=_("Width (pixel):"))
			widthEntry = Gtk.Entry()
			widthEntry.set_visibility(True)
			widthEntry.set_size_request(40,24)
			heightLabel = Gtk.Label(label=_("Height (pixel):"))
			heightEntry = Gtk.Entry()
			heightEntry.set_visibility(True)
			heightEntry.set_size_request(40,24)
			sizeLabel = Gtk.Label(label=_("Enter width and height\n\nLeave blank for default"))
			dialogBox.pack_start(sizeLabel,False,False,0)
			dialogBox.pack_start(widthLabel,False,False,0)
			dialogBox.pack_start(widthEntry,False,False,0)
			dialogBox.pack_start(heightLabel,False,False,0)
			dialogBox.pack_start(heightEntry,False,False,0)
			dialogWindow.show_all()
			response = dialogWindow.run()
			if response == Gtk.ResponseType.CANCEL:
				dialogWindow.destroy()
				print "response: btn cancel %s" % (response)
				return False
			elif response == Gtk.ResponseType.OK:
				WIDTH = widthEntry.get_text().rstrip()
				HEIGHT = heightEntry.get_text().rstrip()
				dialogWindow.destroy()
				if self.LOAD_SRVDATA == True:
					if WIDTH == "": WIDTH = self.SRV_WIDTH_DEFAULT;
					if HEIGHT == "": HEIGHT = self.SRV_HEIGHT_DEFAULT;
					self.SRV_WIDTH = WIDTH
					self.SRV_HEIGHT = HEIGHT
					self.debug(1,"def cb_extserverview_size(): %sx%s" % (self.SRV_WIDTH,self.SRV_HEIGHT))
				else:
					if WIDTH == "": WIDTH = self.SRV_LIGHT_WIDTH_DEFAULT;
					if HEIGHT == "": HEIGHT = self.SRV_LIGHT_HEIGHT_DEFAULT;
					self.SRV_LIGHT_WIDTH = WIDTH
					self.SRV_LIGHT_HEIGHT = HEIGHT
					self.debug(1,"def cb_extserverview_size(): %sx%s" % (self.SRV_LIGHT_WIDTH,self.SRV_LIGHT_HEIGHT))
				self.write_options_file()
				WIDTH = int(WIDTH)
				HEIGHT = int(HEIGHT)
				GLib.idle_add(self.mainwindow.resize,int(WIDTH),int(HEIGHT))
				return True
			else:
				return False

	def cb_set_loaddataevery(self,widget,event):
		if event.button == 1:
			self.debug(1,"def cb_set_loaddataevery()")
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL)
			dialogWindow.set_position(Gtk.WindowPosition.CENTER)
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			text = _("Load Data every X seconds")
			dialogWindow.set_title(text)
			dialogWindow.set_markup(text)
			dialogBox = dialogWindow.get_content_area()
			Label = Gtk.Label(label=_("seconds:"))
			adjustment = Gtk.Adjustment(0, 66, 86400, 1, 10, 0)
			Entry = Gtk.SpinButton()
			Entry.set_adjustment(adjustment)
			Entry.set_visibility(True)
			Entry.set_size_request(40,24)
			dialogBox.pack_start(Label,False,False,0)
			dialogBox.pack_start(Entry,False,False,0)
			dialogWindow.show_all()
			response = dialogWindow.run()
			if response == Gtk.ResponseType.CANCEL:
				dialogWindow.destroy()
				print "response: btn cancel %s" % (response)
				return False
			elif response == Gtk.ResponseType.OK:
				try:
					seconds = int(Entry.get_text().rstrip())
				except:
					dialogWindow.destroy()
					return
				dialogWindow.destroy()
				if seconds <= 66:
					seconds = 66
				self.LOAD_DATA_EVERY = seconds
				self.write_options_file()
				return True
			else:
				return False

	def cb_change_ipmode1(self):
		self.debug(1,"def cb_change_ipmode1()")
		self.OVPN_CONFIGVERSION = "23x"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		if len(self.OVPN_SERVER) == 0:
			self.cb_check_normal_update()
		if self.MAINWINDOW_OPEN == True:
			self.destroy_mainwindow()
		self.UPDATE_SWITCH = True

	def cb_change_ipmode2(self):
		self.debug(1,"def cb_change_ipmode2()")
		self.OVPN_CONFIGVERSION = "23x46"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		if len(self.OVPN_SERVER) == 0:
			self.msgwarn(_("Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://%s to use any IPv6 options!") % (DOMAIN),_("Switched to IPv4+6"))
			self.cb_check_normal_update()
		if self.MAINWINDOW_OPEN == True:
			self.destroy_mainwindow()
		self.UPDATE_SWITCH = True

	# *** fixme: need isValueIPv6 first! ***
	def cb_change_ipmode3(self):
		self.debug(1,"def cb_change_ipmode3()")
		return True
		self.OVPN_CONFIGVERSION = "23x64"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		if len(self.OVPN_SERVER) == 0:
			self.cb_check_normal_update()
		if self.MAINWINDOW_OPEN == True:
			self.destroy_mainwindow()
		self.msgwarn(_("Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://%s to use any IPv6 options!") % (DOMAIN),_("Switched to IPv6+4"))

	def cb_restore_firewallbackup(self,file):
		self.debug(1,"def cb_restore_firewallbackup()")
		fwbak = "%s\\%s" % (self.pfw_dir,file)
		if os.path.isfile(fwbak):
			self.debug(1,"def cb_restore_firewallbackup: %s" % (fwbak))
			self.win_firewall_export_on_start()
			self.NETSH_CMDLIST.append('advfirewall import "%s"' % (fwbak))
			return self.win_join_netsh_cmd()

	def delete_dir(self,path):
		self.debug(1,"def delete_dir()")
		if self.OS == "win32":
			string = 'rmdir /S /Q "%s"' % (path)
			self.debug(1,"def delete_dir: %s" % (string))
			subprocess.check_output("%s" % (string),shell=True)

	def extract_ovpn(self):
		self.debug(1,"def extract_ovpn()")
		try:
			if os.path.isfile(self.zip_cfg) and os.path.isfile(self.zip_crt):
				z1file = zipfile.ZipFile(self.zip_cfg)
				z2file = zipfile.ZipFile(self.zip_crt)
				if os.path.isdir(self.VPN_CFG):
					self.debug(1,"def extract_ovpn: os.path.isdir(%s)"%(self.VPN_CFG))
					self.delete_dir(self.VPN_CFG)
				if not os.path.isdir(self.VPN_CFG):
					try:
						os.mkdir(self.VPN_CFG)
						self.debug(1,"def extract_ovpn: os.mkdir(%s)"%(self.VPN_CFG))
					except:
						self.debug(1,"def extract_ovpn: %s not found, create failed."%(self.VPN_CFG))
				try:
					z1file.extractall(self.VPN_CFG)
					z2file.extractall(self.VPN_CFG)
					if self.write_last_update():
						self.debug(1,"Certificates and Configs extracted.")
						return True
				except:
					self.debug(1,"Error on extracting Certificates and Configs!")
					return False
		except:
			self.debug(1,"def extract_ovpn: failed")

	def API_REQUEST(self,API_ACTION):
		self.debug(1,"def API_REQUEST()")
		if self.APIKEY == False:
			self.msgwarn(_("No API-Key!"),_("Error: def API_REQUEST"))
			return False
		if API_ACTION == "lastupdate": 
			self.TO_CURL = "uid=%s&apikey=%s&action=%s" % (self.USERID,self.APIKEY,API_ACTION)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		if API_ACTION == "getconfigs": 
			if os.path.isfile(self.zip_cfg): os.remove(self.zip_cfg)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION, 'version' : self.OVPN_CONFIGVERSION, 'type' : 'win' }	
		
		if API_ACTION == "requestcerts":
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		if API_ACTION == "getcerts":
			if os.path.isfile(self.zip_crt): os.remove(self.zip_crt)
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
		
		self.body = False
		
		self.debug(1,"def API_REQUEST: API_ACTION = %s" % (API_ACTION))
		
		try:
			r = requests.post(self.APIURL,data=values)
			if API_ACTION == "getconfigs" or API_ACTION == "getcerts":
				self.body = r.content
			else:
				self.body = r.text
			if self.body == "wait":
				pass
			if self.body == "AUTHERROR":
				self.msgwarn(_("Invalid User-ID or API-Key or Account expired!"),_("Error: def API_REQUEST"))
				return False
			
			if self.body.isalnum() and len(self.body) <= 128:
				self.debug(1,"def API_REQUEST: self.body = %s"%(self.body))
		
		except requests.exceptions.ConnectionError as e:
			self.debug(1,text = "def API_REQUEST: requests error on: %s = %s" % (API_ACTION,e))
			return False
		except:
			self.msgwarn(_("API requests on: %s failed!") % (API_ACTION),_("Error: def API_REQUEST"))
			return False
		
		if not self.body == False:
			
			if not self.body == "AUTHERROR":
				self.curldata = self.body.split(":")
				if self.curldata[0] == "AUTHOK":
					self.curldata = self.curldata[1]
					self.debug(1,"def API_REQUEST: self.curldata = '%s'" % (self.curldata))
					return True
			else:
				self.msgwarn(_("Invalid User-ID or API-Key or Account expired!"),_("Error: def API_REQUEST"))
				self.body = False
				self.timer_check_certdl_running = False
				return False
			
			if API_ACTION == "getconfigs":
				try:
					fp = open(self.zip_cfg, "wb")
					fp.write(self.body)
					fp.close()
					return True	
				except:
					return False
			
			elif API_ACTION == "getcerts":
				try:
					fp = open(self.zip_crt, "wb")
					fp.write(self.body)
					fp.close()
					return True
				except:
					return False
			
			if API_ACTION == "requestcerts":
				if self.body == "ready" or self.body == "wait" or self.body == "submitted":
					return True

	def check_inet_connection(self):
		self.debug(3,"def check_inet_connection()")
		if self.LAST_CHECK_INET_FALSE > int(time.time())-15:
			return False
		if not self.try_socket(DOMAIN,443) == True:
			self.debug(3,"def check_inet_connection: failed!")
			self.LAST_CHECK_INET_FALSE = int(time.time())
			return False
		return True

	def try_socket(self,host,port):
		self.debug(3,"def try_socket()")
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(3)
			result = s.connect_ex((host, port))
			s.close()
		except:
			return False
		if result == 0:
			self.debug(3,"def try_socket: %s:%s True" % (host,port))
			return True

	def check_myip(self):
		self.debug(3,"def check_myip()")
		# *** fixme *** missing ipv6 support
		if self.OVPN_CONFIGVERSION == "23x" or self.OVPN_CONFIGVERSION == "23x46":
			if self.LAST_CHECK_MYIP > int(time.time())-random.randint(120,300) and self.OVPN_PING_LAST > 0:
				return True
			try:
				url = "http://%s/myip4" % (self.GATEWAY_OVPN_IP4A)
				r = requests.get(url,timeout=2)
				rip = r.content.strip().split()[0]
				if rip == self.OVPN_CONNECTEDtoIP:
					self.debug(1,"def check_myip: rip == self.OVPN_CONNECTEDtoIP")
					self.LAST_CHECK_MYIP = int(time.time())
					return True
			except:
				self.debug(1,"def check_myip: False")
				return False
		else:
			self.debug(1,"def check_myip: invalid self.OVPN_CONFIGVERSION")
			return False

	def load_firewall_backups(self):
		self.debug(1,"def load_firewall_backups()")
		try:
			if os.path.exists(self.pfw_dir):
				content = os.listdir(self.pfw_dir)
				self.FIREWALL_BACKUPS = list()
				for file in content:
					if file.endswith('.bak.wfw'):
						filepath = "%s\\%s" % (self.pfw_dir,file)
						self.FIREWALL_BACKUPS.append(file)
		except:
			self.debug(1,"def load_firewall_backups: failed")

	def load_ovpn_server(self):
		self.debug(1,"def load_ovpn_server()")
		try:
			if os.path.exists(self.VPN_CFG):
				self.debug(1,"def load_ovpn_server: self.VPN_CFG = '%s'" % (self.VPN_CFG))
				content = os.listdir(self.VPN_CFG)
				self.OVPN_SERVER = list()
				self.OVPN_SERVER_INFO = {}
				for file in content:
					if file.endswith('.ovpn.to.ovpn'):
						filepath = "%s\\%s" % (self.VPN_CFG,file)
						servername = file[:-5]
						countrycode = servername[:2].lower()
						servershort = servername[:3].upper()
						if os.path.isfile(filepath):
							#print filepath
							serverinfo = list()
							for line in open(filepath):
								if "remote " in line:
									#print line
									try:
										ip = line.split()[1]
										port = int(line.split()[2])
										# *** fixme need isValueIPv6 first! ***
										if self.isValueIPv4(ip) and port > 0 and port <= 65535:
											serverinfo.append(ip)
											serverinfo.append(port)
									except:
										self.errorquit(text=_("Could not read Servers Remote-IP:Port from config: %s") % (self.ovpn_server_config_file))
								elif "proto " in line:
									#print line
									try:
										proto = line.split()[1]
										if proto.lower()  == "tcp" or proto.lower() == "udp":
											proto = proto.upper()
											serverinfo.append(proto)
									except:
										self.errorquit(text=_("Could not read Servers Protocol from config: %s") % (self.ovpn_server_config_file))
								elif line.startswith("cipher "):
									#elif "cipher " in line:
									#print line
									try:
										cipher = line.split()[1]
										if cipher == "CAMELLIA-256-CBC":
											cipher = "CAM-256"
										elif cipher == "AES-256-CBC":
											cipher = "AES-256"
										serverinfo.append(cipher)
									except:
										self.errorquit(text=_("Could not read Servers Cipher from config: %s") % (self.ovpn_server_config_file))
								if "fragment " in line or "link-mtu " in line:
									#print line
									try:
										mtu = line.split()[1]
										serverinfo.append(mtu)
									except:
										mtu = 1500
										serverinfo.append(mtu)
										self.debug(1,"Could not read mtu from config: %s" % (self.ovpn_server_config_file))
							# end: for line in open(filepath)
							self.OVPN_SERVER_INFO[servershort] = serverinfo
						self.OVPN_SERVER.append(servername)
						self.debug(5,"def load_ovpn_server: file = '%s' END" % (file))
				# for end
				self.OVPN_SERVER.sort()
			else:
				self.reset_last_update()
		except:
			self.debug(1,"def load_ovpn_server: failed")

	def load_remote_data(self):
		if self.timer_load_remote_data_running == True:
			return False
		self.timer_load_remote_data_running = True
		if self.APIKEY == False:
			self.debug(6,"def load_remote_data: no api data")
			self.timer_load_remote_data_running = False
			return False
		elif self.state_openvpn() == True and self.OVPN_CONNECTEDseconds > 0 and self.OVPN_PING_LAST <= 0:
			self.debug(6,"def load_remote_data: waiting for ovpn connection")
			self.timer_load_remote_data_running = False
			return False
		elif self.state_openvpn() == True and self.OVPN_CONNECTEDseconds > 0 and self.OVPN_PING_LAST > 999:
			self.debug(6,"def load_remote_data: high ping")
			self.timer_load_remote_data_running = False
			return False
		elif self.LOAD_SRVDATA == True and self.LOAD_ACCDATA == True:
			if self.load_serverdata_from_remote() == True:
				self.call_redraw_mainwindow()
			if self.load_accinfo_from_remote() == True:
				GLib.idle_add(self.call_redraw_accwindow)
		elif self.LOAD_SRVDATA == True and self.LOAD_ACCDATA == False:
			if self.load_serverdata_from_remote() == True:
				self.call_redraw_mainwindow()
		elif self.LOAD_SRVDATA == False and self.LOAD_ACCDATA == True:
			if self.load_accinfo_from_remote() == True:
				GLib.idle_add(self.call_redraw_accwindow)
		self.timer_load_remote_data_running = False

	def check_hash_dictdata(self,newdata,olddata):
		self.debug(2,"def check_hash_dictdata()")
		try:
			texta = ""
			textb = ""
			for key,value in sorted(newdata.iteritems()):
				texta = "%s %s %s" % (texta,key,value)
			for key,value in sorted(olddata.iteritems()):
				textb = "%s %s %s" % (textb,key,value)
			hasha = hashlib.sha256(texta).hexdigest()
			hashb = hashlib.sha256(textb).hexdigest()
			self.debug(9,"hasha newdata = '%s'" % (hasha))
			self.debug(9,"hashb olddata = '%s'" % (hashb))
			if hasha == hashb:
				return True
		except:
			self.debug(1,"def check_hash_dictdata: failed")

	def load_serverdata_from_remote(self):
		updatein = self.LAST_OVPN_SRV_DATA_UPDATE + self.LOAD_DATA_EVERY
		now = int(time.time())
		self.debug(46,"def load_serverdata_from_remote: ?")
		if self.LOAD_SRVDATA == False:
			self.debug(46,"def load_serverdata_from_remote: disabled")
			return False
		elif self.MAINWINDOW_OPEN == False:
			self.debug(46,"def load_serverdata_from_remote: mainwindow not open")
			return False
		elif self.MAINWINDOW_HIDE == True:
			self.debug(46,"def load_serverdata_from_remote: mainwindow is hide")
			return False
		elif updatein > now:
			diff = updatein - now
			self.debug(46,"def load_serverdata_from_remote: time = %s update_in = %s (%s)" % (now,updatein,diff))
			return False
		elif self.check_inet_connection() == False:
			self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time()) - self.LOAD_DATA_EVERY + 15
			self.debug(46,"def load_serverdata_from_remote: no inet connection")
			return False
		try:
			API_ACTION = "loadserverdata"
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
			r = requests.post(self.APIURL,data=values,timeout=(3,3))
			self.debug(1,"def load_serverdata_from_remote: posted")
			try:
				if not r.content == "AUTHERROR":
					#self.debug(1,"r.content = '%s'" % (r.content))
					OVPN_SRV_DATA = json.loads(r.content)
					self.debug(9,"OVPN_SRV_DATA = '%s'" % (OVPN_SRV_DATA))
					if len(OVPN_SRV_DATA) > 1:
						if not self.check_hash_dictdata(OVPN_SRV_DATA,self.OVPN_SRV_DATA):
							self.OVPN_SRV_DATA = OVPN_SRV_DATA
							self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
							self.debug(1,"def load_serverdata_from_remote: loaded, len = %s" % (len(self.OVPN_SRV_DATA)))
							return True
						else:
							self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
							self.debug(1,"def load_serverdata_from_remote: loaded, hash match")
							return False
					else:
						self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
						self.debug(1,"def load_serverdata_from_remote: failed! len = %s"%(len(OVPN_SRV_DATA)))
						return False
				else:
					self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
					self.debug(1,"def load_serverdata_from_remote: AUTH ERROR")
					self.msgwarn(_("Invalid User-ID or API-Key or Account expired!"),"Error!")
					return False
			except:
				self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
				self.debug(1,"def load_serverdata_from_remote: json decode error")
				return False
		except:
			self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
			self.debug(1,"def load_serverdata_from_remote: api request failed")
			return False

	def load_accinfo_from_remote(self):
		updatein = self.LAST_OVPN_ACC_DATA_UPDATE + self.LOAD_DATA_EVERY
		now = int(time.time())
		self.debug(46,"def load_accinfo_from_remote: ?")
		if self.LOAD_ACCDATA == False:
			self.debug(46,"def load_accinfo_from_remote: disabled")
			return False
		elif self.ACCWINDOW_OPEN == False:
			self.debug(46,"def load_remote_data: mainwindow not open")
			return False
		elif updatein > now:
			diff = updatein - now
			self.debug(46,"def load_accinfo_from_remote: time = %s update_in = %s (%s)" % (now,updatein,diff))
			return False
		elif self.check_inet_connection() == False:
			self.LAST_OVPN_ACC_DATA_UPDATE = now - self.LOAD_DATA_EVERY + 15
			self.debug(46,"def load_accinfo_from_remote: no inet connection")
			return False
		try:
			API_ACTION = "accinfo"
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
			r = requests.post(self.APIURL,data=values,timeout=(2,2))
			self.debug(1,"def load_accinfo_from_remote: posted")
			try:
				if not r.content == "AUTHERROR":
					#self.debug(1,"r.content = '%s'" % (r.content))
					OVPN_ACC_DATA = json.loads(r.content)
					self.debug(9,"OVPN_ACC_DATA = '%s'" % (OVPN_ACC_DATA))
					if len(OVPN_ACC_DATA) > 1:
						if not self.check_hash_dictdata(OVPN_ACC_DATA,self.OVPN_ACC_DATA):
							self.OVPN_ACC_DATA = OVPN_ACC_DATA
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							self.debug(1,"def load_accinfo_from_remote: loaded, len = %s"%(len(self.OVPN_ACC_DATA)))
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							return True
						else:
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							self.debug(1,"def load_accinfo_from_remote: loaded, hash match")
							return False
					else:
						self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
						self.debug(1,"def load_accinfo_from_remote: failed! len = %s"%(len(OVPN_ACC_DATA)))
						return False
				else:
					self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
					self.debug(1,"def load_accinfo_from_remote: AUTH ERROR")
					self.msgwarn(_("Invalid User-ID or API-Key or Account expired!"),"Error: def load_accinfo_from_remote")
					return False
			except:
				self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
				self.debug(1,"def load_accinfo_from_remote: json decode error")
				return False
		except:
			self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
			self.debug(1,"def load_accinfo_from_remote: api request failed")
			return False

	def build_openvpn_dlurl(self):
		self.debug(1,"def build_openvpn_dlurl()")
		self.PLATFORM = self.os_platform()
		if self.PLATFORM == "AMD64":
			self.OPENVPN_FILENAME = "openvpn-install-%s-%s-x86_64.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V)
			self.OPENVPN_FILEHASH = self.OVPN_WIN_SHA512_x64
		elif self.PLATFORM == "x86":
			self.OPENVPN_FILENAME = "openvpn-install-%s-%s-i686.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V)
			self.OPENVPN_FILEHASH = self.OVPN_WIN_SHA512_x86
		else:
			self.OPENVPN_DL_URL = False
			self.msgwarn(_("Platform '%s' not supported") % (self.PLATFORM),_("Error!"))
			return False
		self.OPENVPN_DL_URL = "%s/%s" % (self.OPENVPN_REM_URL,self.OPENVPN_FILENAME)
		self.OPENVPN_DL_URL_ALT = "%s/%s" % (self.OPENVPN_ALT_URL,self.OPENVPN_FILENAME)
		self.OPENVPN_SAVE_BIN_TO = "%s\\%s" % (self.vpn_dir,self.OPENVPN_FILENAME)
		self.OPENVPN_ASC_FILE = "%s.asc" % (self.OPENVPN_SAVE_BIN_TO)
		#print "def build_openvpn_dlurl: PLATFORM=%s url='%s'" % (self.PLATFORM,self.OPENVPN_DL_URL)
		return True

	def upgrade_openvpn(self):
		self.debug(1,"def upgrade_openvpn()")
		if self.load_openvpnbin_from_remote():
			if self.win_install_openvpn():
				self.debug(1,"def upgrade_openvpn: self.win_install_openvpn() = True")
				return True
		if self.verify_openvpnbin_dl():
			self.errorquit(text=_("openVPN Setup downloaded and hash verified OK!\n\nPlease start setup from file:\n'%s'\n\nVerify GPG with:\n'%s'") % (self.OPENVPN_SAVE_BIN_TO,self.OPENVPN_ASC_FILE))
		else:
			self.errorquit(text=_("openVPN Setup downloaded but hash verify failed!\nPlease install openVPN!\nURL1: %s\nURL2: %s") % (self.OPENVPN_DL_URL,self.OPENVPN_DL_URL_ALT))

	def load_openvpnbin_from_remote(self):
		self.debug(1,"def load_openvpnbin_from_remote()")
		if not self.OPENVPN_DL_URL == False:
			if os.path.isfile(self.OPENVPN_SAVE_BIN_TO):
				return self.verify_openvpnbin_dl()
			else:
				self.tray.set_tooltip_markup("%s - Downloading openVPN (1.8 MB)" % (CLIENT_STRING))
				self.debug(1,"Install OpenVPN %s (%s) (%s)\n\nStarting download (~1.8 MB) from:\n'%s'\nto\n'%s'\n\nPlease wait..." % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V,self.PLATFORM,self.OPENVPN_DL_URL,self.OPENVPN_SAVE_BIN_TO))
				try:
					ascfiledl = "%s.asc" % (self.OPENVPN_DL_URL)
					r1 = requests.get(self.OPENVPN_DL_URL)
					r2 = requests.get(ascfiledl)
					fp1 = open(self.OPENVPN_SAVE_BIN_TO, "wb")
					fp1.write(r1.content)
					fp1.close()
					fp2 = open(self.OPENVPN_ASC_FILE, "wb")
					fp2.write(r2.content)
					fp2.close()
					self.tray.set_tooltip_markup("%s - Verify openVPN" % (CLIENT_STRING))
					return self.verify_openvpnbin_dl()
				except:
					self.debug(1,"def load_openvpnbin_from_remote: failed")
					return False
		else:
			return False

	def verify_openvpnbin_dl(self):
		self.debug(1,"def verify_openvpnbin_dl()")
		if os.path.isfile(self.OPENVPN_SAVE_BIN_TO):
			localhash = self.hash_sha512_file(self.OPENVPN_SAVE_BIN_TO)
			if self.OPENVPN_FILEHASH == localhash:
				self.debug(1,"def verify_openvpnbin_dl: file = '%s' localhash = '%s' OK" % (self.OPENVPN_SAVE_BIN_TO,localhash))
				return True
			else:
				self.msgwarn(_("Invalid File hash: %s !\nlocalhash = '%s'\nbut should be = '%s'") % (self.OPENVPN_SAVE_BIN_TO,localhash,self.OPENVPN_FILEHASH),_("Error!"))
				try:
					os.remove(self.OPENVPN_SAVE_BIN_TO)
				except:
					self.msgwarn(_("Failed remove file: %s") % (self.OPENVPN_SAVE_BIN_TO),_("Error!"))
				self.tray.set_tooltip_markup("%s - Verify openVPN failed" % (CLIENT_STRING))
				return False
		else:
			return False

	def win_install_openvpn(self):
		self.debug(1,"def win_install_openvpn()")
		self.tray.set_tooltip_markup("%s - Install openVPN" % (CLIENT_STRING))
		if self.OPENVPN_SILENT_SETUP == True:
			# silent install
			installtodir = "%s\\runtime" % (self.vpn_dir)
			options = "/S /SELECT_SHORTCUTS=0 /SELECT_OPENVPN=1 /SELECT_SERVICE=0 /SELECT_TAP=1 /SELECT_OPENVPNGUI=0 /SELECT_ASSOCIATIONS=0 /SELECT_OPENSSL_UTILITIES=0 /SELECT_EASYRSA=0 /SELECT_PATH=1"
			parameters = '%s /D=%s' % (options,installtodir)
			netshcmd = '"%s" %s' % (self.OPENVPN_SAVE_BIN_TO,parameters)
			self.debug(1,"def win_install_openvpn: silent cmd =\n'%s'" % (netshcmd))
			self.OPENVPN_DIR = installtodir
		else:
			# popup install
			netshcmd = '"%s"' % (self.OPENVPN_SAVE_BIN_TO)
		self.debug(1,"def win_install_openvpn: '%s'" % (self.OPENVPN_SAVE_BIN_TO))
		try: 
			exitcode = subprocess.call(netshcmd,shell=True)
			if exitcode == 0:
				if self.OPENVPN_SILENT_SETUP == True:
					self.debug(1,"def win_install_openvpn: silent OK!")
				else:
					self.debug(1,"def win_install_openvpn:\n\n'%s'\n\nexitcode = %s" % (netshcmd,exitcode))
				return True
			else:
				self.debug(1,"def win_install_openvpn: '%s' exitcode = %s" % (netshcmd,exitcode))
				return False
		except:
			self.debug(1,"def win_install_openvpn: '%s' failed" % (netshcmd))
			return False

	def win_select_openvpn(self):
		self.debug(1,"def win_select_openvpn()")
		self.msgwarn(_("OpenVPN not found!\n\nPlease select openvpn.exe on next window!\n\nIf you did not install openVPN yet: click cancel on next window!"),_("Setup: openVPN"))
		dialogWindow = Gtk.FileChooserDialog(_("Select openvpn.exe or Cancel to install openVPN"),None,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialogWindow.set_position(Gtk.WindowPosition.CENTER)
		dialogWindow.set_default_response(Gtk.ResponseType.OK)
		filter = Gtk.FileFilter()
		filter.set_name("openvpn.exe")
		filter.add_pattern("openvpn.exe")
		dialogWindow.add_filter(filter)
		try:
			response = dialogWindow.run()
			if response == Gtk.ResponseType.OK:
				dialogWindow.destroy()
				self.OPENVPN_EXE = dialog.get_filename()
				self.debug(1,"selected: %s" % (self.OPENVPN_EXE))
				return True
			else:
				dialogWindow.destroy()
				self.debug(1,"Closed, no files selected")
				return False
		except:
			return False

	def win_detect_openvpn(self):
		self.debug(1,"def win_detect_openvpn()")
		if self.OPENVPN_DIR == False:
			os_programfiles = "PROGRAMFILES PROGRAMFILES(x86) PROGRAMW6432"
			for getenv in os_programfiles.split():
				programfiles = os.getenv(getenv)
				OPENVPN_DIR = "%s\\OpenVPN\\bin" % (programfiles)
				file = "%s\\openvpn.exe" % (OPENVPN_DIR)
				if os.path.isfile(file):
					self.debug(1,"def win_detect_openvpn: %s" % (file))
					self.OPENVPN_EXE = file
					self.OPENVPN_DIR = OPENVPN_DIR
					break
		elif os.path.isdir(self.OPENVPN_DIR):
			file = "%s\\bin\\openvpn.exe" % (self.OPENVPN_DIR)
			if os.path.isfile(file):
				self.OPENVPN_EXE = file
			else:
				self.OPENVPN_DIR = False
		if self.OPENVPN_DIR == False and not self.OPENVPN_EXE == False:
			self.OPENVPN_DIR = self.OPENVPN_EXE.rsplit('\\', 1)[0]
		if self.OPENVPN_EXE == False or (not os.path.isfile(self.OPENVPN_EXE) or self.OPENVPN_EXE == False):
			if not self.win_select_openvpn():
				if self.upgrade_openvpn():
					self.win_detect_openvpn()
		if not self.openvpn_check_files():
			self.msgwarn(_("WARNING! Failed to verify files in\n'%s'\n\nUninstall openVPN and restart oVPN Client Software!\n\nOr install openVPN from URL:\n%s[debug self.LAST_FAILED_CHECKFILE = '%s']") % (self.OPENVPN_DIR,self.OPENVPN_DL_URL,self.LAST_FAILED_CHECKFILE),_("Error!"))
		self.debug(1,"def win_detect_openvpn: self.OPENVPN_EXE = '%s'" % (self.OPENVPN_EXE))
		try:
			out, err = subprocess.Popen("\"%s\" --version" % (self.OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()
		except:
			self.errorquit(text=_("Could not detect openVPN Version!"))
		try:
			self.OVPN_VERSION = out.split('\r\n')[0].split( )[1].replace(".","")
			self.OVPN_BUILT = out.split('\r\n')[0].split("built on ",1)[1].split()
			self.OVPN_LATESTBUILT = self.OVPN_LATEST_BUILT.split()
			self.debug(1,"self.OVPN_VERSION = %s, self.OVPN_BUILT = %s, self.OVPN_LATESTBUILT = %s" % (self.OVPN_VERSION,self.OVPN_BUILT,self.OVPN_LATESTBUILT))
			if self.OVPN_VERSION >= self.OVPN_LATEST:
				if self.OVPN_BUILT == self.OVPN_LATESTBUILT:
					self.debug(1,"self.OVPN_BUILT == self.OVPN_LATESTBUILT: True")
					return True
				else:
					built_mon = self.OVPN_BUILT[0]
					built_day = int(self.OVPN_BUILT[1])
					built_year = int(self.OVPN_BUILT[2])
					builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
					string_built_time = time.strptime(builtstr,"%b/%d/%Y")
					built_month_int = int(string_built_time.tm_mon)
					built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					self.debug(1,"openvpn built_timestamp = %s self.OVPN_LATESTBUILT_TIMESTAMP = %s" % (built_timestamp,self.OVPN_LATEST_BUILT_TIMESTAMP))
					if built_timestamp > self.OVPN_LATEST_BUILT_TIMESTAMP:
						self.CHECK_FILEHASHS = False
						return True
			self.upgrade_openvpn()
		except:
			self.errorquit(text=_("Could not find openVPN"))

	def openvpn_check_files(self):
		self.debug(1,"def openvpn_check_files()")
		try:
			if self.CHECK_FILEHASHS == False:
				return True
			self.OPENVPN_DIR = self.OPENVPN_EXE.rsplit('\\', 1)[0]
			self.debug(1,"def openvpn_check_files: self.OPENVPN_DIR = '%s'" % (self.OPENVPN_DIR))
			dir = self.OPENVPN_DIR
			if os.path.exists(dir):
				content = os.listdir(dir)
				filename = self.openvpn_filename_exe()
				hashs = self.OPENVPN_FILEHASHS[filename]
				self.debug(2,"hashs = '%s'" % (hashs))
				for file in content:
					self.LAST_FAILED_CHECKFILE = file
					if file.endswith('.exe') or file.endswith('.dll'):
						filepath = "%s\\%s" % (dir,file)
						hasha = self.hash_sha512_file(filepath)
						hashb = hashs[file]
						if hasha == hashb:
							self.debug(1,"def openvpn_check_files: hash '%s' OK!" % (file))
						else:
							self.msgwarn(_("Invalid Hash: '%s'! is '%s' != '%s'") % (filepath,hasha,hashb),_("Error!"))
							return False
					else:
						self.msgwarn(_("Invalid content '%s' in '%s'") % (file,self.OPENVPN_DIR),_("Error!"))
						return False
				return True
			else:
				self.debug(1,"Error: '%s' not found!" % (self.OPENVPN_DIR))
				return False
		except:
			self.debug(1,"def openvpn_check_files: failed!")
			return False

	def openvpn_filename_exe(self):
		self.debug(1,"def openvpn_filename_exe()")
		if self.PLATFORM == "AMD64":
			arch = "x86_64"
		elif self.PLATFORM == "x86":
			arch = "i686"
		else:
			self.errorquit(_("arch '%s' not supported!") % (self.PLATFORM))
		self.debug(1,"def openvpn_filename_exe: arch = '%s'" % (arch))
		return "openvpn-install-%s-%s-%s.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V,arch)

	def os_platform(self):
		self.debug(1,"def os_platform()")
		true_platform = os.environ['PROCESSOR_ARCHITECTURE']
		try:
			true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
		except KeyError:
			pass
			#true_platform not assigned to if this does not exist
		return true_platform

	def check_dns_is_whitelisted(self):
		self.debug(1,"def check_dns_is_whitelisted()")
		#if self.GATEWAY_DNS1 == "127.0.0.1" or self.GATEWAY_DNS1 == self.GATEWAY_OVPN_IP4 or self.GATEWAY_DNS1 == "8.8.8.8" or self.GATEWAY_DNS1 == "8.8.4.4" or self.GATEWAY_DNS1 == "208.67.222.222" or self.GATEWAY_DNS1 == "208.67.220.220" or self.GATEWAY_DNS1 in self.d0wns_DNS:
		if self.GATEWAY_DNS1 == "127.0.0.1":
			self.debug(1,"def check_dns_is_whitelisted: True")
			return True
		else:
			self.debug(1,"def check_dns_is_whitelisted: False")
			return False

	def read_d0wns_dns(self):
		self.debug(1,"def read_d0wns_dns()")
		if self.NO_DNS_CHANGE == True:
			return True
		if not os.path.isfile(self.dns_d0wntxt):
			if not self.load_d0wns_dns_from_remote() == True:
				return False
		if os.path.isfile(self.dns_d0wntxt):
			try:
				fp = open(self.dns_d0wntxt,'r')
				dnsdata = fp.read().split('\n')
				fp.close()
				#print dnsdata
				self.d0wns_DNS = {}
				for entry in dnsdata:
					if len(entry) > 0:
						data = entry.split(",")
						
						name = data[0]
						ip4 = data[1]
						ip6 = data[2]
						country = data[3]
						dnscryptfingerprint = data[4]
						dnscryptcertname = data[5]
						dnscryptports = data[6]
						#dnscryptvalidto = data[7]
						dnscryptpubkey = data[8]
						active = data[12]
						if active == "1" and self.check_d0wns_names(name) == True and self.isValueIPv4(ip4) == True and self.check_d0wns_dnscountry(country) == True and self.check_d0wns_dnscryptfingerprint(dnscryptfingerprint) == True and self.check_d0wns_names(dnscryptcertname) == True and self.check_d0wns_dnscryptports(dnscryptports) == True:
							self.d0wns_DNS[name].update({"ip4":ip4,"ip6":ip6,"country":country,"dnscryptfingerprint":dnscryptfingerprint,"dnscryptcertname":dnscryptcertname,"dnscryptports":dnscryptports,"dnscryptpubkey":dnscryptpubkey})
						elif active == "0":
							self.debug(1,"def read_d0wns_dns: offline '%s'" % (name))
						else:
							self.debug(1,"def read_d0wns_dns: failed '%s'" % (data))
				self.debug(1,"def read_d0wns_dns: True len(self.d0wns_DNS) = %s" % (len(self.d0wns_DNS)))
				return True
			except:
				self.debug(1,"def read_d0wns_dns: failed!")
		else:
			self.debug(1,"def read_d0wns_dns: file '%s' not found" % (self.dns_d0wntxt))

	def check_d0wns_dnscryptports(self,value):
		self.debug(59,"def check_d0wns_dnscryptports()")
		try:
			data = value.split()
			for entry in data:
				entry = int(entry)
				if entry > 0 and entry <= 65535:
					return True
				else:
					self.debug(1,"def check_d0wns_dnscryptports: failed value '%s'" % (value))
					return False
			return True
		except:
			return False

	def check_d0wns_names(self,name):
		self.debug(59,"def check_d0wns_names()")
		try:
			data = name.split('.')
			#print "def check_d0wns_names: data = '%s' len(data)='%s'" % (data,len(data))
			if len(data) == 5:
				if data[0].startswith("ns") and data[0].isalnum() and data[1].isalnum() and data[2].isalnum() and data[3].isalnum() and data[4].isalnum():
					self.d0wns_DNS[name] = {"countrycode":data[1]}
					return True
				elif data[0] == "2" and data[1] == "dnscrypt-cert" and data[2].isalnum() and data[3].isalnum() and data[4].isalnum():
					return True
				else:
					self.debug(1,"def check_d0wns_names: name failed value '%s'" % (name))
		except:
			return False

	def check_d0wns_dnscountry(self,value):
		self.debug(59,"def check_d0wns_dnscountry()")
		try:
			if not value.isalnum():
				data = value.split()
				for entry in data:
					if not entry.isalnum():
						self.debug(1,"def check_d0wns_dnscountry: '%s' failed" % (value))
						return False
			return True
		except:
			return False

	def check_d0wns_dnscryptfingerprint(self,value):
		self.debug(59,"def check_d0wns_dnscryptfingerprint()")
		try:
			if len(value) == 79:
				for toc in value.split(':'):
					if not len(toc) == 4 or not toc.isalnum():
						self.debug(1,"def check_d0wns_dnscryptfingerprint: value = '%s' toc '%s'"%(value,toc))
						return False
				self.debug(59,"def check_d0wns_dnscryptfingerprint: True")
				return True
			else:
				self.debug(1,"def check_d0wns_dnscryptfingerprint: len value = %s" % (len(value)))
		except:
			return False

	def load_d0wns_dns_from_remote(self):
		return
		self.debug(1,"def load_d0wns_dns_from_remote()")
		try:
			if not os.path.isfile(self.dns_d0wntxt):
				try:
					url = "https://%s/files/dns/d0wns_dns.txt" % (DOMAIN)
					r = requests.get(url)
					fp = open(self.dns_d0wntxt,'wb')
					fp.write(r.content)
					fp.close()
					self.debug(1,"def load_d0wns_dns_from_remote: True")
					return True
				except:
					return False
			else:
				return True
		except:
			return False

	def show_about_dialog(self,widget,event):
		self.debug(1,"def show_about_dialog()")
		self.destroy_systray_menu()
		if self.WINDOW_ABOUT_OPEN == True:
			self.about_dialog.destroy()
			return True
		try:
			self.WINDOW_ABOUT_OPEN = True
			self.about_dialog = Gtk.AboutDialog()
			self.about_dialog.set_position(Gtk.WindowPosition.CENTER)
			try:
				self.about_dialog.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			self.about_dialog.set_logo(self.app_icon)
			self.about_dialog.set_program_name("oVPN.to Client")
			self.about_dialog.set_website("https://ovpn.to")
			self.about_dialog.set_website_label("oVPN.to")
			self.about_dialog.set_transient_for(self.window)
			self.about_dialog.set_destroy_with_parent (True)
			self.about_dialog.set_name('oVPN.to')
			self.about_dialog.set_version(CLIENTVERSION)
			self.about_dialog.set_copyright('(C) 2010 - 2016 oVPN.to')
			self.about_dialog.set_comments((ABOUT_TEXT))
			self.about_dialog.set_authors(['oVPN.to [ support@ovpn.to ]'])
			response = self.about_dialog.run()
			self.about_dialog.destroy()
			if not response == None:
				self.debug(1,"def show_about_dialog: response = '%s'" % (response))
				self.WINDOW_ABOUT_OPEN = False
		except:
			self.debug(1,"def show_about_dialog: failed")

	def on_closing(self,widget,event):
		self.debug(1,"def on_closing()")
		self.destroy_systray_menu()
		if self.WINDOW_QUIT_OPEN == True:
			self.QUIT_DIALOG.destroy()
			return False
		self.WINDOW_QUIT_OPEN = True
		if self.state_openvpn() == True:
			return False
		else:
			try: 
				self.about_dialog.destroy()
				self.WINDOW_ABOUT_OPEN = False
			except:
				pass
			try:
				self.dialogWindow_form_ask_passphrase.destroy()
			except:
				pass
			try:
				self.destroy_mainwindow()
			except:
				pass
			try:
				self.destroy_accwindow()
			except:
				pass
			try:
				self.destroy_settingswindow()
			except:
				pass
			try:
				dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
				dialog.set_position(Gtk.WindowPosition.CENTER)
				dialog.set_title(_("Quit oVPN.to Client"))
				try:
					dialog.set_icon_from_pixbuf(self.app_icon)
				except:
					pass
				dialog.set_transient_for(self.window)
				self.QUIT_DIALOG = dialog
				dialog.set_markup(_("Do you really want to quit?"))
				response = dialog.run()
				dialog.destroy()
				if response == Gtk.ResponseType.NO:
					self.WINDOW_QUIT_OPEN = False
					return False
				elif response == Gtk.ResponseType.YES:
					if self.ask_loadorunload_fw() == False:
						dialog.destroy()
						self.WINDOW_QUIT_OPEN = False
						return False
					dialog.destroy()
				else:
					dialog.destroy()
					self.WINDOW_QUIT_OPEN = False
					return False
			except:
				pass
			if self.TAP_BLOCKOUTBOUND == True:
				self.win_firewall_whitelist_ovpn_on_tap(option="delete")
			if self.WIN_FIREWALL_ADDED_RULE_TO_VCP == True:
				self.win_firewall_add_rule_to_vcp(option="delete")
			self.debug(1,"close app")
			self.stop_systray_timer = True
			self.stop_systray_timer2 = True
			self.remove_lock()
			Gtk.main_quit()
			sys.exit()

	def ask_loadorunload_fw(self):
		self.debug(1,"def ask_loadorunload_fw()")
		if self.NO_WIN_FIREWALL == True:
			return True
		try:
			if self.WIN_DONT_ASK_FW_EXIT == True:
				self.win_enable_ext_interface()
				if self.WIN_BACKUP_FIREWALL == True and self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
					self.win_firewall_restore_on_exit()
					self.win_firewall_block_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(1,"Firewall rules restored and block outbound!")
					return True
				elif self.WIN_BACKUP_FIREWALL == True and self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == False:
					self.win_firewall_restore_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(1,"Firewall: rules restored!")
					return True
				elif self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
					self.win_firewall_block_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(1,"Firewall: block outbound!")
					return True
				elif self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == False:
					self.win_firewall_allowout()
					self.win_netsh_restore_dns_from_backup()
					self.debug(1,"Firewall: allow outbound!")
					return True
			else:
				try:
					self.dialog_ask_loadorunload_fw.destroy()
				except:
					pass
				try:
					dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
					self.dialog_ask_loadorunload_fw = dialog
					dialog.set_position(Gtk.WindowPosition.CENTER)
					dialog.set_title(_("Firewall Settings"))
					try:
						dialog.set_icon_from_pixbuf(self.app_icon)
					except:
						pass
					dialog.set_transient_for(self.window)
					if self.WIN_BACKUP_FIREWALL == True:
						text = _("Restore previous firewall settings?\n\nPress 'YES' to restore your previous firewall settings!\nPress 'NO' to set profiles to 'blockinbound,blockoutbound'!")
						dialog.set_markup()
					else:
						text = _("Allow outgoing connection to internet?\n\nPress 'YES' to set profiles to 'blockinbound,allowoutbound'!\nPress 'NO' to set profiles to 'blockinbound,blockoutbound'!")
					dialog.set_markup(text)
					self.debug(1,"def ask_loadorunload_fw: text = '%s'" % (text))
					response = dialog.run()
					self.debug(1,"def ask_loadorunload_fw: dialog response = '%s'" % (response))
					if response == Gtk.ResponseType.NO:
						dialog.destroy()
						self.debug(1,"def ask_loadorunload_fw: dialog response = NO '%s'" % (response))
						self.win_firewall_block_on_exit()
						self.win_netsh_restore_dns_from_backup()
						return True
					elif response == Gtk.ResponseType.YES:
						dialog.destroy()
						self.debug(1,"def ask_loadorunload_fw: dialog response = YES '%s'" % (response))
						if self.WIN_BACKUP_FIREWALL == True:
							self.win_firewall_restore_on_exit()
						else:
							self.win_firewall_allowout()
						self.win_netsh_restore_dns_from_backup()
						return True
					else:
						dialog.destroy()
						self.debug(1,"def ask_loadorunload_fw: dialog response = ELSE '%s'" % (response))
						return False
				except:
					self.debug(1,"def ask_loadorunload_fw: dialog failed")
					return False
		except:
			self.debug(1,"def ask_loadorunload_fw: failed")
			return False

	def remove_lock(self):
		self.debug(1,"def remove_lock()")
		try:
			LOCKFILE = self.lock_file
		except:
			return True
		if os.path.isfile(LOCKFILE):
			self.LOCK.close()
			self.debug(1,"def remove_lock: self.LOCK.close()")
			try:
				os.remove(LOCKFILE)
				self.debug(1,"def remove_lock: os.remove(LOCKFILE)")
				return True
			except:
				self.debug(1,"def remove_lock: remove lock failed!")
				return False
		else:
			self.debug(1,"def remove_lock: lock not found!")
			return False

	def errorquit(self,text):
		if self.DEBUG == False:
			self.DEBUG = True
		self.debug(1,"errorquit: %s" % (text))
		try:
			message = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
			message.set_position(Gtk.WindowPosition.CENTER)
			message.set_title(_("Error"))
			try:
				message.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			message.set_markup("%s"%(text))
			message.run()
			message.destroy()
		except:
			self.debug(1,"%s failed" % (text))
		sys.exit()

	def debug(self,level,text):
		#if not level <= self.LOGLEVEL:
		#	return False
		if not level in self.LOGLEVELS:
			return False
		timefromboot = round(time.time() - self.BOOTTIME,3)
		debugstringsht = False
		debugstringsht1 = False
		debugstringsht2 = False
		if self.DEBUGcount > 0 and not self.DEBUGfrombefore == text:
			debugstringsht1 = "(%s):(d1) %s (repeat: %s)" % (timefromboot, self.DEBUGfrombefore,self.DEBUGcount)
			debugstringsht2 = "(%s):(d2) %s" % (timefromboot,text)
			print(debugstringsht1)
			print(debugstringsht2)
			self.DEBUGcount = 0
		elif self.DEBUGcount >= 4096 and self.DEBUGfrombefore == text:
			debugstringsht = "(%s):(d3) %s (repeated: %s e2)" % (timefromboot, self.DEBUGfrombefore,self.DEBUGcount)
			print("%s" % (debugstringsht))
			self.DEBUGcount = 0
		elif self.DEBUGfrombefore == text:
			self.DEBUGcount += 1
			return
		elif not self.DEBUGfrombefore == text:
			debugstringsht = "(%s):(d4) %s"%(timefromboot,text)
			print("%s" % (debugstringsht))
		self.DEBUGfrombefore = text
		if not debugstringsht == False:
			self.write_debug(level,debugstringsht,timefromboot)
		if not debugstringsht1 == False:
			self.write_debug(level,debugstringsht1,timefromboot)
		if not debugstringsht2 == False:
			self.write_debug(level,debugstringsht2,timefromboot)

	def write_debug(self,level,string,timefromboot):
		try:
			if self.DEBUG == True and not self.debug_log == False:
				localtime = time.asctime(time.localtime(time.time()))
				debugstringlog = "%s (%s):(d5) %s"%(localtime,timefromboot,string)
				dbg = open(self.debug_log,'a')
				dbg.write("%s\n" % (debugstringlog))
				dbg.close()
		except:
			print("def write_debug: write to %s failed"%(self.debug_log))

	def init_theme(self):
		get_settings = Gtk.Settings.get_default()
		get_settings.set_property("gtk-theme-name", self.APP_THEME)
		get_settings.set_property("gtk-font-name", self.APP_FONT_SIZE)
		return True

	def init_localization(self,LANG):
		try:
			if not LANG == None:
				loc = LANG
				os.environ['LANGUAGE'] = loc
				os.environ['LANG'] = loc
				os.putenv(loc, 'LANG')
			else:
				try:
					loc = locale.getdefaultlocale()[0][0:2]
					self.debug(1,"def init_localization: OS LANGUAGE %s"% (loc))
				except:
					self.debug(1,"def init_localization: locale.getdefaultlocale() failed")
					loc = False
			
			filename1 = "%s\\locale\\%s\\ovpn_client.mo" % (os.getcwd(),loc)
			filename2 = "E:\\Persoenlich\\ovpn-client\\locale\\%s\\ovpn_client.mo" % (loc)
			
			if not loc == "en" and os.path.isfile(filename1):
				filename = filename1
			elif not loc == "en" and os.path.isfile(filename2):
				filename = filename2
			else:
				filename = False
			self.debug(1,"def init_localization: filename = '%s'"% (filename))
			translation = False
			try:
				if not filename == False:
					translation = gettext.GNUTranslations(open(filename, "rb"))
			except:
				self.debug(1,"def init_localization: %s not found, fallback to en"% (filename))
			if translation == False or filename == False:
				translation = gettext.NullTranslations()
			try:
				translation.install()
			except:
				self.debug(1,"def init_localization: translation.install() failed")
				return False
			self.APP_LANGUAGE = loc
			self.debug(1,"def init_localization: return self.APP_LANGUAGE = '%s'"% (self.APP_LANGUAGE))
			return True
		except:
			self.debug(1,"def init_localization: failed")

	def msgwarn(self,text,title):
		GLib.idle_add(self.msgwarn_glib,text,title)

	def msgwarn_glib(self,text,title):
		try:
			self.msgwarn_window.destroy()
		except:
			pass
		self.debug(1,"def msgwarn: %s"% (text))
		try:
			self.LAST_MSGWARN_WINDOW = int(time.time())
			self.debug(1,"def msgwarn: %s"% (text))
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
			self.msgwarn_window = dialogWindow
			dialogWindow.set_position(Gtk.WindowPosition.CENTER)
			dialogWindow.set_title(title)
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_pixbuf(self.app_icon)
			except:
				pass
			dialogWindow.set_markup("%s"%(text))
			dialogWindow.run()
			dialogWindow.destroy()
		except:
			self.debug(1,"def msgwarn_glib: failed")

	def statusicon_size_changed(widget, size):
		self.debug(1,"def statusicon_size_changed() size = '%s'" % (size))

	def decode_icon(self,icon):
		#self.debug(49,"def decode_icon()")
		try:
			try:
				imgpixbuf = self.ICON_CACHE_PIXBUF[icon]
				if isinstance(imgpixbuf, GdkPixbuf.Pixbuf):
					self.debug(49,"def decode_icon: isinstance self.ICON_CACHE_PIXBUF[%s]"%(icon))
					return imgpixbuf
			except:
				try:
					self.debug(49,"def decode_icon(%s)" % (icon))
					base64_data = base64.b64decode(self.base64_icons(icon))
					base64_stream = Gio.MemoryInputStream.new_from_data(base64_data)
					imgpixbuf = GdkPixbuf.Pixbuf.new_from_stream(base64_stream)
					self.ICON_CACHE_PIXBUF[icon] = imgpixbuf
					return imgpixbuf
				except:
					return False
		except:
			self.debug(1,"def decode_icon: '%s' failed"%(icon))

	def decode_flag(self,flag):
		#self.debug(48,"def decode_flag()")
		try:
			try:
				imgpixbuf = self.FLAG_CACHE_PIXBUF[flag]
				if isinstance(imgpixbuf, GdkPixbuf.Pixbuf):
					self.debug(48,"def decode_flag: isinstance self.FLAG_CACHE_PIXBUF[%s] return"%(flag))
					return imgpixbuf
			except:
				try:
					self.debug(48,"def decode_flag(%s)" % (flag))
					flagfile = "%s.png" % (flag)
					base64_flag = self.FLAGS_B64[flagfile]
				except:
					base64_flag = self.FLAGS_B64["00.png"]
				base64_data = base64.b64decode(base64_flag)
				base64_stream = Gio.MemoryInputStream.new_from_data(base64_data)
				imgpixbuf = GdkPixbuf.Pixbuf.new_from_stream(base64_stream)
				self.FLAG_CACHE_PIXBUF[flag] = imgpixbuf
				return imgpixbuf
		except:
			self.debug(1,"def decode_flag: '%s' failed"%(flag))

	def base64_icons(self, icon):
		self.debug(1,"def base64_icons(%s)"%(icon))

		# else/app_icons/app_icon.ico
		app_icon_b64 = """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"""

		# else/app_icons/connect.ico
		connect_b64 = """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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA///////////////////////4H//gAAf/wAAB/44AAP+eAAD/HAAAfzwAAD+YAAA/mAAAH8gAAB/AAAAf4AAAD/AAAAf4AAAX+AAAG/gAADn4AAA9/AAAPf4AAHn/AADz/4AAB//AAD//8A////////////////////////////8="""

		# else/app_icons/connected_classic.ico
		connected_classic_b64 = """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"""

		# else/app_icons/testing.ico
		testing_b64 = """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"""

		# else/app_icons/disconnect1.ico
		disconnect1_b64 = """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"""

		# else/app_icons/disconnect1_menu.ico
		disconnect1_menu_b64 = """AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAAAAAAAAAAAAG1tOQD///8ArqyUFLGvq1Kqp7OPpqS4rKemtamsq6+FoqKaRVhYSQ2jo5AAAAAAAAAAAAAAAAAAAAAAAKqnlAClonwEube4TZ2bx792dc/0Xl7V/1pZ2P9iYtn/enrb/qCg2u2vrr+rg4F7NwAAAAEZGBUAAAAAAKuonwC1sokEsK26cHl3ze85OdX/KSnX/y4u2P80NNn/Ozvb/0FB3P9NTd3/cnLc/56dwN2Fg4BOAAAAABIREQC9uNsAtrK4V3FvzPEjI9T/Hx/U/yMj1f8oKNb/LS3X/zMz2P85Odr/QEDb/0ZG3f9iYtv/mJa523BuZzSWk5EAyMSwHo6Lx8wsK9P/HBzT/yAg0/8qKtH/LS3S/zEx0/82NtT/OzvV/z8/1/8+Ptr/Q0Pd/21s1P+SkJyiBAMACby4v21tbNP6JibV/x8f0/87O9P/rq7Y/7W11v+ystL/r6/P/6+vzP+QkMz/OjrX/zs72v9GRtv/iIa653BtYjqvrceyamrc/0FB2v8oKNX/SUnW/9ra5P/j4+D/3Nza/9bW1P/S0s7/p6fM/zMz1f8yMtj/Nzfa/25tyPyHg4JzrKnM1HJy4P9fX9//RUXa/1VV2f/f3+n/5+fm/+Dg4P/a2tr/1tbU/6enzv8tLdP/KirW/y4u2P9bWsz/jImPkrGuztWCguP/cXHj/2Nj4P90dOD/5+fw/+3t7P/m5ub/4ODg/9zc2v+pqdH/KCjS/yMj1f8mJtb/VFPL/46KkZK7uc24lJTk/4KC5v91deP/h4fl/+/v9v/19fT/7u7u/+jo5//k5OH/r6/W/ygo0f8iItX/JSXW/2Fgx/yRjY1wyMXLdqmo4PySkun/hobn/5OT6P/o6Pf/6+v1/+bm8f/g4Oz/3Nzn/7Cw3P9DQ9f/Pj7a/0VF2v+LicPmkI2CNs/MxSXAvtrVoqLq/5aW6v+QkOj/k5Po/4qK5v9/f+P/dXXg/2xs3v9fX9z/SUnb/0ND2/9lZdb/pqO2nk1LLAb///8A2djcZMXE7PakpOz/mprq/4+P6P+EhOb/eHjk/2xs4v9hYeD/V1fe/05P3f9YWNn/nJrH2aypoi+6t7cA5uXiAOvr3gfp6fCAxsXr9amp6v+enuv/lZXq/4qK6P9+fuX/cnLj/2dn4f9xcNv/npzL3bazs0n///8Ab25vAAAAAADo5+AA7u7hB9vZ3FzFw9rNtbTg+amo5f+enub/lpbk/5SU3/+endbxsa/HrLq2sjQAAAAAko+GAAAAAAAAAAAAAAAAAMjGrQCGhQAA0M7FG8zKzGLFws6fv73Nur27zLS/vMeNwL27R7m1owzGw7oATkwrAAAAAAAAAAAA8A8AAMADAACAAQAAgAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAEAAIADAADAAwAA4A8AAA=="""

		# else/app_icons/disconnect2.ico
		disconnect2_b64 = """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uP+1tbX/sbGx/6ysrP+oqKj/pqam/6SkpP+kpKT/oaGh/5ycnP+bm5v/mpqarYqKigSampoAj4+PAJGRkTGOjo7tiIiI/42Njf+Xl5f/n5+f/6ysrP+xsbH/s7Oz/7W1tf+3t7f/ubm5/7q6uv+8vLz/vb29/729vf+9vb3/vLy8/7u7u/+3t7f/srKy/6ysrP+oqKj/p6en/6ioqP+enp7/mJiY/5ycnP+bm5vPk5OTEpeXlwCPj48AkZGRRYyMjPiHh4f/jo6O/5iYmP+hoaH/rq6u/7S0tP+3t7f/vr6+/729vf+9vb3/vr6+/8DAwP/AwMD/wMDA/8DAwP+/v7//v7+//7y8vP+4uLj/sbGx/6ysrP+qqqr/rKys/6Ghof+ampr/mpqa/5mZmd+SkpIdk5OTAJCQkACQkJBKjIyM+omJif+VlZX/mZmZ/6Wlpf+xsbH/uLi4/7y8vP/AwMD/wcHB/8PDw//ExMT/xcXF/8TExP/Dw8P/wsLC/8LCwv/BwcH/wMDA/729vf+3t7f/sLCw/66urv+7u7v/tLS0/6mpqf+ioqL/oKCg4JOTkx6VlZUAlZWVAJaWlkWQkJD4jY2N/5iYmP+ioqL/qamp/7S0tP+8vLz/wcHB/8XFxf/Jycn/y8vL/8zMzP/MzMz/ysrK/8jIyP/Gxsb/xcXF/8TExP/Dw8P/wMDA/7y8vP+0tLT/tra2/8nJyf/Hx8f/vLy8/7Kysv+srKzempqaHZycnACYmJgAmpqaMZSUlO2QkJD/m5ub/6Wlpf+rq6v/uLi4/8HBwf/IyMj/zs7O/9PT0//W1tb/19fX/9bW1v/U1NT/09PT/83Nzf/Jycn/yMjI/8bGxv/Dw8P/v7+//7m5uf+3t7f/x8fH/8HBwf+/v7//wMDA/7q6us2ioqIRqKioAJ2dnQCenp4Yl5eX1pSUlP+cnJz/pqam/6+vr/+4uLj/w8PD/8/Pz//Y2Nj/3t7e/+Pj4//k5OT/4uLi/+Dg4P/g4OD/19fX/83Nzf/Ly8v/ycnJ/8bGxv/BwcH/vLy8/7a2tv/Dw8P/xsbG/7+/v//FxcX/vb29q4iIiASvr68ApKSkAKioqASbm5unmZmZ/5+fn/+lpaX/pqam/66urv++vr7/09PT/+Pj4//s7Oz/8/Pz//b29v/x8fH/6urq/+Pj4//Z2dn/0tLS/87O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"""

		# else/app_icons/disconnect3.ico
		disconnect3_b64 = """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"""

		# else/app_icons/disconnect3_menu.ico
		disconnect3_menu_b64 = """AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAQAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVdWViGSjY1gnZiYfqGamnyPjIxYJycnGgAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAd3R0KJ2WmbF4ebP7SVbF/zRP0P9DXdX/cIDV/6eqyvSysLCdOjo6GwAAAAAAAAAAAAAAAAAAAAAAAAAAjYeHTIJ7pPEaIMP/ABLT/wAd2f8BKt//FDvl/y5N6/9JXvH/f4Xk/8LAzOBoZ2czAAAAAAAAAAAAAAAAi4eHNHpzpfUFBcb/AAjK/wASzf8AHNP/ASna/xQ64P8tS+b/SVzs/2Ru9f93fO3/t7XD4T8+Ph0AAAAAHBwcApSMnM8NDMX/AADJ/25xzv+jqdb/pq3a/6mz3v+vuOH/tL3i/7vB5P9rdtX/VGTz/2Ry2/+opKSjAAAAApqVlUdVULX/AADO/wAAyP+nq9n/5Onn/+nt7P/u8fD/9Pb1//n6+f/8/Pz/doTS/zhT7f8wTuz/j5K69zk5OSGqoqKTTEvS/wwM0v8AAMn/nKHP/9Pa1//Y39z/3eTh/+Po5v/o7Ov/7fDv/2Z5zP8cQef/Fz3m/05hxf+NiYlkqaKluj8/4v89Pd7/ExPP/46Rv/+7wb//w8rH/8vSz//R2Nb/197b/9zj4P9WbcX/BjDh/wMt4P8jQMn/mJKSiqymrL87O+f/PT3h/z8/3P+ensT/ra6t/62vrv+ztrX/ur+9/8HIxf/J0M3/T2G+/wAh2v8AH9r/HzTH/5aPj4++trakQEDg/zk55P87O97/sLDW/87Ozv/BwcH/tbW1/6+vr/+ur6//s7W0/1Bct/8UJ9j/KDvc/2Rsyv+PiIhzvbi4Zmln2P80NOf/Nzfh/7e34P/d3d3/2NjY/9TU1P/Q0ND/zMzM/8jIyP9+g8j/TFXe/09X3/+Jhrj+bmtrNI+Ojg+uq8/vMjLn/zIy5v+Zmef/xMTm/8LC4/+/v9//vb3c/7u72f+5udf/bW3Q/0hJ2f9YWNX/mZGXyAAAAAMAAAAAyMbGaoGA3f8uLuj/MDDm/zMz4f81Nd3/Nzfb/zo62f88PNn/Pz/Z/0FB2f9HR9n/j4mv+X55eTwAAAAAAAAAAC0tLQDT0dOXgYDf/y8v5/8uLuf/MTHl/zMz4f81Nd//ODjd/zo63f9GRtr/jIe1/I2GhmUAAAAAAAAAAAAAAAAAAAAAMDAwAM3Ly2+urNTyZWTe/zc35P80NOj/Nzfm/0VF3v9xbsv/nZap4Y2Hh0sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmpiYFMG9vXDBu72wrKe6zamks8qup6emnpeXXk5NTQkAAAAAAAAAAAAAAAAAAAAA8A///+AH///AA///gAH//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//gAH//8AD///gB///8A///w=="""

		# else/app_icons/sync_1a.ico
		sync_1a_b64 = """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"""

		# else/app_icons/sync_1b.ico
		sync_1b_b64 = """AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABILAAASCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAEDAAACAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAACAcGARpINhVAlV8pRrxmLw+5ZS8AAAAAAAAAAAAAAAAAAAAAEDImE01zXTNUdVorFti0YQAkEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAABcZDgRIYkohmLaMTs/SlVaSxXVAFcV4QgAAAAAAAQAAAAAAAAMMCAI1YkkUuaZ+MvGogEOniGhCMVFCLgNlUTUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAcEAgApLCAReWpTLMrDnV/368aUvu7LqDDiqGkA///4AAAAAAAHBAEAAAAADjQmCHGVbRfuxYgj/8KDM/6se0TSjGhFZWZOOhN5XEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCAMALy8fEo1sUjDrw5lf/+7Jmtbs1L9A/8pvAOjUygAAAAAAAAAAAAAAAAMAAAErYkgPs7iFHf/OiSP/y38l/8B1Lf+sbz3xkWVIoHJSQTANGigBZUs+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgMAACApGA2GYkUr7L2JVP/twIv57M+xfuHLxwbly70AAAAAAAAAAAABAQEAAAAADS0gB2WWcBfpzJEg/86HJP/KfCX/xXEm/8BpKf+yZTX8mmNE0X1ZRGBQPDMRq3pjAAEGBwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASFwwGYU0xHt6kaTz/46ds/+3In9PozLUs7MytAAAAAAAAAAAAAAAAAAAAAAECAAEnYEcPqr2MHP7TkiL/zoYk/8d5Jf/Bbyb/wGgn/79iKP+4YS//pWQ/8JRkSZ+KYksxxYxuBAAAAAAAAAAAAAAAAAAAAAABAQAAAAAAAwgEATk0HA64gkch/s98P//or3n+6cemk9rGwwfixrEAAAAAAAAAAAABAAAAAAAACSodBluXchbh1Jsg/9aSI//OhCT/xngl/79sJv+7ZSf/wWs2/89/Uf/Xj2b/1Jh29cyfhbO7knsvAAAAAAAAAAAAAAAAAAAAAAYDAgAAAAANGw0GbVQrFO2mViL/1X48/+aygPXjw6hj//+vANq6pQAAAAAAAAAAAAAAAAEAAAAhZUwPosSVHPzcnSP/1pEl/86EJf/GdyX/vmsm/7tnLf/Jhl362K2U0d68qaDjwq9y2buqRbmaiBcAAAAAAAAAAAAAAAAAAAAAAAAAAAIBACMwGAypdzwa/bZeJf/Pezn/4LCD69/BqUXhwqcA17WlAAAAAAAAAAAAAAAACR8WBU+cdhbg4Kol/+KnMv/cmzT/z4Qq/8d3Jv++ayb/vmkw/8iJZOq9oZFgw8rNDMbQzQN6AAAAzv//AAAAAAAAAAAAAAAAAAAAAAAAAAABDgcDOkUjENGTSyD/u2In/8l6Ov/Zq37h1LagPdi6ogDIpZAAAAAAAG45GQABAAEWfVkWktioLPjru0Xt5rdbysOMR7u7cSnxxXQl/79qJv+8Zi7/w39X87GEalb/qnsAcmNaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQVCwRKVywS5aVTI/++ZCj/yXs6/9isgNzYup801bWZAAAAAAAAAAACAAAAAVwrEhDFfzB16bZXjN++e1DauZAlVzUjPYlOHNi7biT/wWon/79oMP/Hg1zzs4duX//7pwCSdmUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABRgMBVxfMBTqq1cl/79mJ//IeDL/0Z9s58qsmUQAAAAKAiIUHT9eOUF4dURGlWs9DdyQUAzgrnoJ////AP//eQAYDAUpbEAUy7FoIv/BaSf/wWo0/8yKZOy4jnZT/8uXAJN5agAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAAEHg8HXGo1F/GsWCX/vmUn/8dzKv/Fh0byfX1WkDVYH3tVbierpLFv28a4ecSykFshwqVnAAAAAAAAAAAAsWMiACERBzVnPRPOrmUh/8BnJ//Cbjv/z5Jw47+Wfz/OnoMAknpsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAcZDAVVZTIW5KtXJf+8Zib/xHEm/8N8K/2jfy3xnoEe8sOfPv3x257+6tGQjcWjYQbcvn0AAAAAAAAAAAAAAAABGw8HNGxAFteyZyP/v2cp/8d7TP/ZooLKsZSEJrudiwCef24AAAAAAAAAAAAAAAABCwUDDBQMCB0VDQgwFwwGTh4PBopjMhXqqVck/7xnJv/DcSb/ynwl/86GIv/Wlib/7MZ1//Hcot3cxIg87tWKAMSvhwAAAAAAAAAAAAAAAAQmGA1NdUod4b1sJ//DbDH/0o9m/NapkI2XjIYIpZGGAAAAAAAAAAAAAAAAAAAAAAAvGAslSCYTiEkmEr1RKRLcZTMW7o9IHv2xXCX/vGcm/8JyJf/KfiX/0ooj/+CnQ//02p7/6tSZl8eubAnPt3gAAAAAAAAAAAAFAwIAAAAADDEhEmuHWij0zXs2/9OBSv/epoXm1a+ZRt+xlQAAAAAAAAAAAAAAAAAAAAAAYzIWAEklEAlzOxpmlE0j0a9bK/65Xyv/u18p/7xiJ/+9aSb/w3Ml/8p/JP/Tjif/6sJ3//LdquXcxo0+6dKYAAAAAAAAAAAAAAAAAAAAAAEFAwQhSDQaoaNwNv3aj1D/5qyC++a9pJPPrJkN3regAAAAAAAAAAAAAAAAAAAAAAAAAAAAjE4qAH1FJgKlXDIwu2k5n8luOvLKazP/w2gq/8FsJ//EdCX/yoAk/9eaPP/w1Zv/6dOcqM61fA/cxIoAAAAAAAAAAAAIBgUAAAAACCIZD1JqTibWxIxN/+mzg//sya7B27ypLP/bvQC8pZgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUDgqAP+ORQCQVTMNrmM3YsRtOdPNdDb9ynQs/8h4Jv/NhCj/5bt3//DbqungyI5N9s5hANXFqAAAAAAAAAAAAAAAAAIDAgMkSjcbnaR7QPvpuoL/8M6q0d3BqkNzcHQCoJKKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJVULwBkNiACq2I3N8J0O6LPfTbxz4Ar/9aWQf/u0Zz/6tSgq825hxHSvYsAAAAAAAAAAAAAAAADAAAAHD4uF26deTzo5r57/PLUqMHpy6lFu5mHBeO+ngAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACuaTUAomM4DblyM2PNgzPU5LRw//HcrvDcxpRW6dOiAAAAAAAAAAAAWEIqAAsICBJfRyporohH2ea8bdrwy5CH3sKZKWFDMQGri2gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQVSwAez4cA7t8PDfbs3uf48uan9PBlhjfypoAAAAAAAAAAACsfUQAb00pEceYV4Xnu22X7sR6Ps+ugAn/3IsAcmFoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNVyIAPQAAALaISwnPsXYM1cmdAdK9igAAAAAAAAAAAOypWADnnk4B87tpDvvYjQjo37oA9NqdAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//////////////////Hx///A8P//gOA//gHgH/4DwAf8A8AD+AeAAPgHgAD4DwAA8A8AA/APAA/wCAAP8AAID/AAeA/gAHAPAADwDwAA8B+AAeAfwAHgP/ADwD/4A4B//geA//8Hg///h4f///////////////////////////8="""

		# else/app_icons/sync_1c.ico
		sync_1c_b64 = """AAABAAEAICAAAAAAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEYjDBYAAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABVAAADbGMawRwVDiUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACfv78I4unkacPRx7uwzLXesMe12rS7ta21u7VPAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHtiGXLMZCL/PkgZZwAAAAAAAAAAAAAAAAAAAAAAAAAAy9HLJ8DUxthhvXf/N8JX/0LQY/9f2nz/fNuS/5XLof+uuLC4n5+fEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABbWxQnu2Ug9ddlI/93UxupAAAAAgAAAAEAAAACAAAAAb/Kvxirv7DlKoU//xx/M/8fjjn/JadE/y3CUP9A0WL/WNh2/27Rhf+ptqrBf39/BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVQAAA59lHcTXZSP/0GEh/5RaHehKQQ2OY0YPp2pGEKtkQBOXsK2mwTSKSP8beTH/G3kx/x2ENf8hlDz/JaVD/ym1Sf8tv07/Oc1c/2bIfP+xr69pAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAaBtz1Gki/9FkIf/KXyH/w10g/8RdH//FXCD/x10h/8hkKf+PuJX/JaVD/yCOOf8eiDb/H4g3/yCMOf8hkzv/Ipc9/yObP/8ko0L/L8NR/5e3ndEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYGATKMBxH/bUbSH/zWkh/8hlIP/HZCD/yGQg/8ljIf/LYyH/ynpH/4THk/9Hzmb/KK9H/yShQf8ilz3/IJA6/x+KOP8dhTb/HH4z/xx9M/8jnkD/eLeI/JmZmQ8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFUAAAOjdhvG13oh/9N1If/NcSD/zHAg/81vIP/ObiH/z20h/9FsIf/NgEn/mc6l/3vgkv9N0mz/LMFO/yewR/8jn0D/IJA6/x2BNP8acS7/F2Yq/x6GNv9vq3z/wri4GQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg3wcb9mHIP/YgyD/1IAg/9N+IP/TfCD/03sh/9R6If/VfSP/1IYs/9GWUv6rzLL/nuiv/4Pimv9Y2Hb/MctV/ym4S/8kokH/H4s4/xp0L/8XaCr/HYU1/4Ori/WSkpIHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIrWd54aNE+tqQIP/ajiD/2Ywg/9qKIP/biSD/2ooh/6KALJG/f1UktoZtFbG7sea17ML/o+m0/4/ko/9u3Yj/Q9Fj/yy8TP8kokH/Hok3/x6HN/8kkz3/tsK5tgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADYwZsh5b56kuStSvPgmiD/4Zgg/+GXIP/flSD/nHUgpQAAAAIAAAAAurW1b7PPuf+67sb/quq5/5fmqf9/4Zb/YNp8/0DNYP8wvlH/K7tN/3i3h/3r6+tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2b+MFOnHg3/ptlDq5aUj/+SiIP+5iyThAAAADAAAAAB/f38CsrKvr7TTu/++78r/sey//6Dosf+L45//dd6N/2HZff94yoz+2NjYggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANG5iwvozIlu671U39+vL/4sHQo0AAAAAAAAAAC/v78EtLKwhbC+svez1rv/rN23/6Tdsv+j2bD/s8257NHPz2UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMmWYF69KSW3lOIzsAAAAAAAAAAAAAAAAAAAAAvLG8F8bBwWLIxsZ9zcnLfMzGyVWqqqoMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEtDNCIAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC8klK3eU0TlREGAC0AAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwp9euDckGUYAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOjCcIblqyH/w4sd9IJTFKUfDQQ6AAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADw0H94ypdM71o/KWkAAAANAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA48ihQeCjKf/foSL/4aMi/8iLH/qJWRe0LRgHSQAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOTJhhPtwXnv3aRa/p1yS8JJMiNXAAAAFQAAAAYAAAABAAAAAAAAAACOcXEJ3KJH9dmUI//ZliP/2Zcj/9mYIv/IiSD9kl4ZxD4iC1oAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPDWpmrnr2//5KVf/92aVf63eULnnGEyuIhHH5Z3OhmHfD4YjIxIHKTHfjHy0IYk/8+IJP/QiCP/0Ioj/9GMI//UjyP/yo0x+15IIS4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAe7Mp6Xhm1//3Y9N/9uJQ//WfTH/y3Un/8ZzJv/HdCb/yHYl/8h3Jf/HeCX/x3kk/8d6JP/IfST/zIAk/9GEJv/Klk+3AAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1Kp/BunBoKTbh0//0HAw/8RnJ/+/Zif/v2cn/8BpJ//Baib/v2sm/75rJf+/bCX/v24l/8RxJf/Kdib/zYtH741hIx0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAeS4n2jOgVPvuV4o/7leKP+7Xyf/u2An/7lgJ/+3YCb/uGEm/7hiJv+9ZSb/w2kn/815Of+qek1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMacjhLSk3F4xXhKzsJsOvq7YCz/tlwp/7ZeK/+5ZTX8uFwn/8BgKP/IZyv/uXxSswAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmXd3D7OCZy+zfVk5lWpRKcqqlUjBZTH/xmMp/8N3S+5xQiYbAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1KqqBtGAU/TJbjr+oGxRXgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0Ytmt7R3VbEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJoYlfekczGQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA///////v+H//7+Af/8fAD/+AAA//gAAH/wAAB/4AAAf+AAAH/gGAB/8BwA//4cAP//ngP///////////////////P//9/w///v+D//4/gP//AAB//wAAf/+AAP//4AH///gB////4////+f////n//////////////////////8="""

		# else/app_icons/sync_2a.ico
		sync_2a_b64 = """AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACXA2EIlxN3EJcTdfgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACbA2SIlw9yuJcvm/iXQ7P8kz+utAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACfB2QwmwtqHJsnj9ybQ6/8m0Oz/JtDs/ybQ7IwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACfA2AEmv9lfJsbh5ibP6v8n0Oz/J9Ds/yfQ7P8n0Oz/Jsvm7ifG4OYnxd/bJsPdvCa/2Yomv9hEJ8DZAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnwNglJ8XeySjO6P8o0u3/KNLt/yjS7f8o0u3/KNLt/yjS7f8o0u3/KNLt/yjS7f8o0u3/J9Hs/yjM5v8nxuDjJ8HZcijA2AcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACjJ5LIo0ez/KNHt/yjR7f8o0e3/KNHt/yjR7f8o0e3/KNHt/yjR7f8o0e3/KNHt/yjR7f8o0e3/KNHt/yjR7f8ozun/KMXf2ijA2DcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKNHslynR7f8p0e3/KdHt/ynR7f8p0e3/KdHt/ynR7f8p0e3/KdHt/ynR7f8p0e3/KdHt/ynR7f8p0e3/KdHt/ynR7f8p0e3/Kcvl+SnB2lwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACnB2Qcpw9yaKcLaXQAAAAAo0e0LKdLtxSnS7v8p0u7/KdLu/ynS7v8p0u7/KdLu/ynS7v8p0u7/KdLu/ynS7v8p0u7/KdLu/ynS7v8p0u7/KdLu/ynS7v8p0u7/Kc3o/SnD21wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKcXggCrR7f8qzun+KcLcbwAAAAAq0+4QKdLuzirS7v8q0u7/KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/Ks3o+CnA2jcAAAAAAAAAAAAAAAAAAAAAAAAAACrB2Rkqzun1KtLu/yrS7v8qzun+KsTceAAAAAAp0e4VKtLu1yrS7v8q0u7/KtLu/yrS7v8q0u7/KtLu7yrS7uUq0u76KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/KtLu/yrS7v8q0u7/Ksrl2yvB2gkAAAAAAAAAAAAAAAAAAAAAKsjjiSvS7v8r0u7/K9Lu/yvS7v8rzur/KsPdegAAAAAq0u0bKtLt3ivS7v8r0u7/K9Lu/yrS7nwAAAAAAAAAACvS7QYr0u1HKtLtvCvS7v8r0u7/K9Lu/yvS7v8r0u7/K9Lu/yvS7v8r0e3/KsbggQAAAAAAAAAAAAAAACzB2wQrz+nqLNPv/yzT7/8s0+//LNPv/yzT7/8rz+r7K8PbFAAAAAAr0+4iK9Pu5SzT7/8s0+//K9PuUgAAAAAAAAAAAAAAAAAAAAAr0e8AK9PuaizT7vss0+//LNPv/yzT7/8s0+//LNPv/yzT7/8rz+nzK8LaCgAAAAAAAAAALMbhQCzS7v8s0+//LNPv/yzT7/8s0+//LNPv/yzT7vUrzuoPAAAAAAAAAAAr0+4qLNPv6yzT7/8r0u4tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALNLuYSzT7/4s0+//LNPv/yzT7/8s0+//LNPv/CvS7rksyOMFAAAAAAAAAAAszeh8LdPv/y3T7/8t0+//LdPv/y3T7/8t0+//LNPunwAAAAAAAAAAAAAAAAAAAAAs0+8qLNPveC3U7gEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALNPujCzT7vwt0+7qLNPuoy3U71ot1O4TAAAAAAAAAAAAAAAAAAAAACzQ66Ut0+//LdPv/y3T7/8t0+//LdPv/y3T7/8t0+9TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALdPvBS3T7wEAAAAALMHcACzB3CgswdtCLcHcBAAAAAAAAAAALdLuuy7U8P8u1PD/LtTw/y7U8P8u1PD/LtTw/y3U7ygAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACzB3AMtwtw0LMHbcSzE364tyOPqLczn/y3O6f8tx+KkAAAAAAAAAAAu0++9LtTw/y7U8P8u1PD/LtTw/y7U8P8u1PD/LtLtIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALsPbNi7E23wux9+5Lsrk8i7O6P8u0u3/LtTv/y7U8P8u1PD/LtTw/y3S7eIAAAAAAAAAAC7T8Ksv1PD/L9Tw/y/U8P8v1PD/L9Tw/y/U8P8uzOc+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC7F4CYuzej+LtLu/y/U8P8v1PD/L9Tw/y/U8P8v1PD/L9Tw/y/U8P8v1PD/LtPv4wAAAAAAAAAAL9Xwhi/V8P8v1fD/L9Xw/y/V8P8v1fD/L9Xw/y/O6IYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL9PvAS/V8JMv1fD+L9Xw/y/V8P8v1fD/L9Xw/y/V8P8v1fD/L9Xw/y/V8P8v1fDjAAAAAAAAAAAw1fBNMNXx/zDV8f8w1fH/MNXx/zDV8f8w1fH/L9Dr7DDE2xIAAAAAAAAAADDE2wwwxNsJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC/U8Fsw1fD0MNXx/zDV8f8w1fH/MNXx/zDV8f8w1fH/MNXx/zDV8OMAAAAAAAAAADDV8Asw1fD0MdXx/zHV8f8x1fH/MdXx/zHV8f8x1fD/MMnirjDD2zswxd2jMMvk9zDK5LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMLaAzDS7eQx1fH/MdXx/zHV8f8x1fH/MdXx/zHV8f8x1fH/MNXw4wAAAAAAAAAAAAAAADHV8Jsx1fD/MdXw/zHV8P8x1fD/MdXw/zHV8P8x0+7/Mc/p/zHV8P8x1fD/MdXwlwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxyOBeMdXw/zHV8P8x1fD/MdXw/zHV8P8x1fD/MdXw/zHV8P8x1fDjAAAAAAAAAAAAAAAAMdXxIzHV8fky1vL/Mtby/zLW8v8y1vL/Mtby/zLW8v8y1vL/Mtby/zLW8v8x1fFLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMcPbIjHP6usy1vL/Mtby/zLW8v8y1vL/Mtby/zLW8v8y1vL/Mtby/zHV8eMAAAAAAAAAAAAAAAAyw9sIM9PutjPW8f8z1vH/M9bx/zPW8f8z1vH/M9bx/zPW8f8z1vH/M9bx9TLW8QkAAAAAAAAAAAAAAAAAAAAAAAAAADLD2zYyzeXhM9bx/zPW8f8z1vH/M9bx/zPW8f8z1vH/M9bx/zPW8f8z1vH/M9bx4wAAAAAAAAAAMsXdbDPL5Osz0u3/NNbx/zTW8f801vH/NNbx/zTW8f801vH/NNbx/zTW8f8z1fCzAAAAAAAAAAAAAAAAM8TbDjPE3Ekzxt6nM8/o/DTW8P801vH/NNbx/zTW8f801vH/NNbx/zTW8f8z1fDBNNbwwjTW8f801fDhAAAAAAAAAAA00+3CNdfx/zXX8f811/H/Ndfx/zXX8f811/H/Ndfx/zXX8f811/H/Ndfx/zTW8GcAAAAAM8beWjTL5Ok0zeb+NNHr/zTW8f811/H/Ndfx/zXX8f811/H/Ndfx/zXX8f811/H/NNbx+jTW8C401/EENNbxfDTW8HQAAAAAAAAAADTX8gw01vGGNdfx9zXX8v811/L/Ndfy/zXX8v811/L/Ndfy/zXX8v811/L+NNbxHDTF3QU00evvNdfy/zXX8v811/L/Ndfy/zXX8v811/L/Ndfy/zXX8v811/L/Ndfy/zXX8v801vF5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA11vEiNtbyrjbX8f421/L/Ntfy/zbX8v821/L/Ntfy/zbW8c8AAAAANMrjODXW8f821/L/Ntfy/zbX8v821/L/Ntfy/zbX8v821/L/Ntfy/zbX8v821/L/NdbxoTbX8gEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANdbxQjbW8dI21vL/Ntby/zbW8v821vL/NtbxggAAAAA10Op4Ntby/zbW8v821vL/Ntby/zbW8v821vL/Ntby/zbW8v821vL/Ntby/zbW8Zg11/EDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN9bxAzbW8mo21/LrN9fy/zbX8vw21vItAAAAADXT7bg31/L/N9fy/zfX8v831/L/N9fy/zfX8v831/L/N9fy/zbX8u821vJgN9byAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADbX8xE32PNoNtjyPQAAAAA3x98CNtTv8jfX8/831/P/N9fz/zfX8/831/P/N9fz/zfX8+032PKKNtfyFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADfG3gA31vKqONfz3TfW8t441vLTN9bytzfW8oo31vJKONfzBwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//x////wf///wH///wAB//4AAH/+AAA//gAAH+IAAA/hAAAHwIAAA8BAwAOAIPgBgDD8AYB4/geAf/8xgH/+AYB/8AGAf+ABgH/gAYAz+AGAA/gBwAP4AcAD8AHAA+ABgAcAAYAEAAGAAAAf4AgAH/gIAD/8CAD//xAB///4B/8="""

		# else/app_icons/sync_2b.ico
		sync_2b_b64 = """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"""

		# else/app_icons/sync_2c.ico
		sync_2c_b64 = """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"""

		# else/app_icons/bullet_red.png
		bullet_red_b64 = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAACxSURBVDjL7dItC8JQAIXh491HWbDvD1pEDIIKm1zDxqKi0WIULAZFYc1msF3ErEZlMC9Mhxx/gTAR28KpDxx4QRK/DCXwAbDg0oLMTShtQF0F5AlwvwHkqy+Zxxs+lwsmvs8DKrIw8DCh8njNLOxRtxrU4yF3MFRhIBFQ2XxG3W7yXq8xjULGsIsDFwF58zzq0YBpFPDc6XIKp/iFI4S7h5BbWGoFW03gyABVtyzxT8Ab8Xzei+tkcykAAAAASUVORK5CYII="""

		# else/app_icons/bullet_green.png
		bullet_green_b64 = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAC5SURBVDjLY/j//z8DJZhh1ADsBjjsspIC4gb77ZZX7TdbXLVda9Zgs8xEihQDGmZfm/7/0KOD/3ff3/V/6plJ/y3mGjYQbYD9NsurBx4e+D/10tT/nWc6/i+5sui/+RS9q0QbYLfB/OrWO1v+d5/p+t96qvn/3Auz/pt0aRNvgPVyk4appyf+X3xl4f/ZF2b+n3Co579+mSrxXrCcZyhlMV2/wbRP56pRq+ZV3SLlBq1EOanRlEgjAwAXIuIDq5qm/AAAAABJRU5ErkJggg=="""

		# else/app_icons/bullet_white.png
		bullet_white_b64 = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAABbSURBVCjPzdAxDoAgEERRzsFp95JbGI2ASA2SCOX3Ahtr8tuXTDIO959bCxRfpOitWS5vA+lMJg9JbKCTTmMQ1QS3ThqVQbBBlsbgpXLYE8lHCXrqLptf9km7Dzv+FwGTaznIAAAAAElFTkSuQmCC"""

		# else/app_icons/shield_go.png
		shield_go_b64 = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAKZSURBVBgZpcFfaJV1HMfx9+/Zc9QtO0unOMdasEibGf65SLOCJWRX4p0gCCVddBVYF0FEF4Hsom668jIN6iJJvYgoRoOMeTBdEoORf2rqJseca8ftHM+e5/f8ft9P5+JcSJA3vV5OEv9HwiPc+/HlqbnRPeIRnCRq469KJiTtwjQo0+uS3lzVtx9JNG+eRaZvZfa9TBWLVpGpa+Dgb85JYuHnYa3s20+oTZGsXE/6xDZW9e6FjtWAoaJGdrdCNncZv3CVzv5h7k+e5KlDky6lRaZyVh1dWrP7c5ChWKdYvEBafhHnUvzc15S6trJi82FQZP7iJ1i0fbQktPQMn6tb8QBkFPOnKea/w7JbIAOE5X+RV7+ief0jkJEvTCOzCVpS2mQCDEUPVoAzbLmC6yhQzFDMUMhBkaRUJjSXNgK1lDZFAwnMo1jgkggsgytwyjl2tUotzzm+SViMWDSjJaFNJpCh6JE8kgcyoInIyUJB/7ohDp86AuZQtBItKW2KhllO0vk0sTHJBxcvgcbwFvAhsHHNMwz17qKePeDt2xf4tNR5n5aUNpl9tvT7F0e7h45g+W2CeV577g2ijGgRQ1QXZ3m+/yUafpm3Zs5NZ8eSFSltfQcm3p39ZsdR19FFefNBsnCaKOPW39cpLBCsoIgFS3md7U++QqNopr/cGM9SHqJo6xvTP9xLSt1kISPEwIbyAMEiUcadxRnWru7l8ux5zv85fsUHdjpJPOzGl1u3JKXy1Hu1u2SFx5snC57Bni3sHtzHxEyFsWujkz7wQnVEuZPEv/1x4tkNivZOkj724eObhpm/dGb6UH22Z8fA3u6fro396o091RF5Wpwk/suV44Nrow8fmw/vH2jcmYnWsW7ZYmluRIG2fwAIBqNZGcz/tQAAAABJRU5ErkJggg=="""

		# else/app_icons/star.png
		star_b64 = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAAC2klEQVR4nJWSW0iUeRjG3880yhrFhFJKnZrGcTSKcNkKi2ixli02KjMYGCeLDrb9JYoOynTSLFp2G92+Sic7GpUdtGI8plmBFJTTEnUxWXuwKIwK66JSoe/XhdXNGNTFe/O+z/PjhecRQPqbzOkyoFa3ZF3yxGfOniQhX9P1uwREV1rMm/9Kn70KeP715GjR3wVw/CShzd6JbrrOQlcV9Xvta+alyYBvBuhKi+m6735K5z7oLOPFnfx/ildJv18IIJPtov38g4S4ZkpYwWLN1HLAXsDjHdCxAzp2Q0cJjcWWTVucMjQrXcJmpUrIj0miASIXdw7PaKuYtO+Rb3bDy1ZHe++9VT1G+1oIrIYHayGwEQJujEARPX/nd7+4ujLwsCqj7nZ52t6qrdG/ypU/40p7b2RC2wLwzwf/AvBngH8R+B3Q5oTbLriVDTezodUF15z01DuMhsKYEtGVJDftGn6mu2UutM6Ea1OgJRWaJ8DlcdCQAnUpUDMefKngm8r7C3OMuq3DKnQlyZKVLqG6kpTGwsiTvb5Ug1o71NqhJgl8SXDJBtWJcM4KlRa6K+wfat1DD+tKbI4ZEiqAOD9BmgoiKqlO7DNUJcJ5K5wdC5UWODkG4/ho6txDjupKbAun9cX6JY7ceTKwOm/QOk5b4LQFTvWZODEGjo+GI2Yoj+fM+oHLV86RsKAeLPtFwq5vM5VwzAzHzHDUDEcS4FACHIyHsjjYP4qm/PCdWekSGgTIc0j4vaKoerxx4I3D8Jp5XRz79s2e2HfG/gT4ayQUx3LHbTq/bqEMCgJ4cmTY013R7UZpIl0e6/srG001B3K1xaW52tKWDRGNr3+3dht7LPy/OfLuHyskMgigKxnZWTjieWt+VHOZ0rJ1JdYtThm8zSXhuhKbV2nLbqyPuP4kL+qxrmREEKDkN4nUlaTpSmzbXRL+uaqATEkWrWiJDNGVJOtK0jw5Yvp8+wjKjWbfCEzj3wAAAABJRU5ErkJggg=="""

		if icon == "app_icon":
			return app_icon_b64

		if icon == "connect":
			return connect_b64

		if icon == "disconnect1":
			return disconnect1_b64

		if icon == "disconnect2":
			return disconnect2_b64

		if icon == "disconnect3":
			return disconnect3_b64

		if icon == "disconnect1_menu":
			return disconnect1_menu_b64

		if icon == "disconnect3_menu":
			return disconnect3_menu_b64

		if icon == "testing":
			return testing_b64

		if icon == "connected_classic":
			return connected_classic_b64

		if icon == "sync_1a":
			return sync_1a_b64

		if icon == "sync_1b":
			return sync_1b_b64

		if icon == "sync_1c":
			return sync_1c_b64

		if icon == "sync_2a":
			return sync_2a_b64

		if icon == "sync_2b":
			return sync_2b_b64

		if icon == "sync_2c":
			return sync_2c_b64

		if icon == "bullet_red":
			return bullet_red_b64

		if icon == "bullet_green":
			return bullet_green_b64

		if icon == "bullet_white":
			return bullet_white_b64

		if icon == "shield_go":
			return shield_go_b64

		if icon == "star":
			return star_b64

def app():
	Systray()
	Gtk.main()

if __name__ == "__main__":
	app()
