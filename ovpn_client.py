# -*- coding: utf-8 -*-
# when run it manually from cmd type before: set PYTHONIOENCODING=UTF-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, GObject
GObject.threads_init()

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
import requests
import json
from ConfigParser import SafeConfigParser

CLIENTVERSION="v0.5.0z-gtk3"
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
		self.init_localization()
		self.self_vars()
		self.tray = Gtk.StatusIcon()
		self.tray.set_from_stock(Gtk.STOCK_EXECUTE)
		self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		self.window.connect("delete-event", Gtk.main_quit)
		if self.preboot():
			self.tray.connect('popup-menu', self.on_right_click)
			self.tray.connect('activate', self.on_left_click)
			self.tray.set_tooltip_markup(CLIENT_STRING)
			if self.UPDATEOVPNONSTART == True and self.check_inet_connection() == True:
				self.check_remote_update()
			if self.TAP_BLOCKOUTBOUND == True:
				self.win_firewall_tap_blockoutbound()
			self.systray_timer()
			#atexit.register(self.on_closing,widget="atexit")
		else:
			sys.exit()

	def self_vars(self):
		self.APIURL = "https://%s:%s/%s" % (DOMAIN,PORT,API)

		self.OS = sys.platform
		self.MAINWINDOW_OPEN = False
		self.ACCWINDOW_OPEN = False
		self.DEBUG = True
		self.DEBUGfrombefore = False
		self.DEBUGcount = 0
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
		self.systraytext_from_before = False
		self.systrayicon_from_before = False
		self.stop_systray_timer = False
		self.inThread_jump_server_running = False
		self.USERID = False
		self.STATE_OVPN = False
		self.LAST_CFG_UPDATE = 0
		self.LAST_CHECK_MYIP = 0
		self.LAST_PING_EXEC = 0
		self.LAST_CHECK_INET = 0
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS1 = False
		self.GATEWAY_DNS2 = False
		self.WIN_TAP_DEVICE = False
		self.WIN_TAP_DEVS = list()
		self.TAP_BLOCKOUTBOUND = False
		self.WIN_EXT_DEVICE = False
		self.WIN_EXT_DHCP = False
		self.NO_WIN_FIREWALL = False
		self.NO_DNS_CHANGE = False
		self.MYDNS = {}
		self.NETSH_CMDLIST = list()
		self.ROUTE_CMDLIST = list()

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
		self.OVPN_PING_EVERY = "15,30"
		self.INTERFACES = False

		self.d0wns_DNS = {}

		self.PASSPHRASE = False
		self.PPP_NO_SAVE = True
		self.LOAD_ACCDATA = True

		self.FLAG_IMG = {}
		self.FLAG_HASHS = {'ad.png':'8adee4d665c8119ec4f5ad5c43a9a85450e0001c275b6a0ee178ffbf95c4c043','ae.png':'6f20d866841c4514782a46142df22b70b8da9783c513e3d41d8f3313483fe38d','af.png':'c1054fb8d9595948aa96bc57c9ab6fb6b3770d2ee7e09ba7e46b09b21bf51bcd','ag.png':'0dfb5c39e2a3eebe18b431cf41c8c892ab5f1249caa09d43fa1dd7394d486cd7','ai.png':'721542818b00e197fea04303b0afc24763017c14b8cd791dfaf08411d9a99cae','al.png':'3f7278c0c4272b6ff65293c18cdbb7e2e272f59dabe16619c22051d319ef44e0','am.png':'e34d4e7961e7e994775dddfa994e4d9f709876634d36facff6bac70155597c23','an.png':'4c9bd8548dfa58fdf9e6ac703f94c8b96d8136c42b06fbdc8e2d8817e592ffde','ao.png':'49b0a50005440417bd679d03d4d78f9ba0d1c457285c97e94f36e56b1e8b623b','ar.png':'776fbb0600f99ccdc44e2ee7f8b6559988c443f3a754792585b1b7008aaedb91','as.png':'3ef7f1b82b2f28cae0c7df163c5ce9227ef37244da85118374869fc5f2e05868','at.png':'a3acc39d4b61f9cc1056c19176d1559f0dacbb0587a700afdbe4d881040ccd52','au.png':'a7f9683bc4240ef940ee3d4aaf127515add30d25b0b2179a6cdec23944635603','aw.png':'2dc58a1fcd65957140fa06ba9b2f1bd1b3643724cef0905e23e1561a5b3dfa5b','ax.png':'3f38a42fd54e4c7cb1154026f734bc444f9cc942b8b91f099cc65dccf6c7f431','az.png':'45da74f4c8a50cfc13ff612e9052a7df77fae155e20c2b67ec34c4e3d46dcebe','ba.png':'8aab9c83759b1a121043ae5526d7bd4174d6612c7d0c697609731e9f7b819b6b','bb.png':'93977880a9ae72940ed7560758b51a1ba32d27aa5fd2ad5ca38d86fe10061c1a','bd.png':'174d63b291981bb85bc6e90975b23dfd0538a28af9cd99e3530d750dfedf1807','be.png':'45f75a63fadde9018fa5698884c7fb0b2788e8f72ee1f405698b872d59674262','bf.png':'9069275d6c18aaf67463b1fffb7cdefe10da76cd955ee2c5022cff06efa241f2','bg.png':'c4838a24ad388f934b04dbf9dba02a8bc6e9e58d0a1076477b47b5987a5c2d64','bh.png':'d8dfd5dc5157e30aa9e241e4a7d13513dedf608045b6736716ea6c5ca4047855','bi.png':'f2489dfb66723f8585830a51ec1ff4f5a514f5b6fd8bfa423e2880118e18ba75','bj.png':'3eb78453cea7aac6afca9a54ec8a2b0d4998df40a0c5494534992fc38f5c2402','bm.png':'e8087faf03f478266cc279382009391155615af6a7f3eaa47b21717ce8eaa401','bn.png':'05a6a5da710bdd98eb1d8c9b097b687a34ace268e106bd3437298d0ffc8a7473','bo.png':'a802b4b4b31e9c87062e725760b052083ca0d2cc2cced10f44731688289c4ca5','br.png':'dff6f4d907290bdbe74812bf73b590f268694e0a30e64b4bb24b803a47b3e319','bs.png':'aabf518642010552de4ed24400d5d40fa7e6bf1142a183f4989dad88d7cede5e','bt.png':'ae10dea2abad314551038e08771857c6d67d3684487782275c094dab5dfda21e','bv.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','bw.png':'166ffee51259387356bdadeb22cdc7d053fc89ef6f51ae3c774d522a4dfaf08e','by.png':'cc2b61fff898086df311b22f06fcb400e64c4627ef8495755b24e2f7f3e05429','bz.png':'f7ca75c8e16fb2a11cb30d9f9e7006505a719601b84a6135f478f62a7ff214f1','ca.png':'3a6c5facc8613948b81833101a2ff8c3a114813ce24077585faee268b8ffb541','catalonia.png':'58665da49b1ebca85993de6e799f423b4589359b2eb43cb6b8bb81223fc02b10','cc.png':'25d60905c65429304e895c47dfb9da424190d9be01d924b75cc5cb76a1bdf39c','cd.png':'d26464766b63c4c361821355ca7a36ef288ef72fd6bad23421c695e1dd527743','cf.png':'a476f7f6228a456d767f2f97b73b736cee01a64f0acdac1d0721dcd609476e8a','cg.png':'9b8814baab3cff79d037ee1cf49ecd8993d95169d4d8090d9a7d0eccf18d26fd','_ch.png':'da8c749e3f0119f91875ddaa116f265d440150c8f647dd3f634a0eb0b474e2c9','ch.png':'1a847144ea964355e4abd101179c374d3fd6c7c75f1ad58ca2d3b0946a1cd40f','ci.png':'4a5179c7a54ce4395781fbb535bbffb03b4bdbd56046f9209d4f415b1ad5b19c','ck.png':'38d9b787d10aafadd8aa1deeae343dff8fee30d230d86dfab14df9002dfecb01','cl.png':'516cde928be7cf45bedd28cb9bed291035aa9106a21335a922ca1e0987a8fdb6','cm.png':'3e785d74c3a21a99972a38b021eb475d99940239bc0bc1a4020bc77a9ecf70e1','cn.png':'7058233b5bdfdd4279e92e9dfe64bd4a61afd7e76d97dba498ce1d5777b92185','co.png':'ddbda18a0e3a272e63f2a3e734893bd848fceb76855057ad263823edbb4ca4df','cr.png':'f22dbafc8eaee237cac9a35777e98818868e2e87e47b640bbf4c487afc10b07e','cs.png':'3fe11c2a0b4c2b50035c224d2e6c87ba19a05663811c459d4e3a2f780aede957','cu.png':'9fc72810592496349d14e13a4c5b61b8cae7388be4d5d395ac2bf99d2f3ed4fa','cv.png':'22650dac4b404ca32e73fe64df90e21a955ec8f67a3dc2ef50135d342143dabb','cx.png':'8dc0ef0ae06c717937acbf0bafd947cc9a0c9984bd6839bc6ba22c82857acd43','cy.png':'bd7198c76594a6ed1147412a4e37d1ae258d1fd9358d96ded9b524dbeea7bc30','cz.png':'0f39366d88fabe6f6f5c7a3cb6a11165de6bc6bc2108802c49df5f9840bc6541','de.png':'3323814006fe6739493d27057954941830b59eff37ebaac994310e17c522dd57','dj.png':'4be41bfd725282adc410a23488c290028b8a433e614dffaa49d0cb28d6bbb39f','dk.png':'0c9213be3a5cbc5d656093ca415d2b9f52de067d8ed5d7cfd704ce8cd0564d2c','dm.png':'c91813a9d0753c4f99503e7123c1b40b2c805ae36128afb9eb6384c275c38195','do.png':'505c31334e03e2280f5fe3ebbbc210f71f5ee7242c9021c3d5727ec4114b5b68','dz.png':'f2ea00daa66609ba95a18dac13f3ba0a3d2522f8edbcd109e5fd25fcf1289591','ec.png':'ab0ecc4936f0623e3e298ee6f45d88d208e13b72453ec1bbe2be0abdbefeabbb','ee.png':'6ebe8f7e33db530652a0b1c6394ec4f50a2fcc0b4a31d1ab33db65d6815dd087','eg.png':'e4c44b7ce8a72720e2ab8b38b8885fca36dda04daa14ae37909bbd501d853074','eh.png':'61eda51aebe540c16219767b5c8e64b821d6f857832d8594086fb871c817fd19','england.png':'24c0c0d1e833516a54d890cb63adcd6acbb40c14eac80e5bcd07d92df9ff4cfb','er.png':'cabe5eaa395a681fd51029ef603449bf31914b934f9aaa73486ca55ec77c31ba','es.png':'e9aa6fcf5e814e25b7462ed594643e25979cf9c04f3a68197b5755b476ac38a7','et.png':'69975a423a5a5eb1cc33c554756b6d97e9f52f8253f818a9190db1784e55558f','europeanunion.png':'75bd9bf0f8d27cff7b8005c1a1808d75923ab1ee606f7220b4b35616e3e5a8ad','fam.png':'dec6c95977d90a7e468b2b823d74cd92a79ba623ac3705028eeaf3669ba98906','fi.png':'543f426fb35ad2c761641a67977c8faf0d940d4054d0dc1d7433987ebc3aa181','fj.png':'bc4f5f74e61dfe349dcbc110cfcb0342d0adb0c052652831f3995dfa63bb9b70','fk.png':'e0bd7b739e42aeaac268f77133fc70a228e115553662811c015d2e082da054d6','fm.png':'8c115aeccde699d03d5124eb30f853129cde0f03e94e9d255eda0eae9ea58c28','fo.png':'5b9e9e43b1f7969c97a72b65de12afd2429e83d1e644fc21eca48b59a489d82a','fr.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','ga.png':'78565ad916ce1cf8580860cff6184756cf9fbf08f80d04197f567a8f181f9a4b','gb.png':'5d72c5a8bef80fca6f99f476e15ec95ce2d5e5f65c6dab9ee8e56348be0d39fc','gd.png':'859d360193bdc3118b13ded0bc1fe9356deb442090daa91f700267035e9dfecc','ge.png':'a911818976d012613a3cd0afa6f8e996cdffc3a32ba82d88899e69fbc55f67be','gf.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','gh.png':'375fa90eeba5f017b1bfa833e8b9257cde8a0d9f23f668fd508952278b096f22','gi.png':'e86dcc7ad5556b7202d34b1cbac72e3bb0b97b19fc43919ac7321da94a8f3973','gl.png':'2ef3adddb67b87cd2f61652cc6c807556bce0b63433958cc8ad49b8a3b4ff0ae','gm.png':'8f4511b0ca233ebe65e9c435b0d620a58bc607700469c9b4ea446d2b5db79952','gn.png':'a6216497c02291a2ea9b2a04d111362fd44f60e754ff74c81561ee730922dc98','gp.png':'6731b1de195ee6d2f1591c37bb86bc5806a43d559e881ab71f11628852388add','gq.png':'a15608299afdeed2939b687d4bee10e9440395f61d69e402c37a81b4f34bc6ef','gr.png':'5648d2078756ae0b084312c46b02d82905cd9fb84262267cafcf9b71828ac358','gs.png':'1f9d0507de88efae157e75f35c25265f5d9d3f06579178fccbbf50987029c93f','gt.png':'0be4d466871ec85bb3892855ae498b2a78e8fca992024ec7efcc119d08b1a844','gu.png':'b7114f95668c77e6293cb3138bf908989089179c37501a70fdc49eedb73c3d45','gw.png':'720539b86c555880637aef705aff4a2c5497a4b5efd633c1835371aee5d6a7ad','gy.png':'b09eae1eaca0581c47b0064825061e3939ee8a938c4c51d004b0868372f13413','hk.png':'21a3c54b0f51243f34747eeb2feb2b2627c29133e6e3a8a1126b7bda81708dab','hm.png':'a7f9683bc4240ef940ee3d4aaf127515add30d25b0b2179a6cdec23944635603','hn.png':'feb47c8bef0dde53d8f4596fe4791d21a8d0ea060aa5b44e1d16d2583cac63e1','hr.png':'b4d87ecdeef29042f05b26ad81fbfece47292270eb0cfb10ab132f18c3ce98cd','ht.png':'4b60e9e656f44feb7b97a0adac55107fe043fbbc0407950e283451d21d2a9050','hu.png':'61a2cecf8326a8da732499312a098f89d050d13546f6204e6204de38c550437e','id.png':'1f85c9e9a1a0def09db35b63b9aae2a3c4f92202d701322621c8cfddf8880162','ie.png':'c04b1e73243fab30031bcd1b13bbe6ffe5e0e931d2125a6312e239056a972cb4','il.png':'5432e244f03e3973153451b1ec88d649459580eab66e2df936fe2f70f2fed823','in.png':'0aa7543328f3fddde96ab8fc7e3a8b85732de57de6e84447b22964971f399f28','io.png':'00653024642da7ae95c9b56770c878d482cce1bfa7478d41e9f15abc61e1c46c','iq.png':'abf11b67187d489d9321ca074a83bf613b08cf9a9de9565fd923088e51096ab7','ir.png':'2354a8a69f05bf7b0fcfc5ed2f89facd8bd1d692d34513acc066103417783c44','is.png':'82327740504dcaa478299427e9f66903b832b684283e7493d68bfe4808727798','it.png':'c7992f57d67156f994a38c6bb4ec72fa57601a284558db5e065c02dc36ee9d8c','jm.png':'92244b267742bbbfbce7f548d5bd5e75449ee446f53032ab3bef03e53ec7fda1','jo.png':'d5d3b3c24da6db1b1cb098da2f8216aab85a2ba04d2088ad97495bbbb3b99da4','jp.png':'5efce88ac7228ea159bcf7fd1cc56d73c19428394218706524bac0e9151d4c61','ke.png':'38512a3038a8e8f4032aa627157463a0fe942f948159beadbd5c10974ae86a82','kg.png':'98caea2321d6742c57073d56ec0135a7c8bb97e65b9fd062a78c11f42a502e38','kh.png':'5d8706b032eba89228abe0180923cbe1445a27dbb8126b340a9fa4a0ca41827e','ki.png':'652161e3308e25802890895e4bbed778493ec36ced3fa740d8fd83b495f620d0','km.png':'569e0181ef9ac05189ba2a88ebe1de0b2763ba54f737a8251d74b5a94609c2d6','kn.png':'1729d04153ae46884480bc9f995f0852915159e1a0e9c47fac199316ebce1353','kp.png':'6bb1d910ab5186e0cf5518492442f6231470920e22250ad48a27a520b1d376e0','kr.png':'6fdd24bd96b3a482bc058d5c9bcfd6f1c664d91bbd47658d65ac5d852535f7fd','kw.png':'345630ebda3d8a5798bc5447ba38c694921596981289b6c494cab31d5c43e350','ky.png':'c6fe83ab80ec3c1af2e81b2409673af43a0a610eecc0f2e8233d2f3886a48255','kz.png':'b639f1e1e00cf0973f7feaf673326300e13de6e830aad5eb08937bf56ee77c3b','la.png':'d56dc25b3ef4af93f12db2b58b72c293e85da54d8615dae008290a73bdb6d0bd','lb.png':'24efc04e761e01ac6c0aea8941bce30038fe3af40eef643c2cb9f96d1efa0230','lc.png':'fc9572f63afedd18082ff89cc8e9c2b51abbf09610a381939672b763da655f31','li.png':'1235def1c1d682ce8a6c0ec7e569972cd27c70f1c72fb0f2c1ba651895af8eaa','lk.png':'2ea160f5aa9c7155d9b0a15029afe24e4309294b3b61fab6f79442481c6f3c53','lr.png':'008caee046d6d14e91edebcb74343133c4592a2a636f53535c01acbb1757f5ea','ls.png':'a9117dc093a45c55b48faa85495b8e91c4b1bf8ac52ca9e791efe329bd297aa9','lt.png':'23ddd0c23304f715e7c5e47f893afbc827a3504ec6f6f828b4d0beb93eafbd62','lu.png':'6f5ef26b9bebad3c5c6572533d23761e2afa46372a9b350bd08214abda19ada4','lv.png':'0153d9f72dcd5563daedd27f7e0407aee3f39fef74e8d75951777da986e05257','ly.png':'75bfedebfb9cc57d3ed2a6fc640c7540195604bacbd8cc8301b3a053deed199a','ma.png':'61b4918e0904f58a113f7132366b1ad9d458dc5311c505f3b9b94b8458620ee2','mc.png':'d29f945dba8413eb510d42b8b4bfe4e2bdf2bd81158254c4279d056cb0d4b5e2','md.png':'0b4e15588de7b1370b9aedb0cd642b53ecb5352bce6c646e06634c79cecf787e','me.png':'3081af04bbaf03a33b15a177af37f0e46ffdc09469bdd3200795f52626a6d693','mg.png':'cde4f13166c5a8ca794977b62911e567cdf7bb6b420c934f0c5b284df81c25c2','mh.png':'2c90e947b0b12087942c92d69afb98af57e6de1e5acb2059854d91817c3b2176','mk.png':'3c47fe838cab9f56788986f6d46b0b57bcc31b7e7365f6d152bd33dd8c57c48c','ml.png':'b0a3a403ea590be753788de634af4c557d05ae4d2b99e739953208d24eb2b1ac','mm.png':'ecb1de767e97ae04cc8fc646f0a533069bb6f5e87e67c8cff13fc8c88799d6a9','mn.png':'c6e6741d6773b599129eb5ead073d8cd5c59386aab87e80f2e7d0b9ffe2ae505','mo.png':'679136a489c373c80a4b8777411af88256904fdb276e8a15885f5f52baca1dbc','mp.png':'604d309375c31da91dce706037f4b3f1047fd04e82eedacc9d804f4abbaa70e2','mq.png':'990809b24a79d60ddf9c22d555f4c99ca53a2a06773e0da2db4905aa35104056','mr.png':'a74f38227aec752324c052e9dd1851122748801ccec7aef5ecfbaa0f94390e8c','ms.png':'31947948b6ba38909344a0a095c1b20dbc3532a8694c4c98b0d065976c172280','mt.png':'a20c8a35e42004c904e1a06115a9657b170d8090ebe26e96592139e1c8a9e358','mu.png':'5af9de01b0475f0f9e7ed942d4196de6e6ee018a2f24a5162e3dcb833e5cd3d4','mv.png':'d95a38f3825323e8bc65bbe40bc0092c569bd8835ecf5ec7c15d2446bb2fb7c8','mw.png':'be1c170846c234e90ad8b4000ee3ad324d524d8b31e7701540a8cd69f0666db7','mx.png':'656fb035a56a50a6431312527b106f65c7e03bb8711778018c8dc466d1d445ee','my.png':'1e7866925f0e0d350f2c74aa8ac3542be6e90b3c2be3c7f6b1ba0b641b53de9d','mz.png':'a421c9817192c8297e62b03d45309aea3672c8f5574443bab798822f4e5815a1','na.png':'b8dfe39c1ebe4ba174840ba7170a160a48f2b334ee84ea4f39d894a6e54c19ec','nc.png':'34268f88af259368d197e0cdc5448ee6d292704f37794cf1a2e65ff8643f6161','ne.png':'d9bfbea18ec6b302dc3903f8b2e68e15354b6568a39c2f9e38b1c14f910ce225','nf.png':'28a73055985dd55360513b5d178b6b722ce9000c9ee367cbe61d8bb717928501','ng.png':'4c4996cf57a4843fde19bd8b0daf0bde0c471fbd41e0a64ecf45fbab2dfefdfd','ni.png':'8054835206a359ca1b9cae507439a088fb33834c8daabb3f336bf4004abc2aeb','nl.png':'1546928846ee0a8377fd30865d4c43cef501eba7d775d494b98d1ce699627a4a','no.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','np.png':'1e5b552bdfe4c2663f4e287c49d8a57a561c97d497f56212aab6782e942b3240','nr.png':'58d723462b9d68ae1293bb40f72d4a3006fc0f4b0eb96ec08c30c6d07cbc8d69','nu.png':'7dfe8222c16cc1070beb9fa11b6c969ffc6f7482832288950270a125bb774e50','nz.png':'095ebba705ab72032d0c17ca3936f7012a404a778a23a685c2cf943f22d9880e','om.png':'59509c4182f08201f20fb0039ba9477dfa3b3028ae602056f86a9cc982f0ff9f','pa.png':'48fc49c3010bd1530dd86066a61d5a9addadbf31e021c928da9da0cfa0d165f3','pe.png':'aa9ecf69a7d07664c50371368d4b6ab9e1f7f2dc31e0ef3693d8ff2cbab7427a','pf.png':'8346bfd255be99c8bdea0e4f8d6039ac824d4a85c4a974b0cfec245eb9c58318','pg.png':'04cd8be0fbd25ccd8017fb3d9a0a2b511adc215a168dbfe671386ce6a783c802','ph.png':'609f7123d9d23ec401c90b88f677a19125ca24e2899ebe1f3c75598623fdd251','pk.png':'19851391a22a4eee0c6a3bc4b9dec8ec2ee15d0133a8f7c8844f599c261219fb','pl.png':'34f6a1822d880608e7124d2ea0e3da4cd9b3a3b3b7d18171b61031cedbe6e72f','pm.png':'f007111a5672954f4b499ef9bae12bd9e741b7084bbe3c55bea6fd651ee61a27','pn.png':'a02a747916b3a5ed5283b6261258906408ef112351512627db0f2dda57b686cc','pr.png':'4fdcbf2a4a9ca30c22451dca2582c65c473889f75c78d2e6e1253aae82ac1d1a','ps.png':'e53ff276a447b9962ce84b38926dd1f088d6db653f8e936b5c19bfb4584aa688','pt.png':'ba636f1cb6bfd323dac1fb079cd002b5d486ed5eff54f4c4744b81316b257e96','pw.png':'ef5cee4b6289acfae6721efa130076f096d6a3481acad71178016416b17b6b29','py.png':'bd60963b2eb84d58eb01e118a2d0ba5453c717e8564a8fdb4aa10dd6b6473044','qa.png':'140a569d8ed63a59005323a6e06b704a908741c17e0b46b191b2316e2a62e1f7','re.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','ro.png':'0f83abcca7f07368819e3268d42f161edabcee4b56329c67de93779c1fba3ec5','rs.png':'a00b9d05c78c62b3eaee82acb12c2d39cc8f63381ee3563b6b8fc6c285dd4efc','ru.png':'c6e9489e25e7854a58db93acc5a91b3cc023d33a70c4931dce8d2ef2868b5e94','rw.png':'9e0e80b9ec85c4066624ea17a501b0ceeed5353dc27cf956203ab8254263e381','sa.png':'8a82f9366b0218584e72ba24eefdbf0f9dd6030480219e39f13cf1e7fe87a03a','sb.png':'6d4a0283689892275b974704a1b87e65a67af641d8b7034a661b4dbb91bd8416','scotland.png':'500ffdc39a41504133171107588f13ad7a7ebce53fc28b423fa45e3e80f27ce9','sc.png':'ca20860642968fd26776098e80b113d8b9a1d48360837ed8ded94d65b0dc9abf','sd.png':'e0cbd1960cc662ea059c0438b92449a25b6753fada4734875545ba0f79098ce2','se.png':'dc67a89a0d57005dad961a1213206395e0dfd8c7825249a0611e140bf211e323','sg.png':'84684a25002cca288c03df18dc0b2636e38a36dfdcb3d1a7a654aad1009efb17','sh.png':'6a95c6905aa2fc09fe242e417d82b12350c048f606337e1d2cc31e38579c8b88','si.png':'a2eb02e5ee0cdfb2911e2ae65cb45e070e116cd9c471422e62c9710246fe7209','sj.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','sk.png':'dfad70c1a7d2e9aca6c8e11a5a61b16e5f6ce8bf5a28d4b47c479189ace5ffba','sl.png':'0532248fc289611fe2255aa94cbed9de496f9fcd144eee6fcedd2a1eb25ee554','sm.png':'9510efe392a1a661b235c71faaed1f58730b42472caa0f73a7853b1e10d584d5','sn.png':'cbef42bf392f983769bebb6f52b15b2468b633ecdac03204b492fefb694c6d95','so.png':'c1ee2a03d7d92ed81609c610f6bb8b1c211e4da3018162dff14cee0d96c65451','sr.png':'f24fdccbff3e936cbebd5a2beebc30a44cdca6ad85e77ce733009ca88b64fc34','st.png':'356b2af9a06d0db9b05f04c528cf7ccfca73090b29148090ca227f53611d8fba','sv.png':'9722f682cdac58479490bd4ad3e2988aaf69fff9f73c4795f586fd6537cc97af','sy.png':'24c2811e92c20a88522cd9872020bdce2f882d6718962eac26f5fb4c97e14ded','sz.png':'3af4d71e471cbd7d856300a36ee6cde5fc4d29e647f90cb934b0e6f82ffdc1fb','tc.png':'fcac6aff645d8048d395b4a1e0f418be4d823c51525ecbec1d6622e72de9620a','td.png':'2a2e1bd51f95d45678decd51701d3542673f9263fac5bd8d09fe6c70daf69511','tf.png':'8c8d63683cc5ba2b8533f6a7db65cac7b137e5957d37df734e96634ccd0cf2e3','tg.png':'95a500c7fb39f20d5c2687e174626c8cad7969389437feb825257e6cce3cd833','th.png':'9301b5300fa18b50f774512c3549ded45bf41c30359d1824ced7cca0cc75e216','tj.png':'776630c76b77c04a84aa0edb87decb646643c53d519949df2113a5cac4592095','tk.png':'64d2bb4ebc19d7ce6b32a640ef6831c0f3587c54686e3780e5736108b24bcc12','tl.png':'ca5fb285fc6b36cd5d03290983b96d029b0d584a6c03725728a2435969df2636','tm.png':'5012ff744573ece2ed5e8f6aeb6de891bae03a21700141511173d0a9d35a4237','tn.png':'fbf8002c6785f2bc3a7b1074b1b08d6fa96033b3a58f6e362e90e76162064c83','to.png':'f045097a337487211f80bfeaa3391aac99a5b54950380bd32c3d1c96b512f0c8','tr.png':'292d592f7fa1df2fa653ecc1e03d5eb2ae68277c6df264f762aefb8218e23454','tt.png':'393ae78c5cdf66036d404f65822a90abc168672d0a1c5093e4259ce1606e7298','tv.png':'81770d0d4d6ee76a8286becd00d111ea1ffd3220267651f95f559898f76b8d58','tw.png':'e59c331045b010a83f46ad25c592cf3f5415271b612fc9db8d32cf9158447dc6','tz.png':'4bf0a8872442348835eb7cb88cad7ef7992ab7017c2777281493214413bc3d5f','ua.png':'9ae2f204178855c4fdb29ce75a0a1b2588fc3db3a7084d29715876bacd293508','ug.png':'42cd5a9bc8408d673b97fa04e528a194772f85c2f3aa756e1386045cdaa10538','uk.png':'5d72c5a8bef80fca6f99f476e15ec95ce2d5e5f65c6dab9ee8e56348be0d39fc','um.png':'7c655058691a6c837db9aac3c2f8662d8e06a6ebd3dd495cca6e691a67c1bf64','us.png':'36cce5cae3d2e0045b2b2b6cbffdad7a0aba3e99919cc219bbf0578efdc45585','uy.png':'9ab4ccd42c3869331626b86e9074502e47ad19db3253b3596f719bd850ff736e','uz.png':'a2870e6e9927c9ff0b80e6a58b95adb3463714f00733e9c3ddd3be1a2d5d17b5','va.png':'4ceb52d9a612b80c931d9530c273b1b608f32b9507e6b7009a48599eeb7f93e2','vc.png':'0bf42ce1f486108fa32afaba7976f0dea5dbbca2049b559f23d57a052124b6e2','ve.png':'6d04de1086b124d5843753e2bd55f137c2537bd47e0d5ea2c55ff3bc1da7293c','vg.png':'f3720add09557825a652d8998ac7bedf84239e5b9aecbdcffb3930383b7e4682','vi.png':'943fb60916b4286295f32e632fe5a046275e5cf84e87119a94f7f5e1b429e052','vn.png':'d05aa8078604f4560d99aacf12c80e400651e4ef9b0860b3ad478c2d8b08e36d','vu.png':'39779ad6848267e90357d3795bbb396deee7f20722f8e3d6c6be098a6f5f347e','wales.png':'a20ef40f442f089d0a5f5dcd089a76babd86f0fe3c243d9c8e50c6c0e4aef3ab','wf.png':'893ed4ccb23353f597bb7e9544ef8c376c896fc4f6fe56e4ca14aab70e49203e','ws.png':'7eb7d48fd72f83b5bcee0cc9bac9c24ad42c81927e8d336b6fd05fd9aefa0dcb','ye.png':'c2785bb08c181f8708b9a640ff8fe15d5ab5779af8095d11307542b6f03343a3','yt.png':'da7d65c048969b86d3815ed42134336609c9e8d5aead0a18194c025caf64c019','za.png':'48188165205cc507cd36c3465b00b2cd97c1cc315209b8f086f20af607055e49','zm.png':'794a2df87b0952ffd0fbcf18c9f61f713cff6cfafcc4b551745204d930fc1967','zw.png':'b546d55dd33c7049ef9bbfe4b665c785489b3470a04e6a2db4fda1fea403dc62'}
		self.COUNTRYNAMES = {
			'BG':'Bulgaria','CA':'Canada','CH':'Swiss','DE':'Germany','FR':'France','HU':'Hungary','IS':'Iceland','LT':'Lithuania','MD':'Moldova','NL':'Netherlands','RO':'Romania','SE':'Sweden','UA':'Ukraine','UK':'United Kingdom','US':'U.S.A.',
		}
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
		self.LOAD_DATA_EVERY = 60
		self.LOAD_SRVDATA = False
		self.WIN_RESET_EXT_DEVICE = False
		self.WIN_FIREWALL_STARTED = False
		self.WIN_FIREWALL_ADDED_RULE_TO_VCP = False
		self.WIN_BACKUP_FIREWALL = False
		self.WIN_RESET_FIREWALL = False
		self.WIN_DONT_ASK_FW_EXIT = False
		self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = True
		self.WIN_DNS_CHANGED = False
		self.LAST_FAILED_CHECKFILE = False
		self.CA_FIXED_HASH = "f37dff160dda454d432e5f0e0f30f8b20986b59daadabf2d261839de5dfd1e7d8a52ecae54bdd21c9fee9238628f9fff70c7e1a340481d14f3a1bdeea4a162e8"
		self.DISABLE_SRV_WINDOW = False
		self.DISABLE_ACC_WINDOW = False
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

	def thread_idle(self, target):
		#self.debug(text="def thread_idle call %s" %(target))
		GLib.idle_add(target)

	def preboot(self):
		self.debug(text="def preboot()")
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
			self.errorquit(text="Operating System not supported: %s" % (self.OS))
		elif OS == "darwin":
			self.errorquit(text="Operating System not supported: %s" % (self.OS))
		else: 
			self.errorquit(text="Operating System not supported: %s" % (self.OS))

	def win_pre1_check_app_dir(self):
		self.debug(text="def win_pre1_check_app_dir()")
		os_appdata = os.getenv('APPDATA')
		alt_appdata = "appdata"
		if os.path.exists("appdata"):
			print "alternative folder found"
			self.app_dir = "%s\\ovpn" % (alt_appdata)
			self.bin_dir = "."
		else:
			self.app_dir = "%s\\ovpn" % (os_appdata)
			self.bin_dir = "%s\\bin\\client\\dist" % (self.app_dir)
		if not os.path.exists(self.app_dir):
			if self.DEBUG: print("win_pre1_check_app_dir %s not found, creating." % (self.app_dir))
			os.mkdir(self.app_dir)
		if os.path.exists(self.app_dir):
			self.debug(text="win_pre1_check_app_dir self.app_dir=%s :True" % (self.app_dir))
			return True
		else:
			self.errorquit(text = "def check_winapp_dir could not create app_dir: %s" % (self.app_dir))

	def win_pre2_check_profiles_win(self):
		self.debug(text="def win_pre2_check_profiles_win()")
		self.profiles_unclean = os.listdir(self.app_dir)
		self.profiles = list()
		for profile in self.profiles_unclean:
			if profile.isdigit():
				self.profiles.append(profile)
		self.profiles_count = len(self.profiles)
		self.debug(text="def win_pre2_check_profiles_win: profiles_count %s" % (self.profiles_count))
		if self.profiles_count == 0:
			self.debug(text="No profiles found")
			if self.USERID == False:
				self.debug(text="spawn popup userid = %s" % (self.USERID))
				if self.form_ask_userid():
					return True
		elif self.profiles_count == 1 and self.profiles[0] > 1:
			self.USERID = self.profiles[0]
			return True
		elif self.profiles_count > 1:
			if not self.select_userid() == True:
				self.errorquit(text="Select User-ID failed!")
			return True

	def win_pre3_load_profile_dir_vars(self):
		self.debug(text="def win_pre3_load_profile_dir_vars()")
		self.api_dir = "%s\\%s" % (self.app_dir,self.USERID)
		self.debug_log = "%s\\client_debug.log" % (self.api_dir)
		if os.path.isfile(self.debug_log):
			try:
				os.remove(self.debug_log)
			except:
				pass

		self.lock_file = "%s\\lock.file" % (self.app_dir)
		self.opt_file = "%s\\options.cfg" % (self.api_dir)
		self.api_cfg = "%s\\ovpnapi.conf" % (self.api_dir)
		self.vpn_dir = "%s\\openvpn" % (self.api_dir)
		self.prx_dir = "%s\\proxy" % (self.api_dir)
		self.stu_dir = "%s\\stunnel" % (self.api_dir)
		self.pfw_dir = "%s\\pfw" % (self.api_dir)
		self.pfw_bak = "%s\\pfw.%s.bak.wfw" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_private_log = "%s\\pfw.private.%s.log" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_public_log = "%s\\pfw.public.%s.log" % (self.pfw_dir,self.BOOTTIME)
		self.pfw_domain_log = "%s\\pfw.domain.%s.log" % (self.pfw_dir,self.BOOTTIME)

		self.vpn_cfg = "%s\\config" % (self.vpn_dir)
		self.vpn_cfgold = self.vpn_cfg
		self.vpn_cfgip4 = "%s\\ip4" % (self.vpn_cfg)
		self.vpn_cfgip46 = "%s\\ip46" % (self.vpn_cfg)
		self.vpn_cfgip64 = "%s\\ip64" % (self.vpn_cfg)

		self.zip_cfg = "%s\\confs.zip" % (self.vpn_dir)
		self.zip_crt = "%s\\certs.zip" % (self.vpn_dir)
		self.api_upd = "%s\\lastupdate.txt" % (self.vpn_dir)
		if os.path.isfile(self.api_upd):
			os.remove(self.api_upd)

		self.dns_dir =  "%s\\dns" % (self.bin_dir)
		self.dns_d0wntxt =  "%s\\dns.txt" % (self.dns_dir)
		self.dns_ung =  "%s\\ungefiltert" % (self.dns_dir)
		self.dns_ung_alphaindex =  "%s\\alphaindex.txt" % (self.dns_ung)

		self.ico_dir = "%s\\ico" % (self.bin_dir)
		if not os.path.isdir(self.ico_dir):
			return False
		self.systray_icon_connected = "%s\\292.ico" % (self.ico_dir)
		self.systray_icon_disconnected = "%s\\263.ico" % (self.ico_dir)
		self.systray_icon_connect = "%s\\396.ico" % (self.ico_dir)
		self.systray_icon_hourglass = "%s\\205.ico" % (self.ico_dir)
		self.systray_icon_syncupdate = "%s\\266.ico" % (self.ico_dir)
		self.systray_icon_greenshield = "%s\\074.ico" % (self.ico_dir)

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
			self.errorquit(text="Error: WINDIR '%s' not found!" % (self.WINDIR))

		if not os.path.isfile(self.WIN_NETSH_EXE):
			self.errorquit(text="Error: self.WIN_NETSH_EXE '%s' not found!" % (self.WIN_NETSH_EXE))

		if not os.path.isfile(self.WIN_ROUTE_EXE):
			self.errorquit(text="Error: self.WIN_ROUTE_EXE '%s' not found!" % (self.WIN_ROUTE_EXE))

		if not os.path.isfile(self.WIN_IPCONFIG_EXE):
			self.errorquit(text="Error: self.WIN_IPCONFIG_EXE '%s' not found!" % (self.WIN_IPCONFIG_EXE))

		if not os.path.isfile(self.WIN_TASKKILL_EXE):
			self.errorquit(text="Error: self.WIN_TASKKILL_EXE '%s' not found!" % (self.WIN_TASKKILL_EXE))

		self.debug(text="win_pre3_load_profile_dir_vars loaded")
		return True

	def check_config_folders(self):
		self.debug(text="def check_config_folders()")
		try:
			#self.debug(text="def check_config_folders userid = %s" % (self.USERID))
			self.debug(text="def check_config_folders: userid found")
			if not os.path.exists(self.api_dir):
				if self.DEBUG: print("api_dir %s not found, creating." % (self.api_dir))
				os.mkdir(self.api_dir)

			if os.path.isfile(self.lock_file):
				try:
					os.remove(self.lock_file)
				except:
					self.errorquit(text="Could not remove lock file.\nFile itself locked because another oVPN Client instance running?")

			if not os.path.isfile(self.lock_file):
				self.LOCK = open(self.lock_file,'wb')
				self.LOCK.write("%s" % (int(time.time())))

			if not os.path.exists(self.vpn_dir):
				if self.DEBUG: print("vpn_dir %s not found, creating." % (self.vpn_dir))
				os.mkdir(self.vpn_dir)

			if not os.path.exists(self.vpn_cfg):
				if self.DEBUG: print("vpn_cfg %s not found, creating." % (self.vpn_cfg))
				os.mkdir(self.vpn_cfg)

			if not os.path.exists(self.vpn_cfgip4):
				if self.DEBUG: print("vpn_cfgip4 %s not found, creating." % (self.vpn_cfgip4))
				os.mkdir(self.vpn_cfgip4)

			if not os.path.exists(self.vpn_cfgip46):
				if self.DEBUG: print("vpn_cfgip46 %s not found, creating." % (self.vpn_cfgip46))
				os.mkdir(self.vpn_cfgip46)

			if not os.path.exists(self.vpn_cfgip64):
				if self.DEBUG: print("vpn_cfgip64 %s not found, creating." % (self.vpn_cfgip64))
				os.mkdir(self.vpn_cfgip64)

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

			if not os.path.exists(self.dns_ung):
				os.mkdir(self.dns_ung)

			if not self.build_openvpn_dlurl():
				return False

			if os.path.exists(self.api_dir) and os.path.exists(self.vpn_dir) and os.path.exists(self.vpn_cfg) \
			and os.path.exists(self.prx_dir) and os.path.exists(self.stu_dir) and os.path.exists(self.pfw_dir):

				if os.path.isfile(self.api_cfg):
					self.debug(text="def check_config_folders :True")
					return True
				else:
					self.debug(text="def check_config_folders :False self.api_cfg not found")
					if not self.PASSPHRASE == False:
						if self.write_new_apikey_config():
							if self.check_passphrase():
								return True
					else:
						if self.form_ask_userid():
							if self.write_new_apikey_config():
								if self.check_passphrase():
									return True

			else:
				self.errorquit(text="Creating API-DIRS\n%s \n%s \n%s \n%s \n%s failed!" % (self.api_dir,self.vpn_dir,self.prx_dir,self.stu_dir,self.pfw_dir))
		except:
			self.errorquit(text="def check_config_folders: failed")

	def read_options_file(self):
		self.debug(text="def read_options_file()")
		if os.path.isfile(self.opt_file):
			try:
				parser = SafeConfigParser()
				parser.read(self.opt_file)

				try:
					self.DEBUG = parser.getboolean('oVPN','debugmode')
				except:
					pass

				try:
					self.LAST_CFG_UPDATE = parser.get('oVPN','lastcfgupdate')
					if not self.LAST_CFG_UPDATE >= 0:
						self.LAST_CFG_UPDATE = 0
				except:
					pass

				try:
					if self.PASSPHRASE == False:
						self.PASSPHRASE = parser.get('oVPN','passphrase')
						if self.PASSPHRASE == "False":
							self.PASSPHRASE = False
						else:
							self.PPP_NO_SAVE = False
					else:
						self.debug(text="def read_options_file: self.PASSPHRASE = '-NOT_FALSE-'")
				except:
					pass

				try:
					self.OVPN_FAV_SERVER = parser.get('oVPN','favserver')
					if self.OVPN_FAV_SERVER == "False": 
						self.OVPN_FAV_SERVER = False
					self.debug(text="self.OVPN_FAV_SERVER = '%s'" % (self.OVPN_FAV_SERVER))
				except:
					pass

				try:
					self.OVPN_AUTO_CONNECT_ON_START = parser.getboolean('oVPN','autoconnect')
					if not self.OVPN_FAV_SERVER == False and self.OVPN_AUTO_CONNECT_ON_START == False:
						self.OVPN_AUTO_CONNECT_ON_START = True
					self.debug(text="self.OVPN_AUTO_CONNECT_ON_START = '%s'" % (self.OVPN_AUTO_CONNECT_ON_START))
				except:
					pass

				try:
					self.WIN_EXT_DEVICE = parser.get('oVPN','winextdevice')
					if self.WIN_EXT_DEVICE == "False": 
						self.WIN_EXT_DEVICE = False
					self.debug(text="self.WIN_TAP_DEVICE = '%s'" % (self.WIN_EXT_DEVICE))
				except:
					pass

				try:
					self.WIN_TAP_DEVICE = parser.get('oVPN','wintapdevice')
					if self.WIN_TAP_DEVICE == "False": 
						self.WIN_TAP_DEVICE = False
					self.debug(text="self.WIN_TAP_DEVICE = '%s'" % (self.WIN_TAP_DEVICE))
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
					self.debug(text="self.UPDATEOVPNONSTART = '%s'" % (self.UPDATEOVPNONSTART))
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
						self.vpn_cfg = self.vpn_cfgip4
					elif self.OVPN_CONFIGVERSION == "23x46":
						self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4B
						self.vpn_cfg = self.vpn_cfgip46
					elif self.OVPN_CONFIGVERSION == "23x64":
						self.GATEWAY_OVPN_IP4 = self.GATEWAY_OVPN_IP4B
						self.vpn_cfg = self.vpn_cfgip64

					self.move_configs()

					self.debug(text="self.OVPN_CONFIGVERSION = '%s'" % (self.OVPN_CONFIGVERSION))
				except:
					pass

				try:
					self.WIN_RESET_FIREWALL = parser.getboolean('oVPN','winresetfirewall')
					self.debug(text="self.WIN_RESET_FIREWALL = '%s'" % (self.WIN_RESET_FIREWALL))
				except:
					pass

				try:
					self.WIN_BACKUP_FIREWALL = parser.getboolean('oVPN','winbackupfirewall')
					self.debug(text="self.WIN_BACKUP_FIREWALL = '%s'" % (self.WIN_RESET_FIREWALL))
				except:
					pass

				try:
					self.NO_WIN_FIREWALL = parser.getboolean('oVPN','nowinfirewall')
					self.debug(text="self.NO_WIN_FIREWALL = '%s'" % (self.NO_WIN_FIREWALL))
				except:
					pass

				try:
					self.WIN_DONT_ASK_FW_EXIT = parser.getboolean('oVPN','winnoaskfwonexit')
					self.debug(text="self.WIN_DONT_ASK_FW_EXIT = '%s'" % (self.WIN_DONT_ASK_FW_EXIT))
				except:
					pass

				try:
					self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = parser.getboolean('oVPN','winfwblockonexit')
					self.debug(text="self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = '%s'" % (self.WIN_ALWAYS_BLOCK_FW_ON_EXIT))
				except:
					pass

				try:
					self.TAP_BLOCKOUTBOUND = parser.getboolean('oVPN','wintapblockoutbound')
					self.debug(text="self.TAP_BLOCKOUTBOUND = '%s'" % (self.TAP_BLOCKOUTBOUND))
				except:
					pass

				try:
					self.NO_DNS_CHANGE = parser.getboolean('oVPN','nodnschange')
					self.debug(text="self.NO_DNS_CHANGE = '%s'" % (self.NO_DNS_CHANGE))
				except:
					pass

				try:
					if self.PASSPHRASE == False:
						self.LOAD_ACCDATA = False
					else:
						self.LOAD_ACCDATA = parser.getboolean('oVPN','loadaccinfo')
						if self.LOAD_ACCDATA == True:
							if self.read_apikey_config() == True and self.compare_confighash() == True:
								pass
							else:
								self.PASSPHRASE = False
								self.LOAD_ACCDATA = False
					self.debug(text="self.LOAD_ACCDATA = '%s'" % (self.LOAD_ACCDATA))
				except:
					pass

				try:
					if self.PASSPHRASE == False:
						self.LOAD_SRVDATA = False
					else:
						self.LOAD_SRVDATA = parser.getboolean('oVPN','serverviewextend')
						if self.LOAD_SRVDATA == True:
							if self.read_apikey_config() == True and self.compare_confighash() == True:
								pass
							else:
								self.PASSPHRASE = False
								self.LOAD_SRVDATA = False

					self.debug(text="self.LOAD_SRVDATA = '%s'" % (self.LOAD_SRVDATA))
				except:
					pass

				try:
					self.MYDNS = json.loads(parser.get('oVPN','mydns'))
				except:
					self.MYDNS = {}

				return True

			except:
				self.msgwarn(text="def read_options_file: failed!")
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
				parser.set('oVPN','winresetfirewall','False')
				parser.set('oVPN','winbackupfirewall','False')
				parser.set('oVPN','nowinfirewall','False')
				parser.set('oVPN','nodnschange','False')
				parser.set('oVPN','winnoaskfwonexit','True')
				parser.set('oVPN','winfwblockonexit','True')
				parser.set('oVPN','wintapblockoutbound','False')
				parser.set('oVPN','loadaccinfo','False')
				parser.set('oVPN','mydns','False')
				parser.write(cfg)
				cfg.close()
				return True
			except:
				self.debug(text="def read_options_file: create failed")

	def write_options_file(self):
		self.debug(text="def write_options_file()")
		try:

			if self.PPP_NO_SAVE == True:
				plaintext_passphrase = False
			else:
				plaintext_passphrase = self.PASSPHRASE

			cfg = open(self.opt_file,'w')
			parser = SafeConfigParser()
			parser.add_section('oVPN')
			parser.set('oVPN','debugmode','%s'%(self.DEBUG))
			parser.set('oVPN','passphrase','%s'%(plaintext_passphrase))
			parser.set('oVPN','lastcfgupdate','%s'%(self.LAST_CFG_UPDATE))
			parser.set('oVPN','autoconnect','%s'%(self.OVPN_AUTO_CONNECT_ON_START))
			parser.set('oVPN','favserver','%s'%(self.OVPN_FAV_SERVER))
			parser.set('oVPN','winextdevice','%s'%(self.WIN_EXT_DEVICE))
			parser.set('oVPN','wintapdevice','%s'%(self.WIN_TAP_DEVICE))
			parser.set('oVPN','openvpnexe','%s'%(self.OPENVPN_EXE))
			parser.set('oVPN','updateovpnonstart','%s'%(self.UPDATEOVPNONSTART))
			parser.set('oVPN','configversion','%s'%(self.OVPN_CONFIGVERSION))
			parser.set('oVPN','serverviewextend','%s'%(self.LOAD_SRVDATA))
			parser.set('oVPN','winresetfirewall','%s'%(self.WIN_RESET_FIREWALL))
			parser.set('oVPN','winbackupfirewall','%s'%(self.WIN_BACKUP_FIREWALL))
			parser.set('oVPN','nowinfirewall','%s'%(self.NO_WIN_FIREWALL))
			parser.set('oVPN','nodnschange','%s'%(self.NO_DNS_CHANGE))
			parser.set('oVPN','winnoaskfwonexit','%s'%(self.WIN_DONT_ASK_FW_EXIT))
			parser.set('oVPN','winfwblockonexit','%s'%(self.WIN_ALWAYS_BLOCK_FW_ON_EXIT))
			parser.set('oVPN','wintapblockoutbound','%s'%(self.TAP_BLOCKOUTBOUND))
			parser.set('oVPN','loadaccinfo','%s'%(self.LOAD_ACCDATA))
			parser.set('oVPN','mydns','%s'%(json.dumps(self.MYDNS, ensure_ascii=True)))
			parser.write(cfg)
			cfg.close()
			return True
		except:
			self.debug(text="def write_options_file: failed")

	def read_interfaces(self):
		self.debug(text="def read_interfaces()")
		if self.OS == "win32":
			if self.WIN_RESET_EXT_DEVICE == False:
				if self.win_read_interfaces():
					if self.win_firewall_export_on_start():
						if self.win_netsh_read_dns_to_backup():
							if self.read_gateway_from_routes():
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
		self.debug(text="def win_read_interfaces()")
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
			self.errorquit(text="Error reading your Interfaces from netsh.exe. Contact support@ovpn.to with Error-ID:\nADAPTERS[1]=(%s)\n" % (ADAPTERS[1]))

		text = "def win_read_interfaces: LANG = %s" % (LANG)
		self.debug(text=text)
		for line in ADAPTERS:
			self.debug(text="%s"%(line))
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
							self.debug(text="%s"%(nface))
						else:
							nface = iface
					interface = nface
				else:
					interface = interface[0]
				self.INTERFACES.append(interface)
			except:
				pass
		self.INTERFACES.pop(0)
		self.debug(text="INTERFACES: %s"%(self.INTERFACES))
		if len(self.INTERFACES)	< 2:
			self.errorquit(text="Could not read your Network Interfaces! Please install OpenVPN or check if your TAP-Adapter is really enabled and driver installed.")
		#self.win_detect_openvpn()
		string = '"%s" --show-adapters' % (self.OPENVPN_EXE)
		TAPADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		TAPADAPTERS = TAPADAPTERS.split('\r\n')
		self.debug(text="TAP ADAPTERS bp = %s"%(TAPADAPTERS))
		TAPADAPTERS.pop(0)
		self.debug(text="TAP ADAPTERS ap = %s"%(TAPADAPTERS))
		self.WIN_TAP_DEVS = list()
		for line in TAPADAPTERS:
			#self.debug(text="checking line = %s"%(line))
			for INTERFACE in self.INTERFACES:
				#if len(line) >= 1: self.debug(text="is IF: '%s' listed as TAP in line '%s'?"%(INTERFACE,line))
				if line.startswith("'%s' {"%(INTERFACE)) and len(line) >= 1:
					self.debug(text="Found TAP ADAPTER: '%s'" % (INTERFACE))
					self.INTERFACES.remove(INTERFACE)
					self.WIN_TAP_DEVS.append(INTERFACE)
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

		self.debug(text="self.WIN_TAP_DEVS = '%s' len=%s" % (self.WIN_TAP_DEVS,len(self.WIN_TAP_DEVS)))

		if self.WIN_TAP_DEVICE in self.WIN_TAP_DEVS:
			self.debug(text="Found self.WIN_TAP_DEVICE '%s' in self.WIN_TAP_DEVS '%s'" % (self.WIN_TAP_DEVICE,self.WIN_TAP_DEVS))

		if len(self.WIN_TAP_DEVS) == 0:
			self.errorquit(text="No OpenVPN TAP-Windows Adapter found!")

		elif len(self.WIN_TAP_DEVS) == 1 or self.WIN_TAP_DEVS[0] == self.WIN_TAP_DEVICE:
			self.WIN_TAP_DEVICE = self.WIN_TAP_DEVS[0]
			self.debug(text="Selected self.WIN_TAP_DEVICE = %s" % (self.WIN_TAP_DEVICE))
		else:
			self.debug(text="self.WIN_TAP_DEVS (query) = '%s'" % (self.WIN_TAP_DEVS))
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_file(self.systray_icon_connected)
			except:
				self.debug(text="def win_read_interfaces: #1 dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
				pass
			text = "Multiple TAPs found!\n\nPlease select your TAP Adapter!"
			dialogWindow.set_title(text)
			dialogWindow.set_markup(text)
			dialogBox = dialogWindow.get_content_area()
			liststore = Gtk.ListStore(str)
			combobox = Gtk.ComboBox()
			cell = Gtk.CellRendererText()
			combobox.pack_start(cell, True)
			combobox.add_attribute(cell, 'text', 0)
			combobox.set_wrap_width(5)
			for INTERFACE in self.WIN_TAP_DEVS:
				self.debug(text="add tap interface '%s' to combobox" % (INTERFACE))
				liststore.append([INTERFACE])
			combobox.set_model(liststore)
			combobox.connect('changed',self.cb_tap_interface_selector_changed)
			dialogBox.pack_start(combobox,False,False,0)
			dialogWindow.show_all()
			dialogWindow.run()
			dialogWindow.destroy()

		if self.WIN_TAP_DEVICE == False:
			self.errorquit(text="No OpenVPN TAP-Adapter found!\nPlease install openVPN!\nURL1: %s\nURL2: %s" % (self.OPENVPN_DL_URL,self.OPENVPN_DL_URL_ALT))
		else:
			badchars = ["%","&","$"]
			for char in badchars:
				if char in self.WIN_TAP_DEVICE:
					self.errorquit(text="Invalid characters in self.WIN_TAP_DEVICE = '%s'" % char)
			self.debug(text="Selected TAP: '%s'" % (self.WIN_TAP_DEVICE))
			self.win_enable_tap_interface()
			self.debug(text="remaining INTERFACES = %s (cfg: %s)"%(self.INTERFACES,self.WIN_EXT_DEVICE))
			if len(self.INTERFACES) > 1:
				if not self.WIN_EXT_DEVICE == False and self.WIN_EXT_DEVICE in self.INTERFACES:
					self.debug(text="loaded self.WIN_EXT_DEVICE %s from options file"%(self.WIN_EXT_DEVICE))
					return True
				else:
					dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
					dialogWindow.set_transient_for(self.window)
					try:
						dialogWindow.set_icon_from_file(self.systray_icon_connected)
					except:
						self.debug(text="def win_read_interfaces: #2 dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
					text = "Choose your External Network Adapter!"
					dialogWindow.set_title(text)
					dialogWindow.set_markup(text)
					dialogBox = dialogWindow.get_content_area()
					liststore = Gtk.ListStore(str)
					combobox = Gtk.ComboBox()
					cell = Gtk.CellRendererText()
					combobox.pack_start(cell, True)
					combobox.add_attribute(cell, 'text', 0)
					combobox.set_wrap_width(5)
					for INTERFACE in self.INTERFACES:
						self.debug(text="add interface %s to combobox" % (INTERFACE))
						liststore.append([INTERFACE])
					combobox.set_model(liststore)
					combobox.connect('changed',self.cb_interface_selector_changed)
					dialogBox.pack_start(combobox,False,False,0)
					dialogWindow.show_all()
					self.debug(text="open interface selector")
					dialogWindow.run()
					self.debug(text="close interface selector")
					dialogWindow.destroy()
					if not self.WIN_EXT_DEVICE == False:
						return True
			elif len(self.INTERFACES) < 1:
				self.errorquit(text="No Network Adapter found!")
			else:
				self.WIN_EXT_DEVICE = self.INTERFACES[0]
				self.debug(text="External Interface = %s"%(self.WIN_EXT_DEVICE))
				return True

	def select_userid(self):
		self.debug(text="def select_userid()")
		dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK)
		dialogWindow.set_transient_for(self.window)
		try:
			dialogWindow.set_icon_from_file(self.systray_icon_connected)
		except:
			self.debug(text="def select_userid: dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
		text = "Please select your User-ID!"
		dialogWindow.set_title(text)
		dialogWindow.set_markup(text)
		dialogBox = dialogWindow.get_content_area()
		liststore = Gtk.ListStore(str)
		combobox = Gtk.ComboBox()
		cell = Gtk.CellRendererText()
		combobox.pack_start(cell, True)
		combobox.add_attribute(cell, 'text', 0)
		combobox.set_wrap_width(5)
		for userid in self.profiles:
			self.debug(text="add userid '%s' to combobox" % (userid))
			liststore.append([userid])
		combobox.set_model(liststore)
		combobox.connect('changed',self.cb_select_userid)
		dialogBox.pack_start(combobox,False,False,0)
		dialogWindow.show_all()
		self.debug(text="open userid selector")
		dialogWindow.run()
		self.debug(text="close userid interface selector")
		dialogWindow.destroy()
		if self.USERID > 1 and os.path.isdir("%s\\%s" % (self.app_dir,self.USERID)):
			return True

	def load_decryption(self):
		self.debug(text="def load_decryption()")
		if self.PASSPHRASE == False:
			return False
		elif len(self.PASSPHRASE) > 0:
				self.aeskey = hashlib.sha256(self.PASSPHRASE.rstrip()).digest()
				return True

	def read_apikey_config(self):
		#self.debug(text="def read_apikey_config: self.PASSPHRASE = %s" %(self.PASSPHRASE))
		self.debug(text="def read_apikey_config: self.PASSPHRASE = '-NOT_FALSE-'")
		if not self.PASSPHRASE == False and self.load_decryption() and os.path.isfile(self.api_cfg):
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
			#self.PASSPHRASE = False
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
			#text = _("Invalid Passphrase!")
			#self.set_statusbar_text(text)
			self.debug(text="def read_apikey_config passphrase :False")
			self.form_ask_passphrase()
			return False

	def write_new_apikey_config(self):
		self.debug(text="def write_new_apikey_config()")
		self.aeskeyhash = hashlib.sha256(self.PASSPHRASE).digest()
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
			#if self.DEBUG: print("padfill=%s\npaddata=%s" % (self.padfill,self.paddata))
			self.padfill += 1
		self.text2aes = "%s%s" % (self.text2aes,self.paddata)
		self.text2aeslen = len(self.text2aes)
		#if self.DEBUG: print("text2aeslen=%s\n" % (self.text2aeslen))
		#if self.DEBUG: print("\n	#######	#######debug:text2aes=%s\ndebug:aesiv=%s\ndebug:len(self.text2aeslen)=%s\nself.addpad=%s" % (self.text2aes,self.aesiv,self.text2aeslen,self.addpad))
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

	def on_right_click_mainwindow(self, treeview, event):
		self.debug(text="def on_right_click_mainwindow()")
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
		#print 'def on_right_click_mainwindow: servername = %s' % (servername)
		if servername:
			if event.button == 1:
				self.destroy_systray_menu()
				self.debug(text="mainwindow left click (%s)" % (servername))
			elif event.button == 3:
				self.destroy_systray_menu()
				self.make_context_menu_servertab(servername)
				self.debug(text="mainwindow right click (%s)" % (servername))

	def make_context_menu_servertab(self,servername):
		self.debug(text="def make_context_menu_servertab: %s" % (servername))
		context_menu_servertab = Gtk.Menu()
		self.context_menu_servertab = context_menu_servertab

		if self.OVPN_CONNECTEDto == servername:
			disconnect = Gtk.MenuItem("Disconnect %s"%(self.OVPN_CONNECTEDto))
			context_menu_servertab.append(disconnect)
			disconnect.connect('button-release-event', self.cb_kill_openvpn)
		else:
			connect = Gtk.MenuItem('Connect to %s'%(servername))
			context_menu_servertab.append(connect)
			connect.connect('button-release-event',self.cb_jump_openvpn,servername)

		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)

		if self.OVPN_FAV_SERVER == servername:
			delfavorite = Gtk.MenuItem('Remove AutoConnect: %s'%(servername))
			delfavorite.connect('button-release-event',self.cb_del_ovpn_favorite_server,servername)
			context_menu_servertab.append(delfavorite)
		else:
			setfavorite = Gtk.MenuItem('Set AutoConnect: %s'%(servername))
			setfavorite.connect('button-release-event',self.cb_set_ovpn_favorite_server,servername)
			context_menu_servertab.append(setfavorite)

		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)

		self.make_context_menu_servertab_d0wns_dnsmenu(servername)

		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)

		if self.DISABLE_SRV_WINDOW == False:
			if self.LOAD_SRVDATA == True:
				opt = "[enabled]"
			else:
				opt = "[disabled]"
			extserverview = Gtk.MenuItem('Load extended Server-View %s'%(opt))
			extserverview.connect('button-press-event', self.cb_extserverview)
			context_menu_servertab.append(extserverview)

		sep = Gtk.SeparatorMenuItem()
		context_menu_servertab.append(sep)

		refresh = Gtk.MenuItem('Refresh Window')
		refresh.connect('button-release-event',self.cb_redraw_mainwindow_vbox)
		context_menu_servertab.append(refresh)

		context_menu_servertab.show_all()
		context_menu_servertab.popup(None, None, None, 3, int(time.time()), 0)
		self.debug(text="def make_context_menu_servertab: return")
		return

	def make_context_menu_servertab_d0wns_dnsmenu(self,servername):
		try:
			self.debug(text="def make_context_menu_servertab_d0wns_dnsmenu: servername = '%s'" % (servername))
			if len(self.d0wns_DNS) == 0:
				self.load_d0wns_dns_from_remote()
				self.debug(text="len(self.d0wns_DNS) == 0")
				return False

			dnsmenu = Gtk.Menu()
			dnsm = Gtk.MenuItem("Change DNS")
			dnsm.set_submenu(dnsmenu)
			self.dnsmenu = dnsmenu

			try:
				pridns = self.MYDNS[servername]["primary"]["ip4"]
				priname = self.MYDNS[servername]["primary"]["dnsname"]
				pridnsm = Gtk.MenuItem("Primary DNS: %s (%s)" % (priname,pridns))
				cbdata = {servername:{"primary":{"ip4":pridns,"dnsname":priname}}}
				pridnsm.connect('button-release-event',self.cb_del_dns,cbdata)
				self.context_menu_servertab.append(pridnsm)
			except:
				pridns = False

			try:
				secdns = self.MYDNS[servername]["secondary"]["ip4"]
				secname = self.MYDNS[servername]["secondary"]["dnsname"]
				secdnsm = Gtk.MenuItem("Secondary DNS: %s (%s)" % (secname,secdns))
				cbdata = {servername:{"secondary":{"ip4":secdns,"dnsname":secname}}}
				secdnsm.connect('button-release-event',self.cb_del_dns,cbdata)
				self.context_menu_servertab.append(secdnsm)
			except:
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
					imgfile = self.FLAG_IMG[countrycode]
				except:
					imgfile = '%s\\flags\\%s.png' % (self.ico_dir,countrycode)

				if not os.path.isfile(imgfile):
					imgfile = '%s\\flags\\00.png' % (self.ico_dir)
					self.FLAG_IMG[countrycode] = imgfile

				if os.path.isfile(imgfile):
					img.set_from_file(imgfile)
					dnssubm.set_always_show_image(True)
					dnssubm.set_image(img)
					dnsmenu.append(dnssubm)

					cbdata = {servername:{"primary":{"ip4":dnsip4,"dnsname":name}}}
					if pridns == dnsip4:
						setpridns = Gtk.MenuItem("Primary DNS '%s' @ %s" % (pridns,servername))
						setpridns.connect('button-release-event',self.cb_del_dns,cbdata)
					else:
						setpridns = Gtk.MenuItem("Set Primary DNS")
						setpridns.connect('button-release-event',self.cb_set_dns,cbdata)
					dnssubmenu.append(setpridns)

					cbdata = {servername:{"secondary":{"ip4":dnsip4,"dnsname":name}}}
					if secdns == dnsip4:
						setsecdns = Gtk.MenuItem("Secondary DNS '%s' @ %s" % (secdns,servername))
						setsecdns.connect('button-release-event',self.cb_del_dns,cbdata)
					else:
						setsecdns = Gtk.MenuItem("Set Secondary DNS")
						setsecdns.connect('button-release-event',self.cb_set_dns,cbdata)
					dnssubmenu.append(setsecdns)
			dnsm.show_all()
			self.context_menu_servertab.append(dnsm)
			#self.cgmenu.append(dnsm)
		except:
			self.debug(text="def make_context_menu_servertab_d0wns_dnsmenu: failed!")

	def systray_timer(self):
		#self.debug(text="def systray_timer()")
		if self.stop_systray_timer == True:
			return False
		if not self.systray_menu == False:
			self.check_hide_popup()
		systraytext = False

		""" *** fixme *** try to get output
		try:
			print "self.OPENVPN_PROC_output = '%s' , self.OPENVPN_PROC_error = '%s'" % (self.OPENVPN_PROC_output,self.OPENVPN_PROC_error)
		except:
			pass
		"""

		if self.timer_check_certdl_running == True:
			systraytext = "Checking for Updates!"
			systrayicon = self.systray_icon_syncupdate

		elif self.STATE_OVPN == False:
			systraytext = "Disconnected! Have a nice and anonymous day!"
			statusbar_text = systraytext
			systrayicon = self.systray_icon_disconnected
			try:
				if self.OVPN_AUTO_CONNECT_ON_START == True and not self.OVPN_FAV_SERVER == False:
					self.OVPN_AUTO_CONNECT_ON_START = False
					self.debug(text="def systray_timer: self.OVPN_AUTO_CONNECT_ON_START")
					self.cb_jump_openvpn(0,0,self.OVPN_FAV_SERVER)
			except:
				self.debug(text="def timer_statusbar: OVPN_AUTO_CONNECT_ON_START failed")
		elif self.STATE_OVPN == True:
			connectedseconds = int(time.time()) - self.OVPN_CONNECTEDtime
			self.OVPN_CONNECTEDseconds = connectedseconds
			if self.OVPN_PING_STAT == -1:
				systraytext = "Connecting to %s" % (self.OVPN_CONNECTEDto)
				systrayicon = self.systray_icon_connect
				statusbar_text = systraytext
				self.debug(text="def systray_timer: cstate = '%s'" % (systraytext))
			elif self.OVPN_PING_STAT == -2:
				self.OVPN_isTESTING = True
				systraytext = "Testing connection to %s" % (self.OVPN_CONNECTEDto)
				systrayicon = self.systray_icon_hourglass
				statusbar_text = systraytext
				self.debug(text="def systray_timer: cstate = '%s'" % (systraytext))
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
					statusbar_text = "Connected to %s [%s]:%s (%s) [ %s ] (%s / %s ms)" % (self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper(),connectedtime_text,self.OVPN_PING_LAST,self.OVPN_PING_STAT)
					# systraytext Windows only shows the first 64 characters
					systraytext = "%s [%s]:%s (%s) [%s] %sms" % (self.OVPN_CONNECTEDto,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper(),connectedtime_text,self.OVPN_PING_LAST)
					#statusbar_text = systraytext
					systrayicon = self.systray_icon_connected
				except:
					self.debug(text="def systray_timer: systraytext failed")

		try:
			if not self.systraytext_from_before == systraytext and not systraytext == False:
				self.systraytext_from_before = systraytext
				self.tray.set_tooltip_markup(systraytext)
			if not self.systrayicon_from_before == systrayicon:
				self.systrayicon_from_before = systrayicon
				self.tray.set_from_file(systrayicon)
			#fixme: memoryleak
			if self.MAINWINDOW_OPEN == True:
				if not self.statusbartext_from_before == statusbar_text:
					self.set_statusbar_text(statusbar_text)
					self.statusbartext_from_before = statusbar_text
		except:
			pass

		try:
			if self.systray_timer_running == True:
				if self.timer_load_remote_data_running == False:
					thread = threading.Thread(target=self.load_remote_data)
					thread.start()
		except:
			pass

		self.thread_systray_timer = threading.Thread(target=self.thread_idle, args=(self.systray_timer,))
		self.systray_timer_running = True
		time.sleep(0.001)
		self.thread_systray_timer.start()
		#self.debug(text="def systray_timer: return")
		return

	def on_right_click(self, widget, event, event_time):
		self.debug(text="def on_right_click()")
		if not self.systray_menu == False:
			self.destroy_systray_menu()
		else:
			self.make_systray_menu(event)

	def on_left_click(self, widget):
		self.debug(text="def on_left_click()")
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
					self.debug(text="def show_mainwindow() on_left_click failed")
			else:
				self.destroy_mainwindow()

	def make_systray_menu(self, event):
		self.debug(text="def make_systray_menu()")
		try:
			self.systray_menu = Gtk.Menu()
			
			try:
				self.load_ovpn_server()
			except:
				self.debug(text="def make_systray_menu: self.load_ovpn_server() failed")
			
			try:
				self.make_systray_updates_menu()
			except:
				self.debug(text="def make_systray_updates_menu: self.make_systray_updates_menu() failed")
			
			try:
				self.make_systray_options_menu()
			except:
				self.debug(text="def make_systray_menu: self.make_systray_options_menu() failed")
			
			try:
				self.make_systray_firewall_menu()
			except:
				self.debug(text="def make_systray_menu: self.make_systray_firewall_menu() failed")
			
			if len(self.OVPN_SERVER) > 0:
				sep = Gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)
			
			try:
				self.make_systray_server_menu()
			except:
				self.debug(text="def make_systray_menu: self.make_systray_server_menu() failed")
			
			try:
				self.make_systray_openvpn_menu()
			except:
				self.debug(text="def make_systray_menu: self.make_systray_openvpn_menu() failed")
			
			try:
				self.make_systray_bottom_menu()
			except:
				self.debug(text="def make_systray_menu: self.make_systray_bottom_menu() failed")
			
			self.systray_menu.connect('enter-notify-event', self.systray_notify_event)
			self.systray_menu.connect('leave-notify-event', self.systray_notify_event)
			self.systray_menu.show_all()
			self.systray_menu.popup(None, None, None, event, 0, 0)
		except:
			self.destroy_systray_menu()
			self.debug(text="def make_systray_menu: failed")

	def make_systray_options_menu(self):
		self.debug(text="def make_systray_options_menu()")	
		try:
			self.systray_optionsmenu = Gtk.Menu()
			optionsm = Gtk.MenuItem('Options')
			optionsm.set_submenu(self.systray_optionsmenu)

			self.systray_menu.append(optionsm)

			self.make_systray_options_dnsleak()
			self.make_systray_options_ipv6_menu()

			if self.DEBUG == True:
				opt = "[enabled]"
			else:
				opt = "[disabled]"
			switchdebug = Gtk.MenuItem("DEBUG Mode %s" % (opt))
			switchdebug.connect('button-press-event', self.cb_switch_debug)

			self.systray_optionsmenu.append(switchdebug)
		except:
			self.debug(text="def make_systray_options_menu failed")

	def make_systray_options_dnsleak(self):
		self.debug(text="def make_systray_options_dnsleak()")
		try:
			if self.STATE_OVPN == False:
				resetextif = Gtk.MenuItem('Select Network Adapter')
				resetextif.connect('button-press-event', self.cb_resetextif)
				self.systray_optionsmenu.append(resetextif)
			
				if self.NO_DNS_CHANGE == False:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				nodnschange = Gtk.MenuItem('DNS Leak Protection %s'%(opt))
				nodnschange.connect('button-press-event', self.cb_nodnschange)
				self.systray_optionsmenu.append(nodnschange)
		except:
				self.debug(text="def make_systray_options_dnsleak: failed")

	def make_systray_options_ipv6_menu(self):
		self.debug(text="def make_systray_options_ipv6_menu()")
		try:
			ipv6menu = Gtk.Menu()
			ipv6m = Gtk.MenuItem('IPv6 Options')
			ipv6m.set_submenu(ipv6menu)
			self.systray_optionsmenu.append(ipv6m)

			if not self.OVPN_CONFIGVERSION == "23x":
				ipv6entry1 = Gtk.MenuItem('Select: IPv4 Entry Server with Exit to IPv4 (standard)')
				ipv6entry1.connect('button-press-event', self.cb_change_ipmode1)
				ipv6menu.append(ipv6entry1)

			if not self.OVPN_CONFIGVERSION  == "23x46":
				ipv6entry2 = Gtk.MenuItem('Select: IPv4 Entry Server with Exits to IPv4 + IPv6')
				ipv6entry2.connect('button-press-event', self.cb_change_ipmode2)
				ipv6menu.append(ipv6entry2)
			"""
			 *** fixme need isValueIPv6 first! ***
			if not self.OVPN_CONFIGVERSION == "23x64":
				ipv6entry3 = Gtk.MenuItem('Select: IPv6 Entry Server with Exits to IPv6 + IPv4')
				ipv6entry3.connect('button-press-event', self.cb_change_ipmode3)
				ipv6menu.append(ipv6entry3)
			"""
		except:
			self.debug(text="def make_systray_options_ipv6_menu: failed")

	def make_systray_firewall_menu(self):
		self.debug(text="def make_systray_firewall_menu()")
		try:
			fwmenu = Gtk.Menu()
			fwm = Gtk.MenuItem('Firewall')
			fwm.set_submenu(fwmenu)
			self.systray_menu.append(fwm)

			if self.NO_WIN_FIREWALL == False:
				if self.TAP_BLOCKOUTBOUND == True:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				fwentry = Gtk.MenuItem("TAP Adapter block outbound %s" % (opt))
				fwentry.connect('button-press-event', self.cb_tap_blockoutbound)
				fwmenu.append(fwentry)

			if self.STATE_OVPN == False:
				if self.NO_WIN_FIREWALL == False:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				fwentry = Gtk.MenuItem("Use Windows Firewall %s" % (opt))
				fwentry.connect('button-press-event', self.cb_change_winfirewall)
				fwmenu.append(fwentry)

				if self.NO_WIN_FIREWALL == False:
					if self.WIN_RESET_FIREWALL == True:
						opt = "[enabled]"
					else:
						opt = "[disabled]"
					fwentry = Gtk.MenuItem("Clear Rules on Connect %s" % (opt))
					fwentry.connect('button-press-event', self.cb_change_fwresetmode)
					fwmenu.append(fwentry)

					if self.WIN_BACKUP_FIREWALL == True:
						opt = "[enabled]"
					else:
						opt = "[disabled]"
					fwentry = Gtk.MenuItem("Backup on Start / Restore on Quit %s" % (opt))
					fwentry.connect('button-press-event', self.cb_change_fwbackupmode)
					fwmenu.append(fwentry)

					if self.WIN_DONT_ASK_FW_EXIT == True:
						opt = "[enabled]"
					else:
						opt = "[disabled]"
					fwentry = Gtk.MenuItem("Do not ask for FW on Quit %s" % (opt))
					fwentry.connect('button-press-event', self.cb_change_fwdontaskonexit)
					fwmenu.append(fwentry)

					if self.WIN_DONT_ASK_FW_EXIT == True:
						if self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
							opt = "[enabled]"
						else:
							opt = "[disabled]"
						fwentry = Gtk.MenuItem("Always Block Internet on Quit %s" % (opt))
						fwentry.connect('button-press-event', self.cb_change_fwblockonexit)
						fwmenu.append(fwentry)

					self.load_firewall_backups()
					if len(self.FIREWALL_BACKUPS) > 0:
						fwrm = Gtk.MenuItem('Restore Firewall Backups')
						fwrmenu = Gtk.Menu()
						fwrm.set_submenu(fwrmenu)
						fwmenu.append(fwrm)

						for file in self.FIREWALL_BACKUPS:
							fwrentry = Gtk.MenuItem('%s'%(file))
							fwrentry.connect('button-press-event', self.cb_restore_firewallbackup, file)
							fwrmenu.append(fwrentry)
		except:
			self.debug(text="make_systray_firewall_menu: failed")

	def make_systray_updates_menu(self):
		self.debug(text="def make_systray_updates_menu()")
		try:
			try:
				updatesmenu = Gtk.Menu()
				updatesm = Gtk.MenuItem("Updates")
				updatesm.set_submenu(updatesmenu)
				self.systray_menu.append(updatesm)

				normalupdate = Gtk.MenuItem('Normal Config Update')
				normalupdate.connect('button-press-event', self.cb_check_normal_update)
				updatesmenu.append(normalupdate)

				forceupdate = Gtk.MenuItem('Forced Config Update')
				forceupdate.connect('button-press-event', self.cb_force_update)
				updatesmenu.append(forceupdate)

				sep = Gtk.SeparatorMenuItem()
				updatesmenu.append(sep)
			except:
				self.debug(text="def make_systray_updates_menu: #1 failed")

			try:
				if self.UPDATEOVPNONSTART == True:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				autoupdate = Gtk.MenuItem('Update on Start %s' % (opt))
				autoupdate.connect('button-press-event', self.cb_switch_autoupdate)
				updatesmenu.append(autoupdate)
			except:
				self.debug(text="def make_systray_updates_menu: #2 failed")

			try:
				if self.LOAD_ACCDATA == True:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				switchaccinfo = Gtk.MenuItem("Load Account Info %s" % (opt))
				switchaccinfo.connect('button-press-event', self.cb_switch_accinfo)
				updatesmenu.append(switchaccinfo)
			except:
				self.debug(text="def make_systray_updates_menu: #3 failed")

			try:
				if self.LOAD_SRVDATA == True:
					opt = "[enabled]"
				else:
					opt = "[disabled]"
				extserverview = Gtk.MenuItem('Load extended Server-View %s'%(opt))
				extserverview.connect('button-press-event', self.cb_extserverview)
				updatesmenu.append(extserverview)
			except:
				self.debug(text="def make_systray_updates_menu: #4 failed")

			try:
				sep = Gtk.SeparatorMenuItem()
				updatesmenu.append(sep)
				
				resetlogin = Gtk.MenuItem('Reset API Login')
				resetlogin.connect('button-press-event', self.cb_form_reask_userid)
				updatesmenu.append(resetlogin)

				if not self.PASSPHRASE == False:
					clearphram = Gtk.MenuItem('Clear Passphrase from RAM')
					clearphram.connect('button-press-event', self.cb_clear_passphrase_ram)
					updatesmenu.append(clearphram)
					
					clearphcfg = Gtk.MenuItem('Clear Passphrase from CFG')
					clearphcfg.connect('button-press-event', self.cb_clear_passphrase_cfg)
					updatesmenu.append(clearphcfg)
			except:
				self.debug(text="def make_systray_updates_menu: #5 failed")
		except:
			self.debug(text="def make_systray_updates_menu: failed")

	def make_systray_server_menu(self):
		self.debug(text="def make_systray_server_menu()")
		if len(self.OVPN_SERVER) > 0:
			try:
				countrycodefrombefore = 0
				for servername in self.OVPN_SERVER:
					servershort = servername[:3]

					textstring = "%s (%s:%s)" % (servershort,self.OVPN_SERVER_INFO[servershort][2],self.OVPN_SERVER_INFO[servershort][1])
					countrycode = servershort[:2].lower()
					#print "string = %s, countrycode = %s" % (textstring,countrycode)

					if not countrycodefrombefore == countrycode:
						# create countrygroup menu
						countrycodefrombefore = countrycode
						cgmenu = Gtk.Menu()
						self.cgmenu = cgmenu
						try:
							countryname = self.COUNTRYNAMES[countrycode.upper()]
						except:
							countryname = countrycode.upper()

						try:
							cgm = Gtk.ImageMenuItem(countryname)
							img = Gtk.Image()
							try:
								try:
									imgpath = self.FLAG_IMG[countrycode]
									try:
										if os.path.isfile(imgpath):
											img.set_from_file(imgpath)
											cgm.set_always_show_image(True)
											cgm.set_image(img)
											cgm.set_submenu(cgmenu)
											self.systray_menu.append(cgm)
										else:
											self.debug(text="def make_systray_server_menu: imgpath '%s' not found" % (imgpath))
									except:
										self.debug(text="def make_systray_server_menu: if imgpath '%s' is file append to systray failed " % (imgpath))
										self.destroy_systray_menu()
								except:
									self.debug(text="def make_systray_server_menu: imgpath = self.FLAG_IMG[%s] failed" % (countrycode))
									self.destroy_systray_menu()
							except:
								self.debug(text="def make_systray_server_menu: failed self.FLAG_IMG[%s]" % (countrycode))
								self.destroy_systray_menu()
						except:
							self.destroy_systray_menu()
							self.debug(text="def make_systray_server_menu: flagimg group1 failed")

					if self.OVPN_CONNECTEDto == servername:
						textstring = servershort+" [ disconnect ]"
						serveritem = Gtk.ImageMenuItem(textstring)
						serveritem.connect('button-release-event', self.cb_kill_openvpn)
					else:
						serveritem = Gtk.ImageMenuItem(textstring)
						serveritem.connect('button-release-event', self.cb_jump_openvpn, servername)

					img = Gtk.Image()
					imgpath = self.FLAG_IMG[countrycode]
					if os.path.isfile(imgpath):
						img.set_from_file(imgpath)
						serveritem.set_always_show_image(True)
						serveritem.set_image(img)
						cgmenu.append(serveritem)
						#serveritem.show()

			except:
				self.destroy_systray_menu()
				self.debug(text="def make_systray_server_menu: failed")

	def make_systray_openvpn_menu(self):
		self.debug(text="def make_systray_openvpn_menu()")
		if self.STATE_OVPN == True:
			try:
				sep = Gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)
				servershort = self.OVPN_CONNECTEDto[:3]
				textstring = '%s @ [%s]:%s (%s)' % (servershort,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol.upper())
				disconnect = Gtk.ImageMenuItem(textstring)
				img = Gtk.Image()
				img.set_from_file(self.systray_icon_disconnected)
				disconnect.set_always_show_image(True)
				disconnect.set_image(img)
				self.systray_menu.append(disconnect)
				# SIGNALS
				disconnect.connect('button-release-event', self.cb_kill_openvpn)
			except:
				self.debug(text="def make_systray_openvpn_menu: failed")

	def make_systray_bottom_menu(self):
		self.debug(text="def make_systray_bottom_menu()")
		
		try:
			sep = Gtk.SeparatorMenuItem()
			self.systray_menu.append(sep)
		
			mainwindowentry = False
			if self.MAINWINDOW_OPEN == True:
				mainwindowentry = Gtk.MenuItem('Close Servers')
			else:
				if len(self.OVPN_SERVER) > 0:
					mainwindowentry = Gtk.MenuItem('Show Servers')
			if mainwindowentry:
				self.systray_menu.append(mainwindowentry)
				mainwindowentry.connect('button-release-event', self.show_mainwindow)
		except:
			self.debug(text="def make_systray_bottom_menu: mainwindowentry failed")

		try:
			if self.ACCWINDOW_OPEN == True:
				accwindowentry = Gtk.MenuItem('Close Account')
			else:
				accwindowentry = Gtk.MenuItem('Show Account')
			self.systray_menu.append(accwindowentry)
			accwindowentry.connect('button-release-event', self.show_accwindow)
		except:
			self.debug(text="def make_systray_bottom_menu: accwindowentry failed")
			
		if self.STATE_OVPN == False:
			try:
				sep = Gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)
				about = Gtk.MenuItem('About')
				self.systray_menu.append(about)
				about.connect('button-release-event', self.show_about_dialog)
			except:
				self.debug(text="def make_systray_bottom_menu: about failed")
			
			# add quit item
			quit = Gtk.MenuItem('Quit')
			self.systray_menu.append(quit)
			quit.connect('button-release-event', self.on_closing)

	def systray_notify_event(self, widget, event, data = None):
		#self.debug(text="def systray_notify_event()")
		try:
			self.mouse_in_tray_menu = time.time() + 30
		except:
			pass

	def check_hide_popup(self, data = None):
		#self.debug(text="def check_hide_popup()")
		try:
			if not self.mouse_in_tray_menu == None:
				if self.mouse_in_tray_menu < time.time():
					self.destroy_systray_menu()
					self.mouse_in_tray_menu = None
		except:
			pass

	def check_remote_update(self):
		self.debug(text="def check_remote_update()")
		if self.timer_check_certdl_running == False:
			if self.check_inet_connection() == True:
				self.debug(text="def check_remote_update()")
				if self.check_passphrase():
					#self.make_progressbar()
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
		self.debug(text="def make_progressbar()")
		try:
			self.progressbarfraction = 0.1
			self.progresswindow = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
			self.progresswindow.set_default_size(250,128)
			#self.progresswindow.set_border_width(6)
			self.progresswindow.set_title("oVPN Server Update")
			self.progresswindow.set_icon_from_file(self.systray_icon_syncupdate)
			self.progressbar = Gtk.ProgressBar()
			self.progressbar.set_pulse_step(0)
			self.progresswindow.add(self.progressbar)
			self.progresswindow.show_all()
			self.progresswindow.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		except:
			text = "def make_progressbar: failed"
			self.debug(text=text)

	def set_progressbar(self,text):
		self.debug(text="def set_progressbar()")
		try:
			if self.progressbarfraction < 0.95:
				self.progressbarfraction += 0.05
			else:
				self.progressbarfraction = 0.05
			self.progressbar.set_text(text)
			#self.progressbar.set_fraction(self.progressbarfraction)
		except:
			text = "def set_progressbar: failed"
			self.debug(text=text)

	def inThread_timer_check_certdl(self):
		self.debug(text="def inThread_timer_check_certdl()")
		try:
			self.timer_check_certdl_running = True
			try:
				self.load_ovpn_server()
				if len(self.OVPN_SERVER) == 0:
					self.reset_last_update()
			except:
				self.debug(text="def inThread_timer_check_certdl: self.load_ovpn_server() failed")

			self.debug(text="def inThread_timer_check_certdl()")
			if self.API_REQUEST(API_ACTION = "lastupdate"):
				self.debug(text="def inThread_timer_check_certdl: API_ACTION lastupdate")
				if self.check_last_server_update(self.curldata):
					if self.API_REQUEST(API_ACTION = "getconfigs"):
						if self.API_REQUEST(API_ACTION = "requestcerts"):
							while not self.body == "ready":
								time.sleep(6)
								self.API_REQUEST(API_ACTION = "requestcerts")
							# final step to download certs
							if self.API_REQUEST(API_ACTION = "getcerts"):
								if self.extract_ovpn():
									self.debug(text="def inThread_timer_check_certdl: extraction complete")
									self.timer_check_certdl_running = False
									return True
								else:
									self.debug(text="def inThread_timer_check_certdl: extraction failed")
							else:
								self.debug(text="def inThread_timer_check_certdl: downloading certs failed")
							# finish downloading certs
						else:
							self.debug(text="def inThread_timer_check_certdl: self.API_REQUEST(API_ACTION = requestcerts): failed")
					else:
						self.debug(text="def inThread_timer_check_certdl: self.API_REQUEST(API_ACTION = getconfigs): failed")
				else:
					self.debug(text="def inThread_timer_check_certdl: True")
					self.timer_check_certdl_running = False
					return True
			else:
				self.debug(text="def inThread_timer_check_certdl: self.API_REQUEST(API_ACTION = lastupdate): failed")
		except:
			self.debug(text="def inThread_timer_check_certdl: failed")
		self.timer_check_certdl_running = False
		return False
	
	def call_redraw_mainwindow(self):
		self.debug(text="def call_redraw_mainwindow_vbox()")
		if self.MAINWINDOW_OPEN == True:
			self.statusbartext_from_before = False
			try:
				self.treeview.set_model(model=None)
				try:
					self.serverliststore.clear()
				except:
					self.debug(text="def call_redraw_mainwindow: self.serverliststore.clear() failed")
					return False
			except:
				self.debug(text="def call_redraw_mainwindow: self.treeview.set_model(model=None) failed")
				return False
			try:
				GLib.idle_add(self.fill_mainwindow_with_server)
			except TypeError as e:
				self.debug(text="def call_redraw_mainwindow: GLib.idle_add(self.fill_mainwindow_with_server) failed e = '%s'" % (e))
			self.debug(text="def call_redraw_mainwindow: True")
			return True

	def show_mainwindow(self,widget,event):
		self.debug(text="def show_mainwindow()")
		self.destroy_systray_menu()
		self.LAST_OVPN_SRV_DATA_UPDATE = 0
		self.statusbartext_from_before = False
		if self.MAINWINDOW_OPEN == False:
			self.load_ovpn_server()
			try:
				self.mainwindow = Gtk.Window(Gtk.WindowType.TOPLEVEL)
				self.mainwindow.set_position(Gtk.WindowPosition.CENTER)
				self.mainwindow.connect("destroy",self.cb_destroy_mainwindow)
				self.mainwindow.set_title("oVPN Server - %s" % (CLIENT_STRING))
				self.mainwindow.set_icon_from_file(self.systray_icon_connected)
				if self.LOAD_SRVDATA == True:
					self.mainwindow.set_default_size(1780,830)
				else:
					self.mainwindow.set_default_size(510,830)
				self.mainwindow_ovpn_server()
				self.MAINWINDOW_OPEN = True
				return True
			except:
				self.MAINWINDOW_OPEN = False
				self.debug(text="def show_mainwindow: mainwindow failed")
				return False
		else:
			self.destroy_mainwindow()

	def mainwindow_ovpn_server(self):
		self.debug(text="def mainwindow_ovpn_server: go")
		self.mainwindow_vbox = Gtk.VBox(False,1)
		self.mainwindow.add(self.mainwindow_vbox)
		
		if self.OVPN_CONFIGVERSION == "23x":
			mode = "IPv4"
		elif self.OVPN_CONFIGVERSION == "23x46":
			mode = "IPv4 + IPv6"
		elif self.OVPN_CONFIGVERSION == "23x64":
			mode = "IPv6 + IPv4"
		self.debug(text="def mainwindow_ovpn_server: go0")
		label = Gtk.Label("oVPN Server [ %s ]" % (mode))

		self.debug(text="def mainwindow_ovpn_server: go1")
		try:
			self.serverliststore = Gtk.ListStore(GdkPixbuf.Pixbuf,GdkPixbuf.Pixbuf,str,str,str,int,str,int,str,int,int,str,str,str,str,str,str,str,int,int,int,int,int,int,int)
			self.debug(text="def mainwindow_ovpn_server: go2")
		except:
			self.debug(text="def mainwindow_ovpn_server: server-window failed")

		self.debug(text="def mainwindow_ovpn_server: go3")
		self.treeview = Gtk.TreeView(self.serverliststore)
		self.treeview.connect("button_release_event",self.on_right_click_mainwindow)
		self.treeview.set_model(model=None)
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.scrolledwindow.set_size_request(640,480)
		self.debug(text="def mainwindow_ovpn_server: go4")
		self.scrolledwindow.add(self.treeview)
		self.mainwindow_vbox.pack_start(self.scrolledwindow,True,True,0)

		try:
			self.debug(text="def fill_mainwindow_with_server: go2.1")
			cell = Gtk.CellRendererPixbuf()
			column = Gtk.TreeViewColumn(' ',cell, pixbuf=0)
			self.treeview.append_column(column)
			self.debug(text="def fill_mainwindow_with_server: go2.2")
			cell = Gtk.CellRendererPixbuf()
			column = Gtk.TreeViewColumn(' ',cell, pixbuf=1)
			self.treeview.append_column(column)
			self.debug(text="def fill_mainwindow_with_server: go2.3")
		except:
			self.debug(text="cell = Gtk.CellRendererPixbuf failed")

		cellnumber = 2
		cellnames = [ " Server ", " IPv4 ", " IPv6 ", " Port ", " Proto ", " MTU ", " Cipher ", " Mbps ", " Link ", " VLAN IPv4 ", " VLAN IPv6 ", " Processor ", " RAM ", " HDD ", " Traffic ", " Load ", " oVPN % ", " oSSH % ", " SOCK % ", " HTTP % ", " TINC % ", " PING4 ", " PING6 " ]
		for cellname in cellnames:
			align=0.5
			if cellnumber in [ 11 ]:
				align=1
			if cellnumber in [ 3, 4, 11, 12, 13, 16 ]:
				align=0
			cell = Gtk.CellRendererText(xalign=align)
			column = Gtk.TreeViewColumn(cellname, cell, text=cellnumber)
			if cellnumber in [ 2, 5, 7, 9, 10, 17, 18, 19, 20, 21, 22, 23, 24 ]:
				column.set_sort_column_id(cellnumber)
			self.treeview.append_column(column)
			cellnumber = cellnumber + 1

		self.fill_mainwindow_with_server()

		# statusbar
		self.statusbar_text = Gtk.Label()
		self.mainwindow_vbox.pack_start(self.statusbar_text,False,False,0)
		self.mainwindow.show_all()
		
		return

	def fill_mainwindow_with_server(self):
		self.debug(text="def fill_mainwindow_with_server()")
		#print "len(self.OVPN_SERVER) == %s" % (len(self.OVPN_SERVER))
		for server in self.OVPN_SERVER:
			#print "def mainwindow_ovpn_server: %s" % (server)
			countrycode = server[:2].lower()
			servershort = server[:3].upper()
			imgpath = self.FLAG_IMG[countrycode]
			countryimg = GdkPixbuf.Pixbuf.new_from_file(imgpath)
			serverip4  = self.OVPN_SERVER_INFO[servershort][0]
			serverport = self.OVPN_SERVER_INFO[servershort][1]
			serverproto = self.OVPN_SERVER_INFO[servershort][2]
			servercipher = self.OVPN_SERVER_INFO[servershort][3]
			if servercipher == "CAMELLIA-256-CBC":
				servercipher = "CAM-256"
			elif servercipher == "AES-256-CBC":
				servercipher = "AES-256"

			try:
				servermtu = self.OVPN_SERVER_INFO[servershort][4]
			except:
				servermtu = 1500
			# defaults values
			statusimgpath = False
			vlanip4 = "n/a"
			vlanip6 = "n/a"
			traffic = "n/a"
			live = False
			uplink = False
			cpuinfo = "n/a"
			raminfo = "n/a"
			hddinfo = "n/a"
			cpuload = "n/a"
			cpuovpn = False
			cpusshd = False
			cpusock = False
			cpuhttp = False
			cputinc = False
			ping4 = False
			ping6 = False
			serverip6 = "n/a"
			# defaults end
			try:
				vlanip4 = self.OVPN_SRV_DATA[servershort]["vlanip4"]
				vlanip6 = self.OVPN_SRV_DATA[servershort]["vlanip6"]
				traffic = self.OVPN_SRV_DATA[servershort]["traffic"]["eth0"]
				live = self.OVPN_SRV_DATA[servershort]["traffic"]["live"]
				uplink = self.OVPN_SRV_DATA[servershort]["traffic"]["uplink"]
				cpuinfo = self.OVPN_SRV_DATA[servershort]["info"]["cpu"]
				raminfo = self.OVPN_SRV_DATA[servershort]["info"]["ram"]
				hddinfo = self.OVPN_SRV_DATA[servershort]["info"]["hdd"]
				cpuload = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-load"]
				cpuovpn = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-ovpn"]
				cpusshd = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-sshd"]
				cpusock = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-sock"]
				cpuhttp = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-http"]
				cputinc = self.OVPN_SRV_DATA[servershort]["cpu"]["cpu-tinc"]
				ping4 = self.OVPN_SRV_DATA[servershort]["pings"]["ipv4"]
				ping6 = self.OVPN_SRV_DATA[servershort]["pings"]["ipv6"]
				serverip6 = self.OVPN_SRV_DATA[servershort]["extip6"]
				serverstatus = self.OVPN_SRV_DATA[servershort]["status"]
				if serverstatus == "0":
					statusimgpath = "%s\\bullet_red.png" % (self.ico_dir)
				elif serverstatus == "1":
					statusimgpath = "%s\\bullet_green.png" % (self.ico_dir)
				elif serverstatus == "2":
					statusimgpath = "%s\\bullet_white.png" % (self.ico_dir)
			except:
				#self.debug(text="self.serverliststore failed: #1 (defaults) %s" % (server))
				pass

			if server == self.OVPN_CONNECTEDto:
				statusimgpath = "%s\\shield_go.png" % (self.ico_dir)
			elif server == self.OVPN_FAV_SERVER:
				statusimgpath = "%s\\star.png" % (self.ico_dir)
			
			if statusimgpath == False or not os.path.isfile(statusimgpath):
				if not statusimgpath == False:
					self.debug("def fill_mainwindow_with_server: statusimgpath '%s' not found for server %s" % (statusimgpath,server))
				statusimgpath = "%s\\bullet_white.png" % (self.ico_dir)

			try:
				statusimg = GdkPixbuf.Pixbuf.new_from_file(statusimgpath)
				self.serverliststore.append([statusimg,countryimg,str(server),str(serverip4),str(serverip6),int(serverport),str(serverproto),int(servermtu),str(servercipher),int(float(live)),int(uplink),str(vlanip4),str(vlanip6),str(cpuinfo),str(raminfo),str(hddinfo),str(traffic),str(cpuload),int(cpuovpn),int(cpusshd),int(cpusock),int(cpuhttp),int(cputinc),int(float(ping4)),int(float(ping6))])
			except:
				self.debug(text="self.serverliststore.append: failed '%s'" % (server))
			
		self.treeview.set_model(model=self.serverliststore)
		self.debug(text="def fill_mainwindow_with_server: return")
		return

	def destroy_mainwindow(self):
		self.debug(text="def destroy_mainwindow()")
		self.mainwindow.destroy()
		self.MAINWINDOW_OPEN = False
		self.debug(text="def destroy_mainwindow")

	def call_redraw_accwindow(self):
		self.debug(text="def call_redraw_accwindow()")
		if self.ACCWINDOW_OPEN == True:
			try:
				self.accwindow.remove(self.accwindow_accinfo_vbox)
				GLib.idle_add(self.accwindow_accinfo)
				self.debug(text="def call_redraw_accwindow: True")
			except:
				self.debug(text="def call_redraw_accwindow: False")

	def show_accwindow(self,widget,event):
		self.debug(text="def show_accwindow()")
		self.destroy_systray_menu()
		self.LAST_OVPN_ACC_DATA_UPDATE = 0
		if self.ACCWINDOW_OPEN == False:
			try:
				self.accwindow = Gtk.Window(Gtk.WindowType.TOPLEVEL)
				self.accwindow.set_position(Gtk.WindowPosition.CENTER)
				self.accwindow.connect("destroy",self.cb_destroy_accwindow)
				self.accwindow.set_title("oVPN Account - %s" % (CLIENT_STRING))
				self.accwindow.set_icon_from_file(self.systray_icon_connected)
				self.accwindow.set_default_size(370,480)
				self.accwindow_accinfo()
				self.ACCWINDOW_OPEN = True
				return True
			except:
				self.ACCWINDOW_OPEN = False
				self.debug(text="def show_accwindow: accwindow failed")
				return False
		else:
			self.destroy_accwindow()

	def accwindow_accinfo(self):
		self.debug(text="def accwindow_accinfo()")
		self.accwindow_accinfo_vbox = Gtk.VBox(False,0)
		self.accwindow.add(self.accwindow_accinfo_vbox)
		if len(self.OVPN_ACC_DATA) == 0:
			if self.LOAD_ACCDATA == False:
				text = "Systray Menu -> Updates -> 'Load Account Info' [disabled]"
			else:
				text = "No data loaded! Retry in few seconds..."
			entry = Gtk.Entry()
			entry.set_max_length(64)
			entry.set_editable(0)
			entry.set_text(text)
			self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
		elif len(self.OVPN_ACC_DATA) > 0:
			try:
				#self.debug(text="def accwindow_accinfo: try get values")
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
								text = "%s: '%s'" % (coin.upper(),addr.upper())
								#print text
								entry = Gtk.Entry()
								entry.set_max_length(128)
								entry.set_editable(0)
								entry.set_text(text)
								self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
							except:
								self.debug(text="def accwindow_accinfo: coin '%s' failed" % (coin))
						break
					else:
						head = key
					if value1 == False:
						value1 = value
					text = "%s: %s" % (head,value1)
					#self.debug(text="key [%s] = '%s' value = '%s'" % (key,head,value))
					try:
						entry = Gtk.Entry()
						entry.set_max_length(128)
						entry.set_editable(0)
						entry.set_text(text)
						self.accwindow_accinfo_vbox.pack_start(entry,True,True,0)
					except:
						self.debug(text="def accwindow_accinfo: accdata vbox.pack_start entry failed!")
			except:
				self.debug(text="def accwindow_accinfo: self.OVPN_ACC_DATA failed")
		self.accwindow.show_all()
		return

	def destroy_accwindow(self):
		self.debug(text="def destroy_accwindow()")
		self.accwindow.destroy()
		self.ACCWINDOW_OPEN = False
		self.debug(text="def destroy_accwindow")

	def cb_destroy_mainwindow(self,event):
		self.debug(text="def cb_destroy_mainwindow")
		self.destroy_mainwindow()

	def cb_destroy_accwindow(self,event):
		self.debug(text="def cb_destroy_accwindow")
		self.destroy_accwindow()

	def cb_del_dns(self,widget,event,data):
		self.debug(text="def cb_del_dns()")
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
				#self.MYDNS[name]["primary"] = {}
				#self.MYDNS[name]["secondary"] = {}
			try:
				if value["secondary"]["ip4"] == self.MYDNS[name]["secondary"]["ip4"]:
					self.MYDNS[name]["secondary"] = {}
			except:
				pass
		self.write_options_file()
		if self.OVPN_CONNECTEDto == name:
			self.debug(text="def cb_set_dns: self.OVPN_CONNECTEDto = %s , name = %s" % (self.OVPN_CONNECTEDto,name))
			self.win_netsh_set_dns_ovpn()
		return True

	def cb_set_dns(self,widget,event,data):
		self.debug(text="def cb_set_dns()")
		self.destroy_context_menu_servertab()
		for name,value in data.iteritems():
			self.debug(text="def cb_set_dns: name '%s' value: '%s'" % (name,value))
			try:
				newpridns = value["primary"]["ip4"]
				if self.isValueIPv4(newpridns):
					print " set primary dns"
					try:
						print 'try: if newpridns == self.MYDNS[name]["secondary"]["ip4"]'
						if newpridns == self.MYDNS[name]["secondary"]["ip4"]:
							self.MYDNS[name]["secondary"] = {}
							self.debug(text='self.MYDNS[name]["secondary"] = {}')
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
				self.debug(text="def cb_set_dns: self.OVPN_CONNECTEDto = %s , name = %s" % (self.OVPN_CONNECTEDto,name))
				self.win_netsh_set_dns_ovpn()
				return True

	def destroy_context_menu_servertab(self):
		self.debug(text="def destroy_context_menu_servertab()")
		try:
			self.dnssubmenu.hide()
			self.debug(text="def destroy_context_menu_servertab: 0x0001")
		except:
			pass
		try:
			self.dnsmenu.hide()
			self.debug(text="def destroy_context_menu_servertab: 0x0002")
		except:
			pass
		try:
			self.context_menu_servertab.hide()
			self.debug(text="def destroy_context_menu_servertab: 0x0003")
		except:
			pass

	def destroy_systray_menu(self):
		self.debug(text="def destroy_systray_menu()")
		try:
			self.systray_menu.hide()
			self.systray_menu = False
			self.debug(text = "def destroy_systray_menu: true")
		except:
			self.debug(text = "def destroy_systray_menu: failed")
			self.systray_menu = False

	def set_statusbar_text(self,text):
		self.debug(text="def set_statusbar_text()")
		try:
			if self.MAINWINDOW_OPEN == True:
				self.statusbar_text.set_label(text)
		except:
			self.debug(text="def set_statusbar_text: text = '%s' failed" % (text))

	def check_passphrase(self):
		self.debug(text="def check_passphrase()")
		self.read_options_file()
		if self.PASSPHRASE == False:
			self.debug(text="def check_passphrase: popup receive passphrase")
			return self.form_ask_passphrase()
		else:
			if self.read_apikey_config():
				return self.compare_confighash()
			self.PASSPHRASE == False

	def cb_set_ovpn_favorite_server(self,widget,event,server):
		self.debug(text="def cb_set_ovpn_favorite_server()")
		self.destroy_context_menu_servertab()
		try:
			self.OVPN_FAV_SERVER = server
			#self.OVPN_AUTO_CONNECT_ON_START = True
			self.write_options_file()
			text = "oVPN AutoConnect: %s" % (server)
			self.set_statusbar_text(text)
			self.call_redraw_mainwindow()
			return True
		except:
			self.msgwarn(text="def cb_set_ovpn_favorite_server: failed")

	def cb_del_ovpn_favorite_server(self,widget,event,server):
		self.debug(text="def cb_del_ovpn_favorite_server()")
		self.destroy_context_menu_servertab()
		try:
			self.OVPN_FAV_SERVER = False
			self.OVPN_AUTO_CONNECT_ON_START = False
			self.write_options_file()
			text = "oVPN AutoConnect: removed %s" % (server)
			self.set_statusbar_text(text)
			self.call_redraw_mainwindow()
			return True
		except:
			self.msgwarn(text="def cb_del_ovpn_favorite_server: failed")

	def cb_redraw_mainwindow_vbox(self,widget,event):
		self.debug(text="def cb_redraw_mainwindow_vbox()")
		self.destroy_context_menu_servertab()
		if self.LOAD_SRVDATA == True:
			self.LAST_OVPN_SRV_DATA_UPDATE = -1
		if self.LOAD_ACCDATA == True:
			self.LAST_OVPN_ACC_DATA_UPDATE = -1

	def cb_kill_openvpn(self,widget,event):
		self.debug(text="def cb_kill_openvpn()")
		#self.destroy_context_menu_servertab()
		self.destroy_systray_menu()
		self.OVPN_AUTO_CONNECT_ON_START = False
		self.debug(text="def cb_kill_openvpn")
		killthread = threading.Thread(target=self.inThread_kill_openvpn)
		killthread.start()

	def inThread_kill_openvpn(self):
		self.debug(text="def inThread_kill_openvpn()")
		self.kill_openvpn()

	def cb_jump_openvpn(self,widget,event,server):
		self.debug(text="def cb_jump_openvpn()")
		self.destroy_systray_menu()
		self.destroy_context_menu_servertab()
		#if (not self.OVPN_CONNECTEDto == False and not self.OVPN_PING_LAST > 0) or (self.OVPN_CONNECTEDseconds > 0 and self.OVPN_CONNECTEDseconds < 20):
		#	return
		self.debug(text="def cb_jump_openvpn: %s" % (server))
		jumpthread = threading.Thread(target=lambda server=server: self.inThread_jump_server(server))
		jumpthread.start()

	def inThread_jump_server(self,server):
		self.debug(text="def inThread_jump_server()")
		if self.inThread_jump_server_running == True:
			self.debug(text="def inThread_jump_server: running ! return")
			return
		else:
			self.inThread_jump_server_running = True
			self.debug(text="def inThread_jump_server: server %s" % (server))
			if self.STATE_OVPN == True:
				self.kill_openvpn()
			while not self.OVPN_THREADID == False:
				self.debug(text="def cb_jump_openvpn: sleep while self.OVPN_THREADID not == False")
				time.sleep(1)
			self.call_openvpn(server)
			self.inThread_jump_server_running == False
			self.debug(text="def inThread_jump_server: exit")

	def kill_openvpn(self):
		self.debug(text="def kill_openvpn()")
		if self.STATE_OVPN == False:
			return False
		self.debug(text="def kill_openvpn")
		try:
			self.del_ovpn_routes()
		except:
			pass
		try:
			if os.path.isfile(self.WIN_TASKKILL_EXE):
				ovpn_exe = self.OPENVPN_EXE.split("\\")[-1]
				string = '"%s" /F /IM %s' % (self.WIN_TASKKILL_EXE,ovpn_exe)
				exitcode = subprocess.check_call("%s" % (string),shell=True)
				self.debug(text="def kill_openvpn: exitcode = %s" % (exitcode))
		except:
			self.debug(text="def kill_openvpn: failed!")
			self.reset_ovpn_values_disconnected()

	def call_openvpn(self,server):
		self.debug(text="def call_openvpn()")
		try:
			thread_openvpn = threading.Thread(target=lambda server=server: self.openvpn(server))
			thread_openvpn.start()
			self.debug(text="def call_openvpn: thread_openvpn.start()")
		except:
			self.debug(text="def call_openvpn: thread self.openvpn(server) failed")
			return False
		return True

	def openvpn(self,server):
		self.debug(text="def openvpn()")
		while self.timer_check_certdl_running == True:
			self.debug(text="def openvpn: sleep while timer_check_certdl_running")
			time.sleep(0.5)
		self.debug(text="def openvpn: server = '%s'" % (server))
		self.OVPN_CALL_SRV = server
		if self.STATE_OVPN == False:
			self.ovpn_server_UPPER = server
			self.ovpn_server_LOWER = server.lower()
			self.ovpn_server_config_file = "%s\\%s.ovpn" % (self.vpn_cfg,self.ovpn_server_UPPER)
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
							self.debug(text="Could not read Servers Remote-IP:Port from config: %s" % (self.ovpn_server_config_file))
							return False
					if "proto " in line:
						try:
							proto = line.split()[1]
							if proto.lower()  == "tcp" or proto.lower() == "udp":
								self.OVPN_CONNECTEDtoProtocol = proto
						except:
							self.debug(text="Could not read Servers Protocol from config: %s" % (self.ovpn_server_config_file))
							return False
			else:
				self.debug(text="Error: Server Config not found: '%s'" % (self.ovpn_server_config_file))
				return False

			self.ovpn_sessionlog = "%s\\ovpn.log" % (self.vpn_dir)
			self.ovpn_server_dir = "%s\\%s" % (self.vpn_cfg,self.ovpn_server_LOWER)
			self.ovpn_cert_ca = "%s\\%s.crt" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_tls_key = "%s\\%s.key" % (self.ovpn_server_dir,self.ovpn_server_LOWER)
			self.ovpn_cli_crt = "%s\\client%s.crt" % (self.ovpn_server_dir,self.USERID)
			self.ovpn_cli_key = "%s\\client%s.key" % (self.ovpn_server_dir,self.USERID)
			if not os.path.isdir(self.ovpn_server_dir) or \
				not os.path.isfile(self.ovpn_cert_ca) or \
				not os.path.isfile(self.ovpn_tls_key) or \
				not os.path.isfile(self.ovpn_cli_crt) or \
				not os.path.isfile(self.ovpn_cli_key):
					self.msgwarn(text="Error: Files missing: '%s' % (self.ovpn_server_dir)")
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
				self.debug(text="Started: oVPN %s on Thread: %s" % (server,self.OVPN_THREADID))
			except:
				self.debug(text="Error: Unable to start thread: oVPN %s " % (server))
				return False
		else:
			self.debug(text="def openvpn: self.OVPN_THREADID = %s" % (self.OVPN_THREADID))

	def inThread_spawn_openvpn_process(self):
		self.debug(text="def inThread_spawn_openvpn_process")
		exitcode = False
		self.win_enable_tap_interface()
		if not self.openvpn_check_files():
			self.OVPN_CONNECTEDto = False
			return False
		if not self.win_firewall_start():
			self.debug(text="def inThread_spawn_openvpn_process: Could not start Windows Firewall!")
			self.OVPN_CONNECTEDto = False
			return False
		self.win_firewall_modify_rule(option="add")
		self.win_clear_ipv6()
		self.OVPN_CONNECTEDtime = int(time.time())
		self.OVPN_CONNECTEDto = self.OVPN_CALL_SRV
		self.OVPN_PING_STAT = -1
		self.OVPN_PING_LAST = -1
		self.LAST_PING_EXEC = 0
		self.LAST_OVPN_ACC_DATA_UPDATE = 0
		self.LAST_OVPN_SRV_DATA_UPDATE = 0
		self.STATE_OVPN = True
		if self.timer_ovpn_ping_running == False:
			self.debug("def inThread_spawn_openvpn_process: self.inThread_timer_ovpn_ping")
			pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
			pingthread.start()
		self.inThread_jump_server_running = False
		self.call_redraw_mainwindow()
		self.win_netsh_set_dns_ovpn()
		try:
			exitcode = subprocess.check_call("%s" % (self.ovpn_string),shell=True,stdout=None,stderr=None)
		except:
			self.debug(text="def inThread_spawn_openvpn_process: exited")
		self.reset_ovpn_values_disconnected()
		self.call_redraw_mainwindow()
		return

	def reset_ovpn_values_disconnected(self):
		try:
			self.win_firewall_modify_rule(option="delete")
		except:
			self.debug(text="def inThread_spawn_openvpn_process: self.win_firewall_modify_rule option=delete failed!")
		self.win_clear_ipv6()
		self.debug(text="def reset_ovpn_values_after()")
		self.STATE_OVPN = False
		self.OVPN_CONNECTEDto = False
		self.OVPN_CONNECTEDtoIP = False
		self.OVPN_CONNECTEDtime = 0
		self.OVPN_CONNECTEDseconds = 0
		self.OVPN_THREADID = False
		self.OVPN_PING_STAT = 0
		self.OVPN_PING_LAST = 0
		self.OVPN_PING = list()
		try:
			if os.path.isfile(self.ovpn_sessionlog):
				os.remove(self.ovpn_sessionlog)
		except:
			pass
	
	def inThread_timer_ovpn_ping(self):
		#self.debug(text="def inThread_timer_ovpn_ping()")
		if self.timer_ovpn_ping_running == False:
			self.OVPN_PING_STAT = -2
			self.timer_ovpn_ping_running = True
			self.debug(text="def inThread_timer_ovpn_ping: start")

		if self.STATE_OVPN == False:
			self.OVPN_PING_STAT = -1
			self.OVPN_PING = list()
			self.timer_ovpn_ping_running = False
			self.debug("def inThread_timer_ovpn_ping: leaving")
			return

		elif self.STATE_OVPN == True:
			try:
				try:
					if self.LAST_PING_EXEC < int(time.time()) and self.OVPN_CONNECTEDseconds > 5:
						PING = self.get_ovpn_ping()
						if PING > 0 and PING < 1:
							PING = round(PING,3)
						elif PING > 1:
							PING = int(PING)
						if PING > 0 and self.check_myip() == True:
							randint = random.randint(15,30)
							self.LAST_PING_EXEC = int(time.time())+randint
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
							#self.debug(text="def inThread_timer_ovpn_ping: %s ms, next in %s s"%(PING,randint))
				except:
					self.OVPN_PING_LAST = -2
					self.debug(text="ping failed")
					pass
			except:
				self.debug(text="def inThread_timer_ovpn_ping: failed")
			time.sleep(0.5)
			try:
				pingthread = threading.Thread(target=self.inThread_timer_ovpn_ping)
				pingthread.start()
				return True
			except:
				self.debug(text="rejoin def inThread_timer_ovpn_ping() failed")

	def get_ovpn_ping(self):
		#self.debug(text="def get_ovpn_ping()")
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
					#self.debug(text="def get_ovpn_ping: %s ms" % (PING))
					return PING
				except:
					self.OVPN_PING_LAST = -2
					return -2
		except:
			self.debug(text="def get_ovpn_ping: failed")

	def read_gateway_from_routes(self):
		self.debug(text="def read_gateway_from_routes()")
		try:
			output = self.win_return_route_cmd('print')
			for line in output:
				split = line.split()
				try:
					if split[0] == "0.0.0.0" and split[1] == "0.0.0.0":
						self.GATEWAY_LOCAL = split[2]
						self.debug(text="self.GATEWAY_LOCAL #1: %s" % (self.GATEWAY_LOCAL))
						return True
				except:
					self.debug(text="def read_gateway_from_routes: #1 failed")
				try:
					if self.OVPN_CONNECTEDtoIP in line:
						self.debug(text="def read_ovpn_routes: self.OVPN_CONNECTEDtoIP in line '%s'" % (line))
						self.GATEWAY_LOCAL = line.split()[2]
						self.debug(text="self.GATEWAY_LOCAL #2: %s" % (self.GATEWAY_LOCAL))
						return True
				except:
					self.debug(text="def read_gateway_from_routes: #2 failed")
		except:
			self.debug(text="def read_gateway_from_routes: failed")

	def del_ovpn_routes(self):
		self.debug(text="def del_ovpn_routes()")
		try:
			if self.read_gateway_from_routes():
				if not self.GATEWAY_LOCAL == False:
					self.ROUTE_CMDLIST.append("DELETE %s MASK 255.255.255.255 %s" % (self.OVPN_CONNECTEDtoIP,self.GATEWAY_LOCAL))
					self.ROUTE_CMDLIST.append("DELETE 0.0.0.0 MASK 128.0.0.0 %s" % (self.GATEWAY_OVPN_IP4))
					self.ROUTE_CMDLIST.append("DELETE 128.0.0.0 MASK 128.0.0.0 %s" % (self.GATEWAY_OVPN_IP4))
					return self.win_join_route_cmd()
		except:
			self.debug(text="def del_ovpn_routes: failed")

	def win_clear_ipv6(self):
		self.debug(text="def win_clear_ipv6()")
		self.win_clear_ipv6_dns()
		self.win_clear_ipv6_addr()
		self.win_clear_ipv6_routes()

	def win_clear_ipv6_dns(self):
		self.debug(text="def win_clear_ipv6_dns()")
		try:
			netshcmd = 'interface ipv6 show dnsservers "%s"' % (self.WIN_TAP_DEVICE)
			#self.debug(text="def win_clear_ipv6_dns: netshcmd = '%s'" % (netshcmd))
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
							text = "def win_clear_ipv6_dns: removed %s '%s'" % (ipv6addr,string)
							self.debug(text=text)
						except subprocess.CalledProcessError as e:
							text = "def win_clear_ipv6_dns: %s %s failed '%s': %s" % (ipv6addr,self.WIN_TAP_DEVICE,string,e.output)
							self.debug(text=text)
						except:
							text = "def win_clear_ipv6_dns: %s %s failed '%s'" % (ipv6addr,self.WIN_TAP_DEVICE,string)
							self.debug(text=text)
		except:
			self.debug(text="def win_clear_ipv6_dns: failed")

	def win_clear_ipv6_addr(self):
		self.debug(text="def win_clear_ipv6_addr()")
		try:
			try:
				netshcmd = 'interface ipv6 show addresses "%s"' % (self.WIN_TAP_DEVICE)
				#self.debug(text="def win_clear_ipv6_addr: netshcmd = '%s'" % (netshcmd))
				netsh_output = self.win_return_netsh_cmd(netshcmd)
				try:
					for line in netsh_output:
						if " fd48:8bea:68a5:" in line or " fe80:" in line:
							self.debug(text="def win_clear_ipv6_addr: found: line = '%s'" % (line))
							if not "%" in line:
								ipv6addr = line.split()[1]
								netshcmd = 'interface ipv6 delete address address="%s" interface="%s" store=active' % (ipv6addr,self.WIN_TAP_DEVICE)
								self.NETSH_CMDLIST.append(netshcmd)
					if len(self.NETSH_CMDLIST) > 0:
						self.win_join_netsh_cmd()
				except:
					self.debug(text="def win_clear_ipv6_addr: failed #2")
			except:
				self.debug(text="def win_clear_ipv6_addr: failed #1")
		except:
			self.debug(text="def win_clear_ipv6_addr: failed")

	def win_clear_ipv6_routes(self):
		self.debug(text="def win_clear_ipv6_routes()")
		try:
			netshcmd = 'interface ipv6 show route'
			netsh_output = self.win_return_netsh_cmd(netshcmd)
			#self.debug(text="def win_clear_ipv6_routes: netshcmd = '%s'" % (netshcmd))
			for line in netsh_output:
				if " fd48:8bea:68a5:" in line or " fe80:" in line:
					self.debug(text="def win_clear_ipv6_routes: found: line = '%s'" % (line))
					ipv6 = line.split()[3]
					output = self.win_return_route_cmd("DELETE %s" % (ipv6))
					self.debug(text="def win_clear_ipv6_routes: %s %s" % (ipv6,output))
		except:
			self.debug(text="def win_clear_ipv6_routes: failed")

	def win_netsh_set_dns_ovpn(self):
		self.debug(text="def win_netsh_set_dns_ovpn()")
		if self.NO_DNS_CHANGE == True:
			self.debug(text="def win_netsh_set_dns_ovpn: self.NO_DNS_CHANGE")
			return True
		if self.check_dns_is_whitelisted() == True:
			return True
		servername = self.OVPN_CONNECTEDto
		self.debug(text="def win_netsh_set_dns_ovpn: servername = '%s'" % (servername))
		try:
			pridns = self.MYDNS[servername]["primary"]["ip4"]
			self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_EXT_DEVICE,pridns))
			self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no' % (self.WIN_TAP_DEVICE,pridns))
			try:
				secdns = self.MYDNS[servername]["secondary"]["ip4"]
				self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no' % (self.WIN_EXT_DEVICE,secdns))
				self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no' % (self.WIN_TAP_DEVICE,secdns))
			except:
				self.debug(text="def win_netsh_set_dns_ovpn: secdns not found")
		except:
			self.debug(text="def win_netsh_set_dns_ovpn: pridns not found")
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
			self.debug(text="def win_netsh_set_dns_ovpn: failed!")

	def win_netsh_restore_dns_from_backup(self):
		self.debug(text="def win_netsh_restore_dns_from_backup()")
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
						self.debug(text="DNS restored to DHCP.")
						return True
					else:
						return False
			except:
				self.debug(text="def win_netsh_restore_dns_from_backup: restore DHCP on IF: '%s' failed " % (self.WIN_EXT_DEVICE))

			try:
				if not self.GATEWAY_DNS1 == self.GATEWAY_OVPN_IP4A:
					self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" static %s primary no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS1))
					if self.win_join_netsh_cmd():
						self.debug(text="Primary DNS restored to: %s"%(self.GATEWAY_DNS1))
						if self.GATEWAY_DNS2 == False:
							return True
						else:
							self.NETSH_CMDLIST.append('interface ip add dnsservers "%s" %s index=2 no'%(self.WIN_EXT_DEVICE,self.GATEWAY_DNS2))
							if self.win_join_netsh_cmd():
								self.debug(text="Secondary DNS restored to %s" % (self.GATEWAY_DNS2))
								return True
							else:
								self.msgwarn(text="Error: Restore Secondary DNS to %s failed." % (self.GATEWAY_DNS2))
								return False
					else:
						self.msgwarn(text="Error: Restore Primary DNS to %s failed." % (self.GATEWAY_DNS1))
						return False
				else:
					self.NETSH_CMDLIST.append('interface ip set dnsservers "%s" dhcp' % (self.WIN_EXT_DEVICE))
					if self.win_join_netsh_cmd():
						self.debug(text="DNS restored to DHCP")
						return True
					else:
						return False
			except:
				self.debug(text="def win_netsh_restore_dns_from_backup: Restore DNS failed")
		except:
			self.debug(text="def win_netsh_restore_dns_from_backup: failed")

	def win_netsh_read_dns_to_backup(self):
		self.debug(text="def win_netsh_read_dns_to_backup()")
		self.read_d0wns_dns()

		if self.NO_DNS_CHANGE == True:
			return True
		try:
			netshcmd = 'interface ipv4 show dns'
			netsh_output = self.win_return_netsh_cmd(netshcmd)
			search = '"%s"' % (self.WIN_EXT_DEVICE)
			i, m1, m2, t = 0, 0, 0 ,0
			self.debug(text="def win_netsh_read_dns_to_backup: search = %s" % (search))
			for line in netsh_output:
				if search in line:
					self.debug(text="found: %s in %s line %s" % (search,line,i))
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
								self.debug(text="1st DNS '%s' IF: %s backuped" % (dns1,search))
						except:
							self.debug(text="def win_netsh_read_dns_to_backup: 1st DNS failed read on line '%s' search '%s'" % (line,search))

				if i == m2:
					try:
						dns2 = line.strip()
						if self.isValueIPv4(dns2):
								self.GATEWAY_DNS2 = dns2
								self.debug(text="2nd DNS '%s' IF: %s backuped" % (dns2,search))
								break
					except:
						self.debug(text="def win_netsh_read_dns_to_backup: 2nd DNS failed read on line '%s' search '%s'" % (line,search))

				i+=1
			self.debug(text="def win_netsh_read_dns_to_backup: self.GATEWAY_DNS1 = %s + self.GATEWAY_DNS2 = %s"%(self.GATEWAY_DNS1,self.GATEWAY_DNS2))
			if not self.GATEWAY_DNS1 == False:
				return True
			else:
				self.WIN_EXT_DHCP = True
				return True
		except:
			self.errorquit(text="def win_netsh_read_dns_to_backup: failed!")

	def hash_sha512_file(self,file):
		self.debug(text="def hash_sha512_file()")
		if os.path.isfile(file):
			hasher = hashlib.sha512()
			fp = open(file, 'rb')
			with fp as afile:
				buf = afile.read()
				hasher.update(buf)
			fp.close()
			return hasher.hexdigest()

	def hash_sha256_file(self,file):
		self.debug(text="def hash_sha256_file()")
		if os.path.isfile(file):
			hasher = hashlib.sha256()
			fp = open(file, 'rb')
			with fp as afile:
				buf = afile.read()
				hasher.update(buf)
			fp.close()
			return hasher.hexdigest()

	def load_ca_cert(self):
		self.debug(text="def load_ca_cert()")
		if os.path.isfile(self.CA_FILE):
			self.CA_FILE_HASH = self.hash_sha512_file(self.CA_FILE)
			if self.CA_FILE_HASH == self.CA_FIXED_HASH:
				try:
					os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), self.CA_FILE)
					return True
				except:
					self.msgwarn(text="Error:\nSSL Root Certificate for %s not loaded %s" % (DOMAIN,self.CA_FILE))
					return False
			else:
				self.msgwarn(text = "Error:\nInvalid SSL Root Certificate for %s in:\n'%s'\nhash is:\n'%s'\nbut should be '%s'" % (DOMAIN,self.CA_FILE,self.CA_FILE_HASH,self.CA_FIXED_HASH))
				return False
		else:
			self.msgwarn(text="Error:\nSSL Root Certificate for %s not found in:\n'%s'!" % (DOMAIN,self.CA_FILE))
			return False

	def win_firewall_start(self):
		self.debug(text="def win_firewall_start()")
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
		self.debug(text="def win_firewall_tap_blockoutbound()")
		try:
			if self.NO_WIN_FIREWALL == True:
				return True
			if self.TAP_BLOCKOUTBOUND == True:
				self.win_firewall_whitelist_ovpn_on_tap(option="delete")
				self.win_firewall_whitelist_ovpn_on_tap(option="add")
				self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,blockoutbound")
			else:
				self.win_firewall_whitelist_ovpn_on_tap(option="delete")
				self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,allowoutbound")		
			self.win_join_netsh_cmd()
			self.debug(text="Block outbound on TAP!\n\nAllow Whitelist to Internal oVPN Services\n\n'%s'\n\nSee all Rules:\n Windows Firewall with Advanced Security\n --> Outgoing Rules" % (self.WHITELIST_PUBLIC_PROFILE))
			return True
		except:
			self.debug(text="def win_firewall_tap_blockoutbound: failed!")

	def win_firewall_allowout(self):
		self.debug(text="def win_firewall_allowout()")
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
		self.debug(text="def win_firewall_block_on_exit()")
		if self.NO_WIN_FIREWALL == True:
			return True
		self.NETSH_CMDLIST.append("advfirewall set allprofiles state on")
		self.NETSH_CMDLIST.append("advfirewall set privateprofile firewallpolicy blockinbound,blockoutbound")
		self.NETSH_CMDLIST.append("advfirewall set domainprofile firewallpolicy blockinbound,blockoutbound")
		self.NETSH_CMDLIST.append("advfirewall set publicprofile firewallpolicy blockinbound,blockoutbound")
		return self.win_join_netsh_cmd()

	def win_firewall_whitelist_ovpn_on_tap(self,option):
		self.debug(text="def win_firewall_whitelist_ovpn_on_tap()")
		if self.NO_WIN_FIREWALL == True:
			self.debug("def win_firewall_whitelist_ovpn_on_tap: self.NO_WIN_FIREWALL == True")
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
			self.debug(text="Whitelist: %s %s %s %s" % (entry,ip,port,protocol))
		self.win_join_netsh_cmd()
		return True

	def win_firewall_add_rule_to_vcp(self,option):
		self.debug(text="def win_firewall_add_rule_to_vcp()")
		if self.NO_WIN_FIREWALL == True:
			return True
		self.debug(text="def win_firewall_add_rule_to_vcp()")
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
		self.debug(text="def win_firewall_export_on_start()")
		if self.NO_WIN_FIREWALL == True:
			return True
		if self.WIN_BACKUP_FIREWALL == False:
			return True
		self.debug(text="def win_firewall_export_on_start()")
		if os.path.isfile(self.pfw_bak):
			os.remove(self.pfw_bak)
		self.NETSH_CMDLIST.append('advfirewall export "%s"' % (self.pfw_bak))
		return self.win_join_netsh_cmd()

	def win_firewall_restore_on_exit(self):
		self.debug(text="def win_firewall_restore_on_exit()")
		if self.NO_WIN_FIREWALL == True:
			return True
		if self.WIN_BACKUP_FIREWALL == False:
			return True
		if self.WIN_FIREWALL_STARTED == True:
			self.debug(text="def win_firewall_restore_on_exit()")
			self.NETSH_CMDLIST.append("advfirewall reset")
			if os.path.isfile(self.pfw_bak):
				self.NETSH_CMDLIST.append('advfirewall import "%s"' % (self.pfw_bak))
			return self.win_join_netsh_cmd()

	def win_enable_tap_interface(self):
		self.debug(text="def win_enable_tap_interface()")
		self.NETSH_CMDLIST.append('interface set interface "%s" ENABLED'%(self.WIN_TAP_DEVICE))
		return self.win_join_netsh_cmd()

	"""
	*fixme* (unused)
	def win_disable_interface(self):
		self.debug(text="def win_disable_interface()")
		self.NETSH_CMDLIST.append('interface set interface "%s" DISABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()		
		
	def win_ensable_interface(self):
		self.debug(text="def win_ensable_interface()")
		self.NETSH_CMDLIST.append('interface set interface "%s" ENABLED'%(self.WIN_EXT_DEVICE))
		return self.win_join_netsh_cmd()
	"""

	def win_firewall_modify_rule(self,option):
		try:
			self.debug(text="def win_firewall_modify_rule()")
			if self.NO_WIN_FIREWALL == True:
				return True
			rule_name = "Allow OUT oVPN-IP %s to Port %s Protocol %s" % (self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
			if option == "add":
				rule_string = "advfirewall firewall %s rule name=\"%s\" remoteip=\"%s\" remoteport=\"%s\" protocol=\"%s\" profile=private dir=out action=allow" % (option,rule_name,self.OVPN_CONNECTEDtoIP,self.OVPN_CONNECTEDtoPort,self.OVPN_CONNECTEDtoProtocol)
			if option == "delete":
				rule_string = "advfirewall firewall %s rule name=\"%s\"" % (option,rule_name)
			#self.debug(text="def pfw: %s"%(rule_string))
			self.NETSH_CMDLIST.append(rule_string)
			return self.win_join_netsh_cmd()
		except:
			self.debug(text="def win_firewall_modify_rule: option = '%s' failed" %(option))

	def win_return_netsh_cmd(self,cmd):
		self.debug(text="def win_return_netsh_cmd()")
		if os.path.isfile(self.WIN_NETSH_EXE):
			netshcmd = '%s %s' % (self.WIN_NETSH_EXE,cmd)
			try: 
				read = subprocess.check_output('%s' % (netshcmd),shell=True)
				output = read.strip().decode('cp1258','ignore').strip(' ').split('\r\n')
				#self.debug(text="def win_return_netsh_cmd: output = '%s'" % (output))
				return output
			except:
				self.debug(text="def win_return_netsh_cmd: '%s' failed" % (netshcmd))
		else:
			self.errorquit(text="Error: netsh.exe not found!")

	def win_join_netsh_cmd(self):
		self.debug(text="def win_join_netsh_cmd()")
		if os.path.isfile(self.WIN_NETSH_EXE):
			i=0
			for cmd in self.NETSH_CMDLIST:
				netshcmd = '"%s" %s' % (self.WIN_NETSH_EXE,cmd)
				try: 
					exitcode = subprocess.call('%s' % (netshcmd),shell=True)
					if exitcode == 0:
						self.debug(text="netshOK: '%s': exitcode = %s" % (netshcmd,exitcode))
						i+=1
					else:
						self.debug(text="netshERROR: '%s': exitcode = %s" % (netshcmd,exitcode))
				except:
					self.debug(text="def win_join_netsh_cmd: '%s' failed" % (netshcmd))

			if len(self.NETSH_CMDLIST) == i:
				self.NETSH_CMDLIST = list()
				return True
			else:
				self.NETSH_CMDLIST = list()
				return False
		else:
			self.errorquit(text="Error: netsh.exe not found!")

	def win_return_route_cmd(self,cmd):
		self.debug(text="def win_return_route_cmd()")
		if os.path.isfile(self.WIN_ROUTE_EXE):
			routecmd = '"%s" %s' % (self.WIN_ROUTE_EXE,cmd)
			try: 
				read = subprocess.check_output('%s' % (routecmd),shell=True)
				output = read.strip().decode('cp1258','ignore').strip(' ').split('\r\n')
				#self.debug(text="def win_return_route_cmd: output = '%s'" % (output))
				return output
			except:
				self.debug(text="def win_return_route_cmd: '%s' failed" % (routecmd))
				return False
		else:
			self.errorquit(text="Error: route.exe not found!")

	def win_join_route_cmd(self):
		self.debug(text="def win_join_route_cmd()")
		if os.path.isfile(self.WIN_ROUTE_EXE):
			i=0
			for cmd in self.ROUTE_CMDLIST:
				routecmd = '"%s" %s' % (self.WIN_ROUTE_EXE,cmd)
				try: 
					exitcode = subprocess.call('%s' % (routecmd),shell=True)
					if exitcode == 0:
						self.debug(text="routeOK: '%s': exitcode = %s" % (routecmd,exitcode))
						i+=1
					else:
						self.debug(text="routeERROR: '%s': exitcode = %s" % (routecmd,exitcode))
				except:
					self.debug(text="def win_join_route_cmd: '%s' failed" % (routecmd))

			if len(self.ROUTE_CMDLIST) == i:
				self.ROUTE_CMDLIST = list()
				return True
			else:
				self.ROUTE_CMDLIST = list()
				return False
		else:
			self.errorquit(text="Error: route.exe not found!")

	def win_ipconfig_flushdns(self):
		self.debug(text="def win_ipconfig_flushdns()")
		if os.path.isfile(self.WIN_IPCONFIG_EXE):
			try: 
				cmdstring = '"%s" /flushdns' % (self.WIN_IPCONFIG_EXE)
				exitcode = subprocess.call("%s" % (cmdstring),shell=True)
				if exitcode == 0:
					self.debug(text="%s: exitcode = %s" % (cmdstring,exitcode))
					return True
				else:
					self.debug(text="%s: exitcode = %s" % (cmdstring,exitcode))
			except:
				self.debug(text="def win_join_ipconfig_cmd: '%s' failed" % (cmdstring))
		else:
			self.errorquit(text="def win_ipconfig_flushdns: ipconfig.exe not found!")

	def win_ipconfig_displaydns(self):
		self.debug(text="def win_ipconfig_displaydns()")
		if os.path.isfile(self.WIN_IPCONFIG_EXE):
			try: 
				cmdstring = '"%s" /displaydns' % (self.WIN_IPCONFIG_EXE)
				out = subprocess.check_output("%s" % (cmdstring),shell=True)
				return out
			except:
				self.debug(text="def win_ipconfig_displaydns: failed" % (cmdstring))
		else:
			self.errorquit(text="def win_ipconfig_displaydns: ipconfig.exe not found!")

	def isValueIPv4(self,value):
		#self.debug(text="def isValueIPv4()")
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

	# *** fixme ***
	def isValueIPv6(self,value):
		self.debug(text="def isValueIPv6()")
		return True

	def form_ask_passphrase(self):
		self.debug(text="def form_ask_passphrase()")
		self.destroy_systray_menu()
		try:
			self.dialogWindow_form_ask_passphrase.destroy()
		except:
			pass
		if self.timer_check_certdl_running == False:
			try:
				dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL)
				dialogWindow.set_transient_for(self.window)
				try:
					dialogWindow.set_icon_from_file(self.systray_icon_connected)
				except:
					self.debug(text="def form_ask_passphrase: dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
				text = "Enter your Passphrase"
				dialogWindow.set_title(text)
				dialogWindow.set_markup(text)
				dialogBox = dialogWindow.get_content_area()
				checkbox = Gtk.Switch()
				checkbox_title = Gtk.Label(label="Save Passphrase in File?")
				checkbox.set_active(False)
				ph1Entry = Gtk.Entry()
				ph1Entry.set_visibility(False)
				ph1Entry.set_invisible_char("X")
				ph1Entry.set_size_request(200,24)
				ph1Label = Gtk.Label(label="Passphrase()")
				dialogBox.pack_start(ph1Label,False,False,0)
				dialogBox.pack_start(ph1Entry,False,False,0)
				dialogBox.pack_start(checkbox_title,False,False,0)
				dialogBox.pack_start(checkbox,False,False,0)
				dialogWindow.show_all()
				response = dialogWindow.run()
				self.dialogWindow_form_ask_passphrase = dialogWindow
				ph1 = ph1Entry.get_text().rstrip()
				saveph = checkbox.get_active()
				self.debug(text="checkbox saveph = %s" %(saveph))
				if response == Gtk.ResponseType.CANCEL:
					dialogWindow.destroy()
					print "response: btn cancel %s" % (response)
					self.PASSPHRASE = False
					return False
				elif response == Gtk.ResponseType.OK:
					dialogWindow.destroy()
					if len(ph1) > 0:
						self.PASSPHRASE = ph1
						if self.read_apikey_config():
							if self.compare_confighash():
								self.debug(text="def check_passphrase: self.compare_confighash() :True")
								if saveph == True:
									self.PPP_NO_SAVE = False
									self.write_options_file()
									return True
								else:
									self.PPP_NO_SAVE = True
									self.write_options_file()
									return True
							else:
								self.PASSPHRASE = False
								return False
					else:
						dialogWindow.destroy()
						self.PASSPHRASE = False
						return False
				else:
					self.PASSPHRASE = False
					return False
			except:
				self.debug(text="def form_ask_passphrase: Failed")

	def form_ask_userid(self):
		self.debug(text="def form_ask_userid()")
		try:
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL)
			try:
				dialogWindow.set_icon_from_file(self.systray_icon_connected)
			except:
				self.debug(text="def form_ask_userid: dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
			dialogWindow.set_transient_for(self.window)
			dialogWindow.set_title("oVPN.to Setup")
			dialogWindow.set_markup("Enter your oVPN.to Details")
			dialogBox = dialogWindow.get_content_area()

			useridEntry = Gtk.Entry()
			useridEntry.set_visibility(True)
			useridEntry.set_max_length(9)
			useridEntry.set_size_request(200,24)
			useridLabel = Gtk.Label(label="User-ID:")

			apikeyEntry = Gtk.Entry()
			apikeyEntry.set_visibility(False)
			apikeyEntry.set_max_length(128)
			apikeyEntry.set_invisible_char("*")
			apikeyEntry.set_size_request(200,24)
			apikeyLabel = Gtk.Label(label="API-Key:")

			ph1Entry = Gtk.Entry()
			ph1Entry.set_visibility(False)
			ph1Entry.set_invisible_char("X")
			ph1Entry.set_size_request(200,24)
			ph0Label = Gtk.Label(label="\n\nEnter a secure passphrase to encrypt your API-Login!")
			ph1Label = Gtk.Label(label="Passphrase:")

			ph2Entry = Gtk.Entry()
			ph2Entry.set_visibility(False)
			ph2Entry.set_invisible_char("X")
			ph2Entry.set_size_request(200,24)
			ph2Label = Gtk.Label(label="Repeat:")

			dialogBox.pack_start(useridLabel,False,False,0)
			dialogBox.pack_start(useridEntry,False,False,0)

			dialogBox.pack_start(apikeyLabel,False,False,0)
			dialogBox.pack_start(apikeyEntry,False,False,0)

			dialogBox.pack_start(ph0Label,False,False,0)
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

			if response == Gtk.ResponseType.OK:
				if userid.isdigit() and userid > 1 and len(apikey) == 128 and apikey.isalnum() and ph1 == ph2 and len(ph1) > 0:
					dialogWindow.destroy()
					self.USERID = userid
					self.APIKEY = apikey
					self.PASSPHRASE = ph1
					return True
				else:
					self.form_ask_userid()
		except:
			self.debug(text="def form_ask_userid: Failed")

	def form_reask_userid(self):
		self.debug(text="def form_reask_userid()")
		if self.form_ask_userid():
			if self.write_new_apikey_config():
				if self.check_passphrase():
					return True
		return False

	def cb_interface_selector_changed(self, combobox):
		self.debug(text="def cb_interface_selector_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_EXT_DEVICE = model[index][0]
			self.debug(text="def cb_interface_selector_changed: selected IF = '%s'" % (self.WIN_EXT_DEVICE))
		return

	def cb_select_userid(self, combobox):
		self.debug(text="def cb_select_userid()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1 and model[index][0].isdigit() and model[index][0] > 1:
			self.USERID = model[index][0]
			self.debug(text="def cb_select_userid: selected USERID = '%s'" % (self.USERID))
		return

	def cb_tap_interface_selector_changed(self, combobox):
		self.debug(text="def cb_tap_interface_selector_changed()")
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_TAP_DEVICE = model[index][0]
			self.debug(text="def cb_tap_interface_selector_changed: selected tap IF = '%s'" % (self.WIN_TAP_DEVICE))
		return

	def cb_form_reask_userid(self,widget,event):
		self.debug(text="def cb_form_reask_userid()")
		self.destroy_systray_menu()
		self.PASSPHRASE = False
		self.write_options_file()
		self.form_reask_userid()

	def cb_clear_passphrase_ram(self,widget,event):
		self.debug(text="def cb_clear_passphrase_ram()")
		self.destroy_systray_menu()
		self.PASSPHRASE = False
		self.LOAD_SRVDATA = False
		self.APIKEY = False
		self.CFGSHA = False

	def cb_clear_passphrase_cfg(self,widget,event):
		self.debug(text="def cb_clear_passphrase_cfg()")
		self.destroy_systray_menu()
		self.PASSPHRASE = False
		self.LOAD_SRVDATA = False
		self.APIKEY = False
		self.CFGSHA = False
		self.write_options_file()

	def cb_switch_debug(self,widget,event):
		self.debug(text="def cb_switch_debug()")
		self.destroy_systray_menu()
		if self.DEBUG == False:
			self.DEBUG = True
			self.write_options_file()
			self.msgwarn(text="DEBUG Mode enabled.\nLogfile:\n'%s'" % (self.debug_log))
		else:
			self.DEBUG = False
			self.write_options_file()
			if os.path.isfile(self.debug_log):
				os.remove(self.debug_log)

	def make_confighash(self):
		self.debug(text="def make_confighash()")
		self.text2hash1 = "USERID=%s,APIKEY=%s" % (self.USERID,self.APIKEY)
		self.hash2aes = hashlib.sha256(self.text2hash1).hexdigest()

	def compare_confighash(self):
		self.debug(text="def compare_confighash()")
		self.make_confighash()
		if self.hash2aes == self.CFGSHA:
			#self.debug(text="def compare_confighash :True : self.PASSPHRASE = '%s'" % (self.PASSPHRASE))
			self.debug(text="def compare_confighash :True : self.PASSPHRASE = '-NOT_FALSE-'")
			return True
		else:
			self.PASSPHRASE = False
			return False

	def check_last_server_update(self,remote_lastupdate):
		self.debug(text="def check_last_server_update()")
		if self.LAST_CFG_UPDATE < remote_lastupdate:
			self.remote_lastupdate = remote_lastupdate
			self.debug(text="def check_last_server_update: requesting update")
			return True
		else:
			self.debug(text="def check_last_server_update: no update")
			return False

	def write_last_update(self):
		self.debug(text="def write_last_update()")
		self.LAST_CFG_UPDATE = self.remote_lastupdate
		if self.write_options_file():
			return True

	def reset_last_update(self):
		self.debug(text="def reset_last_update()")
		self.LAST_CFG_UPDATE = 0
		if self.write_options_file():
			return True

	def cb_check_normal_update(self,widget,event):
		self.debug(text="def cb_check_normal_update()")
		self.destroy_systray_menu()
		self.debug(text="def cb_check_normal_update()")
		if self.check_inet_connection() == False:
			self.msgwarn(text="Internet Connection Error!")
			return False
		if self.check_remote_update():
			self.debug(text="def cb_check_normal_update: self.check_remote_update() == True")
			return True

	def cb_force_update(self,widget,event):
		self.debug(text="def cb_force_update()")
		self.destroy_systray_menu()
		if self.check_inet_connection() == False:
			self.msgwarn(text="Internet Connection Error!")
			return False
		if self.reset_last_update():
			self.debug(text="def cb_force_update: self.reset_last_update")
			self.cb_check_normal_update(widget,event)

	def cb_switch_autoupdate(self,widget,event):
		self.debug(text="def cb_switch_autoupdate()")
		self.destroy_systray_menu()
		if self.UPDATEOVPNONSTART == False:
			self.UPDATEOVPNONSTART = True
		else:
			self.UPDATEOVPNONSTART = False
			self.PASSPHRASE = False
		self.write_options_file()

	def cb_resetextif(self,widget,event):
		self.debug(text="def cb_resetextif()")
		self.destroy_systray_menu()
		self.WIN_EXT_DEVICE = False
		self.WIN_TAP_DEVICE = False
		self.WIN_RESET_EXT_DEVICE = True
		self.read_interfaces()
		self.write_options_file()

	def cb_nodnschange(self,widget,event):
		self.debug(text="def cb_nodnschange()")
		self.destroy_systray_menu()
		if self.NO_DNS_CHANGE == False:
			self.win_netsh_restore_dns_from_backup()
			self.NO_DNS_CHANGE = True
		elif self.NO_DNS_CHANGE == True:
			self.NO_DNS_CHANGE = False
		self.write_options_file()

	def cb_extserverview(self,widget,event):
		self.debug(text="def cb_extserverview()")
		self.destroy_systray_menu()
		if self.LOAD_SRVDATA == False:
			if self.check_passphrase() == True:
				self.LOAD_SRVDATA = True
				self.LAST_OVPN_SRV_DATA_UPDATE = 0
				self.debug(text="def cb_extserverview: self.PASSPHRASE = '-NOT_FALSE-'")
		else:
			self.LOAD_SRVDATA = False
			self.OVPN_SRV_DATA = {}
			self.LAST_OVPN_SRV_DATA_UPDATE = 0
		self.write_options_file()
		#self.call_redraw_mainwindow()
		self.destroy_mainwindow()
		self.show_mainwindow(widget,event)

	def cb_change_ipmode1(self,widget,event):
		self.debug(text="def cb_change_ipmode1()")
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		#self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://%s to use any IPv6 options!" % (DOMAIN))
		self.call_redraw_mainwindow()

	def cb_change_ipmode2(self,widget,event):
		self.debug(text="def cb_change_ipmode2()")
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x46"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://%s to use any IPv6 options!" % (DOMAIN))
		self.call_redraw_mainwindow()

	# *** fixme: need isValueIPv6 first! ***
	def cb_change_ipmode3(self,widget,event):
		self.debug(text="def cb_change_ipmode3()")
		return True
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x64"
		self.write_options_file()
		self.read_options_file()
		self.load_ovpn_server()
		self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://%s to use any IPv6 options!" % (DOMAIN))

	def cb_change_fwresetmode(self,widget,event):
		self.debug(text="def cb_change_fwresetmode()")
		self.destroy_systray_menu()
		if self.WIN_RESET_FIREWALL == True:
			self.WIN_RESET_FIREWALL = False
		elif self.WIN_RESET_FIREWALL == False:
			self.WIN_RESET_FIREWALL = True
			if not self.win_firewall_export_on_start():
				self.msgwarn(text="Could not export Windows Firewall Backup!")
		self.write_options_file()

	def cb_change_fwbackupmode(self,widget,event):
		self.debug(text="def cb_change_fwbackupmode()")
		self.destroy_systray_menu()
		if self.WIN_BACKUP_FIREWALL == True:
			self.WIN_BACKUP_FIREWALL = False
		elif self.WIN_BACKUP_FIREWALL == False:
			self.WIN_BACKUP_FIREWALL = True
			if not self.win_firewall_export_on_start():
				self.msgwarn(text="Could not export Windows Firewall Backup!")
		self.write_options_file()

	def cb_change_fwblockonexit(self,widget,event):
		self.debug(text="def cb_change_fwblockonexit()")
		self.destroy_systray_menu()
		if self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
			self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = False
		elif self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == False:
			self.WIN_ALWAYS_BLOCK_FW_ON_EXIT = True
		self.write_options_file()

	def cb_change_fwdontaskonexit(self,widget,event):
		self.debug(text="def cb_change_fwdontaskonexit()")
		self.destroy_systray_menu()
		if self.WIN_DONT_ASK_FW_EXIT == True:
			self.WIN_DONT_ASK_FW_EXIT = False
		elif self.WIN_DONT_ASK_FW_EXIT == False:
			self.WIN_DONT_ASK_FW_EXIT = True
		self.write_options_file()

	def cb_tap_blockoutbound(self,widget,event):
		self.debug(text="def cb_tap_blockoutbound()")
		self.destroy_systray_menu()	
		if self.TAP_BLOCKOUTBOUND == True:
			self.TAP_BLOCKOUTBOUND = False
				
		elif self.TAP_BLOCKOUTBOUND == False:
			self.TAP_BLOCKOUTBOUND = True
			
		if self.win_firewall_tap_blockoutbound():
			self.write_options_file()

	def cb_change_winfirewall(self,widget,event):
		self.debug(text="def cb_change_winfirewall()")
		self.destroy_systray_menu()
		if self.NO_WIN_FIREWALL == True:
			self.NO_WIN_FIREWALL = False
		elif self.NO_WIN_FIREWALL == False:
			self.NO_WIN_FIREWALL = True
		self.write_options_file()
		self.ask_loadorunload_fw()

	def cb_restore_firewallbackup(self,widget,event,file):
		self.debug(text="def cb_restore_firewallbackup()")
		self.destroy_systray_menu()
		fwbak = "%s\\%s" % (self.pfw_dir,file)
		if os.path.isfile(fwbak):
			self.debug(text="def cb_restore_firewallbackup: %s" % (fwbak))
			self.win_firewall_export_on_start()
			self.NETSH_CMDLIST.append('advfirewall import "%s"' % (fwbak))
			return self.win_join_netsh_cmd()

	def cb_switch_accinfo(self,widget,event):
		self.debug(text="def cb_switch_accinfo()")
		self.destroy_systray_menu()
		if self.LOAD_ACCDATA == True:
			self.LOAD_ACCDATA = False
			#self.OVPN_ACC_DATA = {}
			self.LAST_OVPN_ACC_DATA_UPDATE = 0
		elif self.LOAD_ACCDATA == False:
			self.LOAD_ACCDATA = True
			if self.PASSPHRASE == False:
				self.form_ask_passphrase()
			if not self.read_apikey_config():
				self.LOAD_ACCDATA = False
			else:
				self.LAST_OVPN_ACC_DATA_UPDATE = 0
		self.write_options_file()

	def delete_dir(self,path):
		self.debug(text="def delete_dir()")
		if self.OS == "win32":
			string = 'rmdir /S /Q "%s"' % (path)
			#text = "def delete_dir: %s" % (string)
			#self.debug(text=text)
			subprocess.check_output("%s" % (string),shell=True)

	def extract_ovpn(self):
		self.debug(text="def extract_ovpn()")
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

	def API_REQUEST(self,API_ACTION):
		self.debug(text="def API_REQUEST()")
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
		text = "def API_REQUEST: API_ACTION = %s" % (API_ACTION)
		self.debug(text=text)

		try:
			#if self.check_inet_connection() == False:
			#	return False
			r = requests.post(self.APIURL,data=values)
			if API_ACTION == "getconfigs" or API_ACTION == "getcerts":
				self.body = r.content
			else:
				self.body = r.text
			#self.debug(text="def API_REQUEST: response = '%s'" % (self.body))
			if self.body == "wait":
				pass
				#self.set_progressbar(text="Waiting for oVPN Certificates...")

			if self.body.isalnum() and len(self.body) <= 128:
				self.debug("def API_REQUEST: self.body = %s"%(self.body))

		except requests.exceptions.ConnectionError as e:
			text = "def API_REQUEST: requests error on: %s = %s" % (API_ACTION,e)
			#self.set_progressbar(text)
			self.debug(text=text)
			return False
		except:
			self.msgwarn(text="def API_REQUEST: requests error on: %s failed!" % (API_ACTION))
			return False

		if not self.body == False:

			if not self.body == "AUTHERROR":
				self.curldata = self.body.split(":")
				if self.curldata[0] == "AUTHOK":
					self.curldata = self.curldata[1]
					self.debug(text="def API_REQUEST: self.curldata = '%s'" % (self.curldata))
					return True
			else:
				text = "Invalid User-ID / API-Key or Account expired."
				self.body = False
				#self.set_progressbar(text)
				self.timer_check_certdl_running = False
				#self.progressbar.set_fraction(0)
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
		self.debug(text="def check_inet_connection()")
		if not self.try_socket(DOMAIN,443) == True:
			self.debug(text="def check_inet_connection: failed!")
			return False
		return True

	def try_socket(self,host,port):
		self.debug(text="def try_socket()")
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(3)
			result = s.connect_ex((host, port))
			s.close()
		except:
			return False
		if result == 0:
			#self.debug(text="def try_socket: %s:%s True" % (host,port))
			return True

	def check_myip(self):
		#self.debug(text="def check_myip()")
		# *** fixme *** missing ipv6 support
		if self.OVPN_CONFIGVERSION == "23x" or self.OVPN_CONFIGVERSION == "23x46":
			if self.LAST_CHECK_MYIP > int(time.time())-random.randint(120,300) and self.OVPN_PING_LAST > 0:
				return True
			try:
				#self.debug(text="def check_myip: go0")
				url = "http://%s/myip4" % (self.GATEWAY_OVPN_IP4A)
				#self.debug(text="def check_myip: url = %s" % (url))
				t1 = time.time()
				r = requests.get(url,timeout=2)
				t2 = time.time()
				latency = (t2-t1)*1000
				rip = r.content.strip().split()[0]
				if rip == self.OVPN_CONNECTEDtoIP:
					self.debug(text="def check_myip: rip = '%s' (latency = %s ms)" % (rip,latency))
					self.LAST_CHECK_MYIP = int(time.time())
					return True
			except:
				self.debug(text="def check_myip: False")
				return False
		else:
			self.debug(text="def check_myip: invalid self.OVPN_CONFIGVERSION")
			return False

	def load_firewall_backups(self):
		self.debug(text="def load_firewall_backups()")
		try:
			if os.path.exists(self.pfw_dir):
				content = os.listdir(self.pfw_dir)
				self.FIREWALL_BACKUPS = list()
				for file in content:
					if file.endswith('.bak.wfw'):
						filepath = "%s\\%s" % (self.pfw_dir,file)
						self.FIREWALL_BACKUPS.append(file)
		except:
			self.debug(text="def load_firewall_backups: failed")

	def move_configs(self):
		self.debug(text="def move_configs()")
		if os.path.exists(self.vpn_cfgold):
			content = os.listdir(self.vpn_cfgold)
			for file in content:
				if file.endswith('.ovpn.to.ovpn') or file.endswith('.ovpn.to') or file.endswith('.txt') or file.endswith('.log'):
					netshcmd = 'move /Y "%s\\%s" "%s\\"' % (self.vpn_cfgold,file,self.vpn_cfg)
					self.debug(text="def move_configs: '%s'" % netshcmd)
					exitcode = subprocess.call('%s' % (netshcmd),shell=True)
					if exitcode == 0:
						self.debug(text="def move_configs: exitcode = %s" % (exitcode))
					else:
						self.debug(text="def move_configs: exitcode = %s" % (exitcode))

	def load_ovpn_server(self):
		self.debug(text="def load_ovpn_server()")
		try:
			if os.path.exists(self.vpn_cfg):
				content = os.listdir(self.vpn_cfg)
				#self.debug(text="def load_ovpn_server: self.body = %s " % (self.body))
				self.OVPN_SERVER = list()
				self.OVPN_SERVER_INFO = {}
				for file in content:
					if file.endswith('.ovpn.to.ovpn'):
						filepath = "%s\\%s" % (self.vpn_cfg,file)
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
										self.errorquit(text="Could not read Servers Remote-IP:Port from config: %s" % (self.ovpn_server_config_file))

								elif "proto " in line:
									#print line
									try:
										proto = line.split()[1]
										if proto.lower()  == "tcp" or proto.lower() == "udp":
											proto = proto.upper()
											serverinfo.append(proto)
									except:
										self.errorquit(text="Could not read Servers Protocol from config: %s" % (self.ovpn_server_config_file))

								elif line.startswith("cipher "):
									#elif "cipher " in line:
									#print line
									try:
										cipher = line.split()[1]
										serverinfo.append(cipher)
									except:
										self.errorquit(text="Could not read Servers Cipher from config: %s" % (self.ovpn_server_config_file))

								if "fragment " in line or "link-mtu " in line:
									#print line
									try:
										mtu = line.split()[1]
										serverinfo.append(mtu)
									except:
										mtu = 1500
										serverinfo.append(mtu)
										self.debug(text="Could not read mtu from config: %s" % (self.ovpn_server_config_file))
							# end: for line in open(filepath)
							self.OVPN_SERVER_INFO[servershort] = serverinfo
						try:
							flagicon = self.FLAG_IMG[countrycode]
						except:
							imgfile = '%s\\flags\\%s.png' % (self.ico_dir,countrycode)
							if not os.path.isfile(imgfile):
								imgfile = '%s\\flags\\00.png' % (self.ico_dir)
							self.FLAG_IMG[countrycode] = imgfile
						self.OVPN_SERVER.append(servername)
						#self.debug(text="def load_ovpn_server: file = %s " % (file))
				# for end
				self.OVPN_SERVER.sort()
			else:
				self.reset_last_update()
		except:
			self.msgwarn(text="def load_ovpn_server: failed")

	def load_remote_data(self):
		if self.timer_load_remote_data_running == True:
			return False
		self.timer_load_remote_data_running = True
		if self.APIKEY == False or self.PASSPHRASE == False:
			#self.debug(text="def load_remote_data: no api data")
			self.timer_load_remote_data_running = False
			return False
		elif self.STATE_OVPN == True and self.OVPN_CONNECTEDseconds > 0 and self.OVPN_PING_LAST <= 0:
			#self.debug(text="def load_remote_data: waiting for ovpn connection")
			self.timer_load_remote_data_running = False
			return False
		elif self.STATE_OVPN == True and self.OVPN_CONNECTEDseconds > 0 and self.OVPN_PING_LAST > 999:
			#self.debug(text="def load_remote_data: high ping")
			self.timer_load_remote_data_running = False
			return False
		elif self.LOAD_SRVDATA == True and self.LOAD_ACCDATA == True:
			if self.load_serverdata_from_remote() == True:
				self.call_redraw_mainwindow()
			if self.load_accinfo_from_remote() == True:
				self.call_redraw_accwindow()
		elif self.LOAD_SRVDATA == True and self.LOAD_ACCDATA == False:
			if self.load_serverdata_from_remote() == True:
				self.call_redraw_mainwindow()
		elif self.LOAD_SRVDATA == False and self.LOAD_ACCDATA == True:
			if self.load_accinfo_from_remote() == True:
				self.call_redraw_accwindow()
		self.timer_load_remote_data_running = False

	def check_hash_dictdata(self,newdata,olddata):
		self.debug(text="def check_hash_dictdata()")
		try:
			texta = ""
			textb = ""

			for key,value in sorted(newdata.iteritems()):
				texta = "%s %s %s" % (texta,key,value)

			for key,value in sorted(olddata.iteritems()):
				textb = "%s %s %s" % (textb,key,value)

			hasha = hashlib.sha256(texta).hexdigest()
			hashb = hashlib.sha256(textb).hexdigest()

			#self.debug(text="hasha newdata = '%s'" % (hasha))
			#self.debug(text="hashb olddata = '%s'" % (hashb))
			if hasha == hashb:
				return True
		except:
			self.debug(text="def check_hash_dictdata: failed")

	def load_serverdata_from_remote(self):
		updatein = self.LAST_OVPN_SRV_DATA_UPDATE + self.LOAD_DATA_EVERY
		now = int(time.time())
		#self.debug(text="def load_serverdata_from_remote: ?")
		if self.LOAD_SRVDATA == False:
			#self.debug(text="def load_serverdata_from_remote: disabled")
			return False
		elif self.MAINWINDOW_OPEN == False:
			#self.debug(text="def load_remote_data: mainwindow not open")
			return False
		elif updatein > now:
			#self.debug(text="def load_serverdata_from_remote: time = %s update_in = %s" % (now,updatein))
			return False
		elif self.check_inet_connection() == False:
			self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
			self.debug(text="def load_serverdata_from_remote: no inet connection")
			return False
		try:
			API_ACTION = "loadserverdata"
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
			r = requests.post(self.APIURL,data=values,timeout=(3,3))
			self.debug(text="def load_serverdata_from_remote: posted")
			try:
				if not r.content == "AUTHERROR":
					#self.debug(text="r.content = '%s'" % (r.content))
					OVPN_SRV_DATA = json.loads(r.content)
					#self.debug(text="OVPN_SRV_DATA = '%s'" % (OVPN_SRV_DATA))
					if len(OVPN_SRV_DATA) > 1:
						if not self.check_hash_dictdata(OVPN_SRV_DATA,self.OVPN_SRV_DATA):
							self.OVPN_SRV_DATA = OVPN_SRV_DATA
							self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
							self.debug(text="def load_serverdata_from_remote: loaded, len = %s" % (len(self.OVPN_SRV_DATA)))
							return True
						else:
							self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
							self.debug(text="def load_serverdata_from_remote: loaded, hash match")
							return False
					else:
						self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
						self.debug(text="def load_serverdata_from_remote: failed! len = %s"%(len(OVPN_SRV_DATA)))
						return False
				else:
					self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
					self.debug(text="def load_serverdata_from_remote: AUTH ERROR")
					return False
			except:
				self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
				self.debug(text="def load_serverdata_from_remote: json decode error")
				return False
		except:
			self.LAST_OVPN_SRV_DATA_UPDATE = int(time.time())
			self.debug(text="def load_serverdata_from_remote: api request failed")
			return False

	def load_accinfo_from_remote(self):
		updatein = self.LAST_OVPN_ACC_DATA_UPDATE + self.LOAD_DATA_EVERY
		now = int(time.time())
		#self.debug(text="def load_accinfo_from_remote: ?")
		if self.LOAD_ACCDATA == False:
			#self.debug(text="def load_accinfo_from_remote: disabled")
			return False
		elif self.ACCWINDOW_OPEN == False:
			#self.debug(text="def load_remote_data: mainwindow not open")
			return False
		elif updatein > now:
			#self.debug(text="def load_accinfo_from_remote: time = %s update_in = %s" % (now,updatein))
			return False
		elif self.check_inet_connection() == False:
			self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
			self.debug(text="def load_accinfo_from_remote: no inet connection")
			return False
		try:
			API_ACTION = "accinfo"
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }
			r = requests.post(self.APIURL,data=values,timeout=(2,2))
			self.debug(text="def load_accinfo_from_remote: posted")
			try:
				if not r.content == "AUTHERROR":
					#self.debug(text="r.content = '%s'" % (r.content))
					OVPN_ACC_DATA = json.loads(r.content)
					#self.debug(text="OVPN_ACC_DATA = '%s'" % (OVPN_ACC_DATA))
					if len(OVPN_ACC_DATA) > 1:
						if not self.check_hash_dictdata(OVPN_ACC_DATA,self.OVPN_ACC_DATA):
							self.OVPN_ACC_DATA = OVPN_ACC_DATA
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							self.debug(text="def load_accinfo_from_remote: loaded, len = %s"%(len(self.OVPN_ACC_DATA)))
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							return True
						else:
							self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
							self.debug(text="def load_accinfo_from_remote: loaded, hash match")
							return False
					else:
						self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
						self.debug(text="def load_accinfo_from_remote: failed! len = %s"%(len(OVPN_ACC_DATA)))
						return False
				else:
					self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
					self.debug(text="def load_accinfo_from_remote: AUTH ERROR")
					return False
			except:
				self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
				self.debug(text="def load_accinfo_from_remote: json decode error")
				return False
		except:
			self.LAST_OVPN_ACC_DATA_UPDATE = int(time.time())
			self.debug(text="def load_accinfo_from_remote: api request failed")
			return False

	def build_openvpn_dlurl(self):
		self.debug(text="def build_openvpn_dlurl()")
		self.PLATFORM = self.os_platform()
		if self.PLATFORM == "AMD64":
			self.OPENVPN_FILENAME = "openvpn-install-%s-%s-x86_64.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V)
			self.OPENVPN_FILEHASH = self.OVPN_WIN_SHA512_x64
		elif self.PLATFORM == "x86":
			self.OPENVPN_FILENAME = "openvpn-install-%s-%s-i686.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V)
			self.OPENVPN_FILEHASH = self.OVPN_WIN_SHA512_x86
		else:
			self.OPENVPN_DL_URL = False
			self.msgwarn(text="Platform '%s' not supported" % (self.PLATFORM))
			return False
		self.OPENVPN_DL_URL = "%s/%s" % (self.OPENVPN_REM_URL,self.OPENVPN_FILENAME)
		self.OPENVPN_DL_URL_ALT = "%s/%s" % (self.OPENVPN_ALT_URL,self.OPENVPN_FILENAME)
		self.OPENVPN_SAVE_BIN_TO = "%s\\%s" % (self.vpn_dir,self.OPENVPN_FILENAME)
		self.OPENVPN_ASC_FILE = "%s.asc" % (self.OPENVPN_SAVE_BIN_TO)
		#print "def build_openvpn_dlurl: PLATFORM=%s url='%s'" % (self.PLATFORM,self.OPENVPN_DL_URL)
		return True

	def upgrade_openvpn(self):
		self.debug(text="def upgrade_openvpn()")
		if self.load_openvpnbin_from_remote():
			if self.win_install_openvpn():
				self.debug(text="def upgrade_openvpn: self.win_install_openvpn() = True")
				return True
		if self.verify_openvpnbin_dl():
			self.errorquit(text="openVPN Setup downloaded and hash verified OK!\n\nPlease start setup from file:\n'%s'\n\nVerify GPG with:\n'%s'" % (self.OPENVPN_SAVE_BIN_TO,self.OPENVPN_ASC_FILE))
		else:
			self.errorquit(text="openVPN Setup downloaded but hash verify failed!\nPlease install openVPN!\nURL1: %s\nURL2: %s" % (self.OPENVPN_DL_URL,self.OPENVPN_DL_URL_ALT))

	def load_openvpnbin_from_remote(self):
		self.debug(text="def load_openvpnbin_from_remote()")
		if not self.OPENVPN_DL_URL == False:
			if os.path.isfile(self.OPENVPN_SAVE_BIN_TO):
				return self.verify_openvpnbin_dl()
			self.msgwarn(text="Install OpenVPN %s (%s) (%s)\n\nStarting download (~1.8 MB) from:\n'%s'\nto\n'%s'\n\nPlease wait..." % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V,self.PLATFORM,self.OPENVPN_DL_URL,self.OPENVPN_SAVE_BIN_TO))
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

				return self.verify_openvpnbin_dl()
			except:
				self.debug(text="def load_openvpnbin_from_remote: failed")
				return False
		else:
			return False

	def verify_openvpnbin_dl(self):
		self.debug(text="def verify_openvpnbin_dl()")
		if os.path.isfile(self.OPENVPN_SAVE_BIN_TO):
			localhash = self.hash_sha512_file(self.OPENVPN_SAVE_BIN_TO)
			if self.OPENVPN_FILEHASH == localhash:
				self.debug(text="def verify_openvpnbin_dl: file = '%s' localhash = '%s' OK" % (self.OPENVPN_SAVE_BIN_TO,localhash))
				return True
			else:
				self.msgwarn(text="Invalid File hash: %s !\nlocalhash = '%s'\nbut should be = '%s'" % (self.OPENVPN_SAVE_BIN_TO,localhash,self.OPENVPN_FILEHASH))
				try:
					os.remove(self.OPENVPN_SAVE_BIN_TO)
				except:
					self.msgwarn(text="Failed remove file: %s" % (self.OPENVPN_SAVE_BIN_TO))
				return False
		else:
			#self.msgwarn(text="def verify_openvpnbin_dl: file not found '%s'" % (self.OPENVPN_SAVE_BIN_TO))
			return False

	def win_install_openvpn(self):
		self.debug(text="def win_install_openvpn()")
		if self.OPENVPN_SILENT_SETUP == True:
			# silent install
			installtodir = "%s\\runtime" % (self.vpn_dir)
			options = "/S /SELECT_SHORTCUTS=0 /SELECT_OPENVPN=1 /SELECT_SERVICE=0 /SELECT_TAP=1 /SELECT_OPENVPNGUI=0 /SELECT_ASSOCIATIONS=0 /SELECT_OPENSSL_UTILITIES=0 /SELECT_EASYRSA=0 /SELECT_PATH=1"
			parameters = '%s /D=%s' % (options,installtodir)
			netshcmd = '"%s" %s' % (self.OPENVPN_SAVE_BIN_TO,parameters)
			self.debug(text="def win_install_openvpn: silent cmd =\n'%s'" % (netshcmd))
			self.OPENVPN_DIR = installtodir
		else:
			# popup install
			netshcmd = '"%s"' % (self.OPENVPN_SAVE_BIN_TO)

		self.debug(text="def win_install_openvpn: '%s'" % (self.OPENVPN_SAVE_BIN_TO))
		try: 
			exitcode = subprocess.call(netshcmd,shell=True)
			if exitcode == 0:
				if self.OPENVPN_SILENT_SETUP == True:
					self.debug(text="def win_install_openvpn: silent OK!")
				else:
					self.debug(text="def win_install_openvpn:\n\n'%s'\n\nexitcode = %s" % (netshcmd,exitcode))
				return True
			else:
				self.debug(text="def win_install_openvpn: '%s' exitcode = %s" % (netshcmd,exitcode))
				return False
		except:
			self.debug(text="def win_install_openvpn: '%s' failed" % (netshcmd))
			return False

	def win_select_openvpn(self):
		self.debug(text="def win_select_openvpn()")
		self.msgwarn(text="OpenVPN not found!\n\nPlease select openvpn.exe on next window!\n\nIf you did not install openVPN yet: click cancel on next window!")
		dialogWindow = Gtk.FileChooserDialog("Select openvpn.exe or Cancel to install openVPN",None,Gtk.FileChooserAction.OPEN,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
				self.debug(text = "selected: %s" % (self.OPENVPN_EXE))
				return True
			else:
				dialogWindow.destroy()
				self.debug(text = "Closed, no files selected")
				return False
		except:
			return False

	def win_detect_openvpn(self):
		self.debug(text="def win_detect_openvpn()")
		if self.OPENVPN_DIR == False:
			os_programfiles = "PROGRAMFILES PROGRAMFILES(x86) PROGRAMW6432"
			for getenv in os_programfiles.split():
				programfiles = os.getenv(getenv)
				OPENVPN_DIR = "%s\\OpenVPN\\bin" % (programfiles)
				file = "%s\\openvpn.exe" % (OPENVPN_DIR)
				if os.path.isfile(file):
					self.debug(text="def win_detect_openvpn: %s" % (file))
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
			self.msgwarn(text="WARNING! Failed to verify files in\n'%s'\n\nUninstall openVPN and restart oVPN Client Software!\n\nOr install openVPN from URL:\n%s[debug self.LAST_FAILED_CHECKFILE = '%s']" % (self.OPENVPN_DIR,self.OPENVPN_DL_URL,self.LAST_FAILED_CHECKFILE))

		self.debug(text = "def win_detect_openvpn: self.OPENVPN_EXE = '%s'" % (self.OPENVPN_EXE))
		try:
			out, err = subprocess.Popen("\"%s\" --version" % (self.OPENVPN_EXE),shell=True,stdout=subprocess.PIPE).communicate()
		except:
			self.errorquit(text="Could not detect openVPN Version!")
		try:
			self.OVPN_VERSION = out.split('\r\n')[0].split( )[1].replace(".","")
			self.OVPN_BUILT = out.split('\r\n')[0].split("built on ",1)[1].split()
			self.OVPN_LATESTBUILT = self.OVPN_LATEST_BUILT.split()
			self.debug(text="self.OVPN_VERSION = %s, self.OVPN_BUILT = %s, self.OVPN_LATESTBUILT = %s" % (self.OVPN_VERSION,self.OVPN_BUILT,self.OVPN_LATESTBUILT))
			if self.OVPN_VERSION >= self.OVPN_LATEST:
				if self.OVPN_BUILT == self.OVPN_LATESTBUILT:
					self.debug(text="self.OVPN_BUILT == self.OVPN_LATESTBUILT: True")
					return True
				else:
					built_mon = self.OVPN_BUILT[0]
					built_day = int(self.OVPN_BUILT[1])
					built_year = int(self.OVPN_BUILT[2])
					builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
					string_built_time = time.strptime(builtstr,"%b/%d/%Y")
					built_month_int = int(string_built_time.tm_mon)
					built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
					self.debug(text = "openvpn built_timestamp = %s self.OVPN_LATESTBUILT_TIMESTAMP = %s" % (built_timestamp,self.OVPN_LATEST_BUILT_TIMESTAMP))
					if built_timestamp > self.OVPN_LATEST_BUILT_TIMESTAMP:
						self.CHECK_FILEHASHS = False
						return True
			self.upgrade_openvpn()
		except:
			self.errorquit(text="def win_detect_openvpn: failed")

	def openvpn_check_files(self):
		self.debug(text="def openvpn_check_files()")
		try:
			if self.CHECK_FILEHASHS == False:
				return True
			self.OPENVPN_DIR = self.OPENVPN_EXE.rsplit('\\', 1)[0]
			self.debug(text="def openvpn_check_files: self.OPENVPN_DIR = '%s'" % (self.OPENVPN_DIR))
			dir = self.OPENVPN_DIR
			if os.path.exists(dir):
				content = os.listdir(dir)
				filename = self.openvpn_filename_exe()
				hashs = self.OPENVPN_FILEHASHS[filename]
				#self.debug(text="hashs = '%s'" % (hashs))
				for file in content:
					self.LAST_FAILED_CHECKFILE = file
					if file.endswith('.exe') or file.endswith('.dll'):
						filepath = "%s\\%s" % (dir,file)
						hasha = self.hash_sha512_file(filepath)
						hashb = hashs[file]
						if hasha == hashb:
							self.debug(text="def openvpn_check_files: hash '%s' OK!" % (file))
						else:
							self.debug(text="Invalid Hash: '%s'! is '%s' != '%s'" % (filepath,hasha,hashb))
							return False
					else:
						self.debug(text="Invalid content '%s' in '%s'" % (file,self.OPENVPN_DIR))
						return False
				return True
			else:
				self.debug(text="Error: '%s' not found!" % (self.OPENVPN_DIR))
				return False
		except:
			self.debug(text="def openvpn_check_files: failed!")
			return False

	def openvpn_filename_exe(self):
		self.debug(text="def openvpn_filename_exe()")
		if self.PLATFORM == "AMD64":
			arch = "x86_64"
		elif self.PLATFORM == "x86":
			arch = "i686"
		else:
			self.errorquit("arch '%s' not supported!" % (self.PLATFORM))
		self.debug("def openvpn_filename_exe: arch = '%s'" % (arch))
		return "openvpn-install-%s-%s-%s.exe" % (self.OPENVPN_VERSION,self.OPENVPN_BUILT_V,arch)

	def os_platform(self):
		self.debug(text="def os_platform()")
		true_platform = os.environ['PROCESSOR_ARCHITECTURE']
		try:
			true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
		except KeyError:
			pass
			#true_platform not assigned to if this does not exist
		return true_platform

	def check_dns_is_whitelisted(self):
		self.debug(text="def check_dns_is_whitelisted()")
		#if self.GATEWAY_DNS1 == "127.0.0.1" or self.GATEWAY_DNS1 == self.GATEWAY_OVPN_IP4 or self.GATEWAY_DNS1 == "8.8.8.8" or self.GATEWAY_DNS1 == "8.8.4.4" or self.GATEWAY_DNS1 == "208.67.222.222" or self.GATEWAY_DNS1 == "208.67.220.220" or self.GATEWAY_DNS1 in self.d0wns_DNS:
		if self.GATEWAY_DNS1 == "127.0.0.1":
			self.debug(text="def check_dns_is_whitelisted: True")
			return True
		else:
			self.debug(text="def check_dns_is_whitelisted: False")
			return False

	def read_d0wns_dns(self):
		self.debug(text="def read_d0wns_dns()")
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
							self.debug(text="def read_d0wns_dns: offline '%s'" % (name))
						else:
							self.debug(text="def read_d0wns_dns: failed '%s'" % (data))
				self.debug(text="def read_d0wns_dns: True len(self.d0wns_DNS) = %s" % (len(self.d0wns_DNS)))
				return True
			except:
				self.debug(text="def read_d0wns_dns: failed!")

	def check_d0wns_dnscryptports(self,value):
		#self.debug(text="def check_d0wns_dnscryptports()")
		try:
			data = value.split()
			for entry in data:
				entry = int(entry)
				if entry > 0 and entry <= 65535:
					return True
				else:
					self.debug(text="def check_d0wns_dnscryptports: failed value '%s'" % (value))
					return False
			return True
		except:
			return False

	def check_d0wns_names(self,name):
		#self.debug(text="def check_d0wns_names()")
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
					self.debug(text="def check_d0wns_names: name failed value '%s'" % (name))
		except:
			return False

	def check_d0wns_dnscountry(self,value):
		#self.debug(text="def check_d0wns_dnscountry()")
		try:
			if not value.isalnum():
				data = value.split()
				for entry in data:
					if not entry.isalnum():
						self.debug(text="def check_d0wns_dnscountry: '%s' failed" % (value))
						return False
			return True
		except:
			return False

	def check_d0wns_dnscryptfingerprint(self,value):
		#self.debug(text="def check_d0wns_dnscryptfingerprint()")
		try:
			if len(value) == 79:
				for toc in value.split(':'):
					if not len(toc) == 4 or not toc.isalnum():
						self.debug(text="def check_d0wns_dnscryptfingerprint: value = '%s' toc '%s'"%(value,toc))
						return False
				#self.debug(text="def check_d0wns_dnscryptfingerprint: True")
				return True
			else:
				self.debug(text="def check_d0wns_dnscryptfingerprint: len value = %s" % (len(value)))
		except:
			return False

	def load_d0wns_dns_from_remote(self):
		#self.debug(text="def load_d0wns_dns_from_remote()")
		try:
			if not os.path.isfile(self.dns_d0wntxt):
				try:
					url = "https://%s/files/dns/d0wns_dns.txt" % (DOMAIN)
					r = requests.get(url)
					fp = open(self.dns_d0wntxt,'wb')
					fp.write(r.content)
					fp.close()
					self.debug(text="def load_d0wns_dns_from_remote: True")
					return True
				except:
					return False
			else:
				return True
		except:
			return False

	def show_about_dialog(self,widget,event):
		self.debug(text="def show_about_dialog()")
		self.destroy_systray_menu()
		if self.WINDOW_ABOUT_OPEN == True:
			self.about_dialog.destroy()
			return True
		try:
			self.WINDOW_ABOUT_OPEN = True
			self.about_dialog = Gtk.AboutDialog()
			self.about_dialog.set_icon_from_file(self.systray_icon_connected)
			self.about_dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.systray_icon_connected))
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
				self.debug(text="def show_about_dialog: response = '%s'" % (response))
				self.WINDOW_ABOUT_OPEN = False
		except:
			self.debug(text="def show_about_dialog: failed")

	def on_closing(self,widget,event):
		self.debug(text="def on_closing()")
		self.destroy_systray_menu()
		if self.WINDOW_QUIT_OPEN == True:
			self.QUIT_DIALOG.destroy()
			return False
		self.WINDOW_QUIT_OPEN = True
		if self.STATE_OVPN == True:
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
				dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
				dialog.set_title("Quit oVPN.to Client")
				dialog.set_icon_from_file(self.systray_icon_connected)
				dialog.set_transient_for(self.window)
				self.QUIT_DIALOG = dialog
				dialog.set_markup("Do you really want to quit?")
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
			self.debug(text="close app")
			self.stop_systray_timer = True
			self.remove_lock()
			Gtk.main_quit()
			sys.exit()

	def ask_loadorunload_fw(self):
		self.debug(text="def ask_loadorunload_fw()")
		if self.NO_WIN_FIREWALL == True:
			return True
		try:
			if self.WIN_DONT_ASK_FW_EXIT == True:
				if self.WIN_BACKUP_FIREWALL == True and self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
					self.win_firewall_restore_on_exit()
					self.win_firewall_block_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(text="Firewall rules restored and block outbound!")
					return True

				elif self.WIN_BACKUP_FIREWALL == True and self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == False:
					self.win_firewall_restore_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(text="Firewall: rules restored!")
					return True

				elif self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == True:
					self.win_firewall_block_on_exit()
					self.win_netsh_restore_dns_from_backup()
					self.debug(text="Firewall: block outbound!")
					return True

				elif self.WIN_ALWAYS_BLOCK_FW_ON_EXIT == False:
					self.win_firewall_allowout()
					self.win_netsh_restore_dns_from_backup()
					self.debug(text="Firewall: allow outbound!")
					return True
			else:
				try:
					dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
					dialog.set_title("Firewall Settings")
					dialog.set_icon_from_file(self.systray_icon_connected)
					dialog.set_transient_for(self.window)
					if self.WIN_BACKUP_FIREWALL == True:
						text = "Restore previous firewall settings?\n\nPress 'YES' to restore your previous firewall settings!\nPress 'NO' to set profiles to 'blockinbound,blockoutbound'!"
						dialog.set_markup()
					else:
						text = "Allow outgoing connection to internet?\n\nPress 'YES' to set profiles to 'blockinbound,allowoutbound'!\nPress 'NO' to set profiles to 'blockinbound,blockoutbound'!"

					dialog.set_markup(text)
					self.debug(text="def ask_loadorunload_fw: text = '%s'" % (text))
					response = dialog.run()
					self.debug(text="def ask_loadorunload_fw: dialog response = '%s'" % (response))
					if response == Gtk.ResponseType.NO:
						dialog.destroy()
						self.debug(text="def ask_loadorunload_fw: dialog response = NO '%s'" % (response))
						self.win_firewall_block_on_exit()
						self.win_netsh_restore_dns_from_backup()
						return True
					elif response == Gtk.ResponseType.YES:
						dialog.destroy()
						self.debug(text="def ask_loadorunload_fw: dialog response = YES '%s'" % (response))
						if self.WIN_BACKUP_FIREWALL == True:
							self.win_firewall_restore_on_exit()
						else:
							self.win_firewall_allowout()
						self.win_netsh_restore_dns_from_backup()
						return True
					else:
						dialog.destroy()
						self.debug(text="def ask_loadorunload_fw: dialog response = ELSE '%s'" % (response))
						return False
				except:
					self.msgwarn(text="def ask_loadorunload_fw: dialog failed")
					return False
		except:
			self.msgwarn(text="def ask_loadorunload_fw: failed")
			return False

	def remove_lock(self):
		self.debug(text="def remove_lock()")
		if os.path.isfile(self.lock_file):
			self.debug(text="close lock")
			self.LOCK.close()
			try:
				os.remove(self.lock_file)
				self.debug(text="remove lock")
				return True
			except:
				sys.exit()
		else:
			sys.exit()

	def errorquit(self,text):
		if self.DEBUG == False:
			self.DEBUG = True
		text = "errorquit: %s" % (text)
		self.debug(text=text)
		try:
			message = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
			message.set_title("Error")
			message.set_icon_from_file(self.systray_icon_connected)
			message.set_markup("%s"%(text))
			message.run()
			message.destroy()
		except:
			text = "%s failed" % (text)
			self.debug(text=text)
		sys.exit()

	def debug(self,text):
		timefromboot = round(time.time() - self.BOOTTIME,3)
		if self.DEBUGcount > 0 and not self.DEBUGfrombefore == text:
			debugstringsht1 = "(%s):(d1) %s (repeat: %s)" % (timefromboot, self.DEBUGfrombefore,self.DEBUGcount)
			debugstringsht2 = "(%s):(d2) %s" % (timefromboot,text)
			print(debugstringsht1)
			print(debugstringsht2)
			self.DEBUGcount = 0
		elif self.DEBUGcount >= 4096 and self.DEBUGfrombefore == text:
			debugstringsht = "(%s):(d3) %s (repeated: %s e2)" % (timefromboot, self.DEBUGfrombefore,self.DEBUGcount)
			print(debugstringsht)
			self.DEBUGcount = 0
		elif self.DEBUGfrombefore == text:
			self.DEBUGcount += 1
			return
		elif not self.DEBUGfrombefore == text:
			debugstringsht = "(%s):(d4) %s"%(timefromboot,text)
			print(debugstringsht)
		self.DEBUGfrombefore = text
		if self.DEBUG == True:
			if not self.debug_log == False:
				try:
					localtime = time.asctime(time.localtime(time.time()))
					debugstringlog = "%s (%s):(d5) %s"%(localtime,timefromboot,text)
					try:
						debugstringlog = localtime+" "+debugstringsht1+"\n"+debugstringlog
					except:
						pass
					if len(text) > 1:
						dbg = open(self.debug_log,'a')
						dbg.write("%s\n" % (debugstringlog))
						dbg.close()
					return True
				except:
					print("Write to %s failed"%(self.debug_log))

	def init_localization(self):
		return
		loc = locale.getdefaultlocale()[0][0:2]
		filename = "locale/messages_%s.mo" % loc
		try:
			translation = gettext.GNUTranslations(open(filename, "rb"))
		except IOError:
			translation = gettext.NullTranslations()
			#print "Language file for %s not found" % loc
		translation.install()

	def msgwarn(self,text):
		if self.DEBUG == False:
			self.DEBUG = True
		try:
			self.debug(text=text)
			dialogWindow = Gtk.MessageDialog(type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
			dialogWindow.set_title("Info")
			dialogWindow.set_transient_for(self.window)
			try:
				dialogWindow.set_icon_from_file(self.systray_icon_connected)
			except:
				self.debug(text="def msgwarn: dialogWindow.set_icon_from_file(self.systray_icon_connected) failed")
			dialogWindow.set_markup("%s"%(text))
			dialogWindow.run()
			dialogWindow.destroy()
		except:
			self.debug(text=text)

def app():
	Systray()
	Gtk.main()

if __name__ == "__main__":
	app()
