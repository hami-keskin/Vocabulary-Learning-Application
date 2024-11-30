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
