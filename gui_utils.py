import tkinter as tk

def create_label(parent, text, font=("Arial", 16), pady=20):
    label = tk.Label(parent, text=text, font=font, bg="#1e1e1e", fg="#ffffff")
    label.pack(pady=pady)
    return label

def create_button(parent, text, command, pady=10, width=20):
    button = tk.Button(parent, text=text, command=command, pady=pady, width=width)
    button.pack()
    return button

def clear_window():
    for widget in tk._default_root.winfo_children():
        widget.destroy()

def center_frame():
    frame = tk.Frame(tk._default_root, bg="#1e1e1e")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame
