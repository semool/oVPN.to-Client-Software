# -*- coding: utf-8 -*-
import gtk
#import gio,pango,cairo
from datetime import datetime as datetime
from Crypto.Cipher import AES
import types
import os
import platform
import sys
import hashlib
import random
import base64
import urllib
import urllib2
import time
import zipfile
import subprocess
import threading
import win32com.client
import socket
import random
import struct
import gettext
import locale
import _winreg
#import csv

# compiler needs: http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/pygtk-all-in-one-2.24.0.win32-py2.7.msi

CLIENTVERSION="v0.2.1-gtk"

ABOUT_TEXT = """Credits and Cookies go to...
+ ... all our customers! We can not exist without you!
+ ... d0wn for hosting DNS on dns.d0wn.biz!
+ ... bauerj for code submits!
+ ... dogpellet for DNStest() ideas!
+ ... ungefiltert-surfen.de for WorldWide DNS!
+ ... famfamfam.com for flag and silk icons!
"""

try:
	if sys.argv[1] == "debug":
		DEBUG = True
except:
	DEBUG = True

DOMAIN = "vcp.ovpn.to"
PORT="443"
API="xxxapi.php"
	
class Systray:
	def __init__(self):
		self.init_localization()
		self.self_vars()
		if self.preboot_check(logout=False):
			self.tray = gtk.StatusIcon()
			self.tray.set_from_stock(gtk.STOCK_PROPERTIES)
			self.tray.connect('popup-menu', self.on_right_click)
			#self.tray.connect('activate', self.on_left_click)
			self.tray.set_tooltip(('oVPN.to Client'))
			self.systray_timer()
		else:
			sys.exit()
		

	def self_vars(self):
		self.MAINWINDOW_OPEN = False
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
		self.statustext_from_before = False
		self.systraytext_from_before = False
		self.stop_systray_timer = False
		#self.statusbar_text = StringVar()
		self.statusbar_freeze = False
		self.SYSTRAYon = False
		self.screen_width = 320
		self.screen_height = 240
		self.USERID = False
		self.PH = False
		self.extract = False
		self.STATE_OVPN = False
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS1 = False
		self.GATEWAY_DNS2 = False
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
		#self.save_passphrase = IntVar()
		
		self.FLAG_IMG = {}
		self.on_left_click_counter = 0
		self.OVPN_SERVER_INFO = {}

		
	def on_right_click_mainwindow(self, widget):
		model,iter = self.treeview.get_selection().get_selected()
		if not iter: return
		print iter
		servername = model.get_value(iter,1)
		servershort = servername[:3]
		print servershort
		

		#print 'def on_right_click_mainwindow: widget = %s' % (widget)
		#if event.button == 1:
		#	self.debug(text="mainwindow left click")		
		#if event.button == 3:
		#	self.debug(text="mainwindow right click")
		#self.treeview.get_selection().connect('changed',self.make_context_menu_servertab)
		self.make_context_menu_servertab(servername)
			
	def make_context_menu_servertab(self,servername):
		#print event
		context_menu_servertab = gtk.Menu()
		
		connect = gtk.MenuItem('Connect to %s'%(servername))
		connect.show()
		context_menu_servertab.append(connect)
		connect.connect('button-release-event',self.call_openvpn,servername)
		sep = gtk.SeparatorMenuItem()
		sep.show()
		context_menu_servertab.append(sep)	
		context_menu_servertab.popup(None, None, None, 3, int(time.time()), self.treeview)
		self.context_menu_servertab = context_menu_servertab
		
	"""		
	def on_cell_radio_toggled(self, widget, path):
		#path = gtk.tree_path_new_from_string(path)
		print 'path=%s'%(path)
		#selected_path = gtk.TreePath(path)
		#path = self.mainwindow_liststore.get_path(path)
		for row in self.mainwindow_liststore:			
			#print 'row.path[0]=%s'%(row.path[0])
			if row.path[0] == int(path):
				print 'row.path[0]==path, row[6]=%s' %(row[6])
				#self.mainwindow_liststore[6] = (row.path == path)
				print self.mainwindow_liststore[6]
	"""
		
	def on_right_click(self, widget, event_button, event_time):
		#print 'widget = %s' % (widget)
		#print 'event_button = %s' % (event_button)
		try:
			self.systray_menu.popdown()
		except:
			pass		
		self.make_systray_menu(event_button, event_time)

	def on_left_click(self, widget):
		try:
			self.systray_menu.popdown()
		except:
			self.show_mainwindow(widget)


	def make_systray_menu(self, event_button, event_time):
		
		self.load_ovpn_server()
		self.systray_menu = gtk.Menu()

		#show update item
		update = gtk.MenuItem('Check for Server Updates')
		update.show()
		self.systray_menu.append(update)
		update.connect('activate', self.check_remote_update)		

		sep = gtk.SeparatorMenuItem()
		sep.show()
		self.systray_menu.append(sep)
		
		if len(self.OVPN_SERVER) > 0:
			self.make_systray_server_menu()

		if self.STATE_OVPN == True:
			sep = gtk.SeparatorMenuItem()
			sep.show()
			self.systray_menu.append(sep)		
			# add quit item
			servershort = self.OVPN_CONNECTEDto[:3]
			textstring = '[ %s ] IP: %s Port: %s (%s)' % (servershort,self.OVPN_SERVER_INFO[servershort][0],self.OVPN_SERVER_INFO[servershort][1],self.OVPN_SERVER_INFO[servershort][2].upper())
			
			disconnect = gtk.ImageMenuItem(textstring)
			img = gtk.Image()
			img.set_from_file(self.systray_icon_disconnected)
			disconnect.set_always_show_image(True)
			disconnect.set_image(img)
			disconnect.show()
			self.systray_menu.append(disconnect)
			disconnect.connect('activate', self.kill_openvpn)			

		#show server view
		sep = gtk.SeparatorMenuItem()
		sep.show()
		self.systray_menu.append(sep)
		if self.MAINWINDOW_OPEN:
			mainwindow = gtk.MenuItem('Close Full View')
		else:
			mainwindow = gtk.MenuItem('Open Full View')
		mainwindow.show()
		self.systray_menu.append(mainwindow)
		mainwindow.connect('activate', self.show_mainwindow)
		
		
		if self.STATE_OVPN == False:
			sep = gtk.SeparatorMenuItem()
			sep.show()
			self.systray_menu.append(sep)		
			# show about dialog
			about = gtk.MenuItem('About')
			about.show()
			self.systray_menu.append(about)
			about.connect('activate', self.show_about_dialog)
			# add quit item
			quit = gtk.MenuItem('Quit')
			quit.show()
			self.systray_menu.append(quit)
			quit.connect('activate', self.on_closing)

		#self.systray_menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.tray)
		self.systray_menu.popup(None, None, None, event_button, event_time, self.tray)
		print "systray created: event_button = %s" % (event_button)
	
	def make_systray_server_menu(self):
		for menuserver in self.OVPN_SERVER:
			servershort = menuserver[:3]
			textstring = "%s (%s:%s)" % (servershort,self.OVPN_SERVER_INFO[servershort][2],self.OVPN_SERVER_INFO[servershort][1])
			flagcountry = servershort[:2].lower()
			if self.OVPN_CONNECTEDto == menuserver:
				servershort = "[ "+servershort+" ]"
				serveritem = gtk.ImageMenuItem(servershort)
			else:
				serveritem = gtk.ImageMenuItem(textstring)
				serveritem.connect('button-press-event', self.call_openvpn, menuserver)
			img = gtk.Image()
			imgpath = self.FLAG_IMG[flagcountry]
			img.set_from_file(imgpath)
			serveritem.set_always_show_image(True)
			serveritem.set_image(img)				
			self.systray_menu.append(serveritem)
			serveritem.show()

		
	
	"""
	def make_systray_server_menu(self):
		imenu = gtk.Menu()
		serverm = gtk.MenuItem("Server")
		serverm.set_submenu(imenu)
		self.systray_menu.append(serverm)		
		for menuserver in self.OVPN_SERVER:
			self.countrycode = menuserver[:2]
			servershort = menuserver[:3]
			if self.OVPN_CONNECTEDto == menuserver:
				servershort = "[ "+servershort+" ]"
				serveritem = gtk.MenuItem(servershort)
			else:
				servershort = menuserver[:3]
				serveritem = gtk.MenuItem(servershort)			
				serveritem.connect('button-press-event', self.call_openvpn, menuserver)
			imenu.append(serveritem)
			serveritem.show()
		serverm.show()
	"""
	
	def check_remote_update(self,widget):
		if self.timer_check_certdl_running == False:	
			if self.check_inet_connection():
				self.debug(text="def check_remote_update:")
				if self.check_passphrase(widget):
					self.make_progressbar()
					try:
						thread_certdl = threading.Thread(name='certdl',target=lambda self=self: self.inThread_timer_check_certdl())
						thread_certdl.daemon = True
						thread_certdl.start()
						threadid_certdl = threading.currentThread()
						self.debug(text="threadid_certdl = %s" %(threadid_certdl))
						#self.debug(text="def check_remote_update: start inThreadTimer_check_certdl()")
						return True
					except:
						self.debug(text="starting thread_certdl failed")
		return False

	def make_progressbar(self):
		self.progressbarfraction = 0.1
		self.progresswindow = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
		self.progresswindow.set_border_width(6)
		self.progresswindow.set_title("oVPN Server Update")
		self.progresswindow.set_icon_from_file(self.systray_icon_syncupdate)
		self.progressbar = gtk.ProgressBar()
		self.progressbar.set_pulse_step(0)
		self.progresswindow.add(self.progressbar)
		self.progresswindow.show_all()
		self.progresswindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		
	def set_progressbar(self,text):
		if self.progressbarfraction < 0.95:
			self.progressbarfraction += 0.05
		else:
			self.progressbarfraction = 0.05
		text = "oVPN Update: %s" % (text)
		self.progressbar.set_text("%s"%(text))
		self.progressbar.set_fraction(self.progressbarfraction)
		
	def inThread_timer_check_certdl(self):
		self.timer_check_certdl_running = True
		text="Checking for oVPN Updates..."
		self.set_progressbar(text)
		self.debug(text="def inThread_timer_check_certdl:")
		if self.curl_api_request(API_ACTION = "lastupdate"):
			text="Checking for Update"
			self.set_progressbar(text)
			self.debug(text="def inThread_timer_check_certdl: API_ACTION lastupdate")
			self.remote_lastupdate = self.curldata
			if self.check_last_server_update():
				text = _("Updating oVPN Configurations...")
				self.set_progressbar(text)
				if self.curl_api_request(API_ACTION = "getconfigs"):
					text = _("Requesting oVPN Certificates...")
					self.set_progressbar(text)
					if self.curl_api_request(API_ACTION = "requestcerts"):
						text = _("Requested oVPN Certificates...")
						self.set_progressbar(text)	
						while not self.body == "done":
							text = _("Waiting for oVPN Certificates...")
							self.set_progressbar(text)
							time.sleep(3)
							self.curl_api_request(API_ACTION = "requestcerts")
							text = _("Downloading oVPN Certificates...")
							self.set_progressbar(text)							
							if self.body == "ready":
								if self.curl_api_request(API_ACTION = "getcerts"):	
									self.body = False
									text = _("Extracting oVPN Certificates...")
									self.set_progressbar(text)										
									if self.extract_ovpn():										
										self.debug(text="extraction complete")
										#self.tray.set_from_stock(gtk.STOCK_DISCONNECT)										
										text = _("Complete!")
										self.set_progressbar(text)
										self.body = "done"
										self.timer_check_certdl_running = False
										self.progressbar.set_fraction(1)
										return True
									else:										
										self.debug(text="extraction failed")
										#self.tray.set_from_stock(gtk.STOCK_DIALOG_ERROR)
										text = _("Error: Extraction failed!")
										self.set_progressbar(text)										
										self.body = "done"
										self.timer_check_certdl_running = False
										self.progressbar.set_fraction(0)
										return False
			else:
				text = _("Certificates and Configs up to date!")
				self.set_progressbar(text)
				self.progressbar.set_fraction(1)
				self.timer_check_certdl_running = False
				return True
				
		else:
			self.debug(text="self.curl_api_request(API_ACTION = lastupdate): failed")
		self.debug(text="def inThread_timer_check_certdl: ends")
	

	def show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		self.about_dialog = about_dialog
		about_dialog.set_destroy_with_parent (True)
		about_dialog.set_name('oVPN.to')		
		about_dialog.set_version('Client %s'%(CLIENTVERSION))
		about_dialog.set_copyright('(C) 2010 - 2015 oVPN.to')
		about_dialog.set_comments((ABOUT_TEXT))
		#about_dialog.set_authors(['oVPN.to <support@ovpn.to>'])
		about_dialog.run()
		about_dialog.destroy()

		
	def show_mainwindow(self,widget):
		print 'self.MAINWINDOW_OPEN = %s' % (self.MAINWINDOW_OPEN)
		if self.MAINWINDOW_OPEN == False:
			self.load_ovpn_server()
			try:
				mainwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
				mainwindow.connect("destroy",self.show_mainwindow)
				mainwindow.set_title("oVPN.to Client %s"%(CLIENTVERSION))
				mainwindow.set_icon_name(gtk.STOCK_HOME)
				mainwindow.set_border_width(4)
				mainframe = gtk.Frame()
				mainwindow.add(mainframe)
				mainframe.set_label("Anonymous oVPN Server")
				
				""" build serverlist """
				#liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str,'gboolean')
				liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str)
				treeview = gtk.TreeView(liststore)
				for server in self.OVPN_SERVER:
					countrycode = server[:2].lower()
					servershort = server[:3].upper()
					imgpath = self.FLAG_IMG[countrycode]
					countryimg = gtk.gdk.pixbuf_new_from_file(imgpath)
					#serverip = "127.0.0.1"
					serverip  = self.OVPN_SERVER_INFO[servershort][0]
					serverport = self.OVPN_SERVER_INFO[servershort][1]
					serverproto = self.OVPN_SERVER_INFO[servershort][2]
					servercipher = self.OVPN_SERVER_INFO[servershort][3]
					connected = True
					liststore.append([countryimg,server,serverip,serverport,serverproto,servercipher])
		
				cell = gtk.CellRendererPixbuf()
				column = gtk.TreeViewColumn('Country',cell)
				column.add_attribute(cell,"pixbuf",0)
				treeview.append_column(column)
				
				cell = gtk.CellRendererText()
				column = gtk.TreeViewColumn('Server',cell)
				column.add_attribute(cell,"text",1)
				column.set_sort_column_id(1)
				treeview.append_column(column)
				
				cell = gtk.CellRendererText()
				column = gtk.TreeViewColumn('IPv4',cell)
				column.add_attribute(cell,"text",2)
				column.set_sort_column_id(2)
				treeview.append_column(column)
				
				cell = gtk.CellRendererText()
				column = gtk.TreeViewColumn('Port',cell)
				column.add_attribute(cell,"text",3)
				column.set_sort_column_id(3)
				treeview.append_column(column)
				
				cell = gtk.CellRendererText()
				column = gtk.TreeViewColumn('Proto',cell)
				column.add_attribute(cell,"text",4)
				column.set_sort_column_id(4)
				treeview.append_column(column)				

				cell = gtk.CellRendererText()
				column = gtk.TreeViewColumn('Cipher',cell)
				column.add_attribute(cell,"text",5)
				column.set_sort_column_id(5)
				treeview.append_column(column)
				
				"""
				cell = gtk.CellRendererToggle()
				cell.set_radio(True)
				#cell.set_activatable(True)
				#cell.set_active(True)
				cell.connect("toggled",self.on_cell_radio_toggled)
				column = gtk.TreeViewColumn('Connected',cell)
				treeview.append_column(column)
				"""

				treeview.show()
				#treeview.connect("button_press_event",self.on_right_click_mainwindow)
				treeview.connect("cursor-changed",self.on_right_click_mainwindow)
				#treeview.connect("popup-menu",self.on_right_click_mainwindow)
				#treeview.connect("clicked",self.on_right_click_mainwindow)
				mainframe.add(treeview)
				mainwindow.show()
				mainframe.show()
				self.mainwindow = mainwindow
				self.treeview = treeview
				self.MAINWINDOW_OPEN = True
				self.mainwindow_liststore = liststore
				print 'mainwindow created'
				return True
			except:
				self.MAINWINDOW_OPEN = False
				print 'mainwindow failed'
		else:
			self.mainwindow.destroy()
			self.MAINWINDOW_OPEN = False
			print 'mainwindow destroy'
			

	def check_passphrase(self,widget):
		if self.PH == False:
			self.debug(text="def check_passphrase: popup receive passphrase")
			self.form_ask_passphrase()

		self.debug("def check_passphrase: passphrase loaded, try decrypt")
		#self.input_PH = self.plaintext_passphrase
		if self.read_config():
			if self.compare_confighash():
				#self.plaintext_passphrase = False
				#self.PH = False
				self.debug(text="def check_passphrase: self.compare_confighash() :True")
				return True
			else:
				try:
					os.remove(self.api_cfg)
					self.errorquit(text = "def check_passphrase: self.compare_confighash() failed. CFG deleted.")
				except:
					self.errorquit(text = "def check_passphrase: self.compare_confighash() failed. CFG delete failed.")
		else:
			self.PH = False
			self.check_remote_update(widget)
			try:
				os.remove(self.plaintext_passphrase_file)
				#self.errorquit(text=_("Decryption with plaintext_passphrase failed. txt removed."))
			except:
				pass
				#self.errorquit(text=_("Decryption with plaintext_passphrase failed. txt remove failed."))
					

	def preboot_check(self,logout):
		if self.pre0_detect_os():
			print "preboot_check: done"
			return True
		else:
			print "preboot_check: failed"
				
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
			if self.win_get_interfaces():
				if self.win_netsh_read_dns_to_backup():
					if self.win_detect_openvpn():
						if self.win_pre1_check_app_dir():
							if self.win_pre2_check_profiles_win():
								if self.win_pre3_load_profile_dir_vars():
									if self.check_config_folders():				
										return True
		elif OS == "linux2" :
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))	
		elif OS == "darwin":
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))
		else: 
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))

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
				return True
				
	def call_openvpn(self,widget,event,server):
		try:
			self.context_menu_servertab.popdown()
		except:
			pass
		try:
			thread_openvpn = threading.Thread(target=lambda server=server: self.openvpn(server))
			thread_openvpn.start()
		except:
			return False
		return True

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
				#self.statusbar_freeze = 6000
				#self.statusbar_text.set(text)
				#self.msgwarn(text=text)
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
					#self.statusbar_freeze = 6000
					text = "Could not start oVPN Watchdog"
					#self.statusbar_text.set(text)
					self.debug(text=text)
			else:
				self.debug("def openvpn: self.OVPN_AUTO_RECONNECT == False")
				
		else:
			self.debug(text="def openvpn: self.OVPN_THREADID = %s" % (self.OVPN_THREADID))
			#if tkMessageBox.askyesno("Change oVPN Server?", "oVPN is connected to: %s\n\nSwitch to oVPN Server: %s?"%(self.OVPN_CONNECTEDto,server)):
			self.debug(text="Change oVPN to %s" %(server))
			self.kill_openvpn()
			self.call_openvpn(None,None,server)
		#self.UPDATE_MENUBAR = True
		

	def inThread_timer_ovpn_ping(self):
		
		if self.timer_ovpn_ping_running == False:
			self.OVPN_PING_STAT = -2
			self.debug(text="def inThread_timer_ovpn_ping")
			self.timer_ovpn_ping_running = True
		
		if self.STATE_OVPN == True:
			
			if self.OS == "win32":
				ovpn_ping_cmd = "ping.exe -n 1 %s" % (self.OVPN_GATEWAY_IP4)
				PING_PROC = False
				try:
					PING_PROC = subprocess.check_output("%s" % (ovpn_ping_cmd),shell=True)
				except:
					self.debug(text="def inThread_timer_ovpn_ping: ping.exe failed")
					pass
					
				try:
					OVPN_PING_out = PING_PROC.split('\r\n')[2].split()[4].split('=')[1][:-2]
				except:
					if self.OVPN_PING_STAT < 0:
						self.debug(text="def inThread_timer_ovpn_ping: split ping failed, but normally not an issue while connection is testing")
						OVPN_PING_out = -2
					elif self.OVPN_PING_STAT >= 0:
						OVPN_PING_out = 9999
						#self.statusbar_freeze = 9000
						#text = _("oVPN connection to %s is unstable or timed out.") % (self.OVPN_CONNECTEDto)
						#self.statusbar_text.set(text)
						#self.debug(text="def inThread_timer_ovpn_ping: split ping failed, connection timed out")
				
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
					time.sleep(2)
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
			pass
			#self.msgwarn(_("Could not start Windows Firewall!"))
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
				string2 = "route.exe DELETE 0.0.0.0 MASK 128.0.0.0 %s" % (self.OVPN_GATEWAY_IP4)
				string3 = "route.exe DELETE 128.0.0.0 MASK 128.0.0.0 %s" % (self.OVPN_GATEWAY_IP4)
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
			self.call_openvpn(None,None,self.call_ovpn_srv)
			text = "oVPN process crashed and restarted."
			self.debug(text=text)
			return False
		elif self.STATE_OVPN == True:
			#self.debug(text="Watchdog: oVPN is running to %s %s" %(self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP))
			if self.timer_ovpn_ping_running == False: 
				self.debug("def inThread_timer_openvpn_reconnect starting ping timer")
				pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
				pingthread.start()
			else:
				#self.debug("def inThread_timer_openvpn_reconnect: timer_ovpn_ping is running")
				pass
			threading.Thread(target=self.inThread_timer_openvpn_reconnect).start()
			time.sleep(3)
			return True

			
	def kill_openvpn(self,*args):
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
		#self.UPDATE_MENUBAR = True
		self.del_ovpn_routes()
		
		
	def win_netsh_set_dns_ovpn(self):
		if not self.GATEWAY_DNS1 == self.OVPN_GATEWAY_IP4:
			self.debug(text="def win_netsh_set_dns_ovpn:")
			string1 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_EXT_DEVICE,self.OVPN_GATEWAY_IP4)
			string2 = "netsh interface ip set dnsservers \"%s\" static %s primary no" % (self.WIN_TAP_DEVICE,self.OVPN_GATEWAY_IP4)
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
			#self.statusbar_freeze = 5000
			#self.statusbar_text.set(text)
			self.DNS_SELECTED = dns_ipv4
			self.DNS_SELECTEDcountry = countrycode
			#self.UPDATE_MENUBAR = True
			self.debug(text=":true")
		except:
			#self.statusbar_freeze = 5000
			#self.statusbar_text.set(_("oVPN DNS Change failed!"))		
			self.debug(text="def win_netsh_change_dns_server: failed\n%s\n%s"%(string1,string2))
		
	
	def win_netsh_restore_dns_dhcp(self):
		os.system('netsh interface ip set dnsservers "%" dhcp'%(self.WIN_EXT_DEVICE))

		
	def win_netsh_restore_dns_from_backup(self):
		self.netsh_cmdlist = list()
		if not self.GATEWAY_DNS1 == self.OVPN_GATEWAY_IP4:
			string = 'interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS1)
			self.netsh_cmdlist.append(string)
			if self.win_join_netsh_cmd():
				text=_("Primary DNS Server restored to: %s")%(self.GATEWAY_DNS1)
				self.debug(text=text)
				#self.msgwarn(text=text)
			else:
				text=_("Error: Restoring your 1st DNS Server to %s failed.")%(self.GATEWAY_DNS2)
				self.debug(text=text)
				#self.msgwarn(text=text)
				
		if not self.GATEWAY_DNS2 == False:
			string = 'interface ip add dnsservers "%s" %s index=2 no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS2)
			self.netsh_cmdlist.append(string)
			if self.win_join_netsh_cmd():
				text=_("Secondary DNS Server restored to: %s")%(self.GATEWAY_DNS2)
				self.debug(text=text)
				#self.msgwarn(text=text)
			else:
				text=_("Error: Restoring your 2nd DNS Server to %s failed.")%(self.GATEWAY_DNS2)
				self.debug(text=text)
				#self.msgwarn(text=text)	
			

		
	def win_netsh_read_dns_to_backup(self):
		try:
			string = "netsh interface ipv4 show dns"
			read = subprocess.check_output("%s" % (string),shell=True)
			read = read.strip().decode('cp1258','ignore')
			search = '"%s"' % (self.WIN_EXT_DEVICE)
			list = read.strip(' ').split('\r\n')
			i, m1, m2, t = 0, 0, 0 ,0
			for line in list:
				#self.debug(text=line)
				if search in line:
					self.debug(text=line)
					self.debug(text="%s"%(i))
					m1=i+1

				if i == m1:
					if "DNS" in line:
						m2=i+1
						try:
							dns1 = line.strip().split(":")[1].lstrip()
							self.debug(text=dns1)
							if self.isValueIPv4(dns1):
								self.GATEWAY_DNS1 = dns1
						except:
							self.debug(text=line)
							
				if i == m2:
					try:
						dns2 = line.strip()
						if self.isValueIPv4(dns2):
								self.GATEWAY_DNS2 = dns2
								break					
					except:
						self.debug(text=line)

				i+=1
			self.debug(text="self.GATEWAY_DNS1 = %s + self.GATEWAY_DNS2 = %s"%(self.GATEWAY_DNS1,self.GATEWAY_DNS2))
			if not self.GATEWAY_DNS1 == False:				
				return True
		except:
			self.errorquit(_("Error in def win_netsh_read_dns_to_backup()"))

	def win_firewall_start(self):
		#self.pfw_bak = "%s\\pfw.%s.bak.wfw" % (self.pfw_dir,int(time.time()))
		#self.pfw_log = "%s\\pfw.%s.log" % (self.pfw_dir,int(time.time()))
		self.netsh_cmdlist = list()
		#self.netsh_cmdlist.append("advfirewall export %s" % (self.pfw_bak))
		#self.netsh_cmdlist.append("advfirewall reset")
		self.netsh_cmdlist.append("advfirewall set allprofiles state on")
		#self.netsh_cmdlist.append("advfirewall set currentprofile logging filename \"%s\"" % (self.pfw_log))
		self.netsh_cmdlist.append("advfirewall set privateprofile firewallpolicy blockinbound,blockoutbound")
		self.netsh_cmdlist.append("advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound")
		self.netsh_cmdlist.append("advfirewall set domainprofile firewallpolicy blockinbound,blockoutbound")
		return self.win_join_netsh_cmd()

		
	def win_firewall_add_rule_to_vcp(self,option):
		self.debug(text="def win_firewall_add_rule_to_vcp:")
		self.netsh_cmdlist = list()
		url = "https://%s" % (DOMAIN)
		ips = list()
		ips.append("178.17.170.116")
		ips.append(self.OVPN_GATEWAY_IP4)
		port = 443
		protocol = "tcp"
		for ip in ips:
			rule_name = "Allow OUT to %s at %s to Port %s Protocol %s" % (url,ip,port,protocol)
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % \
					(option,rule_name,ip,port,protocol)
			self.netsh_cmdlist.append(rule_string)			
		return self.win_join_netsh_cmd()

		
	def win_firewall_allow_outbound(self):
		self.debug(text="def win_firewall_allow_outbound:")
		self.netsh_cmdlist = list()
		self.netsh_cmdlist.append("advfirewall set privateprofile firewallpolicy blockinbound,allowoutbound")
		#self.netsh_cmdlist.append('interface set interface "%s" DISABLED'%(self.WIN_EXT_DEVICE))	
		#self.netsh_cmdlist.append('interface set interface "%s" ENABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()

		
	def win_firewall_modify_rule(self,option):
		self.netsh_cmdlist = list()
		rule_name = "Allow OUT oVPN-IP %s to Port %s Protocol %s" % (self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
		if option == "add":
			rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % (option,rule_name,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
		if option == "delete":
			rule_string = "advfirewall firewall %s rule name=\"%s\"" % (option,rule_name)
		#self.debug(text="def pfw: %s"%(rule_string))
		self.netsh_cmdlist.append(rule_string)
		return self.win_join_netsh_cmd()
			
	
	def win_join_netsh_cmd(self):
		self.pfw_cmd = "netsh.exe"
		i=0
		for cmd in self.netsh_cmdlist:
			fullstring = "%s %s" % (self.pfw_cmd,cmd)
			try: 
				exitcode = subprocess.call("%s" % (fullstring),shell=True)
				if exitcode == 0:
					self.debug(text="netshOK: %s: exitcode = %s" % (fullstring,exitcode))
					i+=1
				else:
					self.debug(text="netshERROR: %s: exitcode = %s" % (fullstring,exitcode))
			except:
				self.debug(text="def win_join_netsh_cmd: %s failed" % (fullstring))
		if len(self.netsh_cmdlist) == i:
			self.netsh_cmdlist = list()
			return True			
			
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
				if self.form_ask_userid():
					#if self.win_pre3_load_profile_dir_vars():
					return True
				
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
			
	def form_ask_passphrase(self):
		dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK)
		dialogWindow.set_title(_("Enter your Passphrase"))
		dialogWindow.set_markup(_("Enter your Passphrase"))	
		dialogBox = dialogWindow.get_content_area()
		ph1Entry = gtk.Entry()
		ph1Entry.set_visibility(False)
		ph1Entry.set_invisible_char("X")
		ph1Entry.set_size_request(200,24)
		ph1Label = gtk.Label("Passphrase:")		
		dialogBox.pack_start(ph1Label,False,False,0)
		dialogBox.pack_start(ph1Entry,False,False,0)
		dialogWindow.show_all()
		response = dialogWindow.run()
		self.dialogWindow_form_ask_passphrase = dialogWindow
		ph1 = ph1Entry.get_text().rstrip()		
		dialogWindow.destroy()
		if len(ph1) > 0:
			self.PH = ph1
			return True
		
		
	def form_ask_userid(self):
		dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK)
		dialogWindow.set_title(_("oVPN.to Setup"))
		dialogWindow.set_markup(_("Enter your oVPN.to Details"))
		dialogBox = dialogWindow.get_content_area()

		useridEntry = gtk.Entry()
		useridEntry.set_visibility(True)
		useridEntry.set_max_length(9)
		useridEntry.set_size_request(200,24)
		useridLabel = gtk.Label("User-ID:")
		
		apikeyEntry = gtk.Entry()
		apikeyEntry.set_visibility(False)
		apikeyEntry.set_max_length(128)
		apikeyEntry.set_invisible_char("*")
		apikeyEntry.set_size_request(200,24)
		apikeyLabel = gtk.Label("API-Key:")
		
		ph1Entry = gtk.Entry()
		ph1Entry.set_visibility(False)
		ph1Entry.set_invisible_char("X")
		ph1Entry.set_size_request(200,24)
		ph1Label = gtk.Label("Enter passphrase for encryption:")

		ph2Entry = gtk.Entry()
		ph2Entry.set_visibility(False)
		ph2Entry.set_invisible_char("X")
		ph2Entry.set_size_request(200,24)
		ph2Label = gtk.Label("Repeat your passphrase:")
		
		dialogBox.pack_start(useridLabel,False,False,0)
		dialogBox.pack_start(useridEntry,False,False,0)
		
		dialogBox.pack_start(apikeyLabel,False,False,0)
		dialogBox.pack_start(apikeyEntry,False,False,0)
		
		dialogBox.pack_start(ph1Label,False,False,0)
		dialogBox.pack_start(ph1Entry,False,False,0)
		
		dialogBox.pack_start(ph2Label,False,False,0)
		dialogBox.pack_start(ph2Entry,False,False,0)		
		
		dialogWindow.show_all()
		response = dialogWindow.run()
		
		userid = useridEntry.get_text().rstrip()
		apikey = apikeyEntry.get_text().rstrip()
		ph1 = ph1Entry.get_text().rstrip()
		ph2 = ph2Entry.get_text().rstrip()
		
		dialogWindow.destroy()
		
		if userid.isdigit() and userid > 1 and len(apikey) == 128 and apikey.isalnum() and ph1 == ph2 and len(ph1) > 0:
			self.USERID, self.profile = userid, userid
			self.APIKEY = apikey
			self.PH = ph1
			return True
		else:
			self.form_ask_userid()
			
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
		#self.root.iconbitmap(self.taskbar_icon)
		
		self.systray_icon_connected = "%s\\ico\\292.ico" % (self.bin_dir)
		self.systray_icon_disconnected = "%s\\ico\\263.ico" % (self.bin_dir)
		self.systray_icon_connect = "%s\\ico\\396.ico" % (self.bin_dir)
		self.systray_icon_hourglass = "%s\\ico\\205.ico" % (self.bin_dir)
		self.systray_icon_syncupdate = "%s\\ico\\266.ico" % (self.bin_dir)
		self.systray_icon_greenshield = "%s\\ico\\074.ico" % (self.bin_dir)
		
		if DEBUG: print("win_pre3_load_profile_dir_vars loaded")
		return True


	def check_config_folders(self):
		#try:
		#self.debug(text="def check_config_folders userid = %s" % (self.USERID))
		self.debug(text="def check_config_folders: userid found")
		if not os.path.exists(self.api_dir):
			if DEBUG: print("api_dir %s not found, creating." % (self.api_dir))
			os.mkdir(self.api_dir)
			
		if os.path.isfile(self.lock_file):				
			try:
				os.remove(self.lock_file)
			except:
				self.errorquit(_("Could not remove lock file.\nFile itself locked because another oVPN Client instance running?"))
			
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
			self.PH = ph
			
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
				self.debug(text="def check_config_folders :False self.api_cfg not found")
				if not self.PH == False:
					if self.write_new_config():
						if self.check_passphrase(None):
							return True
				else:
					if self.form_ask_userid():
						if self.write_new_config():
							if self.check_passphrase(None):
								return True
		else:
			self.errorquit(text = _("Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!") % (self.api_dir,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))
		#except:
		#	self.errorquit(text="def check_config_folders: failed")

	def load_decryption(self):
		self.debug(text="def load_decryption")
		if self.plaintext_passphrase == False:
			try:
				if len(self.PH) > 0: 
					self.aeskey = hashlib.sha256(self.PH.rstrip()).digest()
					return True
			except:
				return False
		else:
			try:
				if len(self.PH) > 0:
					self.aeskey = hashlib.sha256(self.PH.rstrip()).digest()
					return True
			except:
				return False		
		
	def read_config(self):
		self.debug(text="def read_config")
		if not self.PH == False and self.load_decryption():
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
							self.debug(text="def read_config CFGSHA = %s" % (CFGSHA))
							self.APIKEY = APIKEY[1]
							self.CFGSHA = CFGSHA[1]
							return True
			#self.statusbar_text.set(_("Invalid Passphrase!"))
			self.debug(text="def read_config passphrase :False")
			return False
		
	def write_new_config(self):
		self.aeskeyhash = hashlib.sha256(self.PH).digest()
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
		try:	
			cfg = open(self.api_cfg,'wb')
			cipherd_data_b64 = base64.b64encode(data2file)
			cfg.write(cipherd_data_b64)
			cfg.close()
			self.aesiv = False
			self.aeskeyhash = False
			self.hash2aes = False
			self.text2aes = False
			self.paddata = False			
			return True
		except:
			return False

			
	def make_confighash(self):
		self.text2hash1 = "USERID=%s,APIKEY=%s" % (self.USERID,self.APIKEY)
		self.hash2aes = hashlib.sha256(self.text2hash1).hexdigest()
			
			
	def compare_confighash(self):
		self.make_confighash()
		if self.hash2aes == self.CFGSHA:
			self.debug(text="def compare_confighash :True")
			return True
			
			
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

	def extract_ovpn(self):
		try:
			if os.path.isfile(self.zip_cfg) and os.path.isfile(self.zip_crt):			
				z1file = zipfile.ZipFile(self.zip_cfg)
				z2file = zipfile.ZipFile(self.zip_crt)
				if not os.path.isfile(self.vpn_cfg):
					try:
						os.mkdir(self.vpn_cfg)
					except:
						self.debug(text="def extract_ovpn: %s not found, create failed."%(self.vpn_cfg))
				z1file.extractall(self.vpn_cfg)
				z2file.extractall(self.vpn_cfg)
				if self.write_last_update():
					self.extract = True
					#self.statusbar_text.set("Certificates and Configs extracted.")
					return True
		except:
			self.debug(text="def extract_ovpn: failed")
				

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
			text = text=_("API Connection Timeout to https://%s!"%(DOMAIN))
			self.debug(text=text)
			#self.msgwarn(text=text)
			
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
			
			
	def check_inet_connection(self):
		s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = DOMAIN
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
					#self.msgwarn(text=text)			
					return False
		return True
	
	def systray_timer(self):
		if self.stop_systray_timer == True:
			return False
		self.systray_timer_running = True
		text = False
		systraytext = False
		
		if self.timer_check_certdl_running == True:
			text = _("Checking for Updates!")
			systraytext = text
			systrayicon = self.systray_icon_syncupdate
			
		elif self.STATE_OVPN == False:
			text = _("oVPN disconnected!")
			systraytext = text
			systrayicon = self.systray_icon_disconnected
			try:
				if self.OVPN_AUTO_CONNECT_ON_START == True and not self.OVPN_FAV_SERVER == False:
					self.call_openvpn(widget,event,self.OVPN_FAV_SERVER)
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
			elif self.OVPN_PING_LAST == 9999:
				text = _("oVPN connection to %s is unstable or timed out.") % (self.OVPN_CONNECTEDto)
				systraytext = text
				systrayicon = self.systray_icon_disconnected
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
				d, h = divmod(h, 24)
				self.OVPN_CONNECTEDtimetext = "%d:%d:%02d:%02d"  % (d,h,m,s)
				#systraytext = _("oVPN is connected to %s")%(self.OVPN_CONNECTEDto)
				text = _("oVPN is connected to %s ( %s / %s ms ) %s")%(self.OVPN_CONNECTEDto,self.OVPN_PING_LAST,self.OVPN_PING_STAT,self.OVPN_CONNECTEDtimetext)
				systraytext = text
				systrayicon = self.systray_icon_connected
				
		if not self.systraytext_from_before == systraytext and not systraytext == False:
			self.systraytext_from_before = systraytext
			self.tray.set_from_file(systrayicon)
			self.tray.set_tooltip(('%s'%(systraytext)))
			
		if not self.statustext_from_before == text:
			#self.statusbar_text.set(text)
			self.statustext_from_before = text
		
		time.sleep(1)
		self.thread_systray_timer = threading.Thread(target=self.systray_timer)
		self.thread_systray_timer.start()
				
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
			
		
	def load_ovpn_server(self):
		if os.path.exists(self.vpn_cfg):
			content = os.listdir(self.vpn_cfg)
			#self.debug(text="def load_ovpn_server: content = %s " % (content))
			self.OVPN_SERVER = list()
			for file in content:
				if file.endswith('.ovpn.to.ovpn'):
					filepath = "%s\\%s" % (self.vpn_cfg,file)
					servername = file[:-5]
					flagcountry = servername[:2].lower()
					servershort = servername[:3].upper()					
					try:
						serverinfo = self.OVPN_SERVER_INFO[servershort]
					except:
						if os.path.isfile(filepath):
							serverinfo = list()
							for line in open(filepath):
								if "remote " in line:
									#print line
									try:
										ip = line.split()[1]
										port = int(line.split()[2])
										if self.isValueIPv4(ip) and port > 0 and port < 65535:
											serverinfo.append(ip)
											serverinfo.append(port)																						
									except:
										self.errorquit(text=_("Could not read Servers Remote-IP:Port from config: %s") % (self.ovpn_server_config_file) )

										
								if "proto " in line:
									#print line
									try:
										proto = line.split()[1]
										if proto.lower()  == "tcp" or proto.lower() == "udp":
											proto = proto.upper()
											serverinfo.append(proto)
									except:
										self.errorquit(text=_("Could not read Servers Protocol from config: %s") % (self.ovpn_server_config_file) )
										
								if "cipher " in line:
								#print line
									try:
										cipher = line.split()[1]
										serverinfo.append(cipher)
									except:
										self.errorquit(text=_("Could not read Servers Cipher from config: %s") % (self.ovpn_server_config_file) )
										
	
							self.OVPN_SERVER_INFO[servershort] = serverinfo
							#print self.OVPN_SERVER_INFO[servershort]
					try:
						flagicon = self.FLAG_IMG[flagcountry]
					except:						
						imgfile = '%s\\ico\\flags\\%s.png' % (self.bin_dir,flagcountry)
						if not os.path.isfile(imgfile):
							imgfile = '%s\\ico\\flags\\00.png' % (self.bin_dir)
						#self.debug(text="loading flagicon: %s"%(imgfile))
						#img = gtk.Image()
						#img.set_from_file(imgfile)
						#self.FLAG_IMG[flagcountry] = img
						self.FLAG_IMG[flagcountry] = imgfile
					self.OVPN_SERVER.append(servername)
					#self.debug(text="def load_ovpn_server: file = %s " % (file))
			self.OVPN_SERVER.sort()
		else:
			cfg = open(self.api_upd,'w')
			cfg.write("0")
			cfg.close()
		
			
	def on_closing(self, widget):
		if self.STATE_OVPN == True:
			return False
		else:
			try: self.about_dialog.destroy()
			except:	pass
			try: self.dialogWindow_form_ask_passphrase.destroy()
			except: pass
			self.win_netsh_restore_dns_from_backup()
			self.win_firewall_allow_outbound()
			text=_("close app")
			self.debug(text=text)
			#self.systray_menu.destroy()
			#gtk.main_quit()
			self.stop_systray_timer = True
			self.remove_lock()
			gtk.main_quit()
			sys.exit()
			
			
	def remove_lock(self):
		if os.path.isfile(self.lock_file):
			text=_("close lock")
			self.debug(text=text)
			self.LOCK.close()
			try:
				os.remove(self.lock_file)
				text=_("remove lock")
				self.debug(text=text)
				return True
			except:
				text=_("remove lock failed")
				self.debug(text=text)
				#self.msgwarn()
		else:
			text=_("Could not delete LOCK. File not found.")
			self.debug(text=text)
			#self.msgwarn()

			
	def errorquit(self,text):
		self.debug(text)
		#tkMessageBox.showinfo(_("Error"),"%s" % (text))
		sys.exit()			
			
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

	def init_localization(self):
		loc = locale.getdefaultlocale()[0][0:2]
		filename = "locale/messages_%s.mo" % loc
		try:
			translation = gettext.GNUTranslations(open(filename, "rb"))
		except IOError:
			translation = gettext.NullTranslations()
			print("Language file for %s not found" % loc)
		
		translation.install()

	def get_now_unixtime(self):
		self.now_unixtime = int(time.time())
		return self.now_unixtime
		
	def defundef(self,widget):
		try:
			print 'widget=%s'%(widget)
		except:
			pass
		self.debug(text="self.defundef()")	

def app():
	Systray()
	try:
		gtk.gdk.threads_init()
		gtk.main()
	except KeyboardInterrupt:
		print('KeyboardInterrupt')

if __name__ == "__main__":
	app()
