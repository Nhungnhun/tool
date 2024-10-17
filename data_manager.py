import os
from tkinter import messagebox

# Hàm đọc dữ liệu từ file
def read_data(data_file):
    if not os.path.exists(data_file):
        return []
    
    with open(data_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        items = line.strip().split(', ')
        if len(items) == 8:
            entry = (
                items[0] == 'True',
                items[1] == 'True',
                items[2] == 'True',
                items[3],
                items[4],
                items[5],
                items[6],
                items[7]
            )
            data.append(entry)
    
    return data

def add_data(sample_data, server_combobox, tree, data_file):
    new_index = len(sample_data)
    server = server_combobox.get()
    new_data = (False, False, False, f'Nhân Vật {new_index + 1}', str(new_index * 10), f"{new_index}. OFFLINE", server, f'Tài khoản {new_index + 1}')
    
    sample_data.append(new_data)
    tree.insert('', 'end', values=new_data + ("Show",))
    write_data(data_file, sample_data)

def remove_data(sample_data, tree, data_file):
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        sample_data.pop(index)
        tree.delete(selected_item)
        write_data(data_file, sample_data)

def show_selected_data(event, tree):
    # Kiểm tra xem tree có phải là None không
    if tree is None:
        print("Tree is None, cannot select item.")
        return
    
    # Lấy item đã chọn
    selected_item = tree.selection()
    
    if selected_item:
        cur_item = tree.focus()
        
        if event:  # Kiểm tra nếu event không phải là None
            col_id = tree.identify_column(event.x)  # Nhận cột của sự kiện
            if col_id == '#9':  # Kiểm tra nếu cột là cột mà bạn muốn xử lý
                item_values = tree.item(cur_item)['values']  # Lấy giá trị item
                # Hiển thị thông tin
                message = (f"Thông tin hàng đã chọn:\n"
                            f"x10: {item_values[0]}\n"
                            f"Chọn: {item_values[1]}\n"
                            f"Buff: {item_values[2]}\n"
                            f"Nhân Vật: {item_values[3]}\n"
                            f"Yên 1h: {item_values[4]}\n"
                            f"Trạng Thái: {item_values[5]}\n"
                            f"Server: {item_values[6]}\n"
                            f"Tài Khoản: {item_values[7]}")
                QtWidgets.QMessageBox.information(tree, "Thông tin hàng", message)
        else:  # Xử lý trường hợp không có sự kiện
            item_values = tree.item(selected_item)['values']  # Lấy giá trị item
            # Hiển thị thông tin
            message = (f"Thông tin hàng đã chọn:\n"
                        f"x10: {item_values[0]}\n"
                        f"Chọn: {item_values[1]}\n"
                        f"Buff: {item_values[2]}\n"
                        f"Nhân Vật: {item_values[3]}\n"
                        f"Yên 1h: {item_values[4]}\n"
                        f"Trạng Thái: {item_values[5]}\n"
                        f"Server: {item_values[6]}\n"
                        f"Tài Khoản: {item_values[7]}")
            QtWidgets.QMessageBox.information(tree, "Thông tin hàng", message)
    else:
        print("No item is selected.")


def write_data(data_file, sample_data):
    with open(data_file, 'w', encoding='utf-8') as file:
        for entry in sample_data:
            file.write(', '.join(str(x) for x in entry) + '\n')
