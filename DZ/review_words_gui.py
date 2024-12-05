import tkinter as tk
import random
from datetime import timedelta

from DZ.file_operations import save_json
from DZ.gui_components import clear_window
from DZ.utils import speak, get_today, parse_date, format_date, show_notification


def create_choice_button(frame, text, command, row):
    """Buton oluşturma fonksiyonu"""
    btn = tk.Button(
        frame,
        text=text,
        command=command,
        wraplength=250,
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        font=("Arial", 14, "bold")
    )
    btn.grid(row=row, column=0, pady=10, padx=10, sticky="ew")
    return btn


def review_words_gui(root, words, file_path, main_menu):
    today = get_today()

    # Seçilen kelimeler, sadece "retry" değeri True olanlar olacak
    retry_words = {
        word: data for word, data in words.items()
        if not data.get("known", False) and not data["memorized"] and data["retry"] and parse_date(data["date"]) <= parse_date(today)
    }
    if not retry_words:
        show_notification(root, "Bugün tekrar edilecek kelime yok!")
        return

    sorted_retry_words = sorted(retry_words.items(), key=lambda item: parse_date(item[1]["date"]))
    word_list = list(sorted_retry_words)
    current_index = 0
    current_word, current_data = word_list[current_index]

    def check_answer(selected, correct_word, btn):
        nonlocal current_index
        current_word, current_data = word_list[current_index]

        if selected == correct_word:
            words[current_word]["correct_streak"] += 1
            streak = words[current_word]["correct_streak"]

            if streak < 7:
                words[current_word]["date"] = format_date(parse_date(today) + timedelta(days=1))
            elif streak < 10:
                words[current_word]["date"] = format_date(parse_date(today) + timedelta(days=7))
            else:
                words[current_word]["memorized"] = True
                words[current_word]["retry"] = False

            show_notification(root, "Doğru! Bir sonraki kelimeye geçiliyor...")
            next_word()
        else:
            words[current_word]["correct_streak"] = 0
            # Doğru butonu yeşil olarak vurgula
            for button in choice_buttons:
                if button.cget("text") == correct_word:
                    button.config(fg="green")

            show_notification(root, "Yanlış! Doğru cevap gösteriliyor.")
        save_json(file_path, words)

    def next_word():
        nonlocal current_index, current_word, current_data
        current_index += 1
        if current_index >= len(word_list):
            show_notification(root, "Bugün tekrar edilecek kelime kalmadı!")
            save_json(file_path, words)
            main_menu(root)
            return

        current_word, current_data = word_list[current_index]
        word_label.config(text=current_data["translation"])  # Update word label with Turkish translation
        root.after(500, lambda: speak(current_word))  # Speak after updating the word
        update_choices(current_word)

    def update_choices(correct_word):
        # Yanlış İngilizce şıklar oluştur
        retry_words_list = list(retry_words.keys())
        wrong_choices = list(set(retry_words_list) - {correct_word})
        choices = random.sample(wrong_choices, min(3, len(wrong_choices))) + [correct_word]
        random.shuffle(choices)

        for btn in choice_buttons:
            btn.destroy()
        choice_buttons.clear()

        # Butonları oluştur ve şıkları güncelle
        for idx, choice in enumerate(choices):
            btn = create_choice_button(main_frame, choice, lambda c=choice: check_answer(c, correct_word, btn), idx + 1)
            choice_buttons.append(btn)

    clear_window(root)
    main_frame = tk.Frame(root, bg="#1e1e1e", padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.4, anchor="center")

    bottom_frame = tk.Frame(root, bg="#1e1e1e", pady=10)
    bottom_frame.place(relx=0.5, rely=0.7, anchor="center")

    # Kelimenin Türkçe karşılığı başlıkta gösterilecek
    word_label = tk.Label(main_frame, text=current_data["translation"], font=("Arial", 24), bg="#1e1e1e", fg="white", wraplength=300)
    word_label.grid(row=0, column=0, pady=20)
    root.after(100, lambda: speak(current_word))

    choice_buttons = []
    update_choices(current_word)

    tk.Button(bottom_frame, text="Sonraki Kelime", command=next_word, bg="#333333", fg="white").pack(side="left", padx=10, pady=5)
    tk.Button(bottom_frame, text="Kelimeyi Tekrar Oku", command=lambda: speak(current_word), bg="#333333", fg="white").pack(side="left", padx=10, pady=5)
    tk.Button(bottom_frame, text="Ana Menüye Dön", command=lambda: [save_json(file_path, words), main_menu(root)], bg="#333333", fg="white").pack(side="right", padx=10, pady=5)
