# -*- coding: utf-8 -*-
import gtk
from datetime import datetime as datetime
from Crypto.Cipher import AES
import types
import os
import platform
import sys
import hashlib
import random
import base64
import time
import zipfile
import subprocess
import threading
import socket
import gettext
import locale
import _winreg
import requests
from ConfigParser import SafeConfigParser


CLIENTVERSION="v0.3.0-gtk"

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
		if self.preboot_check(logout=False) == True:
			self.tray = gtk.StatusIcon()
			self.tray.set_from_stock(gtk.STOCK_PROPERTIES)
			self.tray.connect('popup-menu', self.on_right_click)
			self.tray.connect('activate', self.on_left_click)
			self.tray.set_tooltip(('oVPN.to Client'))
			self.systray_timer()
		else:
			sys.exit()
		

	def self_vars(self):
		self.MAINWINDOW_OPEN = False
		self.debug_log = False
		self.OVPN_LATEST = 238
		self.OVPN_LATEST_BUILT = "Aug 4 2015"
		self.OVPN_LATEST_BUILT_TIMESTAMP = 1438639200
		self.OVPN_DL_URL = False
		self.OVPN_WIN_DL_URL_x86 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.8-I601-i686.exe"
		self.OVPN_WIN_DLHASH_x86 = ".."
		self.OVPN_WIN_DL_URL_x64 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.8-I601-x86_64.exe"
		self.OVPN_WIN_DLHASH_x64 = ".."

		self.MAIN_WINDOW_OPEN = True
		self.isSMALL_WINDOW = False
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
		self.statusbar_freeze = False
		self.SYSTRAYon = False
		self.screen_width = 320
		self.screen_height = 240
		self.USERID = False
		self.PH = False
		self.STATE_OVPN = False
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS1 = False
		self.GATEWAY_DNS2 = False
		self.WIN_TAP_DEVICE = False
		self.WIN_EXT_DEVICE = False
		self.WIN_EXT_DHCP = False
		self.OVPN_SERVER = list()
		self.OVPN_FAV_SERVER = False
		#self.OVPN_FAV_SERVER = "BG1.ovpn.to"
		self.OPENVPN_EXE = False
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
		
		self.ENABLE_mainwindow_menubar = False
		self.SHOW_ABOUT_DIALOG = False
		self.ENABLE_statusbar_text = False
		
		#self.save_passphrase = IntVar()
		
		self.FLAG_IMG = {}
		self.systray_menu = False
		self.OVPN_SERVER_INFO = {}

		
	def on_right_click_mainwindow(self, treeview, event):
		try:
			path, column, __, __ = self.treeview.get_path_at_pos(int(event.x), int(event.y))
		except:
			return False
		try:
			self.systray_menu.popdown()
			self.systray_menu = False
		except:
			pass
		selected_row = int(path[0])
		servername = self.OVPN_SERVER[selected_row]
		print servername
		#print 'def on_right_click_mainwindow: widget = %s' % (widget)
		#if event.button == 1:
		#	self.debug(text="mainwindow left click")		
		if event.button == 3:
			self.debug(text="mainwindow right click")
			self.make_context_menu_servertab(servername)

	
	def make_context_menu_servertab(self,servername):
		#print event
		context_menu_servertab = gtk.Menu()
		
		if self.OVPN_CONNECTEDto == servername:
			disconnect = gtk.MenuItem("Disconnect %s"%(self.OVPN_CONNECTEDto))
			disconnect.show()
			disconnect.connect('activate', self.kill_openvpn)
			context_menu_servertab.append(disconnect)
		else:		
			connect = gtk.MenuItem('Connect to %s'%(servername))
			connect.show()
			context_menu_servertab.append(connect)
			connect.connect('button-release-event',self.call_openvpn,servername)
		sep = gtk.SeparatorMenuItem()
		sep.show()
		context_menu_servertab.append(sep)	
		
		if self.OVPN_FAV_SERVER == servername:
			delfavorite = gtk.MenuItem('Remove AutoConnect: %s'%(servername))
			delfavorite.show()
			delfavorite.connect('button-release-event',self.del_ovpn_favorite_server,servername)
			context_menu_servertab.append(delfavorite)
		else:
			setfavorite = gtk.MenuItem('Set AutoConnect: %s'%(servername))
			setfavorite.show()
			setfavorite.connect('button-release-event',self.set_ovpn_favorite_server,servername)
			context_menu_servertab.append(setfavorite)
			
		
		context_menu_servertab.popup(None, None, None, 3, int(time.time()), self.treeview)
		self.context_menu_servertab = context_menu_servertab
		
	"""
	*fixme*
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
		if not self.systray_menu == False:
			self.destroy_systray_menu()
		else:
			self.make_systray_menu(event_button, event_time)
		

	def on_left_click(self, widget):
		try:
			self.systray_menu.popdown()
			self.systray_menu = False
		except:
			pass
			
	""" *fixme* (unused)	
	def systray_focus_out(self,widget,event):
		print 'systray_focus_out'
		self.systray_menu.popdown()
		self.systray_menu = False
	"""

	def make_systray_menu(self, event_button, event_time):
		try:
			self.load_ovpn_server()
			self.systray_menu = gtk.Menu()

			#show force update item
			forceupdate = gtk.MenuItem('Force Config Update')
			forceupdate.show()
			self.systray_menu.append(forceupdate)
			
			#show normal update item
			normalupdate = gtk.MenuItem('Check Config Update')
			normalupdate.show()
			self.systray_menu.append(normalupdate)
			
			
			# SIGNALS
			normalupdate.connect('activate', self.check_remote_update_cb)
			forceupdate.connect('activate', self.cb_force_update)

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
				# SIGNALS
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
			# SIGNALS
			mainwindow.connect('activate', self.show_mainwindow)
			
			
			if self.STATE_OVPN == False:
				sep = gtk.SeparatorMenuItem()
				sep.show()
				self.systray_menu.append(sep)		
				# show about dialog
				about = gtk.MenuItem('About')
				about.show()
				self.systray_menu.append(about)
				# SIGNALS
				about.connect('activate', self.show_about_dialog)
				# add quit item
				quit = gtk.MenuItem('Quit')
				quit.show()
				self.systray_menu.append(quit)
				# SIGNALS
				quit.connect('activate', self.on_closing)

			self.systray_menu.popup(None, None, None, event_button, event_time, self.tray)
		except:
			text="def make_systray_menu: failed"
			self.debug(text=text)

	
	def make_systray_server_menu(self):
		try:
			for menuserver in self.OVPN_SERVER:
				servershort = menuserver[:3]
				textstring = "%s (%s:%s)" % (servershort,self.OVPN_SERVER_INFO[servershort][2],self.OVPN_SERVER_INFO[servershort][1])
				countrycode = servershort[:2].lower()
				if self.OVPN_CONNECTEDto == menuserver:
					servershort = "[ "+servershort+" ]"
					serveritem = gtk.ImageMenuItem(servershort)
				else:
					serveritem = gtk.ImageMenuItem(textstring)
					# SIGNALS
					serveritem.connect('button-press-event', self.call_openvpn, menuserver)
				img = gtk.Image()
				imgpath = self.FLAG_IMG[countrycode]
				img.set_from_file(imgpath)
				serveritem.set_always_show_image(True)
				serveritem.set_image(img)				
				self.systray_menu.append(serveritem)
				serveritem.show()
		except:
			self.destroy_systray_menu()
			text = "def make_systray_server_menu: failed"
			self.debug(text=text)

		
	
	"""
	*fixme* duplicate old backup
	
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
	
	def check_remote_update_cb(self,widget):
		self.destroy_systray_menu()
		if self.check_remote_update():
			return True
	
	def check_remote_update(self):
		if self.timer_check_certdl_running == False:	
			if self.check_inet_connection():
				self.debug(text="def check_remote_update:")
				if self.check_passphrase():
					self.make_progressbar()
					try:
						thread_certdl = threading.Thread(name='certdl',target=self.inThread_timer_check_certdl)
						thread_certdl.start()
						threadid_certdl = threading.currentThread()
						self.debug(text="threadid_certdl = %s" %(threadid_certdl))
						return True
					except:
						self.debug(text="starting thread_certdl failed")
		return False
		
	def make_progressbar(self):
		try:
			self.progressbarfraction = 0.1
			self.progresswindow = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
			self.progresswindow.set_default_size(250,128)
			self.progresswindow.set_border_width(6)
			self.progresswindow.set_title("oVPN Server Update")
			self.progresswindow.set_icon_from_file(self.systray_icon_syncupdate)
			#self.progresswindow.set_resizable(False)
			#self.progresswindow.set_type_hint(GDK_WINDOW_TYPE_HINT_MENU)
			#self.progresswindow.
			self.progressbar = gtk.ProgressBar()
			self.progressbar.set_pulse_step(0)
			self.progresswindow.add(self.progressbar)
			self.progresswindow.show_all()
			self.progresswindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		except:
			text = "def make_progressbar: failed"
			self.debug(text=text)
			
	def set_progressbar(self,text):
		try:
			if self.progressbarfraction < 0.95:
				self.progressbarfraction += 0.05
			else:
				self.progressbarfraction = 0.05
			self.progressbar.set_text(text)
			self.progressbar.set_fraction(self.progressbarfraction)
		except:
			text = "def set_progressbar: failed"
			self.debug(text=text)
		
	def inThread_timer_check_certdl(self):
		self.timer_check_certdl_running = True
		text="Checking for oVPN Updates..."
		self.set_progressbar(text)
		try:
			if len(self.OVPN_SERVER) == 0:
				cfg = open(self.api_upd,'w')
				cfg.write("0")
				cfg.close()		
		except:
			pass
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
										text = _("Error: Extraction failed!")
										self.set_progressbar(text)										
										self.body = "done"
										self.timer_check_certdl_running = False
										self.progressbar.set_fraction(0)
										return False
			else:
				text = _("Certificates and Configs up to date!")
				self.set_progressbar(text)
				self.set_statusbar_text(text)
				self.progressbar.set_fraction(1)
				self.timer_check_certdl_running = False
				return True
				
		else:
			self.PH = False
			self.debug(text="self.curl_api_request(API_ACTION = lastupdate): failed")
	

	def show_about_dialog(self, widget):
		self.destroy_systray_menu()
		if self.SHOW_ABOUT_DIALOG == False:	
			try:
				about_dialog = gtk.AboutDialog()
				self.about_dialog = about_dialog
				about_dialog.set_destroy_with_parent (True)
				about_dialog.set_name('oVPN.to')		
				about_dialog.set_version('Client %s'%(CLIENTVERSION))
				about_dialog.set_copyright('(C) 2010 - 2015 oVPN.to')
				about_dialog.set_comments((ABOUT_TEXT))
				about_dialog.set_authors(['oVPN.to <support@ovpn.to>'])
				about_dialog.run()
				about_dialog.destroy()
				self.SHOW_ABOUT_DIALOG = True
			except:
				text = "def show_about_dialog: failed"
				self.debug(text=text)
		else:
			self.about_dialog.destroy()
			self.SHOW_ABOUT_DIALOG = False
			
	""" fixme """
	def mainwindow_menubar(self):
		if self.ENABLE_mainwindow_menubar == True:
			try:
				self.mb.destroy()
				print 'menubar destroy1'
			except:
				pass
			try:
				self.mb = gtk.MenuBar()
				
				#self.mainwindow_vbox.add(self.mb)
				self.mainwindow_vbox.pack_start(self.mb,False,False,0)
				optionsmenu = gtk.Menu()
				options = gtk.MenuItem('Options')
				options.set_submenu(optionsmenu)
				

				
				#if not self.PH == False:
				#	del_PH = gtk.MenuItem("Clear Passphrase from Disk and RAM")
				#	del_FAV.connect('button-release-event',self.defundef,None)
				#	optionsmenu.append(del_PH)				
				
				if not self.OVPN_FAV_SERVER == False:
					del_FAV = gtk.MenuItem("Disable AutoConnect")
					del_FAV.connect('button-release-event',self.del_ovpn_favorite_server,self.OVPN_FAV_SERVER)
					optionsmenu.append(del_FAV)

				if not self.OVPN_FAV_SERVER == False and self.STATE_OVPN == False:
					con_FAV = gtk.MenuItem("Connect to %s" % (self.OVPN_FAV_SERVER))				
					con_FAV.connect('button-release-event',self.call_openvpn,self.OVPN_FAV_SERVER)
					optionsmenu.append(con_FAV)
					
				if self.STATE_OVPN == True:
					disconnect = gtk.MenuItem("Disconnect %s"%(self.OVPN_CONNECTEDto))
					disconnect.connect('activate', self.kill_openvpn)
					optionsmenu.append(disconnect)
				
				
					
				forceupdate = gtk.MenuItem("Force Server-Config Update")
				forceupdate.connect('activate', )
				optionsmenu.append(forceupdate)
					
				self.mb.append(options)
				self.mb.show_all()
			except:
				try:
					self.mb.destroy()
				except:
					pass
	
		
	def mainwindow_ovpn_server(self):
		self.notebook = gtk.Notebook()	
		label = gtk.Label(_("oVPN Server"))
		vbox = gtk.VBox(False,1)	
		self.notebook.append_page(vbox,label)
		self.mainwindow_vbox.add(self.notebook)
		mainframe = gtk.Frame()
		vbox.pack_start(mainframe,True,True,0)
		mainframe.set_label("Anonymous oVPN Server")
		""" build serverlist """
		#liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str,'gboolean')
		liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str)
		self.mainwindow_liststore = liststore
		treeview = gtk.TreeView(liststore)
		self.treeview = treeview
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
		*fixme*
		cell = gtk.CellRendererToggle()
		cell.set_radio(True)
		#cell.set_activatable(True)
		#cell.set_active(True)
		cell.connect("toggled",self.on_cell_radio_toggled)
		column = gtk.TreeViewColumn('Connected',cell)
		treeview.append_column(column)
		"""

		treeview.connect("button_release_event",self.on_right_click_mainwindow)
		scrolledwindow = gtk.ScrolledWindow()
		scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrolledwindow.add(treeview)
		mainframe.add(scrolledwindow)

		""" statusbar """
		label = gtk.Label()
		text = "Welcome to oVPN.to! Have a nice and anonymous day!"
		self.statusbar_text = label
		self.statusbar_text.set_label(text)
		vbox.pack_start(label,False,False,0)
		
	def show_mainwindow(self,widget):
		self.destroy_systray_menu()
		print 'self.MAINWINDOW_OPEN = %s' % (self.MAINWINDOW_OPEN)
		if self.MAINWINDOW_OPEN == False:
			self.load_ovpn_server()
			try:
				mainwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
				self.mainwindow = mainwindow
				mainwindow.connect("destroy",self.show_mainwindow)
				mainwindow.set_title("oVPN.to Client %s"%(CLIENTVERSION))
				mainwindow.set_icon_name(gtk.STOCK_HOME)
				mainwindow.set_default_size(640,480)
				mainwindow.set_border_width(4)
				
				self.mainwindow_vbox = gtk.VBox(False,1)
				self.mainwindow.add(self.mainwindow_vbox)
				
				self.mainwindow_ovpn_server()
				
				self.mainwindow_menubar()
				
				mainwindow.show_all()
				self.MAINWINDOW_OPEN = True
				print 'mainwindow created'
				return True
			except:
				self.MAINWINDOW_OPEN = False
				print 'mainwindow failed'
		else:
			self.mainwindow.destroy()
			self.MAINWINDOW_OPEN = False
			#self.destroy_systray_menu()
			print 'mainwindow destroy'
	
	def destroy_systray_menu(self):
		try:
			self.systray_menu.popdown()
			self.systray_menu = False
		except:
			text = "def destroy_systray_menu: failed"
			self.debug(text=text)
	
	def set_statusbar_text(self,text):
		if self.MAINWINDOW_OPEN == True:
			if self.ENABLE_statusbar_text:
				self.statusbar_text.set_label(text)
				self.statusbar_freeze = True

	def check_passphrase(self):
		self.read_options_file()
		if self.PH == False:
			self.debug(text="def check_passphrase: popup receive passphrase")
			self.form_ask_passphrase()
		self.debug("def check_passphrase: passphrase loaded, try decrypt")
		if self.read_apikey_config():
			if self.compare_confighash():
				self.debug(text="def check_passphrase: self.compare_confighash() :True")
				return True
		else:
			self.form_reask_userid()
					

	def preboot_check(self,logout):
		if self.pre0_detect_os():
			self.load_ovpn_server()
			""" *fixme* """
			#self.show_mainwindow(widget="NULL")
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

					
			if self.win_pre1_check_app_dir():
				if self.win_pre2_check_profiles_win():
					if self.win_pre3_load_profile_dir_vars():
						if self.check_config_folders():
							if self.read_options_file():
								if self.read_interfaces():									
									if self.write_options_file():
										return True
										
		elif OS == "linux2" :
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))	
		elif OS == "darwin":
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))
		else: 
			self.errorquit(text = _("Operating System not supported: %s") % (self.OS))

	"""	
	*fixme* (unused)
	def get_connection_name_from_guid(self,iface_guids):
		iface_names = ['(unknown)' for i in range(len(iface_guids))]
		reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		reg_key = _winreg.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
		for i in range(len(iface_guids)):
			try:
				reg_subkey = _winreg.OpenKey(reg_key, iface_guids[i] + r'\Connection')
				iface_names[i] = _winreg.QueryValueEx(reg_subkey, 'Name')[0]
			except:
				pass
		return iface_names
	"""
	
	def read_interfaces(self):
		if self.OS == "win32":
			if self.win_read_interfaces():
				if self.win_netsh_read_dns_to_backup():
					return True
			
	def win_read_interfaces(self):
		self.INTERFACES = list()
		string = "netsh interface show interface"
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
			text="Possible Error reading your Interfaces from netsh.exe. Contact support@ovpn.to with Error-ID:\nADAPTERS[1]=(%s)\n" % (ADAPTERS[1])
			self.msgwarn(text=text)
		
		text = "def win_read_interfaces: LANG = %s" % (LANG)
		self.debug(text=text)
		for line in ADAPTERS:
			print line
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
							print nface
						else:
							nface = iface
					interface = nface
				else:
					interface = interface[0]
				self.INTERFACES.append(interface)
			except:
				pass
		self.INTERFACES.pop(0)		
		self.debug(text="%s"%(self.INTERFACES))			
		if len(self.INTERFACES)	< 2:
			self.errorquit(text=_("Could not read your Network Interfaces! Please install OpenVPN or check if your TAP-Adapter is really enabled and driver installed."))
		self.win_detect_openvpn()
		string = '"%s" --show-adapters' % (self.OPENVPN_EXE)
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
					self.win_enable_tap_interface()
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
			text = _("No OpenVPN TAP-Adapter found! Please install openVPN Version\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64)	
			self.errorquit(text=text)
		else:
			self.INTERFACES.remove(self.WIN_TAP_DEVICE)
			self.debug(text="remaining INTERFACES = %s"%(self.INTERFACES))
			if len(self.INTERFACES) > 1:
				if not self.WIN_EXT_DEVICE == False:
					if self.WIN_EXT_DEVICE in self.INTERFACES:
						self.debug(text="loaded self.WIN_EXT_DEVICE %s from options file"%(self.WIN_EXT_DEVICE))					
						return True
						
				dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK)
				text = _("Choose your External Network Adapter!")
				dialogWindow.set_title(text)
				dialogWindow.set_markup(text)
				dialogBox = dialogWindow.get_content_area()
				
				liststore = gtk.ListStore(str)
				combobox = gtk.ComboBox(liststore)
				cell = gtk.CellRendererText()
				combobox.pack_start(cell, True)
				combobox.add_attribute(cell, 'text', 0)
				combobox.set_wrap_width(5)
				for INTERFACE in self.INTERFACES:
					print "add interface %s to combobox" % (INTERFACE)
					liststore.append([INTERFACE])
				combobox.set_model(liststore)
				combobox.connect('changed',self.interface_selector_changed_cb)			
					
				dialogBox.pack_start(combobox,False,False,0)
				dialogWindow.show_all()
				print "open interface selector"
				dialogWindow.run()
				print "close interface selector"
				if not self.WIN_EXT_DEVICE == False:
					dialogWindow.destroy()
					return True					
			elif len(self.INTERFACES) < 1:
				self.errorquit(text=_("No Network Adapter found!"))
			else:
				self.WIN_EXT_DEVICE = self.INTERFACES[0]
				text = _("External Interface = %s")%(self.WIN_EXT_DEVICE)
				#self.msgwarn(text=text)
				self.debug(text=text)
				return True
			
	def interface_selector_changed_cb(self, combobox):
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_EXT_DEVICE = model[index][0]
			text = "selected IF: %s" % (self.WIN_EXT_DEVICE)
			self.debug(text=text)
		return

	def set_ovpn_favorite_server(self,widget,event,server):
		try:
			self.OVPN_FAV_SERVER = server
			self.OVPN_AUTO_CONNECT_ON_START = True
			self.write_options_file()
			try:
				self.context_menu_servertab.popdown()
			except:
				pass
			self.mainwindow_menubar()	
			text = "oVPN AutoConnect: %s" % (server)
			self.set_statusbar_text(text)
			return True
		except:
			self.msgwarn(text="def set_ovpn_favorite_server: failed")
			
	def del_ovpn_favorite_server(self,widget,event,server):
		try:
			self.OVPN_FAV_SERVER = False
			self.OVPN_AUTO_CONNECT_ON_START = False
			self.write_options_file()
			try:
				self.context_menu_servertab.popdown()
			except:
				pass
			self.mainwindow_menubar()			
			text = "oVPN AutoConnect: removed %s" % (server)
			self.set_statusbar_text(text)
			return True
		except:
			self.msgwarn(text="def del_ovpn_favorite_server: failed")			
				
	def call_openvpn(self,widget,event,server):
		self.destroy_systray_menu()		
		try:
			self.context_menu_servertab.popdown()
		except:
			pass
		self.mainwindow_menubar()
		try:
			thread_openvpn = threading.Thread(target=lambda server=server: self.openvpn(server))
			thread_openvpn.start()
		except:
			return False
		return True

	def openvpn(self,server):
		if self.STATE_OVPN == False:
			self.mainwindow_menubar()
			self.OVPN_AUTO_RECONNECT = True
			self.ovpn_server_UPPER = server
			self.ovpn_server_LOWER = server.lower()

			self.ovpn_server_config_file = "%s\%s.ovpn" % (self.vpn_cfg,self.ovpn_server_UPPER)
			if os.path.isfile(self.ovpn_server_config_file):
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
			else:
				return False
				
			
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
				self.set_statusbar_text(text)
				self.msgwarn(text=text)
				
			if self.OVPN_AUTO_RECONNECT == True:
				self.debug("def openvpn: self.OVPN_AUTO_RECONNECT == True")
				self.OVPN_RECONNECT_NOW = False
				try:
					#threading.Thread(target=self.inThread_timer_openvpn_reconnect).start()
					thread_timer_openvpn_reconnect = threading.Thread(target=self.inThread_timer_openvpn_reconnect)
					thread_timer_openvpn_reconnect.start()
					self.OVPN_PING_TIMER_THREADID = threading.currentThread()
					self.debug(text="Started: self.inThread_timer_openvpn_reconnect() on Thread: %s" %(self.OVPN_PING_TIMER_THREADID))
					text = "oVPN Watchdog enabled. Connecting to %s" % (server)
					self.set_statusbar_text(text)
					self.debug(text=text)
					self.mainwindow_menubar()
				except:
					text = "Could not start oVPN Watchdog"
					self.set_statusbar_text(text)
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
						#text = _("oVPN connection to %s is unstable or timed out.") % (self.OVPN_CONNECTEDto)
						#self.set_statusbar_text(text)
						#self.debug(text="def inThread_timer_ovpn_ping: split ping failed, connection timed out")
				
				pingsum = 0
				if OVPN_PING_out > 0:
					self.OVPN_PING.append(OVPN_PING_out)
					self.OVPN_PING_LAST = OVPN_PING_out
				if len(self.OVPN_PING) > 16:
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
					#self.debug(text="done: rejoin def inThread_timer_ovpn_ping() %s: total threads: %s, ping=%s" %(self.OVPN_PING_TIMER_THREADID,threading.active_count(),OVPN_PING_out))	
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
		self.win_enable_tap_interface()
		self.OVPN_CONNECTEDto = self.call_ovpn_srv
		self.win_netsh_set_dns_ovpn()
		self.OVPN_PING_STAT = -1
		self.OVPN_PING_LAST = -1
		self.debug(text="def call_openvpn self.OVPN_CONNECTEDto = %s" %(self.OVPN_CONNECTEDto))
		self.OVPN_CONNECTEDtime = self.get_now_unixtime()
		self.mainwindow_menubar()
		if not self.win_firewall_start():
			self.msgwarn(_("Could not start Windows Firewall!"))
		self.win_firewall_modify_rule(option="add")
		time.sleep(5)		
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
		self.mainwindow_menubar()
		
		
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
		time.sleep(10)
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
			return True

			
	def kill_openvpn(self,*args):
		self.destroy_systray_menu()
		self.mainwindow_menubar()
		self.OVPN_AUTO_RECONNECT = False
		self.OVPN_RECONNECT_NOW = False
		self.debug(text="def kill_openvpn")	
		exe = self.OPENVPN_EXE.split("\\")[-1]
		string = "taskkill /im %s /f" % (exe)
		try:
			self.OVPN_KILL2 = subprocess.check_output("%s" % (string),shell=True)
		except:
			pass
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
			self.set_statusbar_text(text)
			self.DNS_SELECTED = dns_ipv4
			self.DNS_SELECTEDcountry = countrycode
			#self.UPDATE_MENUBAR = True
			self.debug(text=":true")
		except:
			text = _("oVPN DNS Change failed!")
			#set_statusbar_text(self,text)		
			self.debug(text="def win_netsh_change_dns_server: failed\n%s\n%s"%(string1,string2))
		
	
	
	def win_netsh_restore_dns_from_backup(self):
		self.netsh_cmdlist = list()
		if self.WIN_EXT_DHCP == True:
			string = 'interface ip set dnsservers "%s" dhcp' % (self.WIN_EXT_DEVICE)
			self.netsh_cmdlist.append(string)
			if self.win_join_netsh_cmd():
				text=_("Primary DNS Server restored to DHCP.")
				self.debug(text=text)
				return True
			else:
				text=_("Error: Restoring your Primary DNS Server to DHCP failed.")%(self.GATEWAY_DNS2)
				self.debug(text=text)
				#self.msgwarn(text=text)
				return False
			
			
		if not self.GATEWAY_DNS1 == self.OVPN_GATEWAY_IP4:
			string = 'interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS1)
			self.netsh_cmdlist.append(string)
			if self.win_join_netsh_cmd():
				text=_("Primary DNS Server restored to: %s")%(self.GATEWAY_DNS1)
				self.debug(text=text)
			else:
				text=_("Error: Restoring your Primary DNS Server to %s failed.")%(self.GATEWAY_DNS2)
				self.debug(text=text)
				#self.msgwarn(text=text)
				
		if not self.GATEWAY_DNS2 == False:
			string = 'interface ip add dnsservers "%s" %s index=2 no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS2)
			self.netsh_cmdlist.append(string)
			if self.win_join_netsh_cmd():
				text=_("Secondary DNS Server restored to: %s")%(self.GATEWAY_DNS2)
				self.debug(text=text)
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
			self.debug(text="def win_netsh_read_dns_to_backup:")
			for line in list:
				if search in line:
					text = "found: %s in %s line %s" % (search,line,i)
					self.debug(text=text)
					m1=i+1

				if i == m1:
					if "DHCP" in line:
						self.WIN_EXT_DHCP = True
						return True
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
		ips.append("93.115.92.252")
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
		return self.win_join_netsh_cmd()
		
	def win_enable_tap_interface(self):
		self.debug(text="def win_enable_tap_interface:")
		self.netsh_cmdlist = list()
		self.netsh_cmdlist.append('interface set interface "%s" ENABLED'%(self.WIN_TAP_DEVICE))
		return self.win_join_netsh_cmd()
		
	"""
	*fixme* (unused)
	def win_disable_interface(self):
		self.debug(text="def win_disable_interface:")
		self.netsh_cmdlist = list()
		self.netsh_cmdlist.append('interface set interface "%s" DISABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()		
		
	def win_ensable_interface(self):
		self.debug(text="def win_ensable_interface:")
		self.netsh_cmdlist = list()
		self.netsh_cmdlist.append('interface set interface "%s" ENABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()
	"""
		
		
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

	def win_select_openvpn(self):
		text = "OpenVPN not found, please select openvpn.exe"
		self.msgwarn(text=text)
		dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,
									   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("*.exe")
		filter.add_pattern("*.exe")
		response = dialog.run()

		if response == gtk.RESPONSE_OK:
			self.OPENVPN_EXE = dialog.get_filename()
			text = dialog.get_filename(), 'selected: %s' % (self.OPENVPN_EXE)			
			self.debug(text=text)
			dialog.destroy()
			return True
		elif response == gtk.RESPONSE_CANCEL:
			text = 'Closed, no files selected'
			self.debug(text=text)
			dialog.destroy()
			return False			
				

		
	
	def win_detect_openvpn(self):
		os_programfiles = "PROGRAMFILES PROGRAMFILES(x86) PROGRAMW6432"
		for getenv in os_programfiles.split():
			programfiles = os.getenv(getenv)
			file = "%s\\OpenVPN\\bin\\openvpn.exe" % (programfiles)
			if os.path.isfile(file): 
				self.debug(text="def win_detect_openvpn: %s" % (file))
				self.OPENVPN_EXE = file
				break
		
		if self.OPENVPN_EXE == False or not os.path.isfile(self.OPENVPN_EXE):
			if not self.win_select_openvpn():
				text = _("No OpenVPN TAP-Adapter found! Please install openVPN Version\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64)
				self.errorquit(text=text)
	
		text = "Using: %s" % (self.OPENVPN_EXE)
		self.debug(text=text)		
		try:
			out, err = subprocess.Popen("\"%s\" --version" % (self.OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()		
		except:
			self.errorquit(text=_("Could not detect openVPN Version!"))
		try:	
			self.OVPN_VERSION = out.split('\r\n')[0].split( )[1].replace(".","")
			self.OVPN_BUILT = out.split('\r\n')[0].split("built on ",1)[1].split()
			self.OVPN_LATEST_BUILT = self.OVPN_LATEST_BUILT.split()
			text = "self.OVPN_VERSION = %s, self.OVPN_BUILT = %s, self.OVPN_LATEST_BUILT = %s" % (self.OVPN_VERSION,self.OVPN_BUILT,self.OVPN_LATEST_BUILT)
			self.debug(text=text)
			if self.OVPN_VERSION >= self.OVPN_LATEST:
				if self.OVPN_BUILT == self.OVPN_LATEST_BUILT:
					text = "self.OVPN_BUILT == self.OVPN_LATEST_BUILT: True"
					self.debug(text=text)
					return True
				else:
					built_mon = self.OVPN_BUILT[0]
					built_day = int(self.OVPN_BUILT[1])
					built_year = int(self.OVPN_BUILT[2])
					builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
					string_built_time = time.strptime(builtstr,"%b/%d/%Y")
					built_month_int = int(string_built_time.tm_mon)
					built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					text = "openvpn built_timestamp = %s self.OVPN_LATEST_BUILT_TIMESTAMP = %s" % (built_timestamp,self.OVPN_LATEST_BUILT_TIMESTAMP)
					self.debug(text=text)
					if built_timestamp >= self.OVPN_LATEST_BUILT_TIMESTAMP:						
						return True
					else:
						text = _("Please update your openVPN Version to\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64)
						self.msgwarn(text=text)
			else:
				text = _("Please update your openVPN Version to\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64)
				self.msgwarn(text=text)
		except:
			self.errorquit(text=_("def win_detect_openvpn: failed"))
		
			
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
		self.destroy_systray_menu()
		if self.timer_check_certdl_running == False:
			try:
				dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK_CANCEL)
				dialogWindow.set_title(_("Enter your Passphrase"))
				dialogWindow.set_markup(_("Enter your Passphrase"))	
				dialogBox = dialogWindow.get_content_area()
				checkbox = gtk.CheckButton("Save Passphrase in File?")
				checkbox.show()
				ph1Entry = gtk.Entry()
				ph1Entry.set_visibility(False)
				ph1Entry.set_invisible_char("X")
				ph1Entry.set_size_request(200,24)
				ph1Label = gtk.Label("Passphrase:")
				
				dialogBox.pack_start(ph1Label,False,False,0)
				dialogBox.pack_start(ph1Entry,False,False,0)
				dialogBox.pack_start(checkbox,False,False,0)
				dialogWindow.show_all()
				response = dialogWindow.run()
				self.dialogWindow_form_ask_passphrase = dialogWindow
				ph1 = ph1Entry.get_text().rstrip()
				saveph = checkbox.get_active()
				print 'checkbox saveph = %s' %(saveph)

				if response == gtk.RESPONSE_CANCEL:
					print "response: btn cancel %s" % (response)
					self.PH = False				
				
				if response == gtk.RESPONSE_OK:	
					if len(ph1) > 0:
						self.PH = ph1
						if self.read_apikey_config():
							if self.compare_confighash():
								self.debug(text="def check_passphrase: self.compare_confighash() :True")		
								if saveph == True:
									self.write_options_file()
				
				dialogWindow.destroy()
				
			except:
				self.debug(text="def form_ask_passphrase: Failed")
		
		
	def form_ask_userid(self):
		try:
			dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK_CANCEL)
			dialogWindow.set_title(_("oVPN.to Setup"))
			dialogWindow.set_markup(_("Enter your oVPN.to Details"))
			dialogBox = dialogWindow.get_content_area()

			useridEntry = gtk.Entry()
			useridEntry.set_visibility(True)
			useridEntry.set_max_length(9)
			useridEntry.set_size_request(200,24)
			useridLabel = gtk.Label("oVPN.to User-ID:")
			
			apikeyEntry = gtk.Entry()
			apikeyEntry.set_visibility(False)
			apikeyEntry.set_max_length(128)
			apikeyEntry.set_invisible_char("*")
			apikeyEntry.set_size_request(200,24)
			apikeyLabel = gtk.Label("Update API-Key:")
			
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
			if response == gtk.RESPONSE_OK:			
				if userid.isdigit() and userid > 1 and len(apikey) == 128 and apikey.isalnum() and ph1 == ph2 and len(ph1) > 0:
					self.USERID, self.profile = userid, userid
					self.APIKEY = apikey
					self.PH = ph1
					return True
				else:
					self.form_ask_userid()
		except:
			self.debug(text="def form_ask_userid: Failed")
			
	def form_reask_userid(self):
		if self.form_ask_userid():
			if self.write_new_apikey_config():
				if self.check_passphrase():
					return True
		return False
			
	def win_pre3_load_profile_dir_vars(self):
		self.api_dir = "%s\\%s" % (self.app_dir,self.profile)
		self.bin_dir = "%s\\bin\\client\\dist" % (self.app_dir)
		self.lock_file = "%s\\lock.file" % (self.app_dir)
		
		self.debug_log = "%s\\client_debug.log" % (self.api_dir)
		if DEBUG:
			try:
				dbg = open(self.debug_log,'wb')
				dbg.write("DEBUG_LOG START\r\n")
				dbg.close()
			except: 
				print("Delete %s failed"%(self.debug_log))
		
		self.opt_file = "%s\\options.cfg" % (self.api_dir)		
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
		
		self.systray_icon_connected = "%s\\ico\\292.ico" % (self.bin_dir)
		self.systray_icon_disconnected = "%s\\ico\\263.ico" % (self.bin_dir)
		self.systray_icon_connect = "%s\\ico\\396.ico" % (self.bin_dir)
		self.systray_icon_hourglass = "%s\\ico\\205.ico" % (self.bin_dir)
		self.systray_icon_syncupdate = "%s\\ico\\266.ico" % (self.bin_dir)
		self.systray_icon_greenshield = "%s\\ico\\074.ico" % (self.bin_dir)
		
		self.CA_FILE = "%s\\cacert_ovpn.pem" % (self.bin_dir)
		if os.path.isfile(self.CA_FILE):
			os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), self.CA_FILE)
		else:
			self.debug(text="CA_FILE not found")
		
		self.debug(text="win_pre3_load_profile_dir_vars loaded")
		return True


	def check_config_folders(self):
		try:
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
					text = "writing lastupdate to %s" % (self.api_upd)
					self.debug(text=text)
					self.reset_last_update()
					
				if not os.path.isfile(self.api_upd):
					self.errorquit(text = _("Creating FILE\n%s\nfailed!") % (self.api_upd))
					
				if os.path.isfile(self.api_cfg):
					self.debug(text="def check_config_folders :True")
					return True
				else:
					self.debug(text="def check_config_folders :False self.api_cfg not found")
					if not self.PH == False:
						if self.write_new_apikey_config():
							if self.check_passphrase():
								return True
					else:
						if self.form_ask_userid():
							if self.write_new_apikey_config():
								if self.check_passphrase():
									return True
			else:
				self.errorquit(text = _("Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!") % (self.api_dir,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))
		except:
			self.errorquit(text="def check_config_folders: failed")
		
	def read_options_file(self):		
		if os.path.isfile(self.opt_file):
			try:
				parser = SafeConfigParser()
				parser.read(self.opt_file)
				
				try:
					self.PH = parser.get('oVPN','passphrase')
					if self.PH == "False":
						self.PH = False
				except:
					pass					
				
				try:
					self.OVPN_AUTO_CONNECT_ON_START = parser.getboolean('oVPN','autoconnect')
					if self.OVPN_AUTO_CONNECT_ON_START == "False": 
						self.OVPN_AUTO_CONNECT_ON_START = False
				except:
					pass			
				
					
				try:
					self.OVPN_FAV_SERVER = parser.get('oVPN','favserver')
					if self.OVPN_FAV_SERVER == "False": 
						self.OVPN_FAV_SERVER = False
				except:
					pass					
				
				try:
					self.WIN_EXT_DEVICE = parser.get('oVPN','winextdevice')
					if self.WIN_EXT_DEVICE == "False": 
						self.WIN_EXT_DEVICE = False
				except:
					pass

				try:
					self.OPENVPN_EXE = parser.get('oVPN','openvpnexe')
					if self.OPENVPN_EXE == "False":
						self.OPENVPN_EXE = False
				except:
					pass
					
				return True
			except:
				self.msgwarn(text="def read_options_file: read failed")
				try:
					self.os.remove(self.opt_file)
				except:
					pass
		else:
			try:
				cfg = open(self.opt_file,'w')
				parser = SafeConfigParser()
				parser.add_section('oVPN')
				parser.set('oVPN','passphrase','False')
				parser.set('oVPN','autoconnect','False')
				parser.set('oVPN','favserver','False')
				parser.set('oVPN','winextdevice','False')
				parser.set('oVPN','openvpnexe','False')
				parser.write(cfg)
				cfg.close()
				return True
			except:
				self.debug(text="def read_options_file: create failed")
	
	def write_options_file(self):
		try:
			cfg = open(self.opt_file,'w')
			parser = SafeConfigParser()
			parser.add_section('oVPN')
			parser.set('oVPN','passphrase','%s'%(self.PH))
			parser.set('oVPN','autoconnect','%s'%(self.OVPN_AUTO_CONNECT_ON_START))
			parser.set('oVPN','favserver','%s'%(self.OVPN_FAV_SERVER))
			parser.set('oVPN','winextdevice','%s'%(self.WIN_EXT_DEVICE))
			parser.set('oVPN','openvpnexe','%s'%(self.OPENVPN_EXE))
			
			parser.write(cfg)
			cfg.close()
			return True
		except:
			self.debug(text="def write_options_file: failed")

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
		
	def read_apikey_config(self):
		#self.debug(text="def read_apikey_config: self.PH = %s" %(self.PH))
		if not self.PH == False and self.load_decryption() and os.path.isfile(self.api_cfg):
			self.debug(text="def read_apikey_config: go")
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
					#self.debug(text="def read_apikey_config USERID = %s :True" % (USERID))
					#self.debug(text="def read_apikey_config USERID = profile-folder :True" % (USERID))
					if len(APIKEY) == 2 and len(APIKEY[1]) == 128 and APIKEY[1].isalnum():						
						#self.debug(text="def read_apikey_config APIKEY len = %s :True" % (len(APIKEY)))			
						if len(CFGSHA) == 2 and len(CFGSHA[1]) == 64 and CFGSHA[1].isalnum():
							#self.debug(text="def read_apikey_config CFGSHA = %s" % (CFGSHA))
							self.APIKEY = APIKEY[1]
							self.CFGSHA = CFGSHA[1]
							return True
			text = _("Invalid Passphrase!")
			self.set_statusbar_text(text)
			self.debug(text="def read_apikey_config passphrase :False")
			self.form_ask_passphrase()
			return False
		
	def write_new_apikey_config(self):
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
		else:
			self.PH = False
			return False
			
			
	def check_last_server_update(self):
		if os.path.isfile(self.api_upd):
			cfg = open(self.api_upd,'r')
			read_data = cfg.read()
			cfg.close()
			if read_data < self.remote_lastupdate:
				text = "our last update: %s" % (read_data)
				self.debug(text=text)
				return True
		else:
			cfg = open(self.api_upd,'wb')
			cfg.write("0")
			cfg.close()
			return True
			
	
	def write_last_update(self):
		try:
			cfg = open(self.api_upd,'wb')
			cfg.write("%s" % (self.get_now_unixtime()))
			cfg.close()
			return True
		except:
			self.debug(text="def write_last_update: Failed")
			return False
			
			
	def reset_last_update(self):
		try:
			cfg = open(self.api_upd,'wb')
			cfg.write("0")
			cfg.close()
			return True
		except:
			self.debug(text="def write_last_update: Failed")
			return False		

	def cb_force_update(self,widget):
		self.destroy_systray_menu()
		if self.reset_last_update():
			self.check_remote_update_cb(widget)
			
	def delete_dir(self,path):
		if self.OS == "win32":
			string = 'rmdir /S /Q "%s"' % (path)
			text = "def delete_dir: %s" % (string)
			self.debug(text=text)
			subprocess.check_output("%s" % (string),shell=True)
		
			
	def extract_ovpn(self):
		try:
			if os.path.isfile(self.zip_cfg) and os.path.isfile(self.zip_crt):			
				z1file = zipfile.ZipFile(self.zip_cfg)
				z2file = zipfile.ZipFile(self.zip_crt)
				if os.path.isdir(self.vpn_cfg):
					self.delete_dir(self.vpn_cfg)
				if not os.path.isdir(self.vpn_cfg):
					try:
						os.mkdir(self.vpn_cfg)
					except:
						self.debug(text="def extract_ovpn: %s not found, create failed."%(self.vpn_cfg))
				try:
					z1file.extractall(self.vpn_cfg)
					z2file.extractall(self.vpn_cfg)
					if self.write_last_update():
						text = "Certificates and Configs extracted."
						self.set_statusbar_text(text)
						return True
				except:
						text = "Error on extracting Certificates and Configs!"
						self.set_statusbar_text(text)
						self.debug(text=text)
						return False
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
			
		self.body = False
		text = "def curl_api_request: API_ACTION = %s" % (API_ACTION)
		self.debug(text=text)			

		try:
			r = requests.post(url,data=values)
			if self.API_ACTION == "getconfigs" or self.API_ACTION == "getcerts":
				self.body = r.content
			else:
				self.body = r.text
			if self.body.isalnum() and len(self.body) <= 128:
				self.set_progressbar(text=self.body)
				self.debug("requests: self.body = %s"%(self.body))
		except requests.exceptions.ConnectionError as e:
			text = "def curl_api_request: requests error on: %s = %s" % (self.API_ACTION,e)
			self.set_progressbar(text)
			self.debug(text=text)
			return False
		except:
			text = "def curl_api_request: requests error on: %s failed!" % (self.API_ACTION,e)
			self.set_progressbar(text)
			self.debug(text=text)
		
		
		if not self.body == False:
		
			if not self.body == "AUTHERROR":
				self.curldata = self.body.split(":")
				if self.curldata[0] == "AUTHOK":
					self.curldata = self.curldata[1]
					return True
			else:
				text = _("Invalid User-ID / API-Key or Account expired.")
				self.msgwarn(text=text)
				#os.remove(self.api_cfg)
				#self.errorquit()				
				return self.form_reask_userid()
		
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
			self.msgwarn(text=text)
			self.win_firewall_add_rule_to_vcp(option="add")
			time.sleep(2)
			if not self.try_socket(host,port):
				text=_("2) Could not connect to vcp.ovpn.to\nRetry")
				self.msgwarn(text=text)
				time.sleep(2)
				if not self.try_socket(host,port):
					#text="3) Could not connect to vcp.ovpn.to\nTry setting firewall rule to allowing outbound connections to world!"
					#self.win_firewall_allow_outbound()
					text=_("3) Could not connect to vcp.ovpn.to\n")
					self.msgwarn(text=text)			
					return False
		return True
	
	def systray_timer(self):
		if self.stop_systray_timer == True:
			return False
		self.systray_timer_running = True
		text = False
		systraytext = False
		
		if self.statusbar_freeze == True:
			time.sleep(1)
			self.thread_systray_timer = threading.Thread(target=self.systray_timer)
			self.thread_systray_timer.start()
			self.statusbar_freeze = False
			return True
		
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
					self.call_openvpn(None,None,self.OVPN_FAV_SERVER)
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
			#elif self.OVPN_PING_LAST == 9999:
				#text = _("oVPN connection to %s is unstable or timed out.") % (self.OVPN_CONNECTEDto)
				#systraytext = text
				#systrayicon = self.systray_icon_disconnected
				#self.debug(text=text)
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
				#text = _("oVPN is connected ( %s ) to %s ( %s / %s ms )")%(self.OVPN_CONNECTEDtimetext,self.OVPN_CONNECTEDto,self.OVPN_PING_LAST,self.OVPN_PING_STAT)
				text = _("oVPN is connected ( %s ) to %s ( %s ms )")%(self.OVPN_CONNECTEDtimetext,self.OVPN_CONNECTEDto,self.OVPN_PING_LAST)
				systraytext = text
				systrayicon = self.systray_icon_connected
		try:	
			if not self.systraytext_from_before == systraytext and not systraytext == False:
				self.systraytext_from_before = systraytext
				self.tray.set_from_file(systrayicon)
				self.tray.set_tooltip(('%s'%(systraytext)))
			
			#fixme: memoryleak
			if not self.statustext_from_before == text:
				self.set_statusbar_text(text)
				self.statustext_from_before = text
			
		except:
			pass
		
		time.sleep(5)
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
					countrycode = servername[:2].lower()
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
						flagicon = self.FLAG_IMG[countrycode]
					except:						
						imgfile = '%s\\ico\\flags\\%s.png' % (self.bin_dir,countrycode)
						if not os.path.isfile(imgfile):
							if not self.load_flags_from_remote(countrycode,imgfile) == True:
								imgfile = '%s\\ico\\flags\\00.png' % (self.bin_dir)
						self.FLAG_IMG[countrycode] = imgfile
					self.OVPN_SERVER.append(servername)
					#self.debug(text="def load_ovpn_server: file = %s " % (file))
			self.OVPN_SERVER.sort()
		else:
			cfg = open(self.api_upd,'w')
			cfg.write("0")
			cfg.close()
	
	def load_flags_from_remote(self,countrycode,imgfile):
		try:
			url = "https://%s/img/flags/%s.png" % (DOMAIN,countrycode)
			r = requests.get(url)
			body = r.content
			
			fp = open(imgfile, "wb")
			fp.write(body)
			fp.close()
			self.debug(text="def load_flags_from_remote: %s loaded"%(countrycode))
			return True
		except:
			self.debug(text="def load_flags_from_remote: %s failed"%(countrycode))
			
	def on_closing(self, widget):
		if self.STATE_OVPN == True:
			return False
		else:
			try: 
				self.about_dialog.destroy()
			except:	
				pass
			try: 
				self.dialogWindow_form_ask_passphrase.destroy()
			except: 
				pass
			
			dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_NONE)
			dialog.set_markup("Do you really want to quit?")
			dialog.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL)
			dialog.add_button(gtk.STOCK_QUIT,gtk.RESPONSE_CLOSE)
			response = dialog.run()
			dialog.destroy()
			
			if response == gtk.RESPONSE_CANCEL:
				return False
			if response == gtk.RESPONSE_CLOSE:
				self.ask_loadorunload_fw()
			else:
				return False			
			
			
			text=_("close app")
			self.debug(text=text)
			#self.systray_menu.destroy()
			self.stop_systray_timer = True
			self.remove_lock()
			gtk.main_quit()
			sys.exit()
			
	def ask_loadorunload_fw(self):
		try:
			dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
			dialog.set_markup("Do you want to disable the firewall?\n\nPress 'YES' to allow direct access to the internet!\nPress 'NO' to keep your internet blocked!")
			response = dialog.run()
			dialog.destroy()
			if self.OS == "win32":
				if response == gtk.RESPONSE_NO:
					self.win_firewall_start()
					self.win_netsh_restore_dns_from_backup()
						
				if response == gtk.RESPONSE_YES:
					self.win_firewall_allow_outbound()
					self.win_netsh_restore_dns_from_backup()
					
		except:
			text = "def ask_loadorunload_fw: failed"
			self.msgwarn(text=text)
			
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
				self.msgwarn(text=text)
		else:
			text=_("Could not delete LOCK. File not found.")
			self.msgwarn(text=text)

			
	def errorquit(self,text):
		text = "errorquit: %s" % (text)
		self.debug(text=text)
		try:
			message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
			message.set_markup("%s"%(text))
			message.run()
			message.destroy()
		except:
			text = "%s failed" % (text)
			self.debug(text=text)
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
		return int(time.time())
		
	def defundef(self,widget):
		try:
			print 'widget=%s'%(widget)
		except:
			pass
		self.debug(text="self.defundef()")
		
	def msgwarn(self,text):
		try:
			self.debug(text=text)
			message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
			message.set_markup("%s"%(text))
			message.run()
			message.destroy()
		except:
			self.debug(text=text)

		
		
def app():
	Systray()
	try:
		gtk.gdk.threads_init()
		gtk.main()
	except KeyboardInterrupt:
		print('KeyboardInterrupt')

if __name__ == "__main__":
	app()
