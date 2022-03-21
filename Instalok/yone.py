from pprint import pprint
from tkinter import W
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con, win32gui


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


champ = input("Enter champion name: ")
index = None

with open("ru_names.txt", encoding="utf-8") as file:
    data = file.read()
    new_data = data.split(",")
    for item in new_data:
        if item == champ:
            index = new_data.index(item)

with open("eng_names.txt") as file:
    data = file.read()
    new_data = data.split(",")
    for item in new_data:
        if item == champ:
            eng_champ = champ
    if index != None:
        eng_champ = new_data[index]


while keyboard.is_pressed("=") == False:
    try:
        hwnd = win32gui.FindWindow(None, r"League of Legends")
        dimensions = win32gui.GetWindowRect(hwnd)
        if (
            pyautogui.locateOnScreen(
                "ban.png", confidence=0.8, region=dimensions, grayscale=True
            )
            != None
        ):
            click(dimensions[0] + 958, dimensions[1] + 128)  # Нажимает на строку поиска
            keyboard.write("Ёнэ")
            time.sleep(0.5)
            click(dimensions[0] + 480, dimensions[1] + 200)  # Нажимает на чемпиона
            time.sleep(0.4)
            click(dimensions[0] + 780, dimensions[1] + 770)  # Нажимает на бан
            time.sleep(1)
            if (
                pyautogui.locateOnScreen(
                    f"{eng_champ.lower()}.png",
                    confidence=0.8,
                    region=dimensions,
                    grayscale=True,
                )
                != None
            ):
                # Подтверждает бан если у союзника был этот чемпион
                click(dimensions[0] + 680, dimensions[1] + 550)
            time.sleep(30)
        else:
            pass
    except:
        continue
