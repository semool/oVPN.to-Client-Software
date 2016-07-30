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
	reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	reg_key = OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
	for i in range(len(iface_guids)):
		try:
			reg_subkey = OpenKey(reg_key, iface_guids[i] + r'\Connection')
			iface_name = QueryValueEx(reg_subkey, 'Name')[0]
			iface_names[i] = iface_name
		except:
			pass
	return iface_names

def get_networkadapterlist():
	newlist = []
	list1 = get_networkadapterlist_from_guids(get_networkadapter_guids())
	list2 = get_networkadapterlist_from_netsh()
	for name in list1:
		for line in list2:
			if line.endswith(name):
				newlist.append(name)
	return newlist

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