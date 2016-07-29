from distutils.core import setup
import py2exe, sys, os, site, shutil, time, platform, struct, subprocess
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

SOURCEDIR = os.getcwd()
DIST_DIR = "%s\\%s" % (SOURCEDIR,release_version.setup_data()["DIST_DIR2"])
BINARY = "%s\\check_bin.exe" % (DIST_DIR)

SIGNTOOL="E:\\codesign\\bin_w10sdk\\signtool.exe"
SIGNCERTSHA1="0775a45c76fad6989cbeb35c87e476642ccc172f"

setup_dict = dict(
	version = release_version.setup_data()["version"],
	name = release_version.setup_data()["name"],
	description = release_version.setup_data()["description"],
	data_files = [('Microsoft.VC90.CRT',['includes/'+crt+'/Microsoft.VC90.CRT.manifest','includes/'+crt+'/msvcp90.dll','includes/'+crt+'/msvcr90.dll']),],
	zipfile = "check_bin.lib",
	windows=[
		{
			"script":"check_bin.py",
			"icon_resources" : [(1, 'else\\app_icons\\shield_exe.ico')],
			"copyright" : "Copyright %s" % (release_version.setup_data()["copyright"]),
			"company_name" : "%s %s" % (release_version.org_data()["ORG"],release_version.org_data()["ADD"]),
			"other_resources" : [(24,1,manifest)],
		}
	],
	options={
		'py2exe': {
		'dist_dir': DIST_DIR,
		'bundle_files' : 1,
		'optimize'     : 2,
		'skip_archive' : False,
		'compressed'   : True,
		'unbuffered'   : False,
		'includes'     : [ 'os','sys','time','hashlib','struct','subprocess','threading' ],
		'excludes'     : release_version.setup_data()["py2exe_excludes"],
		'packages'     : [ ],
		'dll_excludes' : [ 'pywintypes27.dll','crypt32.dll','tcl85.dll', 'tk85.dll','DNSAPI.DLL','USP10.DLL','MPR.DLL','MSIMG32.DLL','API-MS-Win-Core-LocalRegistry-L1-1-0.dll','IPHLPAPI.DLL','w9xpopen.exe','mswsock.dll','powrprof.dll']
		}
	}
)

setup(**setup_dict)
setup(**setup_dict)

def sign_py2exe(BINARY):
	if not os.path.isfile(SIGNTOOL):
		print "SINGTOOL '%s' NOT FOUND" % (SIGNTOOL)
		sys.exit()
	
	SIGNTOOLCMD1="%s sign /sha1 %s /fd sha1 /t http://timestamp.comodoca.com/?td=sha1 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	#SIGNTOOLCMD2="%s sign /as /sha1 %s /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	#SIGNTOOLCMD3="%s sign /as /sha1 %s /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	SIGNTOOLCMD4="%s sign /as /sha1 %s /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	SIGNTOOLCMDS = [SIGNTOOLCMD1,SIGNTOOLCMD4]
	for CMD in SIGNTOOLCMDS:
		print CMD
		subprocess.check_call(CMD)
	print "\nSIGNED BINARY '%s'" % (BINARY)

sign_py2exe(BINARY)
