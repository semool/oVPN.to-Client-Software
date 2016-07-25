print "join release_version.py"


def version_data():
	data = {
			"VERSION" : "0.5.8",
			"NAME":"%s Client" % (org_data()["ORG"]),
		}
	return data

def build_data():
	from datetime import date
	import time
	data = {
		"YEAR" : date.today().year,
		"MONTH" : date.today().month,
		"DAY" : date.today().day,
		"STAMP" : int(time.time())
	}
	return data

def org_data():
	data = {
			"ORG" : "oVPN.to",
			"ADD" : "Anonymous Services",
			"SITE" : "https://oVPN.to",
			"EMAIL" : "support@ovpn.to",
			"SUPPORT" : "https://vcp.ovpn.to/?site=support",
			"CHAT_URL" : "https://webirc.ovpn.to",
			"IRC_ADDR" : "irc://irc.ovpn.to:6697 (SSL)",
			"UPDATES" : "https://board.ovpn.to/v4/index.php?thread/57314-ovpn-client-for-windows-beta-binary-releases/&action=firstNew",
			"VCP_DOMAIN" : "vcp.ovpn.to",
			"API_POST" : "xxxapi.php",
			"API_DOMAIN" : "vcp.ovpn.to",
			"API_PORT" : "443",
		}
	return data

def setup_data():
	data = { 
			"script" : "ovpn_client.py",
			"version" : "0.%s" % (version_data()["VERSION"]),
			"name" : "%s for Windows" % (version_data()["NAME"]),
			"description" : "Built: %d-%02d-%02d (%d)" % (build_data()["YEAR"],build_data()["MONTH"],build_data()["DAY"],build_data()["STAMP"]),
			"copyright" : "(C) 2010 - %s %s" % (build_data()["YEAR"],org_data()["ORG"]),
		}
	return data

print "version_data() = '%s'" % (version_data())
print "build_data() = '%s'" % (build_data())
print "org_data() = '%s'" % (org_data())
print "setup_data() = '%s'" % (setup_data())


import sys
if len(sys.argv) > 1:
	if sys.argv[1] == "SET_VERSION_FILES":
		import os
		VERSION = version_data()["VERSION"]
		inno = { "file" : "set_version.txt", "content" : "#define Version" }
		winb = { "file" : "set_version.bat", "content" : "set RELEASE=" }
		
		file = inno["file"]
		data = '%s "%s"' % (inno["content"],VERSION)
		if os.path.isfile(file):
			fp = open(file, "wb")
			fp.write(data)
			fp.close()
			print "written: inno data '%s' to file '%s'" % (data,file)
		
		file = winb["file"]
		data = '%s%s' % (winb["content"],VERSION)
		if os.path.isfile(file):
			fp = open(file, "wb")
			fp.write(data)
			fp.close()
			print "written: winb data '%s' to file '%s'" % (data,file)

print "leave release_version.py"