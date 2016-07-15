
# oVPN.to Client Software for Windows

## Setup 32 Bit Dev-Env:
+ [Python 2.7.12 win32](https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi) (install to C:\Python27) !!!
+ [py2exe 0.6.9 win32](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download)
+ [crypt32.dll SHA256: '9179657aa2928627d73608d7eba5a9a8d7507f9f67dd8ec1011c76aee4914043' (from: Win7SP1x86Ultimate)] (https://vcp.ovpn.to/files/ovpn_cli/crypt32_win32.7z)

+ open cmd.exe as admin:
+ C:\Python27\Scripts\pip.exe install --upgrade pip
+ C:\Python27\Scripts\pip.exe install pycrypto
+ C:\Python27\Scripts\pip.exe install requests


## Setup 64 Bit Dev-Env:
+ [Python 2.7.12 win64](https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi) (install to C:\Python27_64) !!!
+ [py2exe 0.6.9 win64](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win64-py2.7.amd64.exe/download)
+ [crypt32.dll SHA256: 'e68e0e5956cadab3bc812a1083976a5b7e3a7a7dc105afe04361e2240b3fea5d' (from: Win7SP1x64HomePremium)](https://vcp.ovpn.to/files/ovpn_cli/crypt32_win64.7z)

+ open cmd.exe as admin:
+ C:\Python27_64\Scripts\pip.exe install --upgrade pip
+ C:\Python27_64\Scripts\pip.exe install pycrypto
+ C:\Python27_64\Scripts\pip.exe install requests


## Basic Requirements:
+ [PyGObject 3.18.2 AIO](https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev7-setup.exe/download) Select only: 'Base packages' + 'GTK+ 3.18.9' and install into 32 and 64 bit!
+ [7-zip SFX Builder](http://sourceforge.net/projects/s-zipsfxbuilder/)
+ [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266)
+ [7-zip 16.02 x64](http://7-zip.org/a/7z1602-x64.exe)

## Developer Imports: how to run or build from source
+ create a link (name: DEBUG32) to debug.bat: edit link, set target 'X:\????\ovpn-client\debug.bat 32' and run link as admin!
+ create a link (name: BUILD32) to build.bat: edit link, set target 'X:\????\ovpn-client\build.bat 32' and run link normally!
+ same for 64 bits!
+ do not run any of the *.bat files directly! you need links do 'debug.bat' and 'build.bat' with bits argument!
+ edit 'set_version.bat' and 'set_dirs.bat' to your needs!
+ go to includes folder and unzip 'Adwaita.7z' + 'MS-Windows.7z'
+ put 'crypt32_win32.dll' + 'crypt_win64.dll' into 'includes/' for working cross-builds

## Generate locales:
+ run generate_po.bat
+ start poedit 1.8+
+ open file 'locale/de/ovpn_client.po'
+ catalog -> update from POT -> './messages.pot'