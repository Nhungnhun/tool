import sys
import threading
import time
import psutil
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt  # Thêm dòng này
from data_manager import read_data, write_data

# Tên file lưu trữ dữ liệu
data_file = "data.txt"

# Danh sách dữ liệu mẫu
sample_data = read_data(data_file)

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.selected_row = None  # Biến để lưu chỉ số hàng đã chọn
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.create_top_area(layout)
        self.create_system_info_area(layout)
        self.create_data_display_area(layout)
        self.create_settings_area(layout)
        self.setLayout(layout)
        self.setWindowTitle('Game Tool')
        self.setGeometry(100, 100, 1050, 600)
        self.show()

    def create_top_area(self, layout):
        top_layout = QtWidgets.QHBoxLayout()
        btn_open_game = QtWidgets.QPushButton("Mở Game")
        btn_open_game.clicked.connect(self.open_game)
        top_layout.addWidget(btn_open_game)

        btn_add = QtWidgets.QPushButton("Thêm")
        btn_add.clicked.connect(self.add_data)
        top_layout.addWidget(btn_add)



        btn_remove = QtWidgets.QPushButton("Xóa")
        btn_remove.clicked.connect(self.remove_data)
        top_layout.addWidget(btn_remove)

        layout.addLayout(top_layout)

    def create_system_info_area(self, layout):
        system_info_layout = QtWidgets.QHBoxLayout()
        self.cpu_label = QtWidgets.QLabel("CPU: ")
        self.ram_label = QtWidgets.QLabel("RAM: ")
        system_info_layout.addWidget(self.cpu_label)
        system_info_layout.addWidget(self.ram_label)

        layout.addLayout(system_info_layout)

        threading.Thread(target=self.update_system_info, daemon=True).start()

    def update_system_info(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent

            self.cpu_label.setText(f"CPU: {cpu_percent}%")
            self.ram_label.setText(f"RAM: {ram_percent}%")

            time.sleep(1)

    def create_data_display_area(self, layout):
        # Tạo QTableWidget
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(8)  # Số lượng cột
        self.table.setHorizontalHeaderLabels(["x10", "Chọn", "Buff", "Nhân Vật", "Yên 1h", "Trạng Thái", "Server", "Tài Khoản"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # Chọn hàng
        self.table.setAlternatingRowColors(True)  # Tô màu hàng chẵn và lẻ khác nhau

        # Kết nối sự kiện chọn hàng
        self.table.cellClicked.connect(self.on_row_select)

        # Thêm dữ liệu vào bảng
        self.add_data_to_table()

        layout.addWidget(self.table)

    def add_data_to_table(self):
        self.table.setRowCount(len(sample_data))  # Thiết lập số hàng
        for row_index, data in enumerate(sample_data):
            for col_index, item in enumerate(data):
                if col_index < 3:  # Các cột x10, Chọn, Buff
                    checkbox_item = QtWidgets.QTableWidgetItem()
                    checkbox_item.setCheckState(Qt.Checked if item else Qt.Unchecked)
                    checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # Cho phép người dùng thay đổi checkbox
                    checkbox_item.setTextAlignment(Qt.AlignCenter)  # Căn giữa checkbox
                    self.table.setItem(row_index, col_index, checkbox_item)
                else:
                    text_item = QtWidgets.QTableWidgetItem(str(item))
                    text_item.setTextAlignment(Qt.AlignCenter)  # Căn giữa nội dung text
                    self.table.setItem(row_index, col_index, text_item)



    def create_settings_area(self, layout):
        settings_layout = QtWidgets.QHBoxLayout()
        settings_label = QtWidgets.QLabel("Cài đặt đánh quái")
        settings_layout.addWidget(settings_label)

        self.server_combobox = QtWidgets.QComboBox()
        self.server_combobox.addItems([f'Server {i}' for i in range(1, 11)])
        settings_layout.addWidget(self.server_combobox)

        self.chk_support_skill = QtWidgets.QCheckBox("Dùng chiêu hỗ trợ")
        settings_layout.addWidget(self.chk_support_skill)

        btn_start_auto = QtWidgets.QPushButton("Bắt Auto")
        btn_start_auto.clicked.connect(lambda: print("Auto started"))
        settings_layout.addWidget(btn_start_auto)

        layout.addLayout(settings_layout)

    def open_game(self):
        selected_items = [self.table.item(row, 0).text() for row in range(self.table.rowCount()) if self.table.item(row, 0) is not None]
        print("Selected items:", selected_items)

    def add_data(self):
        new_index = len(sample_data)
        new_data = (False, False, False, f'Nhân Vật {new_index + 1}', str(new_index * 10), f"{new_index}. OFFLINE", f'Server {new_index + 1}', f'Tài khoản {new_index + 1}')
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
        # Chỉ cho phép sửa ô Tài Khoản (cột 7)
        if column == 7:  
            item = self.table.item(row, column)
            if item is not None:
                current_value = item.text()
                
                # Tạo một hộp thoại QDialog để sửa giá trị
                dialog = QtWidgets.QDialog(self)
                dialog.setWindowTitle("Sửa Dữ Liệu")
                dialog.setGeometry(100, 100, 400, 200)  # Kích thước hộp thoại

                layout = QtWidgets.QVBoxLayout(dialog)

                label = QtWidgets.QLabel("Nhập giá trị mới:")
                layout.addWidget(label)

                edit_line = QtWidgets.QLineEdit(current_value)
                layout.addWidget(edit_line)

                # Nút OK
                btn_ok = QtWidgets.QPushButton("OK")
                layout.addWidget(btn_ok)

                # Xử lý sự kiện khi nhấn nút OK
                def update_value():
                    new_value = edit_line.text()
                    item.setText(new_value)  # Cập nhật giá trị trong bảng
                    # Cập nhật dữ liệu trong sample_data
                    sample_data[row] = list(sample_data[row])  # Chuyển đổi tuple thành list để có thể sửa đổi
                    sample_data[row][column] = new_value  # Cập nhật giá trị mới
                    write_data(data_file, sample_data)  # Ghi lại vào tệp
                    dialog.accept()  # Đóng hộp thoại

                btn_ok.clicked.connect(update_value)

                dialog.exec_()  # Hiển thị hộp thoại

    def remove_data(self):
        if self.selected_row is not None:
            del sample_data[self.selected_row]
            self.add_data_to_table()
            self.selected_row = None
            write_data(data_file, sample_data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())
