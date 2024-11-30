from tkinter import messagebox
import tkinter as tk

from date_utils import get_today
from gui_utils import clear_window, center_frame, create_label, create_button
from main import main_menu, root, words
from speech_utils import speak_with_delay, speak
from utils import copy_to_clipboard


def learn_new_words_gui():
    unknown = {word: data for word, data in words.items() if not data["known"] and not data["retry"]}
    if not unknown:
        messagebox.showinfo("Bilgi", "Ezberlenecek yeni kelime yok!")
        return

    def update_word_labels():
        word_label.config(text=current_word)
        translation_label.config(text=current_data['translation'])
        speak_with_delay(current_word, delay=1000)

    def mark_memorized():
        current_data["memorized"] = True
        next_word()

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

    def correct_translation():
        new_translation = simple_dialog("Yeni Çeviriyi Girin", "Çeviriyi Girin:")
        if new_translation:
            current_data['translation'] = new_translation
            update_word_labels()

    def disable_button_for_delay(button):
        button.config(state=tk.DISABLED)
        root.after(2000, lambda: button.config(state=tk.NORMAL))

    clear_window()
    frame = center_frame()
    current_word, current_data = unknown.popitem()
    word_label = create_label(frame, current_word, font=("Arial", 24))
    translation_label = create_label(frame, current_data['translation'], font=("Arial", 20))
    speak_with_delay(current_word, delay=1000)

    button_biliyorum = create_button(frame, "Biliyorum", mark_known)
    button_biliyorum.config(command=lambda: [mark_known(), disable_button_for_delay(button_biliyorum)])

    button_tekraret = create_button(frame, "Tekrar Et", add_to_retry)
    button_tekraret.config(command=lambda: [add_to_retry(), disable_button_for_delay(button_tekraret)])

    button_sonraki = create_button(frame, "Sonraki Kelime", next_word)
    button_sonraki.config(command=lambda: [next_word(), disable_button_for_delay(button_sonraki)])

    button_correct = create_button(frame, "Çeviriyi Düzelt", correct_translation)
    button_correct.config(command=lambda: [correct_translation(), disable_button_for_delay(button_correct)])

    create_button(frame, "Kelimeyi Kopyala", lambda: copy_to_clipboard(current_word))
    create_button(frame, "Kelimeyi Sesli Oku", lambda: speak(current_word))
    create_button(frame, "Geri Dön", main_menu)

def simple_dialog(title, prompt):
    def on_submit():
        entered_value = entry.get()
        if entered_value:
            top.destroy()
            result[0] = entered_value

    result = [None]
    top = tk.Toplevel(root)
    top.title(title)
    create_label(top, prompt)
    entry = tk.Entry(top)
    entry.pack(pady=10)
    create_button(top, "Tamam", on_submit)
    entry.focus_set()
    top.wait_window(top)
    return result[0]
