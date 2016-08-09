from distutils.core import setup
import py2exe
import sys, os, site, shutil, time
import platform
import struct
import release_version

BITS = struct.calcsize("P") * 8

SOURCEDIR = os.getcwd()
DIST_DIR = "%s\\%s" % (SOURCEDIR,release_version.setup_data()["DIST_DIR3"])
BUILD_DIR = "%s\\build%s" % (SOURCEDIR,BITS)

print "version_data() = '%s'" % (release_version.version_data())
print "build_data() = '%s'" % (release_version.build_data())
print "org_data() = '%s'" % (release_version.org_data())
print "setup_data() = '%s'" % (release_version.setup_data())

setup_dict = dict(
	version = release_version.setup_data()["version"],
	name = release_version.setup_data()["name"]+" CMD",
	description = release_version.setup_data()["description"]+" CMD",
	zipfile = None,
	console=[
		{
			"script":release_version.setup_data()["script_cmd"],
			"icon_resources" : [(1, 'else\\app_icons\\shield_exe.ico')],
			"copyright" : "Copyright %s" % (release_version.setup_data()["copyright"]),
			"company_name" : "%s %s" % (release_version.org_data()["ORG"],release_version.org_data()["ADD"]),
		}
	],
	options={
		'build': {'build_base': BUILD_DIR },
		'py2exe': {
		'dist_dir': DIST_DIR,
		'bundle_files' : 1,
		'optimize'     : 2,
		'skip_archive' : False,
		'compressed'   : True,
		'unbuffered'   : False,
		'includes'     : release_version.setup_data()["py2exe_includes_cmd"],
		'excludes'     : release_version.setup_data()["py2exe_excludes"],
		'packages'     : [ ],
		'dll_excludes' : release_version.setup_data()["dll_excludes"],
		}
	}
)

setup(**setup_dict)
setup(**setup_dict)