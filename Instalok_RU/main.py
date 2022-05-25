from os import access
from PyQt5 import QtWidgets, uic
import sys
from pyautogui import *
import pyautogui
import time
import keyboard
import cv2
import win32api, win32con, win32gui

script_dir = os.path.dirname(__file__)
path_ui = os.path.join(script_dir, "instalok.ui")


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def checkClient(state, dimensions):
    return pyautogui.locateOnScreen(
        state, confidence=0.8, region=dimensions, grayscale=True
    )


def checkDimensions(dimensions):
    global path_ban, path_bar, path_btn, path_block, path_accept
    dif = dimensions[2] - dimensions[0]
    handle = {1920: 0, 1600: 1, 1280: 2, 1024: 3}
    for key, value in handle.items:
        if key == dif:
            checker = value
    path_ban = os.path.join(script_dir, f"assets/ban{checker}.png")
    path_bar = os.path.join(script_dir, f"assets/pick_bar{checker}.png")
    path_btn = os.path.join(script_dir, f"assets/pick_btn{checker}.png")
    path_block = os.path.join(script_dir, f"assets/block{checker}.png")
    path_accept = os.path.join(script_dir, f"assets/accept{checker}.png")


def autoPick(dimensions, pick):
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 1.6),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 6.92),
    )  # Нажимает на строку поиска ()
    keyboard.write(pick)
    time.sleep(0.5)
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 3.2),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 4.5),
    )  # Нажимает на чемпиона
    time.sleep(0.4)
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 2),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 1.2),
    )


def autoBan(dimensions, ban, idc):
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 1.6),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 6.92),
    )
    # Нажимает на строку поиска
    keyboard.write(ban)
    time.sleep(0.5)
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 3.2),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 4.5),
    )
    # Нажимает на чемпиона
    time.sleep(0.4)
    click(
        dimensions[0] + round((dimensions[2] - dimensions[0]) / 2),
        dimensions[1] + round((dimensions[3] - dimensions[1]) / 1.2),
    )
    # Нажимает на подтверждение
    if idc == True:
        if checkClient(path_block, dimensions) != None:
            time.sleep(1)
            click(
                dimensions[0] + round((dimensions[2] - dimensions[0]) / 2.35),
                dimensions[1] + round((dimensions[3] - dimensions[1]) / 1.6),
            )


def eventLoop(ban, pick, idc, accept):
    while keyboard.is_pressed("=") == False:
        try:
            hwnd = win32gui.FindWindow(None, r"League of Legends")
            dimensions = win32gui.GetWindowRect(hwnd)
            checkDimensions(dimensions)
            if accept is True:
                if checkClient(path_accept, dimensions) != None:
                    click(
                        dimensions[0] + round((dimensions[2] - dimensions[0]) / 2),
                        dimensions[1] + round((dimensions[3] - dimensions[1]) / 1.3),
                    )
            if checkClient(path_ban, dimensions) != None:
                print("Found ban")
                autoBan(dimensions, ban, idc)
                time.sleep(5)
            if checkClient(path_bar, dimensions) != None:
                if checkClient(path_btn, dimensions) != None:
                    print("Found pick")
                    autoPick(dimensions, pick)
                    break
        except Exception as e:
            print(e)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            print(path_ui)
            super(Ui, self).__init__()
            uic.loadUi(path_ui, self)
            self.show()
            self.run.clicked.connect(self.submit)
        except Exception as e:
            print(e)

    def submit(self):
        try:
            champ_ban = self.ban.text()
            champ_pick = self.pick.text()
            idc = self.idontcare.isChecked()
            accept = self.accept.isChecked()
            self.close()
            try:
                eventLoop(champ_ban, champ_pick, idc, accept)
            except Exception as e:
                print(e)
            self.show()
        except:
            print(f"Submit problem: {champ_ban}, {champ_pick}, {idc}")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
