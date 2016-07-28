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
DISTDIR = "%s\\dist_check_bin" % (SOURCEDIR)
BINARY = "%s\\check_bin.exe" % (DISTDIR)

SIGNTOOL="E:\\codesign\\bin_w10sdk\\signtool.exe"
SIGNCERTSHA1="0775a45c76fad6989cbeb35c87e476642ccc172f"
SIGN_SIZE=24500 # quad-sign
SIGN_SIZE=4612 # CMD1

setup_dict = dict(
	version = release_version.setup_data()["version"],
	name = release_version.setup_data()["name"],
	description = release_version.setup_data()["description"],
	data_files = [('Microsoft.VC90.CRT',['includes/'+crt+'/Microsoft.VC90.CRT.manifest','includes/'+crt+'/msvcp90.dll','includes/'+crt+'/msvcr90.dll']),],
	zipfile = None,
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
		'dist_dir': DISTDIR,
		'bundle_files' : 1,
		'compressed'   : True,
		'unbuffered'   : False,
		'includes'     : [ 'os','sys','time','hashlib','struct','subprocess','threading' ],
		'excludes'     : [ ],
		'optimize'     : 2,
		'packages'     : [ ],
		'dll_excludes' : [ 'crypt32.dll','tcl85.dll', 'tk85.dll','DNSAPI.DLL','USP10.DLL','MPR.DLL','MSIMG32.DLL','API-MS-Win-Core-LocalRegistry-L1-1-0.dll','IPHLPAPI.DLL','w9xpopen.exe','mswsock.dll','powrprof.dll']
		}
	}
)
setup(**setup_dict)


def sign_py2exe(BINARY):
	if not os.path.isfile(SIGNTOOL):
		print "SINGTOOL '%s' NOT FOUND" % (SIGNTOOL)
		sys.exit()
	
	 #First, sign a *copy* of the file so that we know its final size.
	EXECOPY = os.path.join(os.path.dirname(BINARY),"temp-" + os.path.basename(BINARY))
	if os.path.isfile(EXECOPY):
		os.unlink(EXECOPY)
	EXECOPY1 = os.path.join(os.path.dirname(BINARY),"unsigned-" + os.path.basename(BINARY))
	if os.path.isfile(EXECOPY1):
		os.unlink(EXECOPY1)
	print "\nCOPY BINARY '%s' to EXECOPY '%s'" % (BINARY,EXECOPY)
	shutil.copy2(BINARY, EXECOPY)
	shutil.copy2(BINARY, EXECOPY1)
	SIGNTOOLCMDS = []
	SIGNTOOLCMD1="%s sign /sha1 %s /fd sha1 /t http://timestamp.comodoca.com/?td=sha1 %s" % (SIGNTOOL,SIGNCERTSHA1,EXECOPY)
	SIGNTOOLCMD2="%s sign /as /sha1 %s /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256 %s" % (SIGNTOOL,SIGNCERTSHA1,EXECOPY)
	SIGNTOOLCMD3="%s sign /as /sha1 %s /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384 %s" % (SIGNTOOL,SIGNCERTSHA1,EXECOPY)
	SIGNTOOLCMD4="%s sign /as /sha1 %s /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512 %s" % (SIGNTOOL,SIGNCERTSHA1,EXECOPY)
	#SIGNTOOLCMDS = [SIGNTOOLCMD1,SIGNTOOLCMD2,SIGNTOOLCMD3,SIGNTOOLCMD4]
	SIGNTOOLCMDS = [SIGNTOOLCMD1]
	for CMD in SIGNTOOLCMDS:
		print CMD
		subprocess.check_call(CMD)
	print "\nCOPY SIGNED"
	
	# Figure out the size of the appended signature.
	SIGNED_SIZE = int(os.stat(EXECOPY).st_size - os.stat(BINARY).st_size)
	#os.unlink(EXECOPY)
	print "\nSIGNED_SIZE = '%s'" % (SIGNED_SIZE)
	if not SIGNED_SIZE == SIGN_SIZE:
		print "\nINVALID SIGNED_SIZE != %s" % (SIGN_SIZE)
		return False
	
	# Write the correct comment size as the last two bytes of the file.
	with open(BINARY, "r+b") as f:
		offset = None
		f.seek(-2, os.SEEK_END)

		struct_data = struct.pack("<H", SIGNED_SIZE)
		#struct_data = struct.pack("1i", SIGNED_SIZE)
		f.write(struct_data)
		
		string = 0
		
		#f.seek(0, os.SEEK_END)
		#struct_data = struct.pack("<H", string)
		#f.write(struct_data)
		
		#f.seek(0, os.SEEK_END)
		#struct_data = struct.pack("<H", string)
		#f.write(struct_data)
		
	print "\nCOMMENT WRITTEN TO BINARY '%s'" % (BINARY)
	sys.exit()
	# Now we can sign the file for real.
	SIGNTOOLCMD1="%s sign /sha1 %s /fd sha1 /t http://timestamp.comodoca.com/?td=sha1 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	SIGNTOOLCMD2="%s sign /as /sha1 %s /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	SIGNTOOLCMD3="%s sign /as /sha1 %s /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	SIGNTOOLCMD4="%s sign /as /sha1 %s /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512 %s" % (SIGNTOOL,SIGNCERTSHA1,BINARY)
	#SIGNTOOLCMDS = [SIGNTOOLCMD1,SIGNTOOLCMD2,SIGNTOOLCMD3,SIGNTOOLCMD4]
	SIGNTOOLCMDS = [SIGNTOOLCMD1]
	for CMD in SIGNTOOLCMDS:
		print CMD
		subprocess.check_call(CMD)
	print "\nSIGNED BINARY '%s'" % (BINARY)

sign_py2exe(BINARY)
