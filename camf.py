import random
import time
from pynput.mouse import Controller as MouseController
import pytesseract
import ctypes
import win32gui
import win32con
import cv2
import cv_finder
import pyautogui

method = cv2.TM_SQDIFF_NORMED
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'  # место где лежит тесеракт для работы с pytesseract
PROCESS_PER_MONITOR_DPI_AWARE = 2  # хз зачем нужна,но без нее ctypes не хочет работать связано с маштабированием монитора
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)  # хз зачем нужна,но без нее ctypes не хочет работать связано с маштабированием монитора
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
WM_LBUTTONDOWN = 0x0201
window_handle = ctypes.windll.user32.FindWindowW(None, 'STALCRAFT')
WM_LBUTTONUP = 0x0202
PAGE_COUNT = 13
WM_KEYDOWN = 0x0100
BACKSPACE_VIRTUAL_CODE = 0x08


def move_mouse_smoothly(x, y, duration=1):
    mouse = MouseController()
    start_x, start_y = mouse.position
    end_x, end_y = x, y
    steps = random.randint(110, 120)
    sleep_time = duration / steps

    for i in range(steps + 1):
        current_x = start_x + (end_x - start_x) * i / steps
        current_y = start_y + (end_y - start_y) * i / steps
        mouse.position = (current_x, current_y)
        time.sleep(sleep_time)


time.sleep(1)


def mouseclick():
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)
    time.sleep(random.uniform(0.1000, 0.3000))
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)


def stalcraft_foreground():
    win32gui.ShowWindow(window_handle, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(window_handle)


def input_key_massage(message):
    for char in message:
        char_code = ord(char)
        ctypes.windll.user32.SendMessageW(window_handle, win32con.WM_CHAR, char_code, 0)
        time.sleep(random.uniform(0.0100, 0.0300))


def pressP():
    ctypes.windll.user32.SendMessageW(window_handle, WM_KEYDOWN, 0x50, 0)


def scroll(x1, y1, x2, y2):
    move_mouse_smoothly(x1, y1)
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)
    move_mouse_smoothly(x2, y2)
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)


def search_input(item_name):
    for char in item_name:
        char_code = ord(char)
        ctypes.windll.user32.SendMessageW(window_handle, win32con.WM_CHAR, char_code, 0)
        time.sleep(random.uniform(0.0100, 0.0300))


def delete_text():
    for i in range(random.randint(40, 55)):
        ctypes.windll.user32.SendMessageW(window_handle, WM_KEYUP, BACKSPACE_VIRTUAL_CODE, 0)
        time.sleep(random.uniform(0.05, 0.2))




def auction_click():
    coordinates_auction = cv_finder.coordinates_auction()
    auction_x, auction_y = coordinates_auction
    print(auction_x,auction_y)
    move_mouse_smoothly(auction_x,auction_y)
    mouseclick()
    complete=True
    return complete

def buyot_sort():
    coordinates_buyout = cv_finder.coordinates_text_buyout()
    buyout_x, buyout_y = coordinates_buyout
    print(buyout_x, buyout_y)
    move_mouse_smoothly(buyout_x, buyout_y)
    mouseclick()
    time.sleep(random.uniform(0.1,0.3))
    mouseclick()


def scroll2(stage):
    fullscreen_scroll_for_search = cv_finder.take_screenshot_bbox('fullscreen_for_search_scroll','Screenshot/tesseract/online/')
    scroll_searching = 'Screenshot/tesseract/scroll_screen.png'
    ScrollBarX, ScrollBarY = cv_finder.find_element_on_screen_sobel(scroll_searching, fullscreen_scroll_for_search)

    print(f'Скролю на позицию: {stage}')
    startScrollX, startScrollY = cv_finder.find_element_on_screen('Screenshot/tesseract/search_button.png',
                                                              'Screenshot/tesseract/online/fullscreen_for_search_scroll.png')  # поиск кнопка
    print('scroll start', startScrollX, startScrollY)
    startScrollX += 48 #1390 1400
    startScrollY += 14

    scrollX1 = 4 + ScrollBarX
    scrollX2 = 8 + ScrollBarX
    scrollY1 = 10 + ScrollBarY
    scrollY2 = 30 + ScrollBarY

    step = 90

    pyautogui.moveTo(scrollX2, scrollY2, random.uniform(0.2, 0.4))

    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)

    match stage:
        case 0:
            pyautogui.moveTo(startScrollX, startScrollY - (step * (stage + 1)), random.uniform(0.2, 0.4))
        case 1:
            pyautogui.moveTo(startScrollX, startScrollY + step, random.uniform(0.2, 0.4))
        case 2:
            pyautogui.moveTo(startScrollX, startScrollY + (step * 2), random.uniform(0.2, 0.4))
        case 3:
            pyautogui.moveTo(startScrollX, startScrollY + (step * 3), random.uniform(0.2, 0.4))
        case 4:
            pyautogui.moveTo(startScrollX, startScrollY + (step * 4), random.uniform(0.2, 0.4))

    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)
