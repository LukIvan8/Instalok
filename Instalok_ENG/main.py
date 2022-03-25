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
path_ban = os.path.join(script_dir, "ban.png")
path_bar = os.path.join(script_dir, "pick_bar.png")
path_btn = os.path.join(script_dir, "pick_btn.png")
path_block = os.path.join(script_dir, "block.png")


def idontknowhowtofiximportissue():
    WTF = cv2.imread(path_ban, 0)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def checkClient(state, dimensions):
    return pyautogui.locateOnScreen(
        state, confidence=0.8, region=dimensions, grayscale=True
    )


def autoPick(dimensions, pick):
    click(dimensions[0] + 958, dimensions[1] + 128)  # Нажимает на строку поиска
    keyboard.write(pick)
    time.sleep(0.5)
    click(dimensions[0] + 480, dimensions[1] + 200)  # Нажимает на чемпиона
    time.sleep(0.4)
    click(dimensions[0] + 780, dimensions[1] + 770)


def autoBan(dimensions, ban, idc):
    click(dimensions[0] + 958, dimensions[1] + 128)  # Нажимает на строку поиска
    keyboard.write(ban)
    time.sleep(0.5)
    click(dimensions[0] + 480, dimensions[1] + 200)  # Нажимает на чемпиона
    time.sleep(0.4)
    click(dimensions[0] + 780, dimensions[1] + 770)  # Нажимает на подтверждение
    if idc == True:
        if checkClient(path_block, dimensions) != None:
            time.sleep(1)
            click(dimensions[0] + 680, dimensions[1] + 550)


def eventLoop(ban, pick, idc):
    while keyboard.is_pressed("=") == False:
        try:
            hwnd = win32gui.FindWindow(None, r"League of Legends")
            dimensions = win32gui.GetWindowRect(hwnd)
            if checkClient(path_ban, dimensions) != None:
                print("Found ban")
                autoBan(dimensions, ban, idc)
                time.sleep(5)
            if checkClient(path_bar, dimensions) != None:
                if checkClient(path_btn, dimensions) != None:
                    print("Found pick")
                    autoPick(dimensions, pick)
                    break
        except:
            continue


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            print(path_ui)
            super(Ui, self).__init__()
            uic.loadUi(path_ui, self)
            self.show()
            self.run.clicked.connect(self.submit)
        except:
            print("IDK my lord")
            input(" ")

    def submit(self):
        try:
            champ_ban = self.ban.text()
            champ_pick = self.pick.text()
            idc = self.idontcare.isChecked()
            self.close()
            try:
                eventLoop(champ_ban, champ_pick, idc)
            except:
                print("Can't access function eventLoop")
            self.show()
        except:
            print(f"Submit problem: {champ_ban}, {champ_pick}, {idc}")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
