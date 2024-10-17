import tkinter as tk
import subprocess
import time
import pyautogui
import threading

microemulator_path = "E:/Tester/AngelChipEmulator.jar"
open_jar_count = 0
credentials_file = "acc.txt"

def check_log(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        decoded_line = line.strip() 
        if "openJar" in decoded_line:
            status_label.config(text="Đã mở file game thành công!", fg="green")
            # pyautogui.press("down")
            # pyautogui.press("down")
            # pyautogui.press("f2")

def read_credentials():
    try:
        with open(credentials_file, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                username = lines[0].strip()
                password = lines[1].strip()
                return username, password
            else:
                return "", ""
    except FileNotFoundError:
        return "", ""

def save_credentials(username, password):
    with open(credentials_file, 'w') as file:
        file.write(f"{username}\n{password}")
            

def open_game():
    jar_file_path = "C:/Users/Hoantm/Downloads/V6 X6.jar"

    if jar_file_path:
        command = ["java", "-jar", microemulator_path, jar_file_path]
        try:
            #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subprocess.Popen(command)
            time.sleep(2)
            pyautogui.press("enter")
            # threading.Thread(target=check_log, args=(process,), daemon=True).start()
            status_label.config(text="Đang mở game...", fg="black")

            status_label.config(text="Đã mở game thành công!", fg="green")

            # Tiến hành các thao tác tiếp theo
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            time.sleep(15)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            time.sleep(10)
            pyautogui.press("right")
            pyautogui.press("enter")
            status_label.config(text="Đăng nhập thành công!", fg="green")

            # Nhập thông tin tên người dùng và mật khẩu
            username = username_entry.get()
            password = password_entry.get()
            save_credentials(username, password)
            pyautogui.typewrite(username)
            pyautogui.press("down")
            pyautogui.typewrite(password)
            pyautogui.press("enter")
            pyautogui.press("down")
            pyautogui.press("enter")
            time.sleep(10)
            pyautogui.press("right")
            pyautogui.press("enter")
        except Exception as e:
            status_label.config(text=f"Có lỗi xảy ra: {e}", fg="red")

root = tk.Tk()
root.title("Game Launcher")

root.geometry("400x300")

# Nhập liệu tên người dùng
tk.Label(root, text="Tên người dùng:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Nhập liệu mật khẩu
tk.Label(root, text="Mật khẩu:").pack(pady=5)
password_entry = tk.Entry(root, show="*")  # show="*" ẩn mật khẩu
password_entry.pack(pady=5)

# Đọc tên người dùng và mật khẩu từ file ghi chú khi chương trình khởi động
username, password = read_credentials()
username_entry.insert(0, username)
password_entry.insert(0, password)

open_button = tk.Button(root, text="Mở Game", command=open_game)
open_button.pack(pady=20)

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

root.mainloop()
