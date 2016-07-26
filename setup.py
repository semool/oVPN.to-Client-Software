from distutils.core import setup
import py2exe
import sys, os, site, shutil, time
import platform
import release_version

appversion = release_version.setup_data()["version"]
cpu = 'x86'
crt = 'Microsoft.VC90.CRT_win32'
if platform.architecture()[0] == '64bit':
	cpu = 'amd64'
	crt = 'Microsoft.VC90.CRT_win64'

manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" xmlns:asmv3="urn:schemas-microsoft-com:asm.v3" manifestVersion="1.0">
	<assemblyIdentity
		version="{APPVERSION}"
		processorArchitecture="{CPU}"
		name="oVPN.to Client"
		type="win32"
	/>
	<description>oVPN.to Client</description>
	<asmv3:trustInfo xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
		<asmv3:security>
			<asmv3:requestedPrivileges>
				<asmv3:requestedExecutionLevel
				level="requireAdministrator"
				uiAccess="false" />
			</asmv3:requestedPrivileges>
		</asmv3:security>
	</asmv3:trustInfo>
	<asmv3:application>
		<asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">'
			<dpiAware>true</dpiAware>
		</asmv3:windowsSettings>
	</asmv3:application>
	<dependency>
		<dependentAssembly>
			<assemblyIdentity
				type="win32"
				name="Microsoft.Windows.Common-Controls"
				version="6.0.0.0"
				processorArchitecture="{CPU}"
				publicKeyToken="6595b64144ccf1df"
				language="*"
			/>
		</dependentAssembly>
	</dependency>
	<dependency>
		<dependentAssembly>
			<assemblyIdentity
				type="win32"
				name="Microsoft.VC90.CRT"
				version="9.0.30729.4940"
				processorArchitecture="{CPU}"
				publicKeyToken="1fc8b3b9a1e18e3b"
				language="*"
			/>
		</dependentAssembly>
	</dependency>
</assembly>
'''.format(APPVERSION=appversion, CPU=cpu)

site_dir = site.getsitepackages()[1] 
include_dll_path = os.path.join(site_dir, 'gnome')

gtk_dirs_to_include = ['etc\\fonts', 'lib\\gtk-3.0', 'lib\\girepository-1.0', 'share\\glib-2.0', 'share\\icons\\hicolor', 'share\\icons\\Adwaita\\scalable', 'share\\icons\\Adwaita\\32x32', 'share\\locale']

gtk_dlls = []
tmp_dlls = []
cdir = os.getcwd() 
for dll in os.listdir(include_dll_path):
	if dll.lower().endswith('.dll'):
		gtk_dlls.append(os.path.join(include_dll_path, dll))
		tmp_dlls.append(os.path.join(cdir, dll))

for dll in gtk_dlls:
	shutil.copy(dll, cdir)

print release_version.setup_data()
print "\nCHECK DATA, sleeping 10s!\n"
time.sleep(10)
setup_dict = dict(
	version = release_version.setup_data()["version"],
	name = release_version.setup_data()["name"],
	description = release_version.setup_data()["description"],
	data_files = [('Microsoft.VC90.CRT',['includes/'+crt+'/Microsoft.VC90.CRT.manifest','includes/'+crt+'/msvcp90.dll','includes/'+crt+'/msvcr90.dll']),],
	zipfile = None,
	windows=[
		{
			"script":release_version.setup_data()["script"],
			"icon_resources" : [(1, 'else\\app_icons\\shield_exe.ico')],
			"copyright" : "Copyright %s" % (release_version.setup_data()["copyright"]),
			"company_name" : "%s %s" % (release_version.org_data()["ORG"],release_version.org_data()["ADD"]),
			"other_resources" : [(24,1,manifest)],
		}
	],
	options={
		'py2exe': {
		'bundle_files' : 3,
		'compressed'   : False,
		'unbuffered'   : False,
		'includes'     : [ 'gi','requests','cairo','types','os','platform','sys','hashlib','random','time','zipfile','subprocess','threading','socket','random','gettext','locale','_winreg','base64' ],
		'excludes'     : [  ],
		'optimize'     : 2,
		'packages'     : [ 'gi' ],
		'dll_excludes' : [ 'crypt32.dll','tcl85.dll', 'tk85.dll','DNSAPI.DLL','USP10.DLL','MPR.DLL','MSIMG32.DLL','API-MS-Win-Core-LocalRegistry-L1-1-0.dll','IPHLPAPI.DLL','w9xpopen.exe','mswsock.dll','powrprof.dll']
		}
	}
)

setup(**setup_dict)
setup(**setup_dict)

dest_dir = os.path.join(cdir, 'dist')

if not os.path.exists(dest_dir):
	os.makedirs(dest_dir)

for dll in tmp_dlls:
	shutil.copy(dll, dest_dir)
	os.remove(dll)

for d in gtk_dirs_to_include:
	shutil.copytree(os.path.join(site_dir, 'gnome', d), os.path.join(dest_dir, d))
