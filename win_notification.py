# -*- coding: utf-8 -*-
from debug import debug
import os, platform, time

from win32api import GetSystemMetrics, GetModuleHandle, PostQuitMessage, LoadResource
from win32con import SM_CXICONSPACING, SM_CXSMICON, SM_CYSMICON, SM_CXICON, SM_CYICON, CW_USEDEFAULT, IMAGE_ICON, IMAGE_BITMAP, IDI_INFORMATION, IDI_APPLICATION, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_DESTROY, WS_OVERLAPPED, WS_SYSMENU, WM_USER, RT_ICON
from win32gui import CreateIconFromResource, CreateWindow, DestroyWindow, LoadIcon, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY, RegisterClass, UnregisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

WINVER10 = False
if "Windows-10" in platform.platform():
	WINVER10 = True

class notify:
	def __init__(self):

		message_map = { WM_DESTROY: self.send_notify_destroy }
		wc = WNDCLASS()
		self.hinst = wc.hInstance = GetModuleHandle(None)
		wc.lpszClassName = str("PythonTaskbar")
		wc.lpfnWndProc = message_map
		self.classAtom = RegisterClass(wc)

	def send_notify(self,DEBUG,TRAYSIZE,DEV_DIR,text,title):
		if WINVER10 == False:
			return False
		try:
			
			while not self.isDestroyed() == True:
				sleep(0.01)
			self.destroyed = False
			debug(222,"[win_notification.py] def send_notify: [Win10 = %s]" % (WINVER10),DEBUG,True)
			style = WS_OVERLAPPED | WS_SYSMENU
			self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,0, 0, CW_USEDEFAULT,CW_USEDEFAULT,0, 0, self.hinst, None)
			UpdateWindow(self.hwnd)

			try:
				RT_ICON_SIZE = 15
				if TRAYSIZE == 32 or WINVER10 == True:
					RT_ICON_SIZE = 14
				""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648060(v=vs.85).aspx """
				hicon = CreateIconFromResource(LoadResource(None, RT_ICON, RT_ICON_SIZE), True)
				debug(222,"[win_notification.py] def send_notify: CreateIconFromResource() #1",DEBUG,True)
			except Exception as e:
				debug(222,"[win_notification.py] def send_notify: CreateIconFromResource() #1 failed, exception = '%s'"%(e),DEBUG,True)
				try:
					icon_path = False
					icon_path1 = "%s\\else\\app_icons\\app_icon.ico" % (DEV_DIR)
					files = [ icon_path1 ]
					for file in files:
							if os.path.isfile(file):
								icon_path = file
								break
					if icon_path == False:
						raise Exception
					icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
					""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms724385(v=vs.85).aspx """
					#x1 = GetSystemMetrics(SM_CXSMICON)
					#y1 = GetSystemMetrics(SM_CYSMICON)
					#x2 = GetSystemMetrics(SM_CXICON)
					#y2 = GetSystemMetrics(SM_CYICON)
					#ispace = GetSystemMetrics(SM_CXICONSPACING)
					#debug(222,"[win_notification.py] def send_notify: x1 = '%s' y1 = '%s', x2 = '%s' y2 = '%s', ispace = '%s'"%(x1,y1,x2,y2,ispace),DEBUG,True)
					""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648045(v=vs.85).aspx """
					hicon = LoadImage(self.hinst, icon_path,IMAGE_ICON, 0, 0, icon_flags)
					debug(222,"[win_notification.py] def send_notify: LoadImage() #2",DEBUG,True)
				except Exception as e:
					debug(222,"[win_notification.py] def send_notify: LoadImage() #2 failed, exception = '%s'"%(e),DEBUG,True)
					try:
						""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648072(v=vs.85).aspx """
						hicon = LoadIcon(0, IDI_INFORMATION)
						debug(222,"[win_notification.py] def send_notify: LoadIcon() #3",DEBUG,True)
					except Exception as e:
						debug(222,"[win_notification.py] def send_notify: LoadIcon() #3 failed, exception = '%s'"%(e),DEBUG,True)
						return False
			
			flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
			nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "")
			
			Shell_NotifyIcon(NIM_ADD, nid)
			
			icontype = 0 # bad blurry icon
			#icontype = 1 # blue info
			#icontype = 2 # yellow exclamation
			#icontype = 3 # red cross
			#icontype = 4 # icon from filepath
			
			Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,WM_USER + 20,hicon, "", text, 200,title, icontype))
			
			if WINVER10 == False:
				time.sleep(10)
			
			anyreturn = DestroyWindow(self.hwnd)
			debug(222,"[win_notification.py] def send_notify: DestroyWindow() returned = '%s'"%(anyreturn),DEBUG,True)

			#anyreturn = UnregisterClass(self.classAtom, self.hinst)
			#debug(1,"[win_notification.py] def send_notify: UnregisterClass() returned = '%s'"%(anyreturn),DEBUG,True)

			debug(1,"[win_notification.py] def send_notify: [Win10 = %s] return" % (WINVER10),DEBUG,True)
			self.destroyed = True
			return None
		except Exception as e:
			debug(1,"[win_notification.py] def send_notify: failed, exception = '%s'"%(e),DEBUG,True)

	def send_notify_destroy(self, hwnd, msg, wparam, lparam):
		nid = (self.hwnd, 0)
		Shell_NotifyIcon(NIM_DELETE, nid)
		PostQuitMessage(0)
		debug(222,"[win_notification.py] def send_notify_destroy: return",True,True)
		return None

	def isDestroyed(self):
		try:
			return self.destroyed
		except:
			return True
