print "join release_version.py"

def version_data():
	data = {
			"VERSION" : "0.5.8",
			"NAME":"%s Client" % (org_data()["ORG"]),
			"SCRIPT" : "ovpn_client.py"
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
			"version" : "0.%s" % (version_data()["VERSION"]),
			"name" : "%s for Windows" % (version_data()["NAME"]),
			"description" : "Built: %d-%02d-%02d (%d)" % (build_data()["YEAR"],build_data()["MONTH"],build_data()["DAY"],build_data()["STAMP"]),
			"copyright" : "Copyright (C) %s %s" % (build_data()["YEAR"],org_data()["ORG"]),
			"uac_info" : "requireAdministrator"
		}
	return data

def script_data():
	data = {
			"CLIENTVERSION" : version_data()["VERSION"],
			"CLIENT_STRING" : setup_data()["name"]
		}
	return data

print "version_data() = '%s'" % (version_data())
print "build_data() = '%s'" % (build_data())
print "org_data() = '%s'" % (org_data())
print "setup_data() = '%s'" % (setup_data())
print "script_data() = '%s'" % (script_data())

print "leave release_version.py"