# -*- coding: utf-8 -*-
import os, time, subprocess, sys, json
from datetime import datetime
import shlex
import win32process

# .py file imports
from debug import debug
from debug import devmode
import release_version
import hashings
import signtool
import encodes


def values(DEBUG):
    debug(9,"[openvpn.py] def values()",DEBUG,True)
    try:
        ARCH = get_arch(DEBUG)
        BUILT = "Dec 7 2016"
        LATEST = "2314"
        TIMESTAMP = 1481065200
        VERSION = "2.3.14"
        BUILT_V = "I601"
        
        OPENVPN_FILEHASHS ={
                            "openvpn-install-2.3.14-I601-i686.exe": \
                                {"libeay32.dll": "8952625b84146959dc2177255d92117372beba8b9d6463c61e4bbae5c98c0febfaf11adbb89e78ba5e5392e83e81085a97811aded6405a20209b98ef52e2a327", \
                                "openvpn.exe": "1ae87c9129040a33192291887cf9dcc68759655cbcf71eeb94b701aef0cc17a31fe83277312817d7563e4e433c2c4c97bb96436c5a1f0facf203fd7a12561adf", \
                                "openvpnserv.exe": "7efa425ae67579ef6908022d851ed029dd7a172d946b2b3bf1c9960db8e549787768999a6768889d25cb3345b64fe9ea67f6f05a022c467890b967938e98e10c", \
                                "liblzo2-2.dll": "0e98459fbd168dd5bd241facc4b479b5654ec0eab24315ad0cb82d447395a13fadc89ca229bf46bfc58e3d2a6f4e57c85b98d412a752bd7b830ded5c2ce0f0ea", \
                                "openvpn-gui.exe": "31b63591c1975ed88dfc95a59eb3487fbbc131785298e91d8b9dafcb26ff139879556eb189230168a5feb1c17f02b80a9c135f583111727803dc9210ad00f1b3", \
                                "libpkcs11-helper-1.dll": "f3351e56893918ad644e9d509f429f216af122da22ccb2bff8a8e3161a91d6b0ea815e10ee0f040c8ce5be25a3a2364dfbbb7829123048e59733b721943d64d6", \
                                "ssleay32.dll": "e0dd310281572849bdde59dd87bd4d965937da4ee403ec96fd959b1da38cf21c660a0e04919775cd0b14dbb99a63e651502fd70b4784cf8f70d9ad6d92016662", \
                                "openssl.exe": "0c0d1671013f871505ecd2bd91d44c3b48bb8098f8f351c693d95ba9a3aab7fd75a2eb275081e847d733ac7be5f88d284a6304c2f94f51d834f04740c54a42d6"}, \
                            "openvpn-install-2.3.14-I601-x86_64.exe": \
                                {"libeay32.dll": "d27768d48f371f528a3778cb6c59a8452e2e9cf04cd95e64cb5563129e9857ea843b2da9c2f39e2981ab9b8c5101b772275004c1ed3ed0a820a92081a6e038e3", \
                                "openvpn.exe": "abe41e7c0eebfa542da9660f16892326d780938325d27685aa955edd9bf6e0dac2dc9d2b5649e0f958f86a802c41ce5ce924eab1e08754552a4fb079430ca29c", \
                                "openvpnserv.exe": "c7b1bfac2f354dfe5e4e2fac370df8cf1c12bb837104b9505a45aff292014e4052e064f049164f9f941ede847d589c7475ec1aca220cd5b554762c358c829720", \
                                "liblzo2-2.dll": "06923e5e2922e08a6dfaf0e6e8744545b565c0639c905f0fc75016c3b5e6d3744c08882c744a39b2612302be104b159ef4d2a4cc776d2f6b76bbf99d2fdefbd1", \
                                "openvpn-gui.exe": "403c265190d6cd779976d3ee8c8ec874e4db46782017c046ba8a775e3ef69a83e2560bbaca7ab07b3c0d22c111b8a40b503cbbeb593e387b92ff8fe3b04d9da2", \
                                "libpkcs11-helper-1.dll": "1f26958dc7155769dfdb3e77bab77ada418ace57c7fe2d5cf838159680146fcf860a66a6ecdc22dfb668fb34c14bc90417662c18f4e4956fb681d85a133b4c08", \
                                "ssleay32.dll": "32a92abfbe4dbb8d3da3664f9a17e354a23045ff207f39863327088c39ef430b351c77915eeaf732dfad437acf0028e524c8877086379f30e92fb9762f2d199a", \
                                "openssl.exe": "14d4c5f0d77d1598f75d365bc0fd566c6b56bf0995cadf1a372471761dc797ee8de18a00445b9045541c7900e74e765684bc211394c11dc99a2fb853556f20de"}
                            }
        
        SHA_512 = {
            "i686" : "082f195e21547135185dddf4e52c41045bf2065a23ec33f07285db9f8a67ede682c1bf9609263aa51997c40b545fa27040ceb3648460646b1ed2bfb394c8e6dd",
            "x86_64" : "1987e494879f9265d62994b5c34ed7e4c0ea4630599c21847fe168b5186b1b7a4f1971ebc7206a48c809e1f247b7a5ab4b195398bd0e03f885c2123c06c93a02"
            }
            
        F_SIZES = {
            "i686": 1912576,
            "x86_64": 2222656
            }
            
        URLS = {
            "REM" : "https://%s/files/openvpn" % (release_version.org_data()["VCP_DOMAIN"]),
            "ALT" : "https://swupdate.openvpn.net/community/releases"
            }
        
        SETUP_FILENAME = "openvpn-install-%s-%s-%s.exe" % (VERSION,BUILT_V,ARCH)
        OPENVPN_DL_URL =  "%s/%s" % (URLS["REM"],SETUP_FILENAME)
        OPENVPN_DL_URL_ALT = "%s/%s" % (URLS["ALT"],SETUP_FILENAME)
        
        return {
                "ARCH":ARCH, "BUILT":BUILT, "LATEST":LATEST, "TIMESTAMP":TIMESTAMP, "VERSION":VERSION, "BUILT_V":BUILT_V, 
                "SHA_512":SHA_512, "F_SIZES":F_SIZES, "SETUP_FILENAME":SETUP_FILENAME,
                "URLS":URLS, "OPENVPN_DL_URL":OPENVPN_DL_URL, "OPENVPN_DL_URL_ALT":OPENVPN_DL_URL_ALT,
                "OPENVPN_FILEHASHS":OPENVPN_FILEHASHS,
                }
    except:
        debug(1,"[openvpn.py] def values: failed",DEBUG,True)
        sys.exit()

def supported_platforms(DEBUG):
    debug(9,"[openvpn.py] def supported_platforms()",DEBUG,True)
    return [ "AMD64", "x86" ]

def get_arch(DEBUG):
    debug(9,"[openvpn.py] def get_arch()",DEBUG,True)
    data = os_platform(DEBUG)
    if data == "AMD64":
        ARCH = "x86_64"
    elif data == "x86":
        ARCH = "i686"
    else:
        sys.exit()
    debug(9,"[openvpn.py] def get_arch: ARCH = '%s'" % (ARCH),DEBUG,True)
    return ARCH

def os_platform(DEBUG):
    debug(9,"[openvpn.py] def os_platform()",DEBUG,True)
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
        true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
        pass
        #true_platform not assigned to if this does not exist
    if true_platform in supported_platforms(DEBUG):
        debug(9,"[openvpn.py] def os_platform: true_platform = '%s'" % (true_platform),DEBUG,True)
        return true_platform
    else:
        debug(1,"[openvpn.py] def os_platform: true_platform = '%s' NOT SUPPORTED" % (true_platform),DEBUG,True)
        sys.exit()

def win_detect_openvpn(DEBUG,OPENVPN_EXE):
    # returns [ OPENVPN_DIR, OPENVPN_EXE ]
    try:
        debug(1,"[openvpn.py] def win_detect_openvpn()",DEBUG,True)
        if OPENVPN_EXE == False:
            debug(1,"[openvpn.py] def win_detect_openvpn: check programfiles",DEBUG,True)
            programfiles = [ "PROGRAMFILES", "PROGRAMFILES(x86)", "PROGRAMW6432" ]
            for getenv in programfiles:
                programfiles_dir = os.getenv(getenv)
                file = "%s\\OpenVPN\\bin\\openvpn.exe" % (programfiles_dir)
                if os.path.isfile(file):
                    debug(1,"[openvpn.py] def win_detect_openvpn: '%s'" % (file),DEBUG,True)
                    OPENVPN_DIR = "%s\\OpenVPN\\bin" % (programfiles_dir)
                    break
        else:
            try:
                OPENVPN_DIR = OPENVPN_EXE.rsplit('\\', 1)[0]
            except:
                return False
        
        if not OPENVPN_DIR == False and os.path.isdir(OPENVPN_DIR):
            OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
            if os.path.isfile(OPENVPN_EXE):
                return { "OPENVPN_DIR":OPENVPN_DIR,"OPENVPN_EXE":OPENVPN_EXE }
    except:
        debug(1,"[openvpn.py] def win_detect_openvpn: failed",DEBUG,True)
    debug(1,"[openvpn.py] def win_detect_openvpn: return False",DEBUG,True)
    return False

def win_get_openvpn_version(DEBUG,OPENVPN_DIR):
    OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
    if not os.path.isfile(OPENVPN_EXE):
        debug(1,"[openvpn.py] def win_get_openvpn_version: OPENVPN_EXE not found",DEBUG,True)
        return False
    try:
        cmdstring = '"%s" --version' % (OPENVPN_EXE)
        cmdargs = shlex.split(cmdstring)
        p = subprocess.Popen(cmdargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags = win32process.CREATE_NO_WINDOW)
        output, err = p.communicate()
        rc = p.returncode
        #OVPN_VERSION = out.decode('utf-8').split('\r\n')[0].split( )[1].replace(".","")
        OVPN_VERSION = encodes.code_fiesta(DEBUG,'decode',output,'win_get_openvpn_version').splitlines()[0].split( )[1].replace(".","")
        #OVPN_BUILT = out.decode('utf-8').split('\r\n')[0].split("built on ",1)[1].split()
        OVPN_BUILT = encodes.code_fiesta(DEBUG,'decode',output,'win_get_openvpn_version').splitlines()[0].split("built on ",1)[1].split()
        debug(1,"[openvpn.py] def win_get_openvpn_version: OVPN_VERSION = '%s', OVPN_BUILT = '%s'"%(OVPN_VERSION,OVPN_BUILT),DEBUG,True)
        return [ OVPN_VERSION, OVPN_BUILT ]
    except Exception as e:
        debug(1,"[openvpn.py] def win_get_openvpn_version: failed, exception = '%s'"%(e),DEBUG,True)
    return False

def win_detect_openvpn_version(DEBUG,OPENVPN_DIR):
    try:
        debug(1,"[openvpn.py] def win_detect_openvpn_version()",DEBUG,True)
        OVPN_LATEST = values(DEBUG)["LATEST"]
        OVPN_LATEST_BUILT = values(DEBUG)["BUILT"].split()
        OVPN_LATEST_BUILT_TIMESTAMP = values(DEBUG)["TIMESTAMP"]
        DATA = win_get_openvpn_version(DEBUG,OPENVPN_DIR)
        if not DATA == False:
            OVPN_VERSION = DATA[0]
            OVPN_BUILT = DATA[1]
        else:
            debug(1,"[openvpn.py] def win_detect_openvpn_version: failed, DATA == False",DEBUG,True)
            return False
        debug(1,"OVPN_VERSION = %s, OVPN_BUILT = %s, OVPN_LATEST_BUILT = %s" % (OVPN_VERSION,OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
        if OVPN_VERSION >= OVPN_LATEST:
            debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_VERSION '%s' >= OVPN_LATEST '%s': True"%(OVPN_VERSION,OVPN_LATEST),DEBUG,True)
            if len(OVPN_BUILT) == 3 and len(OVPN_LATEST_BUILT) == 3:
                STR1 = str(OVPN_BUILT[0]+OVPN_BUILT[1]+OVPN_BUILT[2])
                STR2 = str(OVPN_LATEST_BUILT[0]+OVPN_LATEST_BUILT[1]+OVPN_LATEST_BUILT[2])
                if STR1 == STR2:
                    debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_BUILT '%s' == OVPN_LATEST_BUILT '%s': True"%(OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
                    return True
                else:
                    built_mon = OVPN_BUILT[0]
                    built_day = int(OVPN_BUILT[1])
                    built_year = int(OVPN_BUILT[2])
                    builtstr = "%s/%s/%s" % (built_mon,built_day,built_year)
                    string_built_time = time.strptime(builtstr,"%b/%d/%Y")
                    built_month_int = int(string_built_time.tm_mon)
                    built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
                    if built_timestamp > OVPN_LATEST_BUILT_TIMESTAMP:
                        debug(1,"[openvpn.py] def win_detect_openvpn_version: built_timestamp '%s' > OVPN_LATEST_BUILT_TIMESTAMP '%s': True" % (built_timestamp,OVPN_LATEST_BUILT_TIMESTAMP),DEBUG,True)
                        return True
        else:
            debug(1,"[openvpn.py] def win_detect_openvpn_version: OVPN_VERSION '%s' too old"%(OVPN_VERSION),DEBUG,True)
    except:
        debug(1,"[openvpn.py] def win_detect_openvpn_version: failed",DEBUG,True)
    debug(1,"[openvpn.py] def win_detect_openvpn_version: return False",DEBUG,True)
    return False

def list_openvpn_files(DEBUG,OPENVPN_DIR,type):
    debug(1,"[openvpn.py] def list_openvpn_files()",DEBUG,True)
    try:
        dir = OPENVPN_DIR
        if os.path.exists(dir):
            content = os.listdir(dir)
            list = []
            for file in content:
                if file.endswith(type):
                    list.append(file)
            if len(list) >= 1:
                debug(1,"[openvpn.py] def list_openvpn_files: dir '%s', files = '%s', list = '%s'" % (dir,len(list),list),DEBUG,True)
                return list
        else:
            debug(1,"[openvpn.py] def list_openvpn_files: dir '%s' not found!" % (dir),DEBUG,True)
    except:
        debug(1,"[openvpn.py] def list_openvpn_files: failed",DEBUG,True)
    debug(1,"[openvpn.py] def list_openvpn_files: return False",DEBUG,True)
    return False

def check_files(DEBUG,OPENVPN_DIR):
    debug(1,"[openvpn.py] def check_files()",DEBUG,True)
    
    if check_file_hashs(DEBUG,OPENVPN_DIR,".exe") == True:
        if check_file_hashs(DEBUG,OPENVPN_DIR,".dll") == True:
            return True
    else:
        # openvpn.exe hash failed, search signtool
        if not signtool.find_signtool(DEBUG) == False:
            # check exe signatures
            files = list_openvpn_files(DEBUG,OPENVPN_DIR,".exe")
            if files == False:
                return False
            for file in files:
                filepath = "%s\\%s" % (OPENVPN_DIR,file)
                if not signtool.signtool_verify(DEBUG,filepath):
                    return False
            # check dll signatures
            files = list_openvpn_files(DEBUG,OPENVPN_DIR,".dll")
            if files == False:
                return False
            for file in files:
                filepath = "%s\\%s" % (OPENVPN_DIR,file)
                if not signtool.signtool_verify(DEBUG,filepath):
                    return False
            # all file signatures verified
            return True
    debug(1,"[openvpn.py] def check_files: failed",DEBUG,True)
    return False

def check_file_hashs(DEBUG,OPENVPN_DIR,type):
    debug(1,"[openvpn.py] def check_file_hashs(%s)"%(type),DEBUG,True)
    #if devmode() == True:
    #   debug(1,"[openvpn.py] def check_file_hashs: DEVMODE ! force signature check",DEBUG,True)
    #   return False
    types = [ ".exe", ".dll" ]
    if not type in types:
        debug(1,"[openvpn.py] def check_file_hashs: type '%s' invalid"%(type),DEBUG,True)
        return False
    try:
        content = list_openvpn_files(DEBUG,OPENVPN_DIR,type)
        if content == False:
            return False
        try:
            filename = values(DEBUG)["SETUP_FILENAME"]
            try:
                hashs = values(DEBUG)["OPENVPN_FILEHASHS"][filename]
            except:
                return False
            
        except:
            debug(2,"[openvpn.py] def check_file_hashs: filename/hashs failed",DEBUG,True)
            sys.exit()
        
        debug(2,"[openvpn.py] filename = '%s' hashs = '%s'"%(filename,hashs),DEBUG,True)
        for file in content:
            debug(2,"[openvpn.py] def check_file_hashs: file = '%s'" % (file),DEBUG,True)
            filepath = "%s\\%s" % (OPENVPN_DIR,file)
            hasha = hashings.hash_sha512_file(DEBUG,filepath)
            debug(2,"[openvpn.py] def check_file_hashs: hasha = '%s'" % (hasha),DEBUG,True)
            try:
                hashb = hashs[file]
            except:
                return False
            if hasha == hashb:
                debug(2,"[openvpn.py] def check_file_hashs: hash file = '%s' OK!" % (file),DEBUG,True)
            else:
                debug(1,"[openvpn.py] def check_file_hashs: hash file = '%s' failed" % (file),DEBUG,True)
                return False
        return True
    except:
        debug(1,"[openvpn.py] def check_file_hashs: failed",DEBUG,True)
        sys.exit()
        return False

"""
def upgrade_openvpn(DEBUG):
    pass

def load_openvpnbin_from_remote(self):
    pass

def verify_openvpnbin_dl(self):
    pass

def win_install_openvpn(self):
    pass

def extract_ovpn(self):
    pass

def win_select_openvpn(self):
    pass

def win_detect_openvpn_version(self):
    pass

def find_signtool(self):
    pass

def signtool_verify(self,file):
    pass
"""