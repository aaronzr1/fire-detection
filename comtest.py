import ctypes, ctypes.wintypes, time

kernel32 = ctypes.windll.kernel32
kernel32.CreateFileW.restype = ctypes.c_void_p

INVALID = 0xFFFFFFFFFFFFFFFF
FILE_FLAG_OVERLAPPED = 0x40000000

# Test 1: without FILE_FLAG_OVERLAPPED (like my earlier raw test)
h = kernel32.CreateFileW(r'\\.\COM19', 0xC0000000, 0, None, 3, 0, None)
print(f'Without overlapped: {"OK" if h and h != INVALID else "FAIL " + str(kernel32.GetLastError())}')
if h and h != INVALID:
    kernel32.CloseHandle(ctypes.c_void_p(h))

time.sleep(0.5)

# Test 2: with FILE_FLAG_OVERLAPPED (like pyserial)
h2 = kernel32.CreateFileW(r'\\.\COM19', 0xC0000000, 0, None, 3, FILE_FLAG_OVERLAPPED, None)
print(f'With overlapped:    {"OK handle=" + str(h2) if h2 and h2 != INVALID else "FAIL " + str(kernel32.GetLastError())}')
if h2 and h2 != INVALID:
    # Now try GetCommState + SetCommState like pyserial does
    class DCB(ctypes.Structure):
        _fields_ = [("DCBlength", ctypes.c_ulong),
                    ("BaudRate", ctypes.c_ulong),
                    ("fBitFields", ctypes.c_ulong),
                    ("wReserved", ctypes.c_ushort),
                    ("XonLim", ctypes.c_ushort),
                    ("XoffLim", ctypes.c_ushort),
                    ("ByteSize", ctypes.c_ubyte),
                    ("Parity", ctypes.c_ubyte),
                    ("StopBits", ctypes.c_ubyte),
                    ("XonChar", ctypes.c_char),
                    ("XoffChar", ctypes.c_char),
                    ("ErrorChar", ctypes.c_char),
                    ("EofChar", ctypes.c_char),
                    ("EvtChar", ctypes.c_char),
                    ("wReserved1", ctypes.c_ushort)]
    dcb = DCB()
    dcb.DCBlength = ctypes.sizeof(DCB)
    r = kernel32.GetCommState(ctypes.c_void_p(h2), ctypes.byref(dcb))
    print(f'GetCommState: {"OK baud=" + str(dcb.BaudRate) if r else "FAIL " + str(kernel32.GetLastError())}')
    dcb.BaudRate = 115200
    r2 = kernel32.SetCommState(ctypes.c_void_p(h2), ctypes.byref(dcb))
    print(f'SetCommState: {"OK" if r2 else "FAIL " + str(kernel32.GetLastError())}')
    kernel32.CloseHandle(ctypes.c_void_p(h2))
