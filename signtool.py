# -*- coding: utf-8 -*-
import os, subprocess

# .py file imports
from debug import debug
from debug import devmode
from debug import devdir
import hashings
import openvpn


def find_signtool(DEBUG):
    debug(1,"[signtool.py] def find_signtool()",DEBUG,True)
    try:
        ARCH = openvpn.get_arch(DEBUG)
        if ARCH == "x64":
            exe = "signtool_w10sdk_x64.exe"
            signtoolhash = "e85d79cc617642f585cb9e4ad5dd919b8d15570a291bdd1e69fd38d4f278bc4b6f110329e8fa6948b7d516917cc2bde43532cde33e8c5e66355d0c97cfd7ebc2"
        else:
            exe = "signtool_w10sdk_x86.exe"
            signtoolhash = "233304669aefeec9ad5d19bd2dd5bb19ea35ce31da0b3aabe5ab859259608a58725fac5993637c9635e5912138d3eb477773351f0ee81cc3ce756d713163cf31"
        
        BIN_DIR = os.getcwd()
        signtool = "%s\\%s" % (BIN_DIR,exe)
        if not os.path.isfile(signtool):
            signtool = "%s\\includes\\codesign\\%s" % (devdir(),exe)
        if os.path.isfile(signtool):
            hash = hashings.hash_sha512_file(DEBUG,signtool)
            if signtoolhash == hash:
                debug(1,"[signtool.py] def find_signtool: signtool = '%s'" % (signtool),DEBUG,True)
                return signtool
            else:
                debug(1,"[signtool.py] def find_signtool: signtoolhash failed",DEBUG,True)
        else:
            debug(1,"[signtool.py] def signtool_verify_files: signtool not found",DEBUG,True)
    except Exception as e:
        debug(1,"[signtool.py] def find_signtool: failed exception '%s'"%(e),DEBUG,True)
    return False

def signtool_verify(DEBUG,file):
    debug(1,"[signtool.py] def signtool_verify(%s)"%(file),DEBUG,True)
    signtool = find_signtool(DEBUG)
    if os.path.isfile(file):
        cscertsha1 = "21F94C255A8B20D21A323CA5ACB8EBF284E09037"
        #if devmode() == True:
        #   cscertsha1 = "1234000012340000123400001234000012340000"
        verbose = "/q"
        if DEBUG == True:
            verbose = "/v"
        string1 = '"%s" verify %s /a /all /pa /tw /sha1 %s "%s"' % (signtool,verbose,cscertsha1,file)
        debug(1,"[signtool.py] def signtool_verify: string1 = '%s'"%(string1),DEBUG,True)
        exitcode1 = 1
        try:
            exitcode1 = subprocess.check_call("%s" % (string1),shell=True)
        except:
            pass
        if exitcode1 == 0:
            debug(1,"[signtool.py] def signtool_verify: file = '%s' signature verified"%(file),DEBUG,True)
            return True
        else:
            debug(1,"[signtool.py] def signtool_verify: file = '%s' signature failed"%(file),DEBUG,True)
            # only check file is signed from same CA if DEVMODE is True
            if devmode() == False:
                return False
            else:
                return False
                debug(1,"[signtool.py] def signtool_verify: file = '%s' check signature CA hash"%(file),DEBUG,True)
                cacertsha1 = "92C1588E85AF2201CE7915E8538B492F605B80C6"
                string2 = '"%s" verify /v /a /all /pa /tw /ca %s "%s"' % (signtool,cacertsha1,file)
                debug(1,"[signtool.py] def signtool_verify: string2 = '%s'"%(string2),DEBUG,True)
                exitcode2 = 1
                try:
                    exitcode2 = subprocess.check_call("%s" % (string2),shell=True)
                except:
                    pass
                if exitcode2 == 0:
                    debug(1,"[signtool.py] def signtool_verify: file = '%s' signature CA verified"%(file),DEBUG,True)
                    return True
                else:
                    debug(1,"[signtool.py] def signtool_verify: file = '%s' signature CA failed"%(file),DEBUG,True)
                    return False
    else:
        debug(1,"[signtool.py] def signtool_verify(%s) not found"%(file),DEBUG,True)
        return False
