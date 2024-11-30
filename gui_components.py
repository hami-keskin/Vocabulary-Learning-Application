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

def create_label(frame, text, font=("Arial", 12), fg="white", bg="black", pady=0, padx=0):
    label = tk.Label(frame, text=text, font=font, fg=fg, bg=bg, pady=pady, padx=padx)
    label.pack(pady=pady, padx=padx)
    return label

def create_button(frame, text, command, fg="white", bg="black"):
    button = tk.Button(frame, text=text, command=command, fg=fg, bg=bg)
    button.pack(pady=10)
    return button

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def center_frame(root):
    frame = tk.Frame(root, bg="#1e1e1e")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame
