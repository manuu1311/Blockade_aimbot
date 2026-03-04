import ctypes
import threading
import win32gui
from ctypes import wintypes

WM_INPUT = 0x00FF
RIDEV_INPUTSINK = 0x00000100
RID_INPUT = 0x10000003
LRESULT = ctypes.c_long
if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

user32 = ctypes.windll.user32

# =========================
# STRUCTURES (FIXED)
# =========================

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM),
    ]


class RAWMOUSE(ctypes.Structure):
    _fields_ = [
        ("usFlags", wintypes.USHORT),
        ("ulButtons", wintypes.ULONG),
        ("ulRawButtons", wintypes.ULONG),
        ("lLastX", wintypes.LONG),
        ("lLastY", wintypes.LONG),
        ("ulExtraInformation", wintypes.ULONG),
    ]


class RAWINPUT(ctypes.Structure):
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("mouse", RAWMOUSE),
    ]


class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND),
    ]


# =========================
# TRACKER
# =========================

class RawMouseYTracker:
    def __init__(self):
        self.total_y = 0
        self.running = False
        self._thread = None
        self.hwnd = None

        # IMPORTANT: proper callback type
        self.WNDPROC = ctypes.WINFUNCTYPE(
            LRESULT,
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )
        self._wndproc_ref = self.WNDPROC(self._wnd_proc)

    # =========================
    # PUBLIC API
    # =========================

    def start_tracking(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()

    def reset(self):
        self.total_y = 0

    def get_total_y(self):
        return self.total_y

    # =========================
    # INTERNALS
    # =========================

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_INPUT:
            self._handle_raw_input(lparam)
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _handle_raw_input(self, lparam):
        dwSize = wintypes.UINT()

        user32.GetRawInputData(
            lparam,
            RID_INPUT,
            None,
            ctypes.byref(dwSize),
            ctypes.sizeof(RAWINPUTHEADER),
        )

        buffer = ctypes.create_string_buffer(dwSize.value)

        user32.GetRawInputData(
            lparam,
            RID_INPUT,
            buffer,
            ctypes.byref(dwSize),
            ctypes.sizeof(RAWINPUTHEADER),
        )

        raw = ctypes.cast(buffer, ctypes.POINTER(RAWINPUT)).contents

        if raw.header.dwType == 0:  # mouse
            self.total_y += raw.mouse.lLastY

    def _message_loop(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wndproc_ref
        wc.lpszClassName = "RawMouseTracker"

        class_atom = win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindow(
            class_atom,
            "RawMouseTracker",
            0,
            0, 0, 0, 0,
            0, 0, 0,
            None,
        )

        rid = RAWINPUTDEVICE()
        rid.usUsagePage = 0x01
        rid.usUsage = 0x02
        rid.dwFlags = RIDEV_INPUTSINK
        rid.hwndTarget = self.hwnd

        user32.RegisterRawInputDevices(
            ctypes.byref(rid), 1, ctypes.sizeof(rid)
        )

        win32gui.PumpMessages()


import ctypes
from ctypes import wintypes

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", MOUSEINPUT),
    ]

def move_mouse(dx, dy):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, 0)
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


class mouse_handler:
    def __init__(self):
        self.listener=RawMouseYTracker()
    
    def start_tracking(self):
        self.listener.start_tracking()

    def reset_tracking(self):
        self.listener.reset()

    def get_y(self):
        return self.listener.get_total_y()
    
    def move_mouse(self,dx,dy):
        move_mouse(dx,dy)

# =========================
# TEST
# =========================
'''
listener = mouse_handler()
listener.start_tracking()

while True:
    time.sleep(2.5)
    print(listener.get_y())
    listener.move_mouse(0, -listener.get_y())
'''
