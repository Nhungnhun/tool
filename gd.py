import tkinter as tk
from tkinter import ttk

def on_show_button_click(item_values):
    print(f"Show button clicked for: {item_values}")

root = tk.Tk()
root.title("Table Interface")

columns = ("x10", "Chọn", "Buff", "Nhân Vật", "Yên 1h", "Trạng Thái", "Server", "Tài Khoản", "Show")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

# Sample data
data = [
    (False, False, False, "", "", "0. OFFLINE", "Shuriken", "xpandex"),
    (False, False, False, "", "", "1. OFFLINE", "Sensha", "tepthui47"),
    (False, False, True, "", "", "2. OFFLINE", "Tessen", "boyburbery"),
    (False, False, False, "", "", "3. OFFLINE", "Sensha", "danhprod1"),
    (False, False, False, "", "", "4. OFFLINE", "Sensha", "daohaui"),
    (False, True, False, "", "", "5. OFFLINE", "Sensha", "hopgame98"),
    (False, True, False, "", "", "6. OFFLINE", "Kunai", "zbuff2"),
]

for item in data:
    item_id = tree.insert("", "end", values=item)
    # Create a button for the "Show" column
    btn = ttk.Button(root, text="SHOW", command=lambda item=item: on_show_button_click(item))
    tree.set(item_id, column="Show", value="")  # Clear the text in the "Show" column
    tree.item(item_id, tags=item_id)
    tree.tag_bind(item_id, '<ButtonRelease-1>', lambda e, item=item: on_show_button_click(item))
    tree.place(x=0, y=0)

tree.pack(expand=True, fill="both")

root.mainloop()