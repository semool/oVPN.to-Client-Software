
# oVPN.to Client Software for Windows

## Setup 32 Bit Dev-Env:
+ [Python 2.7.12 win32](https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi) (install to C:\Python27) !!!
+ [py2exe 0.6.9 win32](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download)

+ open cmd.exe as admin:
+ C:\Python27\Scripts\pip.exe install --upgrade pip
+ C:\Python27\Scripts\pip.exe install pycrypto (not needed atm)
+ C:\Python27\Scripts\pip.exe install requests


## Setup 64 Bit Dev-Env:
+ [Python 2.7.12 win64](https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi) (install to C:\Python27_64) !!!
+ [py2exe 0.6.9 win64](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win64-py2.7.amd64.exe/download)

+ open cmd.exe as admin:
+ C:\Python27_64\Scripts\pip.exe install --upgrade pip
+ C:\Python27_64\Scripts\pip.exe install pycrypto (not needed atm)
+ C:\Python27_64\Scripts\pip.exe install requests


## Basic Requirements:
+ [PyGObject 3.18.2 AIO](https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev7-setup.exe/download) Select only: 'Base packages' + 'GTK+ 3.18.9' and install into 32 and 64 bit!
+ [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266)
+ [Inno Setup 5.5.9](http://www.jrsoftware.org/download.php/is.exe)

## Developer Imports: how to run or build from source
+ create a link (name: DEBUG32) to debug.bat: edit link, set target 'X:\????\ovpn-client\debug.bat 32' and run link as admin!
+ create a link (name: BUILD32) to build_inno.bat: edit link, set target 'X:\????\ovpn-client\build_inno.bat 32' and run link normally!
+ same for 64 bits and do NOT run any of the *.bat files directly!
+ edit 'set_dirs.bat' to your needs!
+ Update Version only in file: 'release_version.py'

## Generate locales:
+ run generate_po.bat
+ start poedit 1.8+
+ open file 'locale/de/ovpn_client.po'
+ catalog -> update from POT -> './messages.pot'