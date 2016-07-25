# -*- coding: utf-8 -*-
print "join release_version.py"

def build_data():
	from datetime import date
	data = {
		"YEAR" : date.today().year,
		"MONTH" : date.today().month,
		"DAY" : date.today().day
	}
	#print "release_version.build_data = '%s'" % (data)
	return data

def org_data():
	data = {
			"ORG" : "oVPN.to",
			"ADD" : "Anonymous Services",
			"SITE" : "https://oVPN.to",
			"SUPPORT" : "https://vcp.ovpn.to/?site=support",
			"UPDATES" : "https://board.ovpn.to/v4/index.php?thread/57314-ovpn-client-for-windows-beta-binary-releases/&action=firstNew",
		}
	#print "release_version.org_data = '%s'" % (data)
	return data

def version_data():
	data = {
			"SCRIPT" : "ovpn_client.py",
			"VERSION" : "0.5.8",
			"NAME":"%s Client" % (org_data()["ORG"])
		}
	#print "release_version.version_data = '%s'" % (data)
	return data

def setup_data():
	data = { 
			"version" : "0.%s" % (version_data()["VERSION"]),
			"name" : "%s for Windows" % (version_data()["NAME"]),
			"description" : "Built (ISO): %d-%02d-%02d" % (build_data()["YEAR"],build_data()["MONTH"],build_data()["DAY"]),
			"copyright" : "Copyright (C) %s %s" % (build_data()["YEAR"],org_data()["ORG"]),
		}
	#print "release_version.setup_data = '%s'" % (data)
	return data

def script_data():
	data = {
			"CLIENTVERSION" : version_data()["VERSION"],
			"CLIENT_STRING" : setup_data()["name"]
		}
	#print "release_version.script_data = '%s'" % (data)
	return data

print "leave release_version.py"