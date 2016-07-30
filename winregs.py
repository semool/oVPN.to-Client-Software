# -*- coding: utf-8 -*-
import os, sys, time, subprocess
from _winreg import *

def get_uninstall_progs():
	aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
	aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
	list = []
	for i in range(1024):
		try:
			keyname = EnumKey(aKey, i)
			asubkey = OpenKey(aKey, keyname)
			val = QueryValueEx(asubkey, "DisplayName")
			print val
			list.append(val)
		except WindowsError:
			pass
	return list

""" NETWORK ADAPTER """

def get_networkadapter_guids():
	import netifaces
	return netifaces.interfaces()

def get_networkadapterlist_from_netsh():
	string = "netsh.exe interface show interface"
	data = subprocess.check_output("%s" % (string),shell=True)
	data = data.split('\r\n')
	return data

def get_networkadapterlist_from_guids(iface_guids):
	iface_names = ['(unknown)' for i in range(len(iface_guids))]
	mapguids = {}
	reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	key = OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
	for i in range(len(iface_guids)):
		try:
			reg_subkey = OpenKey(key, iface_guids[i] + r'\Connection')
			iface_name = QueryValueEx(reg_subkey, 'Name')[0]
			iface_names[i] = iface_name
			mapguids[iface_name] = '%s' % (iface_guids[i])
		except:
			pass
	print "mapguids = '%s'" % (mapguids)
	data = { "iface_names":iface_names,"mapguids":mapguids }
	return data
	#return iface_names

def get_networkadapterlist():
	newlist = []
	list1 = get_networkadapterlist_from_guids(get_networkadapter_guids())["iface_names"]
	list2 = get_networkadapterlist_from_netsh()
	for name in list1:
		for line in list2:
			if line.endswith(name):
				newlist.append(name)
	return newlist

def get_networkadapter_guid(adaptername):
	guids = get_networkadapterlist_from_guids(get_networkadapter_guids())["mapguids"]
	guid = guids[adaptername]
	print "def get_networkadapter_guid: adaptername = '%s' guid = '%s'" % (adaptername,guid)
	return guid
	#return get_networkadapterlist_from_guids(get_networkadapter_guids())["mapguids"][adaptername]

def get_tapadapters(OPENVPN_EXE,INTERFACES):
	if os.path.isfile(OPENVPN_EXE):
		string = '"%s" --show-adapters' % (OPENVPN_EXE)
		TAPADAPTERS = subprocess.check_output("%s" % (string),shell=True)
		TAPADAPTERS = TAPADAPTERS.split('\r\n')
		TAPADAPTERS.pop(0)
		TAP_DEVS = list()
		for line in TAPADAPTERS:
			for INTERFACE in INTERFACES:
				if line.startswith("'%s' {"%(INTERFACE)) and len(line) >= 1:
					INTERFACES.remove(INTERFACE)
					TAP_DEVS.append(INTERFACE)
					break
		return { "INTERFACES":INTERFACES,"TAP_DEVS":TAP_DEVS }

def get_interface_infos_from_guid(guid):
	print "winregs: def get_interface_infos_from_guid(%s)" % (guid)
	"""
	winregs.get_interface_infos_from_guid("{XXXXXXXX-YYYY-ZZZZ-AAAA-CCCCDDDDEEEE}")
	return = {
			'AddressType': 0, 'DefaultGateway': [u'192.168.1.1'], 'SubnetMask': [u'255.255.255.0'],
			'NameServer': u'8.8.8.8,8.8.4.4', 'IPAddress': [u'192.168.1.123'], 
			'DhcpServer': u'255.255.255.255', 'DhcpIPAddress': u'0.0.0.0'}, 'DhcpSubnetMask': u'255.0.0.0'
	"""
	values = { "AddressType":False, "DefaultGateway":False, "IPAddress":False, "SubnetMask":False, "NameServer":False, "DhcpIPAddress":False, "DhcpServer":False, "DhcpSubnetMask":False }
	reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	key = OpenKey(reg, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\%s' % (guid))
	for keyname,value in values.items():
		values[keyname] = QueryValueEx(key, keyname)[0]
	print "get_interface_infos_from_guid: '%s'" % (values)
	return values








"""
def _win32_is_nic_enabled(self, lm, guid, interface_key):
         # Look in the Windows Registry to determine whether the network
         # interface corresponding to the given guid is enabled.
         #
         # (Code contributed by Paul Marks, thanks!)
         #
         try:
             # This hard-coded location seems to be consistent, at least
             # from Windows 2000 through Vista.
             connection_key = _winreg.OpenKey(
                 lm,
                 r'SYSTEM\CurrentControlSet\Control\Network'
                 r'\{4D36E972-E325-11CE-BFC1-08002BE10318}'
                 r'\%s\Connection' % guid)

             try:
                 # The PnpInstanceID points to a key inside Enum
                 (pnp_id, ttype) = _winreg.QueryValueEx(
                     connection_key, 'PnpInstanceID')

                 if ttype != _winreg.REG_SZ:
                     raise ValueError

                 device_key = _winreg.OpenKey(
                     lm, r'SYSTEM\CurrentControlSet\Enum\%s' % pnp_id)

                 try:
                     # Get ConfigFlags for this device
                     (flags, ttype) = _winreg.QueryValueEx(
                         device_key, 'ConfigFlags')

                     if ttype != _winreg.REG_DWORD:
                         raise ValueError

                     # Based on experimentation, bit 0x1 indicates that the
                     # device is disabled.
                     return not (flags & 0x1)

                 finally:
                     device_key.Close()
             finally:
                 connection_key.Close()
         except (EnvironmentError, ValueError):
             # Pre-vista, enabled interfaces seem to have a non-empty
             # NTEContextList; this was how dnspython detected enabled
             # nics before the code above was contributed.  We've retained
             # the old method since we don't know if the code above works
             # on Windows 95/98/ME.
             try:
                 (nte, ttype) = _winreg.QueryValueEx(interface_key,
                                                     'NTEContextList')
                 return nte is not None
             except WindowsError:
                 return False
"""