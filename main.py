import tkinter as tk

from DZ.word_processing_gui import processing_gui
from DZ.utils import show_notification
from DZ.file_operations import load_json, save_json
from DZ.gui_components import apply_dark_mode, clear_window, center_frame, create_button

# Dosya yolu ve kelime yükleme
file_path = 'translated_words.json'
words = load_json(file_path)

# Ana menüye yeni seçenek ekleme
def main_menu(root):
    from DZ.learn_new_words_gui import learn_new_words_gui
    from DZ.review_words_gui import review_words_gui
    from DZ.user_statistics import show_statistics_gui

    def handle_button_click(action):
        if action == "exit":
            save_json(file_path, words)
            root.after(100, root.quit)
        elif action == "save":
            save_json(file_path, words)
            show_notification(root, "Veriler başarıyla kaydedildi!")
        elif action == processing_gui:
            action(root, main_menu, words)  # words parametresini geçir
        else:
            action(root, words, file_path, main_menu)

    actions = [
        ("Yeni Kelime Öğren", learn_new_words_gui),
        ("Kelime Tekrarı Yap", review_words_gui),
        ("İstatistikleri Göster", show_statistics_gui),
        ("Kelime ekle", processing_gui),  # Yeni seçenek
        ("Kaydet", "save"),
        ("Çık", "exit"),
    ]

    clear_window(root)
    frame = center_frame(root)
    for text, action in actions:
        create_button(frame, text, lambda act=action: handle_button_click(act))

# Uygulama başlangıcı
file_path = 'translated_words.json'
words = load_json(file_path)
root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
main_menu(root)
root.mainloop()
