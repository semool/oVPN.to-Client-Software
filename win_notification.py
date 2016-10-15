# -*- coding: utf-8 -*-
from debug import debug
import platform
import time

# ATTENTION
# win32api include in py2exe 0.9.2.2 give a import error pywintypes with python3.4.4. To fix it edit the Hooks file from py2exe:
# C:\Program Files\Python34_64\Lib\site-packages\py2exe\hooks.py
# Comment Line 250 with #
# Now all works fine

from win32api import GetModuleHandle, PostQuitMessage, LoadResource
from win32con import CW_USEDEFAULT, IMAGE_ICON, IDI_APPLICATION, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_DESTROY, WS_OVERLAPPED, WS_SYSMENU, WM_USER, RT_ICON
from win32gui import CreateIconFromResource, CreateWindow, DestroyWindow, LoadIcon, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY, RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

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
		try:
			debug(1,"[win_notification.py] def send_notify: [Win10 = %s]" % (WINVER10),DEBUG,True)
			style = WS_OVERLAPPED | WS_SYSMENU
			self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,0, 0, CW_USEDEFAULT,CW_USEDEFAULT,0, 0, self.hinst, None)
			UpdateWindow(self.hwnd)

			try:
				RT_ICON_SIZE = 11
				if TRAYSIZE == 32 or WINVER10 == True:
					RT_ICON_SIZE = 10
				hicon = CreateIconFromResource(LoadResource(None, RT_ICON, RT_ICON_SIZE), True)
			except:
				try:
					icon_path = "%s\\else\\app_icons\\shield_exe.ico" % (DEV_DIR)
					icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
					hicon = LoadImage(self.hinst, icon_path,IMAGE_ICON, 0, 0, icon_flags)
				except:
					hicon = LoadIcon(0, IDI_APPLICATION)

			flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
			nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Tooltip")
			Shell_NotifyIcon(NIM_ADD, nid)
			Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,WM_USER + 20,hicon, "Balloon Tooltip", text, 200,title))

			if WINVER10 == False:
				time.sleep(10)
			DestroyWindow(self.hwnd)
			return None
		except:
			debug(1,"[win_notification.py] def send_notify: failed",DEBUG,True)

	def send_notify_destroy(self, hwnd, msg, wparam, lparam):
		nid = (self.hwnd, 0)
		Shell_NotifyIcon(NIM_DELETE, nid)
		PostQuitMessage(0)
		return None
