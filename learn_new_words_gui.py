import tkinter as tk
from tkinter import messagebox
from speech_utils import speak_with_delay
from gui_utils import create_label, create_button, clear_window, center_frame
from date_utils import get_today

def learn_new_words_gui(root, words, main_menu):
    unknown = {word: data for word, data in words.items() if not data["known"] and not data["retry"]}
    if not unknown:
        messagebox.showinfo("Bilgi", "Ezberlenecek yeni kelime yok!")
        return

    def update_word_labels():
        word_label.config(text=current_word)
        translation_label.config(text=current_data['translation'])
        speak_with_delay(root, current_word, delay=1000)

    def mark_known():
        current_data["known"] = True
        current_data["correct_streak"] = 0
        next_word()

    def add_to_retry():
        current_data.update({"retry": True, "correct_streak": 0, "date": get_today()})
        next_word()

    def next_word():
        nonlocal current_word, current_data
        if unknown:
            current_word, current_data = unknown.popitem()
            update_word_labels()
        else:
            messagebox.showinfo("Bilgi", "Ezberlenecek kelime kalmadı!")
            main_menu()

    clear_window()
    frame = center_frame()
    current_word, current_data = unknown.popitem()
    word_label = create_label(frame, current_word, font=("Arial", 24))
    translation_label = create_label(frame, current_data['translation'], font=("Arial", 20))
    speak_with_delay(root, current_word, delay=1000)

    create_button(frame, "Biliyorum", mark_known)
    create_button(frame, "Tekrar Et", add_to_retry)
    create_button(frame, "Sonraki Kelime", next_word)
    create_button(frame, "Geri Dön", main_menu)
