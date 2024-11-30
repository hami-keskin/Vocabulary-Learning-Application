import tkinter as tk
from tkinter import messagebox

from file_operations import load_words, save_words
from gui_components import apply_dark_mode, clear_window, center_frame, create_button
from learning import learn_new_words_gui, review_words_gui
from statistics import show_statistics_gui
from utils import get_today

# Application startup
file_path = 'translated_words.json'
words = load_words(file_path)

def main_menu(root):
    from learning import learn_new_words_gui, review_words_gui
    from statistics import show_statistics_gui

    def exit_program():
        save_words(file_path, words)
        if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?"):
            root.destroy()

    clear_window(root)
    frame = center_frame(root)
    create_button(frame, "Yeni Kelime Öğren", lambda: learn_new_words_gui(root, words, file_path, main_menu))
    create_button(frame, "Kelime Tekrarı Yap", lambda: review_words_gui(root, words, file_path, main_menu))
    create_button(frame, "İstatistikleri Göster", lambda: show_statistics_gui(root, words, file_path, main_menu))
    create_button(frame, "Kaydet", lambda: save_words(file_path, words))
    create_button(frame, "Çık", exit_program)

root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
main_menu(root)
root.mainloop()
