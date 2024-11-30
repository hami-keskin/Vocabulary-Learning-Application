import tkinter as tk
from tkinter import messagebox
from file_operations import load_words, save_words
from learn_new_words_gui import learn_new_words_gui
from review_words_gui import review_words_gui
from show_statistics_gui import show_statistics_gui
from theme_utils import apply_dark_mode
from gui_utils import center_frame, clear_window, create_button

# Dosya yolu ve kelimelerin yüklenmesi
file_path = 'translated_words.json'
words = load_words(file_path)

# Ana menü
def main_menu():
    clear_window()
    frame = center_frame()
    create_button(frame, "Yeni Kelime Öğren", lambda: learn_new_words_gui(root, words, main_menu))
    create_button(frame, "Kelime Tekrarı Yap", lambda: review_words_gui(root, words, main_menu, file_path))
    create_button(frame, "İstatistikleri Göster", lambda: show_statistics_gui(root, words, main_menu))
    create_button(frame, "Kaydet", lambda: save_words(file_path, words))
    create_button(frame, "Çık", exit_program)

# Çıkış işlemi
def exit_program():
    save_words(file_path, words)
    if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?"):
        root.destroy()

# Uygulama başlangıcı
root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)
main_menu()
root.mainloop()
