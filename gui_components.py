import tkinter as tk

def apply_dark_mode(widget):
    widget.configure(bg="#1e1e1e")
    if isinstance(widget, (tk.Tk, tk.Toplevel)):
        widget.option_add("*Background", "#1e1e1e")
        widget.option_add("*Foreground", "#ffffff")
        widget.option_add("*Font", "Arial 14")
        widget.option_add("*Button.Background", "#2a2a2a")
        widget.option_add("*Button.Foreground", "#ffffff")
        widget.option_add("*Button.Font", "Arial 14 bold")
        widget.option_add("*Label.Font", "Arial 16 bold")
        widget.option_add("*Button.ActiveBackground", "#3a3a3a")
        widget.option_add("*Button.ActiveForeground", "#ffffff")

def create_label(parent, text, font=("Arial", 16), pady=20):
    label = tk.Label(parent, text=text, font=font, bg="#1e1e1e", fg="#ffffff")
    label.pack(pady=pady)
    return label

def create_button(parent, text, command, pady=10, width=20):
    button = tk.Button(parent, text=text, command=command, pady=pady, width=width)
    button.pack()
    return button

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def center_frame(root):
    frame = tk.Frame(root, bg="#1e1e1e")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame
