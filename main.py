import os
import subprocess
from PyQt5 import QtWidgets
import threading
import pyautogui
import time

microemulator_path = "E:/Tester/AngelChipEmulator.jar"
jar_file_path = "C:/Users/Hoantm/Downloads/v1prox6.jar"

class GameHandler:
    def __init__(self, parent):
        self.parent = parent

    def open_game(self, row):
        thread = threading.Thread(target=self.run_open_game, args=(row,))
        thread.start()

    def run_open_game(self, row_data):
        user_pass = row_data[7]
        user, password = user_pass.split('/')
        # ind, status = row_data[5].split('.')
        # print(ind)

        print("User:", user)
        print("Password:", password)

        if os.path.exists(microemulator_path):
            try:
                command = ["java", "-jar", microemulator_path, jar_file_path]
                subprocess.Popen(command)
                time.sleep(5)
                pyautogui.press("enter")
                time.sleep(5)
                pyautogui.press("enter")
                time.sleep(10)
                pyautogui.press("down")
                pyautogui.press("down")
                pyautogui.press("down")
                pyautogui.press("enter")
                time.sleep(1)
                pyautogui.typewrite(user)
                pyautogui.press("down")
                pyautogui.typewrite(password)
                pyautogui.press("f2")
                pyautogui.press("down")
                pyautogui.press("enter")
                time.sleep(10)
                pyautogui.press("right")
                pyautogui.click()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self.parent, "Lỗi", f"Không thể mở emulator: {e}")
        else:
            QtWidgets.QMessageBox.warning(self.parent, "Cảnh báo", "File .jar không tồn tại.")
