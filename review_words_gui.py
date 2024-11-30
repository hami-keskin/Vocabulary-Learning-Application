import tkinter as tk
from tkinter import messagebox
import random
from gui_utils import create_label, create_button, clear_window, center_frame
from speech_utils import speak_with_delay
from date_utils import get_today, parse_date, format_date
from file_operations import save_words

def review_words_gui(root, words, main_menu, file_path):
    today = get_today()
    retry_words = {
        word: data for word, data in words.items()
        if data["retry"] and parse_date(data["date"]) <= parse_date(today)
    }
    if not retry_words:
        messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime yok!")
        return

    sorted_retry_words = sorted(retry_words.items(), key=lambda item: parse_date(item[1]["date"]))
    word_list = list(sorted_retry_words)
    current_index = 0

    def check_answer(selected):
        nonlocal current_index
        current_word, current_data = word_list[current_index]
        if selected == current_data["translation"]:
            words[current_word]["correct_streak"] += 1
            if words[current_word]["correct_streak"] >= 7:
                words[current_word]["retry"] = False
            messagebox.showinfo("Doğru!", "Doğru cevap!")
        else:
            words[current_word]["correct_streak"] = 0
            messagebox.showerror("Yanlış!", f"Doğru cevap: {current_data['translation']}")
        next_word()

    def next_word():
        nonlocal current_index
        current_index += 1
        if current_index >= len(word_list):
            save_words(file_path, words)
            messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime kalmadı!")
            main_menu()
            return
        current_word, current_data = word_list[current_index]
        word_label.config(text=current_word)
        speak_with_delay(root, current_word, delay=1000)
        update_choices(current_data["translation"])

    def update_choices(correct_translation):
        all_translations = [data["translation"] for data in words.values()]
        choices = random.sample(all_translations, min(3, len(all_translations) - 1))
        if correct_translation not in choices:
            choices.append(correct_translation)
        random.shuffle(choices)

        for btn in choice_buttons:
            btn.destroy()
        choice_buttons.clear()

        for choice in choices:
            btn = create_button(frame, choice, lambda c=choice: check_answer(c))
            choice_buttons.append(btn)

    clear_window()
    frame = center_frame()
    current_word, current_data = word_list[current_index]
    word_label = create_label(frame, current_word, font=("Arial", 24))
    speak_with_delay(root, current_word, delay=1000)

    choice_buttons = []
    update_choices(current_data["translation"])
    create_button(frame, "Geri Dön", lambda: [save_words(file_path, words), main_menu()])
