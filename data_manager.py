import os
from tkinter import messagebox

def read_data(data_file):
    if not os.path.exists(data_file):
        return []

    with open(data_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [tuple(line.strip().split(',')) for line in lines]
        for i in range(len(data)):
            row = data[i]
            data[i] = (
                row[0].strip() == 'True',
                row[1].strip() == 'True',
                row[2].strip() == 'True',
                row[3].strip(),
                row[4].strip(),
                row[5].strip(),
                row[6].strip(),
                row[7].strip(),
            )
        return data
    
def read_maps_from_file(file_path):
    maps = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            maps = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
    return maps

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


def write_data(data_file, sample_data):
    with open(data_file, 'w', encoding='utf-8') as file:
        for entry in sample_data:
            file.write(','.join(map(str, entry)) + '\n')
