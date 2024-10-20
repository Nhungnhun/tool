import sys
import threading
import time
import psutil
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from data_manager import read_data, write_data, read_maps_from_file
import subprocess
import sys
import os
from main import GameHandler
from database import check_key_from_db

data_file = "data.txt"
map_file = "map.txt"
maps = read_maps_from_file(map_file)
sample_data = read_data(data_file)

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.selected_row = None
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.create_top_area(layout)
        self.create_system_info_area(layout)
        self.create_data_display_area(layout)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.itemChanged.connect(self.on_checkbox_changed)
        self.create_settings_area(layout)
        self.setLayout(layout)
        self.setWindowTitle('Game Tool')
        self.setGeometry(100, 100, 1175, 600)
        self.setWindowIcon(QtGui.QIcon('C:/Users/Vu Quang Tung/Downloads/74c532531a8da3d3fa9c.jpg'))
        self.show()

    def create_top_area(self, layout):
        top_layout = QtWidgets.QHBoxLayout()
        
        btn_open_game = QtWidgets.QPushButton("Mở Game")
        btn_open_game.setFixedSize(80, 30)  # Set size to 80x60 pixels
        btn_open_game.clicked.connect(self.open_game)
        top_layout.addWidget(btn_open_game)
        
        btn_add = QtWidgets.QPushButton("Thêm")
        btn_add.setFixedSize(80, 30)  # Set size to 80x60 pixels
        btn_add.clicked.connect(self.add_data)
        top_layout.addWidget(btn_add)
        
        btn_remove = QtWidgets.QPushButton("Xóa")
        btn_remove.setFixedSize(80, 30)  # Set size to 80x60 pixels
        btn_remove.clicked.connect(self.remove_data)
        top_layout.addWidget(btn_remove)
        
        btn_update = QtWidgets.QPushButton("Cập nhật")
        btn_update.setFixedSize(80, 30)  # Set size to 80x60 pixels
        btn_update.clicked.connect(self.update_data)
        top_layout.addWidget(btn_update)
        
        layout.addLayout(top_layout)



    def create_system_info_area(self, layout):
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        system_info_layout = QtWidgets.QVBoxLayout()
        self.cpu_label = QtWidgets.QLabel("CPU: ")
        self.ram_label = QtWidgets.QLabel("RAM: ")
        system_info_layout.addWidget(self.cpu_label)
        system_info_layout.addWidget(self.ram_label)
        frame.setLayout(system_info_layout)
        layout.addWidget(frame)
        threading.Thread(target=self.update_system_info, daemon=True).start()

    def update_system_info(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            self.cpu_label.setText(f"CPU: {cpu_percent}%")
            self.ram_label.setText(f"RAM: {ram_percent}%")
            time.sleep(1)

    def create_data_display_area(self, layout):
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["x10", "Chọn", "Buff", "Nhân Vật", "Yên 1h", "Trạng Thái", "Server", "Tài Khoản", "Show"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.cellClicked.connect(self.on_row_select)
        self.add_data_to_table()

        layout.addWidget(self.table)

    def add_data_to_table(self):
        self.table.setRowCount(len(sample_data))
        for row_index, data in enumerate(sample_data):
            for col_index, item in enumerate(data):
                if col_index < 3:
                    checkbox_item = QtWidgets.QTableWidgetItem()
                    checkbox_item.setCheckState(Qt.Checked if item else Qt.Unchecked)
                    checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    checkbox_item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_index, col_index, checkbox_item)
                elif col_index == 6:
                    combo_box = QtWidgets.QComboBox(self)
                    combo_box.addItems(["Bokken", "Shuriken", "Tessen", "Kunai", "Katana", "Tone", "Sanzu", "Sensha", "Fukiya", "Tekkan"])
                    combo_box.setCurrentText(str(item))
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index: self.update_combo_value(row, index))
                    self.table.setCellWidget(row_index, col_index, combo_box)
                elif col_index == 7:
                    account_value = str(item).split("/")[0] if item else ""
                    text_item = QtWidgets.QTableWidgetItem(account_value)
                    text_item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_index, col_index, text_item)
                else:
                    text_item = QtWidgets.QTableWidgetItem(str(item) if item is not None else "")
                    text_item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_index, col_index, text_item)
            show_button = QtWidgets.QPushButton("Hiển thị")
            show_button.clicked.connect(lambda checked, row=row_index: self.show_row_data(row))
            self.table.setCellWidget(row_index, 8, show_button)

    def update_combo_value(self, row, index):
        combo_box = self.table.cellWidget(row, 6)
        new_value = combo_box.currentText()
        row_data = list(sample_data[row])
        row_data[6] = new_value
        sample_data[row] = tuple(row_data)
        write_data(data_file, sample_data)

    def on_checkbox_changed(self, item):
        row = item.row()
        column = item.column()
        if column < 3:
            is_checked = item.checkState() == Qt.Checked
            row_data = list(sample_data[row])
            row_data[column] = is_checked
            sample_data[row] = tuple(row_data)
            write_data(data_file, sample_data)

    def create_settings_area(self, layout):
        settings_layout = QtWidgets.QHBoxLayout()
        settings_label = QtWidgets.QLabel("Cài đặt đánh quái")
        settings_layout.addWidget(settings_label)
        self.server_combobox = QtWidgets.QComboBox()
        self.server_combobox.addItems(maps)
        settings_layout.addWidget(self.server_combobox)
        self.chk_support_skill = QtWidgets.QCheckBox("Dùng chiêu hỗ trợ")
        settings_layout.addWidget(self.chk_support_skill)
        btn_start_auto = QtWidgets.QPushButton("Bật Auto")
        btn_start_auto.clicked.connect(lambda: print("Auto started"))
        settings_layout.addWidget(btn_start_auto)
        layout.addLayout(settings_layout)

    def show_row_data(self, row):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Thông tin nhân vật")
        dialog.setGeometry(100, 100, 400, 300)
        layout = QtWidgets.QVBoxLayout(dialog)
        
        row_data = sample_data[row]
        for idx, item in enumerate(row_data):
            if idx > 2:
                if idx == 5:
                    index, status = item.split(".")
                    layout.addWidget(QtWidgets.QLabel(f"Trạng thái : {status}"))  
                elif idx == 7:
                    if "/" in item:
                        user, password = item.split("/", 1)
                        layout.addWidget(QtWidgets.QLabel(f"Tài khoản : {user}"))
                        layout.addWidget(QtWidgets.QLabel(f"Mật khẩu : {password}"))
                else:
                    layout.addWidget(QtWidgets.QLabel(f"{self.table.horizontalHeaderItem(idx).text()}: {item}"))
        
        btn_close = QtWidgets.QPushButton("Đóng")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        dialog.exec_()



    def update_data(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Xác nhận cập nhật",
            "Bạn có đồng ý cập nhật không?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.perform_update()
        
    def perform_update(self):
        try:
            subprocess.check_call(["git", "pull"])
            QtWidgets.QMessageBox.information(self, "Cập nhật", "Cập nhật thành công! Đang khởi động lại ứng dụng...")
            QtWidgets.QApplication.quit()
            os.execv(sys.executable, ['python'] + sys.argv)          
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi cập nhật: {e}")

    def open_game(self):
        if self.selected_row is not None:
            row_data = sample_data[self.selected_row]  # Lấy dữ liệu của hàng đã chọn
            print(row_data)
            # Nếu bạn muốn mở game, gọi hàm mở game tại đây
            # self.game_handler.open_game(row_data)  # Gọi hàm mở game với dữ liệu hàng đã chọn
        else:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng trước khi mở game.")
        # self.game_handler = GameHandler(self)
        # self.game_handler.open_game(row_data)

    def add_data(self):
        if len(sample_data) >= 20:
            QtWidgets.QMessageBox.warning(
                self, 
                "Cảnh báo", 
                "Bạn chỉ thêm được 20 tài khoản."
                "Cần báo thêm admin để được thêm tài khoản vào tool"
            )
            return
        new_index = len(sample_data)
        new_data = (
            False,
            True,
            False,
            " ",
            " ",
            f"{new_index}. OFFLINE",
            "Brokken",
            ""
        )
        sample_data.append(new_data)
        self.add_data_to_table()
        write_data(data_file, sample_data)


    def on_row_select(self, row, column):
        if self.selected_row is not None:
            previous_item = self.table.item(self.selected_row, 0)
            if previous_item:
                previous_item.setBackground(QtGui.QColor("white"))
        self.selected_row = row
        self.table.item(row, 0).setBackground(QtGui.QColor("lightgreen"))


    def on_cell_double_clicked(self, row, column):
        if column == 7:
            item_username = self.table.item(row, column)
            if item_username is not None:
                current_username = item_username.text()
                print(current_username)
                dialog = QtWidgets.QDialog(self)
                dialog.setWindowTitle("Sửa Dữ Liệu")
                dialog.setGeometry(100, 100, 400, 300)
                layout = QtWidgets.QVBoxLayout(dialog)
                label_username = QtWidgets.QLabel("User:")
                layout.addWidget(label_username)
                edit_username = QtWidgets.QLineEdit(current_username)
                layout.addWidget(edit_username)
                label_password = QtWidgets.QLabel("Password:")
                layout.addWidget(label_password)
                edit_password = QtWidgets.QLineEdit()
                edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
                layout.addWidget(edit_password)
                btn_ok = QtWidgets.QPushButton("OK")
                layout.addWidget(btn_ok)
                def update_value():
                    new_username = edit_username.text()
                    new_password = edit_password.text()
                    item_username.setText(new_username)
                    row_data = list(sample_data[row])
                    row_data[column] = f"{new_username}/{new_password}"
                    sample_data[row] = tuple(row_data)

                    write_data(data_file, sample_data)
                    dialog.accept()

                btn_ok.clicked.connect(update_value)
                dialog.exec_()

    def remove_data(self, row):
        if self.selected_row is not None:
            del sample_data[self.selected_row]
            self.add_data_to_table()
            self.selected_row = None
            write_data(data_file, sample_data)

def get_admin_key():
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Quản lý")
    dialog.setFixedSize(300, 150)  # Đặt kích thước cho hộp thoại

    layout = QtWidgets.QVBoxLayout(dialog)
    label = QtWidgets.QLabel("Please enter the admin key:")
    layout.addWidget(label)

    input_field = QtWidgets.QLineEdit()
    input_field.setEchoMode(QtWidgets.QLineEdit.Password)  # Hiển thị ký tự ẩn
    layout.addWidget(input_field)

    button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    layout.addWidget(button_box)

    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)

    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        return input_field.text(), True
    else:
        return None, False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Loop until the correct key is entered
    while True:
        key, ok = get_admin_key()
        
        if ok and key == check_key_from_db(key):
            my_app = MyApp()
            my_app.show()
            sys.exit(app.exec_())
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Invalid key! Please try again.")