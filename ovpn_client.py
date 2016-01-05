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
import requests
import json
from ConfigParser import SafeConfigParser


CLIENTVERSION="v0.3.6-gtk"

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
		if self.preboot_check():
			self.tray = gtk.StatusIcon()
			self.tray.set_from_stock(gtk.STOCK_PROPERTIES)
			self.tray.connect('popup-menu', self.on_right_click)
			self.tray.connect('activate', self.on_left_click)
			self.tray.set_tooltip(('oVPN.to Client'))			
			if self.UPDATEOVPNONSTART == True and self.OVPN_AUTO_CONNECT_ON_START == False:
				self.check_remote_update()
			self.systray_timer()
		else:
			sys.exit()
		

	def self_vars(self):
		self.MAINWINDOW_OPEN = False
		self.debug_log = False
		self.OVPN_LATEST = 239
		self.OVPN_LATEST_BUILT = "Dec 16 2015"
		self.OVPN_LATEST_BUILT_TIMESTAMP = 1450220400
		self.OVPN_DL_URL = False
		self.OVPN_WIN_DL_URL_x86 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.9-I601-i686.exe"
		self.OVPN_WIN_DLHASH_x86 = ".."
		self.OVPN_WIN_DL_URL_x64 = "https://swupdate.openvpn.net/community/releases/openvpn-install-2.3.9-I601-x86_64.exe"
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
		self.STATE_OVPN = False
		self.GATEWAY_LOCAL = False
		self.GATEWAY_DNS1 = False
		self.GATEWAY_DNS2 = False
		self.WIN_TAP_DEVICE = False
		self.WIN_TAP_DEVS = list()
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
		self.OVPN_GATEWAY_IP4 = "172.16.32.1"
		self.OVPN_THREADID = False
		self.OVPN_RECONNECT_NOW = False
		self.OVPN_CONFIGVERSION = "23x"
		
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
		self.ENABLE_statusbar_text = True
		
		self.FLAG_IMG = {}
		self.FLAG_HASHS = {'ad.png':'8adee4d665c8119ec4f5ad5c43a9a85450e0001c275b6a0ee178ffbf95c4c043','ae.png':'6f20d866841c4514782a46142df22b70b8da9783c513e3d41d8f3313483fe38d','af.png':'c1054fb8d9595948aa96bc57c9ab6fb6b3770d2ee7e09ba7e46b09b21bf51bcd','ag.png':'0dfb5c39e2a3eebe18b431cf41c8c892ab5f1249caa09d43fa1dd7394d486cd7','ai.png':'721542818b00e197fea04303b0afc24763017c14b8cd791dfaf08411d9a99cae','al.png':'3f7278c0c4272b6ff65293c18cdbb7e2e272f59dabe16619c22051d319ef44e0','am.png':'e34d4e7961e7e994775dddfa994e4d9f709876634d36facff6bac70155597c23','an.png':'4c9bd8548dfa58fdf9e6ac703f94c8b96d8136c42b06fbdc8e2d8817e592ffde','ao.png':'49b0a50005440417bd679d03d4d78f9ba0d1c457285c97e94f36e56b1e8b623b','ar.png':'776fbb0600f99ccdc44e2ee7f8b6559988c443f3a754792585b1b7008aaedb91','as.png':'3ef7f1b82b2f28cae0c7df163c5ce9227ef37244da85118374869fc5f2e05868','at.png':'a3acc39d4b61f9cc1056c19176d1559f0dacbb0587a700afdbe4d881040ccd52','au.png':'a7f9683bc4240ef940ee3d4aaf127515add30d25b0b2179a6cdec23944635603','aw.png':'2dc58a1fcd65957140fa06ba9b2f1bd1b3643724cef0905e23e1561a5b3dfa5b','ax.png':'3f38a42fd54e4c7cb1154026f734bc444f9cc942b8b91f099cc65dccf6c7f431','az.png':'45da74f4c8a50cfc13ff612e9052a7df77fae155e20c2b67ec34c4e3d46dcebe','ba.png':'8aab9c83759b1a121043ae5526d7bd4174d6612c7d0c697609731e9f7b819b6b','bb.png':'93977880a9ae72940ed7560758b51a1ba32d27aa5fd2ad5ca38d86fe10061c1a','bd.png':'174d63b291981bb85bc6e90975b23dfd0538a28af9cd99e3530d750dfedf1807','be.png':'45f75a63fadde9018fa5698884c7fb0b2788e8f72ee1f405698b872d59674262','bf.png':'9069275d6c18aaf67463b1fffb7cdefe10da76cd955ee2c5022cff06efa241f2','bg.png':'c4838a24ad388f934b04dbf9dba02a8bc6e9e58d0a1076477b47b5987a5c2d64','bh.png':'d8dfd5dc5157e30aa9e241e4a7d13513dedf608045b6736716ea6c5ca4047855','bi.png':'f2489dfb66723f8585830a51ec1ff4f5a514f5b6fd8bfa423e2880118e18ba75','bj.png':'3eb78453cea7aac6afca9a54ec8a2b0d4998df40a0c5494534992fc38f5c2402','bm.png':'e8087faf03f478266cc279382009391155615af6a7f3eaa47b21717ce8eaa401','bn.png':'05a6a5da710bdd98eb1d8c9b097b687a34ace268e106bd3437298d0ffc8a7473','bo.png':'a802b4b4b31e9c87062e725760b052083ca0d2cc2cced10f44731688289c4ca5','br.png':'dff6f4d907290bdbe74812bf73b590f268694e0a30e64b4bb24b803a47b3e319','bs.png':'aabf518642010552de4ed24400d5d40fa7e6bf1142a183f4989dad88d7cede5e','bt.png':'ae10dea2abad314551038e08771857c6d67d3684487782275c094dab5dfda21e','bv.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','bw.png':'166ffee51259387356bdadeb22cdc7d053fc89ef6f51ae3c774d522a4dfaf08e','by.png':'cc2b61fff898086df311b22f06fcb400e64c4627ef8495755b24e2f7f3e05429','bz.png':'f7ca75c8e16fb2a11cb30d9f9e7006505a719601b84a6135f478f62a7ff214f1','ca.png':'3a6c5facc8613948b81833101a2ff8c3a114813ce24077585faee268b8ffb541','catalonia.png':'58665da49b1ebca85993de6e799f423b4589359b2eb43cb6b8bb81223fc02b10','cc.png':'25d60905c65429304e895c47dfb9da424190d9be01d924b75cc5cb76a1bdf39c','cd.png':'d26464766b63c4c361821355ca7a36ef288ef72fd6bad23421c695e1dd527743','cf.png':'a476f7f6228a456d767f2f97b73b736cee01a64f0acdac1d0721dcd609476e8a','cg.png':'9b8814baab3cff79d037ee1cf49ecd8993d95169d4d8090d9a7d0eccf18d26fd','_ch.png':'da8c749e3f0119f91875ddaa116f265d440150c8f647dd3f634a0eb0b474e2c9','ch.png':'1a847144ea964355e4abd101179c374d3fd6c7c75f1ad58ca2d3b0946a1cd40f','ci.png':'4a5179c7a54ce4395781fbb535bbffb03b4bdbd56046f9209d4f415b1ad5b19c','ck.png':'38d9b787d10aafadd8aa1deeae343dff8fee30d230d86dfab14df9002dfecb01','cl.png':'516cde928be7cf45bedd28cb9bed291035aa9106a21335a922ca1e0987a8fdb6','cm.png':'3e785d74c3a21a99972a38b021eb475d99940239bc0bc1a4020bc77a9ecf70e1','cn.png':'7058233b5bdfdd4279e92e9dfe64bd4a61afd7e76d97dba498ce1d5777b92185','co.png':'ddbda18a0e3a272e63f2a3e734893bd848fceb76855057ad263823edbb4ca4df','cr.png':'f22dbafc8eaee237cac9a35777e98818868e2e87e47b640bbf4c487afc10b07e','cs.png':'3fe11c2a0b4c2b50035c224d2e6c87ba19a05663811c459d4e3a2f780aede957','cu.png':'9fc72810592496349d14e13a4c5b61b8cae7388be4d5d395ac2bf99d2f3ed4fa','cv.png':'22650dac4b404ca32e73fe64df90e21a955ec8f67a3dc2ef50135d342143dabb','cx.png':'8dc0ef0ae06c717937acbf0bafd947cc9a0c9984bd6839bc6ba22c82857acd43','cy.png':'bd7198c76594a6ed1147412a4e37d1ae258d1fd9358d96ded9b524dbeea7bc30','cz.png':'0f39366d88fabe6f6f5c7a3cb6a11165de6bc6bc2108802c49df5f9840bc6541','de.png':'3323814006fe6739493d27057954941830b59eff37ebaac994310e17c522dd57','dj.png':'4be41bfd725282adc410a23488c290028b8a433e614dffaa49d0cb28d6bbb39f','dk.png':'0c9213be3a5cbc5d656093ca415d2b9f52de067d8ed5d7cfd704ce8cd0564d2c','dm.png':'c91813a9d0753c4f99503e7123c1b40b2c805ae36128afb9eb6384c275c38195','do.png':'505c31334e03e2280f5fe3ebbbc210f71f5ee7242c9021c3d5727ec4114b5b68','dz.png':'f2ea00daa66609ba95a18dac13f3ba0a3d2522f8edbcd109e5fd25fcf1289591','ec.png':'ab0ecc4936f0623e3e298ee6f45d88d208e13b72453ec1bbe2be0abdbefeabbb','ee.png':'6ebe8f7e33db530652a0b1c6394ec4f50a2fcc0b4a31d1ab33db65d6815dd087','eg.png':'e4c44b7ce8a72720e2ab8b38b8885fca36dda04daa14ae37909bbd501d853074','eh.png':'61eda51aebe540c16219767b5c8e64b821d6f857832d8594086fb871c817fd19','england.png':'24c0c0d1e833516a54d890cb63adcd6acbb40c14eac80e5bcd07d92df9ff4cfb','er.png':'cabe5eaa395a681fd51029ef603449bf31914b934f9aaa73486ca55ec77c31ba','es.png':'e9aa6fcf5e814e25b7462ed594643e25979cf9c04f3a68197b5755b476ac38a7','et.png':'69975a423a5a5eb1cc33c554756b6d97e9f52f8253f818a9190db1784e55558f','europeanunion.png':'75bd9bf0f8d27cff7b8005c1a1808d75923ab1ee606f7220b4b35616e3e5a8ad','fam.png':'dec6c95977d90a7e468b2b823d74cd92a79ba623ac3705028eeaf3669ba98906','fi.png':'543f426fb35ad2c761641a67977c8faf0d940d4054d0dc1d7433987ebc3aa181','fj.png':'bc4f5f74e61dfe349dcbc110cfcb0342d0adb0c052652831f3995dfa63bb9b70','fk.png':'e0bd7b739e42aeaac268f77133fc70a228e115553662811c015d2e082da054d6','fm.png':'8c115aeccde699d03d5124eb30f853129cde0f03e94e9d255eda0eae9ea58c28','fo.png':'5b9e9e43b1f7969c97a72b65de12afd2429e83d1e644fc21eca48b59a489d82a','fr.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','ga.png':'78565ad916ce1cf8580860cff6184756cf9fbf08f80d04197f567a8f181f9a4b','gb.png':'5d72c5a8bef80fca6f99f476e15ec95ce2d5e5f65c6dab9ee8e56348be0d39fc','gd.png':'859d360193bdc3118b13ded0bc1fe9356deb442090daa91f700267035e9dfecc','ge.png':'a911818976d012613a3cd0afa6f8e996cdffc3a32ba82d88899e69fbc55f67be','gf.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','gh.png':'375fa90eeba5f017b1bfa833e8b9257cde8a0d9f23f668fd508952278b096f22','gi.png':'e86dcc7ad5556b7202d34b1cbac72e3bb0b97b19fc43919ac7321da94a8f3973','gl.png':'2ef3adddb67b87cd2f61652cc6c807556bce0b63433958cc8ad49b8a3b4ff0ae','gm.png':'8f4511b0ca233ebe65e9c435b0d620a58bc607700469c9b4ea446d2b5db79952','gn.png':'a6216497c02291a2ea9b2a04d111362fd44f60e754ff74c81561ee730922dc98','gp.png':'6731b1de195ee6d2f1591c37bb86bc5806a43d559e881ab71f11628852388add','gq.png':'a15608299afdeed2939b687d4bee10e9440395f61d69e402c37a81b4f34bc6ef','gr.png':'5648d2078756ae0b084312c46b02d82905cd9fb84262267cafcf9b71828ac358','gs.png':'1f9d0507de88efae157e75f35c25265f5d9d3f06579178fccbbf50987029c93f','gt.png':'0be4d466871ec85bb3892855ae498b2a78e8fca992024ec7efcc119d08b1a844','gu.png':'b7114f95668c77e6293cb3138bf908989089179c37501a70fdc49eedb73c3d45','gw.png':'720539b86c555880637aef705aff4a2c5497a4b5efd633c1835371aee5d6a7ad','gy.png':'b09eae1eaca0581c47b0064825061e3939ee8a938c4c51d004b0868372f13413','hk.png':'21a3c54b0f51243f34747eeb2feb2b2627c29133e6e3a8a1126b7bda81708dab','hm.png':'a7f9683bc4240ef940ee3d4aaf127515add30d25b0b2179a6cdec23944635603','hn.png':'feb47c8bef0dde53d8f4596fe4791d21a8d0ea060aa5b44e1d16d2583cac63e1','hr.png':'b4d87ecdeef29042f05b26ad81fbfece47292270eb0cfb10ab132f18c3ce98cd','ht.png':'4b60e9e656f44feb7b97a0adac55107fe043fbbc0407950e283451d21d2a9050','hu.png':'61a2cecf8326a8da732499312a098f89d050d13546f6204e6204de38c550437e','id.png':'1f85c9e9a1a0def09db35b63b9aae2a3c4f92202d701322621c8cfddf8880162','ie.png':'c04b1e73243fab30031bcd1b13bbe6ffe5e0e931d2125a6312e239056a972cb4','il.png':'5432e244f03e3973153451b1ec88d649459580eab66e2df936fe2f70f2fed823','in.png':'0aa7543328f3fddde96ab8fc7e3a8b85732de57de6e84447b22964971f399f28','io.png':'00653024642da7ae95c9b56770c878d482cce1bfa7478d41e9f15abc61e1c46c','iq.png':'abf11b67187d489d9321ca074a83bf613b08cf9a9de9565fd923088e51096ab7','ir.png':'2354a8a69f05bf7b0fcfc5ed2f89facd8bd1d692d34513acc066103417783c44','is.png':'82327740504dcaa478299427e9f66903b832b684283e7493d68bfe4808727798','it.png':'c7992f57d67156f994a38c6bb4ec72fa57601a284558db5e065c02dc36ee9d8c','jm.png':'92244b267742bbbfbce7f548d5bd5e75449ee446f53032ab3bef03e53ec7fda1','jo.png':'d5d3b3c24da6db1b1cb098da2f8216aab85a2ba04d2088ad97495bbbb3b99da4','jp.png':'5efce88ac7228ea159bcf7fd1cc56d73c19428394218706524bac0e9151d4c61','ke.png':'38512a3038a8e8f4032aa627157463a0fe942f948159beadbd5c10974ae86a82','kg.png':'98caea2321d6742c57073d56ec0135a7c8bb97e65b9fd062a78c11f42a502e38','kh.png':'5d8706b032eba89228abe0180923cbe1445a27dbb8126b340a9fa4a0ca41827e','ki.png':'652161e3308e25802890895e4bbed778493ec36ced3fa740d8fd83b495f620d0','km.png':'569e0181ef9ac05189ba2a88ebe1de0b2763ba54f737a8251d74b5a94609c2d6','kn.png':'1729d04153ae46884480bc9f995f0852915159e1a0e9c47fac199316ebce1353','kp.png':'6bb1d910ab5186e0cf5518492442f6231470920e22250ad48a27a520b1d376e0','kr.png':'6fdd24bd96b3a482bc058d5c9bcfd6f1c664d91bbd47658d65ac5d852535f7fd','kw.png':'345630ebda3d8a5798bc5447ba38c694921596981289b6c494cab31d5c43e350','ky.png':'c6fe83ab80ec3c1af2e81b2409673af43a0a610eecc0f2e8233d2f3886a48255','kz.png':'b639f1e1e00cf0973f7feaf673326300e13de6e830aad5eb08937bf56ee77c3b','la.png':'d56dc25b3ef4af93f12db2b58b72c293e85da54d8615dae008290a73bdb6d0bd','lb.png':'24efc04e761e01ac6c0aea8941bce30038fe3af40eef643c2cb9f96d1efa0230','lc.png':'fc9572f63afedd18082ff89cc8e9c2b51abbf09610a381939672b763da655f31','li.png':'1235def1c1d682ce8a6c0ec7e569972cd27c70f1c72fb0f2c1ba651895af8eaa','lk.png':'2ea160f5aa9c7155d9b0a15029afe24e4309294b3b61fab6f79442481c6f3c53','lr.png':'008caee046d6d14e91edebcb74343133c4592a2a636f53535c01acbb1757f5ea','ls.png':'a9117dc093a45c55b48faa85495b8e91c4b1bf8ac52ca9e791efe329bd297aa9','lt.png':'23ddd0c23304f715e7c5e47f893afbc827a3504ec6f6f828b4d0beb93eafbd62','lu.png':'6f5ef26b9bebad3c5c6572533d23761e2afa46372a9b350bd08214abda19ada4','lv.png':'0153d9f72dcd5563daedd27f7e0407aee3f39fef74e8d75951777da986e05257','ly.png':'75bfedebfb9cc57d3ed2a6fc640c7540195604bacbd8cc8301b3a053deed199a','ma.png':'61b4918e0904f58a113f7132366b1ad9d458dc5311c505f3b9b94b8458620ee2','mc.png':'d29f945dba8413eb510d42b8b4bfe4e2bdf2bd81158254c4279d056cb0d4b5e2','md.png':'0b4e15588de7b1370b9aedb0cd642b53ecb5352bce6c646e06634c79cecf787e','me.png':'3081af04bbaf03a33b15a177af37f0e46ffdc09469bdd3200795f52626a6d693','mg.png':'cde4f13166c5a8ca794977b62911e567cdf7bb6b420c934f0c5b284df81c25c2','mh.png':'2c90e947b0b12087942c92d69afb98af57e6de1e5acb2059854d91817c3b2176','mk.png':'3c47fe838cab9f56788986f6d46b0b57bcc31b7e7365f6d152bd33dd8c57c48c','ml.png':'b0a3a403ea590be753788de634af4c557d05ae4d2b99e739953208d24eb2b1ac','mm.png':'ecb1de767e97ae04cc8fc646f0a533069bb6f5e87e67c8cff13fc8c88799d6a9','mn.png':'c6e6741d6773b599129eb5ead073d8cd5c59386aab87e80f2e7d0b9ffe2ae505','mo.png':'679136a489c373c80a4b8777411af88256904fdb276e8a15885f5f52baca1dbc','mp.png':'604d309375c31da91dce706037f4b3f1047fd04e82eedacc9d804f4abbaa70e2','mq.png':'990809b24a79d60ddf9c22d555f4c99ca53a2a06773e0da2db4905aa35104056','mr.png':'a74f38227aec752324c052e9dd1851122748801ccec7aef5ecfbaa0f94390e8c','ms.png':'31947948b6ba38909344a0a095c1b20dbc3532a8694c4c98b0d065976c172280','mt.png':'a20c8a35e42004c904e1a06115a9657b170d8090ebe26e96592139e1c8a9e358','mu.png':'5af9de01b0475f0f9e7ed942d4196de6e6ee018a2f24a5162e3dcb833e5cd3d4','mv.png':'d95a38f3825323e8bc65bbe40bc0092c569bd8835ecf5ec7c15d2446bb2fb7c8','mw.png':'be1c170846c234e90ad8b4000ee3ad324d524d8b31e7701540a8cd69f0666db7','mx.png':'656fb035a56a50a6431312527b106f65c7e03bb8711778018c8dc466d1d445ee','my.png':'1e7866925f0e0d350f2c74aa8ac3542be6e90b3c2be3c7f6b1ba0b641b53de9d','mz.png':'a421c9817192c8297e62b03d45309aea3672c8f5574443bab798822f4e5815a1','na.png':'b8dfe39c1ebe4ba174840ba7170a160a48f2b334ee84ea4f39d894a6e54c19ec','nc.png':'34268f88af259368d197e0cdc5448ee6d292704f37794cf1a2e65ff8643f6161','ne.png':'d9bfbea18ec6b302dc3903f8b2e68e15354b6568a39c2f9e38b1c14f910ce225','nf.png':'28a73055985dd55360513b5d178b6b722ce9000c9ee367cbe61d8bb717928501','ng.png':'4c4996cf57a4843fde19bd8b0daf0bde0c471fbd41e0a64ecf45fbab2dfefdfd','ni.png':'8054835206a359ca1b9cae507439a088fb33834c8daabb3f336bf4004abc2aeb','nl.png':'1546928846ee0a8377fd30865d4c43cef501eba7d775d494b98d1ce699627a4a','no.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','np.png':'1e5b552bdfe4c2663f4e287c49d8a57a561c97d497f56212aab6782e942b3240','nr.png':'58d723462b9d68ae1293bb40f72d4a3006fc0f4b0eb96ec08c30c6d07cbc8d69','nu.png':'7dfe8222c16cc1070beb9fa11b6c969ffc6f7482832288950270a125bb774e50','nz.png':'095ebba705ab72032d0c17ca3936f7012a404a778a23a685c2cf943f22d9880e','om.png':'59509c4182f08201f20fb0039ba9477dfa3b3028ae602056f86a9cc982f0ff9f','pa.png':'48fc49c3010bd1530dd86066a61d5a9addadbf31e021c928da9da0cfa0d165f3','pe.png':'aa9ecf69a7d07664c50371368d4b6ab9e1f7f2dc31e0ef3693d8ff2cbab7427a','pf.png':'8346bfd255be99c8bdea0e4f8d6039ac824d4a85c4a974b0cfec245eb9c58318','pg.png':'04cd8be0fbd25ccd8017fb3d9a0a2b511adc215a168dbfe671386ce6a783c802','ph.png':'609f7123d9d23ec401c90b88f677a19125ca24e2899ebe1f3c75598623fdd251','pk.png':'19851391a22a4eee0c6a3bc4b9dec8ec2ee15d0133a8f7c8844f599c261219fb','pl.png':'34f6a1822d880608e7124d2ea0e3da4cd9b3a3b3b7d18171b61031cedbe6e72f','pm.png':'f007111a5672954f4b499ef9bae12bd9e741b7084bbe3c55bea6fd651ee61a27','pn.png':'a02a747916b3a5ed5283b6261258906408ef112351512627db0f2dda57b686cc','pr.png':'4fdcbf2a4a9ca30c22451dca2582c65c473889f75c78d2e6e1253aae82ac1d1a','ps.png':'e53ff276a447b9962ce84b38926dd1f088d6db653f8e936b5c19bfb4584aa688','pt.png':'ba636f1cb6bfd323dac1fb079cd002b5d486ed5eff54f4c4744b81316b257e96','pw.png':'ef5cee4b6289acfae6721efa130076f096d6a3481acad71178016416b17b6b29','py.png':'bd60963b2eb84d58eb01e118a2d0ba5453c717e8564a8fdb4aa10dd6b6473044','qa.png':'140a569d8ed63a59005323a6e06b704a908741c17e0b46b191b2316e2a62e1f7','re.png':'79a39793efbf8217efbbc840e1b2041fe995363a5f12f0c01dd4d1462e5eb842','ro.png':'0f83abcca7f07368819e3268d42f161edabcee4b56329c67de93779c1fba3ec5','rs.png':'a00b9d05c78c62b3eaee82acb12c2d39cc8f63381ee3563b6b8fc6c285dd4efc','ru.png':'c6e9489e25e7854a58db93acc5a91b3cc023d33a70c4931dce8d2ef2868b5e94','rw.png':'9e0e80b9ec85c4066624ea17a501b0ceeed5353dc27cf956203ab8254263e381','sa.png':'8a82f9366b0218584e72ba24eefdbf0f9dd6030480219e39f13cf1e7fe87a03a','sb.png':'6d4a0283689892275b974704a1b87e65a67af641d8b7034a661b4dbb91bd8416','scotland.png':'500ffdc39a41504133171107588f13ad7a7ebce53fc28b423fa45e3e80f27ce9','sc.png':'ca20860642968fd26776098e80b113d8b9a1d48360837ed8ded94d65b0dc9abf','sd.png':'e0cbd1960cc662ea059c0438b92449a25b6753fada4734875545ba0f79098ce2','se.png':'dc67a89a0d57005dad961a1213206395e0dfd8c7825249a0611e140bf211e323','sg.png':'84684a25002cca288c03df18dc0b2636e38a36dfdcb3d1a7a654aad1009efb17','sh.png':'6a95c6905aa2fc09fe242e417d82b12350c048f606337e1d2cc31e38579c8b88','si.png':'a2eb02e5ee0cdfb2911e2ae65cb45e070e116cd9c471422e62c9710246fe7209','sj.png':'f8dc302371c809ebda3e9183c606264601f8dd851d2b1878fd25f0f6abe2988c','sk.png':'dfad70c1a7d2e9aca6c8e11a5a61b16e5f6ce8bf5a28d4b47c479189ace5ffba','sl.png':'0532248fc289611fe2255aa94cbed9de496f9fcd144eee6fcedd2a1eb25ee554','sm.png':'9510efe392a1a661b235c71faaed1f58730b42472caa0f73a7853b1e10d584d5','sn.png':'cbef42bf392f983769bebb6f52b15b2468b633ecdac03204b492fefb694c6d95','so.png':'c1ee2a03d7d92ed81609c610f6bb8b1c211e4da3018162dff14cee0d96c65451','sr.png':'f24fdccbff3e936cbebd5a2beebc30a44cdca6ad85e77ce733009ca88b64fc34','st.png':'356b2af9a06d0db9b05f04c528cf7ccfca73090b29148090ca227f53611d8fba','sv.png':'9722f682cdac58479490bd4ad3e2988aaf69fff9f73c4795f586fd6537cc97af','sy.png':'24c2811e92c20a88522cd9872020bdce2f882d6718962eac26f5fb4c97e14ded','sz.png':'3af4d71e471cbd7d856300a36ee6cde5fc4d29e647f90cb934b0e6f82ffdc1fb','tc.png':'fcac6aff645d8048d395b4a1e0f418be4d823c51525ecbec1d6622e72de9620a','td.png':'2a2e1bd51f95d45678decd51701d3542673f9263fac5bd8d09fe6c70daf69511','tf.png':'8c8d63683cc5ba2b8533f6a7db65cac7b137e5957d37df734e96634ccd0cf2e3','tg.png':'95a500c7fb39f20d5c2687e174626c8cad7969389437feb825257e6cce3cd833','th.png':'9301b5300fa18b50f774512c3549ded45bf41c30359d1824ced7cca0cc75e216','tj.png':'776630c76b77c04a84aa0edb87decb646643c53d519949df2113a5cac4592095','tk.png':'64d2bb4ebc19d7ce6b32a640ef6831c0f3587c54686e3780e5736108b24bcc12','tl.png':'ca5fb285fc6b36cd5d03290983b96d029b0d584a6c03725728a2435969df2636','tm.png':'5012ff744573ece2ed5e8f6aeb6de891bae03a21700141511173d0a9d35a4237','tn.png':'fbf8002c6785f2bc3a7b1074b1b08d6fa96033b3a58f6e362e90e76162064c83','to.png':'f045097a337487211f80bfeaa3391aac99a5b54950380bd32c3d1c96b512f0c8','tr.png':'292d592f7fa1df2fa653ecc1e03d5eb2ae68277c6df264f762aefb8218e23454','tt.png':'393ae78c5cdf66036d404f65822a90abc168672d0a1c5093e4259ce1606e7298','tv.png':'81770d0d4d6ee76a8286becd00d111ea1ffd3220267651f95f559898f76b8d58','tw.png':'e59c331045b010a83f46ad25c592cf3f5415271b612fc9db8d32cf9158447dc6','tz.png':'4bf0a8872442348835eb7cb88cad7ef7992ab7017c2777281493214413bc3d5f','ua.png':'9ae2f204178855c4fdb29ce75a0a1b2588fc3db3a7084d29715876bacd293508','ug.png':'42cd5a9bc8408d673b97fa04e528a194772f85c2f3aa756e1386045cdaa10538','uk.png':'5d72c5a8bef80fca6f99f476e15ec95ce2d5e5f65c6dab9ee8e56348be0d39fc','um.png':'7c655058691a6c837db9aac3c2f8662d8e06a6ebd3dd495cca6e691a67c1bf64','us.png':'36cce5cae3d2e0045b2b2b6cbffdad7a0aba3e99919cc219bbf0578efdc45585','uy.png':'9ab4ccd42c3869331626b86e9074502e47ad19db3253b3596f719bd850ff736e','uz.png':'a2870e6e9927c9ff0b80e6a58b95adb3463714f00733e9c3ddd3be1a2d5d17b5','va.png':'4ceb52d9a612b80c931d9530c273b1b608f32b9507e6b7009a48599eeb7f93e2','vc.png':'0bf42ce1f486108fa32afaba7976f0dea5dbbca2049b559f23d57a052124b6e2','ve.png':'6d04de1086b124d5843753e2bd55f137c2537bd47e0d5ea2c55ff3bc1da7293c','vg.png':'f3720add09557825a652d8998ac7bedf84239e5b9aecbdcffb3930383b7e4682','vi.png':'943fb60916b4286295f32e632fe5a046275e5cf84e87119a94f7f5e1b429e052','vn.png':'d05aa8078604f4560d99aacf12c80e400651e4ef9b0860b3ad478c2d8b08e36d','vu.png':'39779ad6848267e90357d3795bbb396deee7f20722f8e3d6c6be098a6f5f347e','wales.png':'a20ef40f442f089d0a5f5dcd089a76babd86f0fe3c243d9c8e50c6c0e4aef3ab','wf.png':'893ed4ccb23353f597bb7e9544ef8c376c896fc4f6fe56e4ca14aab70e49203e','ws.png':'7eb7d48fd72f83b5bcee0cc9bac9c24ad42c81927e8d336b6fd05fd9aefa0dcb','ye.png':'c2785bb08c181f8708b9a640ff8fe15d5ab5779af8095d11307542b6f03343a3','yt.png':'da7d65c048969b86d3815ed42134336609c9e8d5aead0a18194c025caf64c019','za.png':'48188165205cc507cd36c3465b00b2cd97c1cc315209b8f086f20af607055e49','zm.png':'794a2df87b0952ffd0fbcf18c9f61f713cff6cfafcc4b551745204d930fc1967','zw.png':'b546d55dd33c7049ef9bbfe4b665c785489b3470a04e6a2db4fda1fea403dc62'}
		self.systray_menu = False
		self.OVPN_SERVER_INFO = {}
		self.OVPN_SERVER_STATS = {}
		self.OVPN_SERVER_STATS_LASTUPDATE = 0
		self.UPDATEOVPNONSTART = False
		self.APIKEY = False
		self.ENABLE_EXTSERVERVIEW = False
		self.WIN_RESET_EXT_DEVICE = False
		
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
			
			text = "def make_systray_menu: event %s" % (event_button)
			self.debug(text=text)
			try: 
				updatemenu = gtk.Menu()
				updatem = gtk.MenuItem('Updates and Options')
				updatem.set_submenu(updatemenu)

				self.systray_menu.append(updatem)

				normalupdate = gtk.MenuItem('Normal Config Update')
				normalupdate.connect('button-press-event', self.check_remote_update_cb)
				updatemenu.append(normalupdate)
				
				forceupdate = gtk.MenuItem('Forced Config Update')
				forceupdate.connect('button-press-event', self.cb_force_update)
				updatemenu.append(forceupdate)

				if self.UPDATEOVPNONSTART == False:
					autoupdate = gtk.MenuItem('Enable Update on Start')
				else:
					autoupdate = gtk.MenuItem('Disable Update on Start')
				autoupdate.connect('button-press-event', self.cb_switch_autoupdate)
				updatemenu.append(autoupdate)
					
				resetlogin = gtk.MenuItem('Reset API Login')
				resetlogin.connect('button-press-event', self.cb_form_reask_userid)
				updatemenu.append(resetlogin)
				
				if self.STATE_OVPN == False:
					resetextif = gtk.MenuItem('Reset Network Adapter')
					resetextif.connect('button-press-event', self.cb_resetextif)
					updatemenu.append(resetextif)					
					
				if self.STATE_OVPN == True:
					if self.ENABLE_EXTSERVERVIEW == False:
						extserverview = gtk.MenuItem('Enable extended Server-View')
					else:
						extserverview = gtk.MenuItem('Disable extended Server-View')
					extserverview.connect('button-press-event', self.cb_extserverview)
					updatemenu.append(extserverview)
					
				
				ipv6menu = gtk.Menu()
				ipv6m = gtk.MenuItem('IPv6 Options')
				ipv6m.set_submenu(ipv6menu)
				updatemenu.append(ipv6m)
				
				if not self.OVPN_CONFIGVERSION == "23x":
					ipv6entry1 = gtk.MenuItem('Select: IPv4 Entry Server with Exit to IPv4 (standard)')
					ipv6entry1.connect('button-press-event', self.cb_change_ipmode1)
					ipv6menu.append(ipv6entry1)

				if not self.OVPN_CONFIGVERSION  == "23x46":
					ipv6entry2 = gtk.MenuItem('Select: IPv4 Entry Server with Exits to IPv4 + IPv6')
					ipv6entry2.connect('button-press-event', self.cb_change_ipmode2)
					ipv6menu.append(ipv6entry2)
				
				if not self.OVPN_CONFIGVERSION == "23x64":				
					ipv6entry3 = gtk.MenuItem('Select: IPv6 Entry Server with Exits to IPv6 + IPv4')
					ipv6entry3.connect('button-press-event', self.cb_change_ipmode3)
					ipv6menu.append(ipv6entry3)
					
				"""
				dnsmenu = gtk.Menu()
				dnsm = gtk.MenuItem('DNS Options')
				dnsm.set_submenu(dnsmenu)
				updatemenu.append(dnsm)
				
				
				dnsentry1 = gtk.MenuItem('Set DNS for VPN connection')
				dnsentry1.connect('button-press-event', self.cb_change_vpndns)
				dnsmenu.append(dnsentry1)
				
				dnsentry2 = gtk.MenuItem('Set DNS for Quit on Windows')
				dnsentry2.connect('button-press-event', self.cb_change_quitdns)
				dnsmenu.append(dnsentry2)				
				"""
				
			except:
				text="def make_systray_menu: updatemenu failed"
				self.debug(text=text)			

				
			sep = gtk.SeparatorMenuItem()
			self.systray_menu.append(sep)
			
			if len(self.OVPN_SERVER) > 0:
				self.make_systray_server_menu()

			if self.STATE_OVPN == True:
				sep = gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)		
				# add quit item
				servershort = self.OVPN_CONNECTEDto[:3]
				textstring = '[ %s ] IP: %s Port: %s (%s)' % (servershort,self.OVPN_SERVER_INFO[servershort][0],self.OVPN_SERVER_INFO[servershort][1],self.OVPN_SERVER_INFO[servershort][2].upper())
				
				disconnect = gtk.ImageMenuItem(textstring)
				img = gtk.Image()
				img.set_from_file(self.systray_icon_disconnected)
				disconnect.set_always_show_image(True)
				disconnect.set_image(img)
				self.systray_menu.append(disconnect)
				# SIGNALS
				disconnect.connect('activate', self.kill_openvpn)			

			#show server view
			sep = gtk.SeparatorMenuItem()
			self.systray_menu.append(sep)
			if self.MAINWINDOW_OPEN:
				mainwindow = gtk.MenuItem('Close Full View')
			else:
				mainwindow = gtk.MenuItem('Open Full View')
			self.systray_menu.append(mainwindow)
			# SIGNALS
			mainwindow.connect('activate', self.show_mainwindow)
			
			
			if self.STATE_OVPN == False:
				sep = gtk.SeparatorMenuItem()
				self.systray_menu.append(sep)		
				# show about dialog
				about = gtk.MenuItem('About')
				self.systray_menu.append(about)
				# SIGNALS
				about.connect('activate', self.show_about_dialog)
				# add quit item
				quit = gtk.MenuItem('Quit')
				self.systray_menu.append(quit)
				# SIGNALS
				quit.connect('activate', self.on_closing)
				
			self.systray_menu.show_all()
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

		
	def check_remote_update_cb(self,widget,event):
		self.destroy_systray_menu()
		self.debug(text="def check_remote_update_cb:")
		if self.check_remote_update():
			self.debug(text="def check_remote_update_cb: self.check_remote_update() == True")
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
										self.progressbar.set_fraction(1)
										return False
			else:
				text = _("Certificates and Configs up to date!")
				self.set_progressbar(text)
				self.set_statusbar_text(text)
				self.progressbar.set_fraction(1)
				self.timer_check_certdl_running = False
				return True
				
		else:
			self.plaintext_passphrase = False
			self.debug(text="self.curl_api_request(API_ACTION = lastupdate): failed")
			self.timer_check_certdl_running = False
			return False
	

	def show_about_dialog(self, widget):
		self.destroy_systray_menu()
		if self.SHOW_ABOUT_DIALOG == False:	
			try:
				about_dialog = gtk.AboutDialog()
				self.about_dialog = about_dialog
				about_dialog.set_destroy_with_parent (True)
				about_dialog.set_name('oVPN.to')		
				about_dialog.set_version('Client %s'%(CLIENTVERSION))
				about_dialog.set_copyright('(C) 2010 - 2016 oVPN.to')
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

				if not self.plaintext_passphrase == False:
					del_PH = gtk.MenuItem("Clear Passphrase from Disk and RAM")
					del_FAV.connect('button-release-event',self.defundef,None)
					optionsmenu.append(del_PH)
				
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
		#if self.OVPN_SERVER_STATS > 0:
		#	self.debug(text="%s"%(self.OVPN_SERVER_STATS))
		""" build serverlist """
		""" *fixme* we should do any checks before adding remote text to output ! """
		if len(self.OVPN_SERVER_STATS) > 0:
			liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str)
		else:
			liststore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,str,str,str)
		self.mainwindow_liststore = liststore
		treeview = gtk.TreeView(liststore)
		self.treeview = treeview
		for server in self.OVPN_SERVER:
			countrycode = server[:2].lower()
			servershort = server[:3].upper()
			imgpath = self.FLAG_IMG[countrycode]
			countryimg = gtk.gdk.pixbuf_new_from_file(imgpath)
			serverip  = self.OVPN_SERVER_INFO[servershort][0]
			serverport = self.OVPN_SERVER_INFO[servershort][1]
			serverproto = self.OVPN_SERVER_INFO[servershort][2]
			servercipher = self.OVPN_SERVER_INFO[servershort][3]
			if len(self.OVPN_SERVER_STATS) > 0:
				vlanip4 = self.OVPN_SERVER_STATS[servershort]["vlanip4"]
				vlanip6 = self.OVPN_SERVER_STATS[servershort]["vlanip6"]
				traffic = self.OVPN_SERVER_STATS[servershort]["traffic"]["eth0"]
				live = self.OVPN_SERVER_STATS[servershort]["traffic"]["live"]
				uplink = self.OVPN_SERVER_STATS[servershort]["traffic"]["uplink"]
				cpuload = self.OVPN_SERVER_STATS[servershort]["cpu"]["cpu-load"]
				
				cpuinfo = self.OVPN_SERVER_STATS[servershort]["info"]["cpu"]
				raminfo = self.OVPN_SERVER_STATS[servershort]["info"]["ram"]
				hddinfo = self.OVPN_SERVER_STATS[servershort]["info"]["hdd"]
				
				serverstatus = self.OVPN_SERVER_STATS[servershort]["status"]
				if serverstatus == "0":
					statustext = "DEAD"
				elif serverstatus == "1":
					statustext = "OK"
				elif serverstatus == "2":
					statustext = "n/a"
				else:
					statustext = "n/a"
					
				liststore.append([countryimg,server,serverip,serverport,serverproto,servercipher,live,uplink,vlanip4,vlanip6,cpuload,cpuinfo,raminfo,hddinfo,traffic,statustext])
			else:
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
		
		if len(self.OVPN_SERVER_STATS) > 0:
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Mbps',cell)
			column.add_attribute(cell,"text",6)			
			#column.set_sort_column_id(6)
			treeview.append_column(column)
			
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Link',cell)
			column.add_attribute(cell,"text",7)
			column.set_sort_column_id(7)
			treeview.append_column(column)			
		
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('VLAN IPv4',cell)
			column.add_attribute(cell,"text",8)
			treeview.append_column(column)
			
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('VLAN IPv6',cell)
			column.add_attribute(cell,"text",9)
			treeview.append_column(column)			
			
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Load',cell)
			column.add_attribute(cell,"text",10)
			treeview.append_column(column)		
			
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Processor',cell)
			column.add_attribute(cell,"text",11)
			treeview.append_column(column)

			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('RAM',cell)
			column.add_attribute(cell,"text",12)
			treeview.append_column(column)

			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('HDD',cell)
			column.add_attribute(cell,"text",13)
			treeview.append_column(column)

			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Traffic',cell)
			column.add_attribute(cell,"text",14)
			treeview.append_column(column)
			
			cell = gtk.CellRendererText()
			column = gtk.TreeViewColumn('Status',cell)
			column.add_attribute(cell,"text",15)
			column.set_sort_column_id(15)
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

	def cb_destroy_systray_menu(self,event,time):
		self.destroy_systray_menu()
			
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
		if self.plaintext_passphrase == False:
			self.debug(text="def check_passphrase: popup receive passphrase")
			self.form_ask_passphrase()
		self.debug("def check_passphrase: passphrase loaded, try decrypt")
		if self.read_apikey_config():
			if self.compare_confighash():
				self.debug(text="def check_passphrase: self.compare_confighash() :True")
				return True
		else:
			self.msgwarn(text="Invalid Passphrase.")
					

	def preboot_check(self):
		if self.pre0_detect_os():
			self.load_ovpn_server()

			""" *fixme* """
			#self.show_mainwindow(widget="NULL")
			return True
		else:
			print "preboot_check: failed"
				
	def pre0_detect_os(self):
		self.self_vars()
		self.OS = sys.platform
		if self.OS == "win32":
			""" *fixme* (unused)
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
			"""
			
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
			if self.WIN_RESET_EXT_DEVICE == False:
				if self.win_read_interfaces():
					if self.win_netsh_read_dns_to_backup():
						return True
			else:
				self.win_netsh_restore_dns_from_backup()
				self.WIN_RESET_EXT_DEVICE = False
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
		TAPADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		TAPADAPTERS = TAPADAPTERS.split('\r\n')
		TAPADAPTERS.pop(0)
		self.debug(text="TAP ADAPTER = %s"%(TAPADAPTERS))
		self.WIN_TAP_DEVS = list()
		for line in TAPADAPTERS:
			#self.debug(text="checking line = %s"%(line))
			for INTERFACE in self.INTERFACES:
				#self.debug(text="is IF: '%s' listed as TAP?"%(INTERFACE))
				if line.startswith("'%s' {"%(INTERFACE)):
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

		if self.WIN_TAP_DEVICE in self.WIN_TAP_DEVS:
			self.debug(text="Found self.WIN_TAP_DEVICE '%s' in self.WIN_TAP_DEVS '%s'" % (self.WIN_TAP_DEVICE,self.WIN_TAP_DEVS))
			
		elif len(self.WIN_TAP_DEVS) == 0:
			self.errorquit(text=_("No OpenVPN TAP-Adapter found! Please install openVPN Version\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64))
				
		elif len(self.WIN_TAP_DEVS) == 1 or self.WIN_TAP_DEVS[0] == self.WIN_TAP_DEVICE:
			self.WIN_TAP_DEVICE = self.WIN_TAP_DEVS[0]

		else:
			self.debug(text="self.WIN_TAP_DEVS = '%s'" % (self.WIN_TAP_DEVS))
			dialogWindow = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_OK)
			text = _("Choose your TAP Adapter!")
			dialogWindow.set_title(text)
			dialogWindow.set_markup(text)
			dialogBox = dialogWindow.get_content_area()

			liststore = gtk.ListStore(str)
			combobox = gtk.ComboBox(liststore)
			cell = gtk.CellRendererText()
			combobox.pack_start(cell, True)
			combobox.add_attribute(cell, 'text', 0)
			combobox.set_wrap_width(5)
			for INTERFACE in self.WIN_TAP_DEVS:
				print "add tap interface '%s' to combobox" % (INTERFACE)
				liststore.append([INTERFACE])
			combobox.set_model(liststore)
			combobox.connect('changed',self.tap_interface_selector_changed_cb)

			dialogBox.pack_start(combobox,False,False,0)
			dialogWindow.show_all()
			print "open tap interface selector"
			dialogWindow.run()
			print "close tap interface selector"
			if not self.WIN_TAP_DEVICE == False:
				dialogWindow.destroy()
			
					
		if self.WIN_TAP_DEVICE == False:
			self.errorquit(text=_("No OpenVPN TAP-Adapter found! Please install openVPN Version\r\nx86: %s\r\nx64: %s") % (self.OVPN_WIN_DL_URL_x86,self.OVPN_WIN_DL_URL_x64))
		else:
			self.debug(text="Selected TAP: '%s'" % (self.WIN_TAP_DEVICE))
			self.win_enable_tap_interface()
			self.debug(text="remaining INTERFACES = %s (cfg: %s)"%(self.INTERFACES,self.WIN_EXT_DEVICE))
			if len(self.INTERFACES) > 1:
				if not self.WIN_EXT_DEVICE == False and self.WIN_EXT_DEVICE in self.INTERFACES:
					self.debug(text="loaded self.WIN_EXT_DEVICE %s from options file"%(self.WIN_EXT_DEVICE))					
					return True
				else:
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
				self.debug(text="External Interface = %s"%(self.WIN_EXT_DEVICE))
				return True
			
	def interface_selector_changed_cb(self, combobox):
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_EXT_DEVICE = model[index][0]
			self.debug(text="selected IF: %s" % (self.WIN_EXT_DEVICE))
		return
		
	def tap_interface_selector_changed_cb(self, combobox):
		model = combobox.get_model()
		index = combobox.get_active()
		if index > -1:
			self.WIN_TAP_DEVICE = model[index][0]			
			self.debug(text="selected tap IF: %s" % (self.WIN_TAP_DEVICE))
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
							if (self.isValueIPv4(ip) or self.isValueIPv6(ip)) and port > 0 and port < 65535:
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
			self.ovpn_string = "\"%s\" --config \"%s\" --ca \"%s\" --cert \"%s\" --key \"%s\" --tls-auth \"%s\" --log \"%s\" --dev-node \"%s\" " % (self.OPENVPN_EXE,self.ovpn_server_config_file,self.ovpn_cert_ca,self.ovpn_cli_crt,self.ovpn_cli_key,self.ovpn_tls_key,self.ovpn_sessionlog,self.WIN_TAP_DEVICE)
			
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
			self.debug(text="Change oVPN to %s" %(server))
			self.kill_openvpn()
			self.call_openvpn(None,None,server)
		

	def inThread_timer_ovpn_ping(self):
		
		if self.timer_ovpn_ping_running == False:
			self.OVPN_PING_STAT = -2
			self.debug(text="def inThread_timer_ovpn_ping")
			self.timer_ovpn_ping_running = True
		
		if self.STATE_OVPN == True:
			time.sleep(2)
			if self.OS == "win32":
			
				try:
					ai_list = socket.getaddrinfo(self.OVPN_GATEWAY_IP4,"443",socket.AF_UNSPEC,socket.SOCK_STREAM)
				except:
					pass
				
				for (family, socktype, proto, canon, sockaddr) in ai_list:
					addr, port = sockaddr[0:2]
					try:
						t1 = time.time()
						s = socket.socket(family, socktype)
						s.connect(sockaddr)
						t2 = time.time()
						s.close()
					except:
						self.OVPN_PING_LAST = -2
						pass
					else:
						self.OVPN_PING_LAST = int((t2-t1)*1000)
						#self.debug(text="ping=%s"%(self.OVPN_PING_LAST))
				
				pingsum = 0
				if self.OVPN_PING_LAST > 0:
					self.OVPN_PING.append(self.OVPN_PING_LAST)
				if len(self.OVPN_PING) > 10:
					self.OVPN_PING.pop(0)
				if len(self.OVPN_PING) > 0:
					for ping in self.OVPN_PING:
						pingsum += int(ping)
					self.OVPN_PING_STAT = pingsum/len(self.OVPN_PING)
				if self.OVPN_PING_STAT >= 0:
					if self.OVPN_CONNECTEDtime > 60:
						time.sleep(12)
					else:
						time.sleep(6)
				else:
					time.sleep(4)
				self.load_serverdata_from_remote()
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
			text = _("def inThread_spawn_openvpn_process: Could not start Windows Firewall!");
			self.debug(text=text)
			return False
		self.win_firewall_modify_rule(option="add")
		self.win_clear_ipv6_addr()
		try:			
			self.ovpn_proc_retcode = subprocess.check_output("%s" % (self.ovpn_string),shell=True)
		except subprocess.CalledProcessError as e:
			self.debug(text="self.ovpn_proc_retcode: output = %s" %(e.output))
			self.OVPN_AUTO_RECONNECT = False
		except:
			self.debug(text="self.ovpn_proc_retcode: failed")
			self.OVPN_AUTO_RECONNECT = False
		self.win_firewall_modify_rule(option="delete")
		try:
			os.remove(self.ovpn_sessionlog)
		except:
			text = _("def inThread_spawn_openvpn_process: Could not remove %s" % (self.ovpn_sessionlog))
			self.debug(text=text)
		self.win_clear_ipv6_addr()
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
				if "%s"%(self.OVPN_CONNECTEDtoIP) in line:
					self.debug(text="def read_ovpn_routes: %s"%(line))
					self.GATEWAY_LOCAL = line.split()[2]
					self.debug(text="self.GATEWAY_LOCAL: %s"%(self.GATEWAY_LOCAL))
		except:
			self.debug(text="def read_gateway_from_routes: failed")

				
	def del_ovpn_routes(self):
		self.read_gateway_from_routes()
		if not self.GATEWAY_LOCAL == False:
			self.debug(text="def del_ovpn_routes")
			string1 = "route.exe DELETE %s MASK 255.255.255.255 %s" % (self.OVPN_CONNECTEDtoIP,self.GATEWAY_LOCAL)
			string2 = "route.exe DELETE 0.0.0.0 MASK 128.0.0.0 %s" % (self.OVPN_GATEWAY_IP4)
			string3 = "route.exe DELETE 128.0.0.0 MASK 128.0.0.0 %s" % (self.OVPN_GATEWAY_IP4)
			try: 
				self.OVPN_DEL_ROUTES1 = subprocess.check_output("%s" % (string1),shell=True)
				self.OVPN_DEL_ROUTES2 = subprocess.check_output("%s" % (string2),shell=True)
				self.OVPN_DEL_ROUTES3 = subprocess.check_output("%s" % (string3),shell=True)
				self.debug(text="self.OVPN_DEL_ROUTES: %s, %s, %s"%(self.OVPN_DEL_ROUTES1,self.OVPN_DEL_ROUTES2,self.OVPN_DEL_ROUTES3))
			except:
				self.debug(text="def del_ovpn_routes: failed")
				pass
				
	def win_clear_ipv6_addr(self):
		if self.OVPN_CONFIGVERSION == "23x":
			return
		
		try:
			string = "netsh interface ipv6 show addresses %s" % (self.WIN_TAP_DEVICE)
			read = subprocess.check_output("%s" % (string),shell=True)
			read = read.strip().decode('cp1258','ignore')
			list = read.strip(' ').split('\r\n')
			for line in list:
				if " fd48:8bea:68a5:" in line or " fe80::" in line:
					if not "%" in line:
						ipv6addr = line.split()[1]
						string = "netsh interface ipv6 delete address address=\"%s\" interface=\"%s\"" % (ipv6addr,self.WIN_TAP_DEVICE)
						try:
							cmd = subprocess.check_output("%s" % (string),shell=True)
							text = "def win_clear_ipv6_addr: removed %s '%s'" % (ipv6addr,string)
							self.debug(text=text)
						except subprocess.CalledProcessError as e:
							text = "def win_clear_ipv6_addr: %s %s failed '%s': %s" % (ipv6addr,self.WIN_TAP_DEVICE,string,e.output)
							self.debug(text=text)
						except:
							text = "def win_clear_ipv6_addr: %s %s failed '%s'" % (ipv6addr,self.WIN_TAP_DEVICE,string)
							self.debug(text=text)
		except:
			text = "def win_clear_ipv6_addr: failed"
			self.debug(text=text)	
			
			
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
			self.del_ovpn_routes()
			self.OVPN_KILL2 = subprocess.check_output("%s" % (string),shell=True)
			
		except:
			pass
		
		
		
		
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
			self.OVPN_LATESTBUILT = self.OVPN_LATEST_BUILT.split()
			text = "self.OVPN_VERSION = %s, self.OVPN_BUILT = %s, self.OVPN_LATESTBUILT = %s" % (self.OVPN_VERSION,self.OVPN_BUILT,self.OVPN_LATESTBUILT)
			self.debug(text=text)
			if self.OVPN_VERSION >= self.OVPN_LATEST:
				if self.OVPN_BUILT == self.OVPN_LATESTBUILT:
					text = "self.OVPN_BUILT == self.OVPN_LATESTBUILT: True"
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
					text = "openvpn built_timestamp = %s self.OVPN_LATESTBUILT_TIMESTAMP = %s" % (built_timestamp,self.OVPN_LATEST_BUILT_TIMESTAMP)
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
		try:
			self.dialogWindow_form_ask_passphrase.destroy()
		except:
			pass
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
					self.plaintext_passphrase = False				
				
				if response == gtk.RESPONSE_OK:	
					if len(ph1) > 0:
						self.plaintext_passphrase = ph1
						if self.read_apikey_config():
							if self.compare_confighash():
								self.debug(text="def check_passphrase: self.compare_confighash() :True")
								if saveph == True:
									self.write_options_file()
								else:
									self.plaintext_passphrase = False
									self.write_options_file()								
									self.plaintext_passphrase = ph1
				
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
			ph1Label = gtk.Label("Local passphrase for encryption:")

			ph2Entry = gtk.Entry()
			ph2Entry.set_visibility(False)
			ph2Entry.set_invisible_char("X")
			ph2Entry.set_size_request(200,24)
			ph2Label = gtk.Label("Repeat your local passphrase:")
			
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
					self.plaintext_passphrase = ph1
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
		
	def cb_form_reask_userid(self,widget,event):
		self.destroy_systray_menu()
		self.form_reask_userid()
			
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
		
		self.dns_dir =  "%s\\dns" % (self.bin_dir)
		self.dns_d0wntxt =  "%s\\dns.txt" % (self.dns_dir)
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
			hasher = hashlib.sha256()
			with open(self.CA_FILE, 'rb') as afile:
				buf = afile.read()
				hasher.update(buf)
			hash = hasher.hexdigest()
			fixedhash = "dc333fc1d45f542f45976b381f47a707d8073257915cf7c84e842adbafe51361"
			if hash == fixedhash:
				try:
					os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), self.CA_FILE)
					text="SSL Root Certificate for %s hash verified and loaded" % (DOMAIN)
					self.debug(text=text)
				except:
					text="Error:\nSSL Root Certificate for %s not loaded" % (DOMAIN,self.CA_FILE)
					self.msgwarn(text=text)
					return False					
			else:
				text = "Error:\nInvalid SSL Root Certificate for %s in:\n'%s'\nSHA256 is:\n'%s'\nbut should be '%s'" % (DOMAIN,self.CA_FILE,hash,fixedhash)
				self.msgwarn(text=text)
				return False
		else:
			text="Error:\nSSL Root Certificate for %s not found in:\n'%s'!" % (DOMAIN,self.CA_FILE)
			self.msgwarn(text=text)
			return False
		
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
				self.plaintext_passphrase = fp.read()
				fp.close()
				
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
					if not self.plaintext_passphrase == False:
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
					self.plaintext_passphrase = parser.get('oVPN','passphrase')
					if self.plaintext_passphrase == "False":
						self.plaintext_passphrase = False
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
					self.WIN_TAP_DEVICE = parser.get('oVPN','wintapdevice')
					if self.WIN_TAP_DEVICE == "False": 
						self.WIN_TAP_DEVICE = False
				except:
					pass

					
				try:
					self.OPENVPN_EXE = parser.get('oVPN','openvpnexe')
					if self.OPENVPN_EXE == "False":
						self.OPENVPN_EXE = False
				except:
					pass

					
				try:
					self.UPDATEOVPNONSTART = parser.get('oVPN','updateovpnonstart')
					self.debug(text="self.UPDATEOVPNONSTART = %s" % (self.UPDATEOVPNONSTART))
					if self.UPDATEOVPNONSTART == "True":
						self.UPDATEOVPNONSTART = True
					else:
						self.UPDATEOVPNONSTART = False
				except:
					pass
					
				try:
					ocfgv = parser.get('oVPN','configversion')
					self.debug(text="self.OVPN_CONFIGVERSION = %s" % (self.OVPN_CONFIGVERSION))
					if ocfgv == "23x" or ocfgv == "23x46" or ocfgv == "23x64":
						self.OVPN_CONFIGVERSION = ocfgv
					else:
						self.OVPN_CONFIGVERSION = "23x"
				except:
					pass					
				if self.write_options_file():
					return True
			except:
				self.msgwarn(text="def read_options_file: read failed")
				try:
					os.remove(self.opt_file)
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
				parser.set('oVPN','wintapdevice','False')				
				parser.set('oVPN','openvpnexe','False')
				parser.set('oVPN','updateovpnonstart','False')
				parser.set('oVPN','configversion','23x')
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
			parser.set('oVPN','passphrase','%s'%(self.plaintext_passphrase))
			parser.set('oVPN','autoconnect','%s'%(self.OVPN_AUTO_CONNECT_ON_START))
			parser.set('oVPN','favserver','%s'%(self.OVPN_FAV_SERVER))
			parser.set('oVPN','winextdevice','%s'%(self.WIN_EXT_DEVICE))
			parser.set('oVPN','wintapdevice','%s'%(self.WIN_TAP_DEVICE))			
			parser.set('oVPN','openvpnexe','%s'%(self.OPENVPN_EXE))
			parser.set('oVPN','updateovpnonstart','%s'%(self.UPDATEOVPNONSTART))
			parser.set('oVPN','configversion','%s'%(self.OVPN_CONFIGVERSION))
			
			parser.write(cfg)
			cfg.close()
			return True
		except:
			self.debug(text="def write_options_file: failed")

	def load_decryption(self):
		self.debug(text="def load_decryption")
		if self.plaintext_passphrase == False:
			try:
				if len(self.plaintext_passphrase) > 0: 
					self.aeskey = hashlib.sha256(self.plaintext_passphrase.rstrip()).digest()
					return True
			except:
				return False
		else:
			try:
				if len(self.plaintext_passphrase) > 0:
					self.aeskey = hashlib.sha256(self.plaintext_passphrase.rstrip()).digest()
					return True
			except:
				return False		
		
	def read_apikey_config(self):
		#self.debug(text="def read_apikey_config: self.plaintext_passphrase = %s" %(self.plaintext_passphrase))
		if not self.plaintext_passphrase == False and self.load_decryption() and os.path.isfile(self.api_cfg):
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
		self.aeskeyhash = hashlib.sha256(self.plaintext_passphrase).digest()
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
			self.plaintext_passphrase = False
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

	def cb_force_update(self,widget,event):
		self.debug(text="def cb_force_update:")
		self.destroy_systray_menu()
		if self.reset_last_update():
			self.debug(text="def cb_force_update: self.reset_last_update")
			self.check_remote_update_cb(widget,event)
			
	def cb_switch_autoupdate(self,widget,event):
		self.debug(text="def cb_switch_autoupdate:")	
		self.destroy_systray_menu()
		if self.UPDATEOVPNONSTART == False:
			self.UPDATEOVPNONSTART = True
		else:
			self.UPDATEOVPNONSTART = False
			self.plaintext_passphrase = False
		self.write_options_file()
		
	def cb_resetextif(self,widget,event):
		self.destroy_systray_menu()
		self.WIN_EXT_DEVICE = False
		self.WIN_TAP_DEVICE = False		
		self.WIN_RESET_EXT_DEVICE = True
		self.write_options_file()
		self.read_interfaces()
		
	def cb_extserverview(self,widget,event):
		self.destroy_systray_menu()
		if self.ENABLE_EXTSERVERVIEW == False:
			if self.check_passphrase():
				self.ENABLE_EXTSERVERVIEW = True
		else:
			self.ENABLE_EXTSERVERVIEW = False
			
			
	def cb_change_ipmode1(self,widget,event):
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x"
		self.write_options_file()
		self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://vcp.ovpn.to to use any IPv6 options!")
		
	def cb_change_ipmode2(self,widget,event):
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x46"
		self.write_options_file()
		self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://vcp.ovpn.to to use any IPv6 options!")

	def cb_change_ipmode3(self,widget,event):
		self.destroy_systray_menu()
		self.OVPN_CONFIGVERSION = "23x64"
		self.write_options_file()
		self.msgwarn(text="Changed Option:\n\nUse 'Forced Config Update' to get new configs!\n\nYou have to join 'IPv6 Beta' on https://vcp.ovpn.to to use any IPv6 options!")
	
	def cb_change_vpndns(self,widget,event):
		self.destroy_systray_menu()
	
	def cb_change_quitdns(self,widget,event):
		self.destroy_systray_menu()
		
	def delete_dir(self,path):
		if self.OS == "win32":
			string = 'rmdir /S /Q "%s"' % (path)
			#text = "def delete_dir: %s" % (string)
			#self.debug(text=text)
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
			values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : self.API_ACTION, 'version' : self.OVPN_CONFIGVERSION, 'type' : 'win' }	
			
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
				self.body = "0"
				self.set_progressbar(text)
				self.timer_check_certdl_running = False
				self.progressbar.set_fraction(0)
				return False
		
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
					return True		
			
			
	def check_inet_connection(self):
		s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = DOMAIN
		port = 443
				
		if not self.try_socket(host,port):
			text=_("1) Could not connect to %s\nTry setting firewall rule to access VCP!"%(DOMAIN))
			self.msgwarn(text=text)
			self.win_firewall_add_rule_to_vcp(option="add")
			time.sleep(2)
			if not self.try_socket(host,port):
				text=_("2) Could not connect to %s\nRetry"%(DOMAIN))
				self.msgwarn(text=text)
				time.sleep(2)
				if not self.try_socket(host,port):
					#text="3) Could not connect to vcp.ovpn.to\nTry setting firewall rule to allowing outbound connections to world!"
					#self.win_firewall_allow_outbound()
					text=_("3) Could not connect to %s"%(DOMAIN))
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
				text = _("oVPN is connected ( %s ) to %s ( %s / %s ms )")%(self.OVPN_CONNECTEDtimetext,self.OVPN_CONNECTEDto,self.OVPN_PING_LAST,self.OVPN_PING_STAT)
				#text = _("oVPN is connected ( %s ) to %s ( %s ms )")%(self.OVPN_CONNECTEDtimetext,self.OVPN_CONNECTEDto,self.OVPN_PING_LAST)
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
					try:
						flagicon = self.FLAG_IMG[countrycode]
					except:						
						imgfile = '%s\\ico\\flags\\%s.png' % (self.bin_dir,countrycode)
						if not os.path.isfile(imgfile):
							if not self.load_flags_from_remote(countrycode,imgfile):
								imgfile = '%s\\ico\\flags\\00.png' % (self.bin_dir)
						self.FLAG_IMG[countrycode] = imgfile
					self.OVPN_SERVER.append(servername)
					#self.debug(text="def load_ovpn_server: file = %s " % (file))
			# for end
			self.OVPN_SERVER.sort()
		else:
			cfg = open(self.api_upd,'w')
			cfg.write("0")
			cfg.close()
	
	def load_flags_from_remote(self,countrycode,imgfile):
		try:
			flagfilename = "%s.png" % (countrycode)
			url = "https://%s/img/flags/%s" % (DOMAIN,flagfilename)
			r = requests.get(url)
			body = r.content
			
			fp = open(imgfile, "wb")
			fp.write(body)
			fp.close()

			try:
				hasher = hashlib.sha256()
				with open(imgfile, 'rb') as afile:
					buf = afile.read()
					hasher.update(buf)
				hash = hasher.hexdigest()			
				if hash == self.FLAG_HASHS[flagfilename]:
					text = "def load_flags_from_remote: %s hash ok" % (flagfilename)
					self.debug(text=text)
					return True
				else:
					text = "def load_flags_from_remote: %s hash failed" % (flagfilename)
					self.msgwarn(text=text)
					if os.path.isfile(flagfilename):
						os.remove(flagfilename)					
					return False
			except:
				self.debug(text="def load_flags_from_remote: try hasher %s failed"%(countrycode))
				if os.path.isfile(flagfilename):
					os.remove(flagfilename)
			
		except:
			self.debug(text="def load_flags_from_remote: %s failed"%(countrycode))
			
			
	def load_serverdata_from_remote(self):
		if self.APIKEY == False or self.plaintext_passphrase == False or self.ENABLE_EXTSERVERVIEW == False:
			return False

		if (self.OVPN_SERVER_STATS_LASTUPDATE < self.get_now_unixtime()-600) and self.OVPN_CONNECTEDtime > 15 and (self.OVPN_PING_STAT >= 0 or self.OVPN_PING_STAT <= 500):
			try:
				url = "https://%s:%s/%s" % (DOMAIN,PORT,API)
				API_ACTION = "loadserverdata"
				values = {'uid' : self.USERID, 'apikey' : self.APIKEY, 'action' : API_ACTION }			
				r = requests.post(url,data=values)
				body = r.content			
				try:
					self.OVPN_SERVER_STATS = {}
					self.OVPN_SERVER_STATS = json.loads(body)				
					self.OVPN_SERVER_STATS_LASTUPDATE = self.get_now_unixtime()
					self.debug(text="def load_serverdata_from_remote: loaded")
				except:
					self.debug(text="def load_serverdata_from_remote: json decode error")
					self.OVPN_SERVER_STATS_LASTUPDATE = self.get_now_unixtime()
			except:
				self.debug(text="def load_serverdata_from_remote: api request failed")

	"""
				
	def load_d0wns_dns(self):
		if os.isfile(self.dns_d0wntxt):
			file = open(self.dns_d0wntxt,'r')
		else:
			try:
				url = "https://dns.d0wn.biz/dns.txt"
				r = requests.get(url)
				body = r.content.split('\n')
				print body
				try:
					self.d0wns_DNS = body.split(',')
					print self.d0wns_DNS
				except:
					pass

	"""
				
				
	def on_closing(self, widget):
		if self.STATE_OVPN == True:
			return False
		else:
			try: 
				self.about_dialog.destroy()
			except:	
				pass
			#try: 
			#	self.dialogWindow_form_ask_passphrase.destroy()
			#except: 
			#	pass
			
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
