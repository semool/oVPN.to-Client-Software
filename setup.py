from distutils.core import setup
import py2exe
import sys, os, site, shutil, time
import struct
import release_version

BITS = struct.calcsize("P") * 8
appversion = release_version.setup_data()["version"]
cpu = 'x86'
inno = 'win32'
crt = 'Microsoft.VC90.CRT_win32'
if BITS == 64:
	cpu = 'amd64'
	inno = 'win64'
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
			<dpiAware>true/PM</dpiAware>
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
DIST_DIR = "%s\\%s" % (SOURCEDIR,release_version.setup_data()["DIST_DIR1"])
BUILD_DIR = "%s\\build%s" % (SOURCEDIR,BITS)

site_dir = site.getsitepackages()[1] 
include_dll_path = os.path.join(site_dir, 'gnome')

gtk_dirs_to_include = ['etc\\fonts', 'lib\\gtk-3.0', 'lib\\girepository-1.0', 'share\\glib-2.0', 'share\\icons\\hicolor', 'share\\icons\\Adwaita\\scalable', 'share\\icons\\Adwaita\\32x32', 'share\\locale']

gtk_dlls = []
tmp_dlls = []
tmpdir = SOURCEDIR+"\\tmp"
tmpdlldir = tmpdir+"\\dll"

if not os.path.exists(tmpdlldir):
	os.makedirs(tmpdlldir)

for dll in os.listdir(include_dll_path):
	if dll.lower().endswith('.dll'):
		gtk_dlls.append(os.path.join(include_dll_path, dll))
		tmp_dlls.append(os.path.join(tmpdlldir, dll))

for dll in gtk_dlls:
	shutil.copy(dll, tmpdlldir)

setup_dict = dict(
	version = release_version.setup_data()["version"],
	name = release_version.setup_data()["name"],
	description = release_version.setup_data()["description"],
	data_files = [('Microsoft.VC90.CRT',['includes/'+crt+'/Microsoft.VC90.CRT.manifest','includes/'+crt+'/msvcp90.dll','includes/'+crt+'/msvcr90.dll']),],
	zipfile = 'ovpn_client.lib',
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
		'build': {'build_base': BUILD_DIR },
		'py2exe': {
		'dist_dir': DIST_DIR,
		'bundle_files' : 3,
		'optimize'     : 2,
		'skip_archive' : False,
		'compressed'   : False,
		'unbuffered'   : False,
		'includes'     : release_version.setup_data()["py2exe_includes"],
		'excludes'     : release_version.setup_data()["py2exe_excludes"],
		'packages'     : [ 'gi' ],
		'dll_excludes' : release_version.setup_data()["dll_excludes"],
		}
	}
)

setup(**setup_dict)
setup(**setup_dict)

if not os.path.exists(DIST_DIR):
	os.makedirs(DIST_DIR)

for dll in tmp_dlls:
	shutil.copy(dll, DIST_DIR)
	os.remove(dll)

for d in gtk_dirs_to_include:
	shutil.copytree(os.path.join(site_dir, 'gnome', d), os.path.join(DIST_DIR, d))

innoscript = "%s\\inno_setup.iss" % (SOURCEDIR)
ind = open(innoscript, "w")
print >> ind, ';!!!DONT EDIT THIS FILE MANUALLY, IT WILL BE OVERWRITTEN IN NEXT BUILD RUN!!!'
print >> ind, '#define AppExeName "%s"' % release_version.setup_data()["exename"]
print >> ind, '#define Version "%s"' % release_version.version_data()["VERSION"]
print >> ind, '#define AppName "%s"' % release_version.version_data()["NAME"]
print >> ind, '#define AppDir "%s"' % release_version.version_data()["NAME"]
print >> ind, '#define AppPublisher "%s %s"' % (release_version.org_data()["ORG"],release_version.org_data()["ADD"])
print >> ind, '#define AppURL "%s"' % release_version.org_data()["SITE"]
print >> ind, '[Setup]'
print >> ind, 'AppVersion=v{#Version}-gtk3_%s' % inno
print >> ind, 'AppVerName={#AppName} v{#Version}-gtk3_%s' % inno
print >> ind, 'AppSupportURL=%s' % release_version.org_data()["SUPPORT"]
print >> ind, 'AppUpdatesURL=%s' % release_version.org_data()["UPDATES"]
print >> ind, 'AppCopyright=Copyright %s'  % release_version.setup_data()["copyright"]
print >> ind, 'OutputBaseFilename=ovpn_client_v{#Version}-gtk3_%s_setup' % inno
if release_version.version_data()["SIGN"] == True:
	print >> ind, 'SignTool=signtool1'
	#print >> ind, 'SignTool=signtool2'
	#print >> ind, 'SignTool=signtool3'
	print >> ind, 'SignTool=signtool4'
if inno == "win32":
	print >> ind, 'DefaultDirName={pf}\{#AppDir}'
else:
	print >> ind, 'DefaultDirName={pf64}\{#AppDir}'
print >> ind, 'SignedUninstaller=yes'
print >> ind, 'Compression=lzma2/max'
print >> ind, 'SolidCompression=yes'
print >> ind, 'AppId={{991F58FC-8D40-4B45-B434-6A10AAC12FBA}'
print >> ind, 'AppName={#AppName}'
print >> ind, 'AppMutex={#AppExeName},Global\{#AppExeName}'
print >> ind, 'SetupMutex={#AppDir},Global\{#AppDir}'
print >> ind, 'AppPublisher={#AppPublisher}'
print >> ind, 'AppContact={#AppPublisher}'
print >> ind, 'AppPublisherURL={#AppURL}'
print >> ind, 'AppReadmeFile={#AppURL}'
print >> ind, 'VersionInfoVersion=0.{#Version}'
print >> ind, 'DefaultGroupName={#AppName}'
print >> ind, 'AllowNoIcons=yes'
print >> ind, 'OutputDir=.'
print >> ind, 'SetupIconFile=else\\app_icons\shield_exe.ico'
print >> ind, 'WizardImageFile=else\\app_icons\shield_exe_2.bmp'
print >> ind, 'WizardSmallImageFile=else\\app_icons\shield_exe.bmp'
print >> ind, 'WizardImageStretch=no'
print >> ind, 'UninstallDisplayIcon={app}\{#AppExeName}'
print >> ind, "Uninstallable=not IsTaskSelected('portablemode')"
print >> ind, 'DisableDirPage=no'
print >> ind, 'LicenseFile=LICENSE'
print >> ind, 'LanguageDetectionMethod=uilanguage'
print >> ind, 'ShowLanguageDialog=auto'
print >> ind, '[Tasks]'
print >> ind, 'Name: portablemode; Description: "Portable Mode"; Flags: unchecked'
print >> ind, '[InstallDelete]'
print >> ind, 'Type: files; Name: "{userdesktop}\oVPN.to Client.lnk";'
print >> ind, 'Type: files; Name: "{commondesktop}\oVPN.to Client.lnk";'
print >> ind, 'Type: filesandordirs; Name: {app}\dns\;'
print >> ind, 'Type: filesandordirs; Name: {app}\etc\;'
print >> ind, 'Type: filesandordirs; Name: {app}\lib\;'
print >> ind, 'Type: filesandordirs; Name: {app}\locale\;'
print >> ind, 'Type: filesandordirs; Name: {app}\share\;'
print >> ind, 'Type: filesandordirs; Name: {app}\ico\;'
print >> ind, 'Type: filesandordirs; Name: {app}\Microsoft.VC90.CRT\;'
print >> ind, 'Type: files; Name: {app}\*.dll;'
print >> ind, 'Type: files; Name: {app}\*.pyd;'
print >> ind, 'Type: files; Name: {app}\*.lib;'
print >> ind, 'Type: files; Name: {app}\*.pem;'
print >> ind, 'Type: files; Name: {app}\{#AppExeName};'
print >> ind, '[Languages]'
print >> ind, 'Name: "english"; MessagesFile: "compiler:Default.isl"'
print >> ind, 'Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"'
print >> ind, 'Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"'
print >> ind, 'Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"'
print >> ind, 'Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"'
print >> ind, 'Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"'
print >> ind, 'Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"'
print >> ind, 'Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"'
print >> ind, 'Name: "french"; MessagesFile: "compiler:Languages\French.isl"'
print >> ind, 'Name: "german"; MessagesFile: "compiler:Languages\German.isl"'
print >> ind, 'Name: "greek"; MessagesFile: "compiler:Languages\Greek.isl"'
print >> ind, 'Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"'
print >> ind, 'Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"'
print >> ind, 'Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"'
print >> ind, 'Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"'
print >> ind, 'Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"'
print >> ind, 'Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"'
print >> ind, 'Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"'
print >> ind, 'Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"'
print >> ind, 'Name: "scottishgaelic"; MessagesFile: "compiler:Languages\ScottishGaelic.isl"'
print >> ind, 'Name: "serbiancyrillic"; MessagesFile: "compiler:Languages\SerbianCyrillic.isl"'
print >> ind, 'Name: "serbianlatin"; MessagesFile: "compiler:Languages\SerbianLatin.isl"'
print >> ind, 'Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"'
print >> ind, 'Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"'
print >> ind, 'Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"'
print >> ind, 'Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"'
print >> ind, '[Tasks]'
print >> ind, 'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
print >> ind, '[Components]'
print >> ind, 'Name: "main"; Description: "%s"; Types: full compact custom; Flags: fixed' % release_version.version_data()["NAME"]
print >> ind, 'Name: "languages"; Description: "Languages"; Types: full'
print >> ind, 'Name: "languages\deutsch"; Description: "Deutsch"; Types: full'
print >> ind, 'Name: "languages\espanol"; Description: "Espanol"; Types: full'
print >> ind, 'Name: "themes"; Description: "Themes"; Types: full'
print >> ind, 'Name: "themes\AdwaitaDark"; Description: "AdwaitaDark"; Types: full'
print >> ind, 'Name: "themes\FlatRemixOS"; Description: "FlatRemixOS"; Types: full'
print >> ind, 'Name: "themes\Greybird"; Description: "Greybird"; Types: full'
print >> ind, 'Name: "themes\Windows"; Description: "Windows"; Types: full'
print >> ind, '[Files]'
print >> ind, 'Source: "%s\*"; DestDir: "{app}"; Flags:replacesameversion' % (DIST_DIR)
print >> ind, 'Source: "%s\\appdata\*"; DestDir: "{app}\\appdata\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\etc\*"; DestDir: "{app}\etc\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\lib\*"; DestDir: "{app}\lib\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\Microsoft.VC90.CRT\*"; DestDir: "{app}\Microsoft.VC90.CRT\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\share\glib-2.0\*"; DestDir: "{app}\share\glib-2.0\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\share\icons\*"; DestDir: "{app}\share\icons\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\share\locale\locale.alias"; DestDir: "{app}\share\locale\"; Flags:replacesameversion' % (DIST_DIR)
print >> ind, 'Source: "%s\share\locale\en\*"; DestDir: "{app}\share\locale\en\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\share\\themes\\Adwaita\*"; DestDir: "{app}\share\\themes\\Adwaita\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR)
print >> ind, 'Source: "%s\locale\de\*"; DestDir: "{app}\locale\de\"; Flags:replacesameversion recursesubdirs; Components: languages\deutsch' % (DIST_DIR)
print >> ind, 'Source: "%s\share\locale\de\*"; DestDir: "{app}\share\locale\de\"; Flags:replacesameversion recursesubdirs; Components: languages\deutsch' % (DIST_DIR)
print >> ind, 'Source: "%s\locale\es\*"; DestDir: "{app}\locale\es\"; Flags:replacesameversion recursesubdirs; Components: languages\espanol' % (DIST_DIR)
print >> ind, 'Source: "%s\share\locale\es\*"; DestDir: "{app}\share\locale\es\"; Flags:replacesameversion recursesubdirs; Components: languages\espanol' % (DIST_DIR)
print >> ind, 'Source: "%s\share\\themes\\Adwaita-dark\*"; DestDir: "{app}\\share\\themes\\Adwaita-dark\"; Flags:replacesameversion recursesubdirs; Components: themes\AdwaitaDark' % (DIST_DIR)
print >> ind, 'Source: "%s\share\\themes\\Flat-Remix-OS\*"; DestDir: "{app}\\share\\themes\\Flat-Remix-OS\"; Flags:replacesameversion recursesubdirs; Components: themes\FlatRemixOS' % (DIST_DIR)
print >> ind, 'Source: "%s\share\\themes\\Greybird\*"; DestDir: "{app}\share\\themes\\Greybird\"; Flags:replacesameversion recursesubdirs; Components: themes\Greybird' % (DIST_DIR)
print >> ind, 'Source: "%s\share\\themes\\MS-Windows\*"; DestDir: "{app}\share\\themes\\MS-Windows\"; Flags:replacesameversion recursesubdirs; Components: themes\Windows' % (DIST_DIR)
print >> ind, '[Icons]'
print >> ind, 'Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"'
print >> ind, 'Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"'
print >> ind, 'Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon'
print >> ind, '[Registry]'
print >> ind, 'Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: string; ValueName: "{app}\{#AppExeName}"; ValueData: "~ HIGHDPIAWARE"; Flags: noerror uninsdeletevalue'
