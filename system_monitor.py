import psutil
import time

def update_system_info(root, cpu_label, ram_label):
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        ram_percent = ram_info.percent
        
        # Cập nhật nhãn thông tin trong GUI bằng cách sử dụng `after` để tránh xung đột với luồng GUI
        root.after(0, cpu_label.config, {'text': f"CPU: {cpu_percent}%"})
        root.after(0, ram_label.config, {'text': f"RAM: {ram_percent}%"})
        
        time.sleep(0.1)
