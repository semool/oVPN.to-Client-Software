import os, subprocess
import release_version
import datetime

def set_task():
	SOURCEDIR = os.getcwd()
	DATE = datetime.datetime.now()

	XMLFILE = "%s\\autostart.xml" % (SOURCEDIR)
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
	print >> ind, '      <Delay>PT30S</Delay>'
	print >> ind, '    </LogonTrigger>'
	print >> ind, '  </Triggers>'
	print >> ind, '  <Principals>'
	print >> ind, '    <Principal id="Author">'
	print >> ind, '      <UserId>%s</UserId>' % os.getenv('username')
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
	print >> ind, '      <Command>"%s\ovpn_client.exe"</Command>' % (SOURCEDIR)
	print >> ind, '      <WorkingDirectory>%s</WorkingDirectory>' % (SOURCEDIR)
	print >> ind, '    </Exec>'
	print >> ind, '  </Actions>'
	print >> ind, '</Task>'
	ind.close()

	if os.path.exists(XMLFILE):
		string = 'schtasks.exe /Create /XML "%s" /TN "%s"' % (XMLFILE,release_version.version_data()["NAME"])
		print string
		try:
			cmd = subprocess.call("%s" % (string),shell=True)
		except:
			pass
		os.remove(XMLFILE)
		return True

def delete_task():
	string = 'schtasks.exe /Delete /TN "%s" /f' % (release_version.version_data()["NAME"])
	print string
	try:
		cmd = subprocess.call("%s" % (string),shell=True)
	except:
		pass
	return True