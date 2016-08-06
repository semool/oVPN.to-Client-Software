import os, subprocess
import release_version
import datetime
from debug import debug

def set_task(istrue,delay):
	DEBUG = istrue
	SOURCEDIR = os.getcwd()
	DATE = datetime.datetime.now()
	USERNAME = os.getenv('username')
	AUTOSTART_DELAY_TIME = delay

	XMLFILE = "%s\\autostart.xml" % (SOURCEDIR)
	remove_xml(DEBUG,XMLFILE)
	ind = open(XMLFILE, "w")
	print >> ind, '<?xml version="1.0" encoding="UTF-16"?>'
	print >> ind, '<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">'
	print >> ind, '  <RegistrationInfo>'
	print >> ind, '    <Date>%s</Date>' % DATE.isoformat()
	print >> ind, '    <Author>%s %s</Author>' % (release_version.org_data()["ORG"],release_version.org_data()["ADD"])
	print >> ind, '    <URI>\%s</URI>' % (release_version.version_data()["NAME"])
	print >> ind, '  </RegistrationInfo>'
	print >> ind, '  <Triggers>'
	print >> ind, '    <LogonTrigger>'
	print >> ind, '      <Enabled>true</Enabled>'
	print >> ind, '      <UserId>%s</UserId>' % USERNAME
	print >> ind, '      <Delay>PT%sS</Delay>' % AUTOSTART_DELAY_TIME
	print >> ind, '    </LogonTrigger>'
	print >> ind, '  </Triggers>'
	print >> ind, '  <Principals>'
	print >> ind, '    <Principal id="Author">'
	print >> ind, '      <UserId>%s</UserId>' % USERNAME
	print >> ind, '      <LogonType>InteractiveToken</LogonType>'
	print >> ind, '      <RunLevel>HighestAvailable</RunLevel>'
	print >> ind, '    </Principal>'
	print >> ind, '  </Principals>'
	print >> ind, '  <Settings>'
	print >> ind, '    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>'
	print >> ind, '    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>'
	print >> ind, '    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>'
	print >> ind, '    <AllowHardTerminate>false</AllowHardTerminate>'
	print >> ind, '    <StartWhenAvailable>false</StartWhenAvailable>'
	print >> ind, '    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>'
	print >> ind, '    <IdleSettings>'
	print >> ind, '      <StopOnIdleEnd>true</StopOnIdleEnd>'
	print >> ind, '      <RestartOnIdle>false</RestartOnIdle>'
	print >> ind, '    </IdleSettings>'
	print >> ind, '    <AllowStartOnDemand>true</AllowStartOnDemand>'
	print >> ind, '    <Enabled>true</Enabled>'
	print >> ind, '    <Hidden>false</Hidden>'
	print >> ind, '    <RunOnlyIfIdle>false</RunOnlyIfIdle>'
	print >> ind, '    <WakeToRun>false</WakeToRun>'
	print >> ind, '    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>'
	print >> ind, '    <Priority>7</Priority>'
	print >> ind, '  </Settings>'
	print >> ind, '  <Actions Context="Author">'
	print >> ind, '    <Exec>'
	print >> ind, '      <Command>"%s\%s"</Command>' % (SOURCEDIR,release_version.setup_data()["exename"])
	print >> ind, '      <WorkingDirectory>%s</WorkingDirectory>' % (SOURCEDIR)
	print >> ind, '    </Exec>'
	print >> ind, '  </Actions>'
	print >> ind, '</Task>'
	ind.close()

	if os.path.exists(XMLFILE):
		string = 'schtasks.exe /Create /XML "%s" /TN "%s"' % (XMLFILE,release_version.version_data()["NAME"])
		try:
			exitcode = subprocess.check_call("%s" % (string),shell=True)
			remove_xml(DEBUG,XMLFILE)
			if exitcode == 0:
				debug(1,"def cb_switch_autostart: enable Ok",DEBUG,True)
				return True
			else:
				debug(1,"def cb_switch_autostart: enable fail, exitcode = '%s'" % (exitcode),DEBUG,True)
				return False
		except:
			remove_xml(DEBUG,XMLFILE)
			debug(1,"def cb_switch_autostart: enable failed",DEBUG,True)

def remove_xml(istrue,XMLFILE):
	DEBUG = istrue
	if os.path.isfile(XMLFILE):
		try:
			os.remove(XMLFILE)
		except:
			debug(1,"def remove_xml: could not remove XMLFILE '%s'" % (XMLFILE),DEBUG,True)
			pass

def delete_task(istrue):
	DEBUG = istrue
	string = 'schtasks.exe /Delete /TN "%s" /f' % (release_version.version_data()["NAME"])
	try:
		exitcode = subprocess.check_call("%s" % (string),shell=True)
		if exitcode == 0:
			debug(1,"def cb_switch_autostart: disable Ok",DEBUG,True)
			return True
		else:
			debug(1,"def cb_switch_autostart: disable fail, exitcode = '%s'" % (exitcode),DEBUG,True)
			return False
	except:
		debug(1,"def cb_switch_autostart: disable failed",DEBUG,True)
		return False
