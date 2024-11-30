import tkinter as tk
import random
from datetime import timedelta
from tkinter import messagebox

from file_operations import save_words
from utils import speak_with_delay, get_today, parse_date, format_date, speak
from gui_components import clear_window, create_label, create_button, center_frame

def review_words_gui(root, words, file_path, main_menu):
    today = get_today()
    retry_words = {
        word: data for word, data in words.items()
        if not data.get("known", False) and not data["memorized"] and data["retry"] and parse_date(data["date"]) <= parse_date(today)
    }
    if not retry_words:
        messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime yok!")
        return

    sorted_retry_words = sorted(retry_words.items(), key=lambda item: parse_date(item[1]["date"]))
    retry_words = {word: data for word, data in sorted_retry_words}
    word_list = list(retry_words.items())
    current_index = 0

    def check_answer(selected):
        nonlocal current_index
        current_word, current_data = word_list[current_index]

        if selected == current_data["translation"]:
            words[current_word]["correct_streak"] += 1
            streak = words[current_word]["correct_streak"]

            if streak < 7:
                words[current_word]["date"] = format_date(parse_date(today) + timedelta(days=1))
            elif streak < 21:
                words[current_word]["date"] = format_date(parse_date(today) + timedelta(days=7))
            else:
                words[current_word]["memorized"] = True
                words[current_word]["retry"] = False

            messagebox.showinfo("Doğru!", f"Doğru cevap! Doğru cevap serisi: {streak}")
        else:
            words[current_word]["correct_streak"] = 0
            messagebox.showerror("Yanlış!", f"Doğru cevap: {current_data['translation']}")

        next_word()

    def next_word():
        nonlocal current_index
        current_index += 1

        if current_index >= len(word_list):
            messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime kalmadı!")
            save_words(file_path, words)
            main_menu(root)
            return

        current_word, current_data = word_list[current_index]
        word_label.config(text=current_word)
        speak_with_delay(current_word, root, delay=1000)
        update_choices(current_data["translation"])

    def update_choices(current_translation):
        all_translations = [data["translation"] for data in words.values()]
        other_translations = list(set(t for t in all_translations if t != current_translation))

        wrong_choices = random.sample(other_translations, min(3, len(other_translations)))
        choices = wrong_choices + [current_translation]
        random.shuffle(choices)

        for btn in choice_buttons:
            btn.destroy()
        choice_buttons.clear()

        for choice in choices:
            btn = create_button(main_frame, choice, lambda c=choice: check_answer(c))
            choice_buttons.append(btn)

    clear_window(root)
    main_frame = center_frame(root)
    bottom_frame = tk.Frame(root, bg="#1e1e1e")
    bottom_frame.place(relx=0.5, rely=0.9, anchor="center")

    current_word, current_data = word_list[current_index]
    word_label = create_label(main_frame, current_word, font=("Arial", 24))
    speak_with_delay(current_word, root, delay=1000)

    choice_buttons = []
    update_choices(current_data["translation"])

    create_button(bottom_frame, "Kelimeyi Tekrar Oku", lambda: speak(current_word))
    create_button(bottom_frame, "Ana Menüye Dön", lambda: [save_words(file_path, words), main_menu(root)])
