import tkinter as tk
from tkinter import filedialog, ttk
import re
import json
from datetime import datetime
from googletrans import Translator

from DZ.file_operations import load_json, save_json
from DZ.gui_components import clear_window, center_frame
from DZ.utils import show_notification

def process_file(input_file):
    try:
        unique_words = set()
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                if re.match(r'^\d+$', line.strip()) or '-->' in line:
                    continue
                words = re.findall(r'\b[a-zA-Z]{2,}\b', line.lower())
                unique_words.update(words)
        return sorted(list(unique_words))
    except Exception as e:
        return f"Hata oluştu: {e}"


def translate_words(words, output_file, sozluk_file, root, progress_bar, progress_label, words_data):
    """Translate words from the input file and save translations."""
    translator = Translator()
    existing_data = load_json(output_file)  # Remove default={} argument
    sozluk_data = load_json(sozluk_file)   # Remove default={} argument

    translations = {}
    total_words = len(words)

    for idx, word in enumerate(words):
        # Check if word exists in the existing data or dictionary
        if word in existing_data:
            translations[word] = existing_data[word]
        elif word in sozluk_data:
            # If found in dictionary, add translation and other fields
            translations[word] = {
                "translation": sozluk_data[word],
                "known": False,
                "memorized": False,
                "retry": False,
                "date": datetime.now().strftime('%Y-%m-%d')
            }
        else:
            # If not in existing data or dictionary, use Google Translate
            try:
                translated = translator.translate(word, src='en', dest='tr')
                if word.lower() != translated.text.lower():
                    translations[word] = {
                        "translation": translated.text,
                        "known": False,
                        "memorized": False,
                        "retry": False,
                        "date": datetime.now().strftime('%Y-%m-%d')
                    }
            except Exception as e:
                show_notification(root, f"Hata oluştu: {word}, {e}", color="red")
                translations[word] = {
                    "translation": None,
                    "known": False,
                    "memorized": False,
                    "retry": False,
                    "date": datetime.now().strftime('%Y-%m-%d')
                }

        # Update progress bar
        progress = int((idx + 1) / total_words * 100)
        progress_bar['value'] = progress
        progress_label.config(text=f"İlerleme: {progress}%")
        root.update_idletasks()

    existing_data.update(translations)
    save_json(output_file, existing_data)
    words_data.update(existing_data)

def processing_gui(root, main_menu, words_data):

    def browse_input_file():
        file_path = filedialog.askopenfilename(
            title="Dosyayı Seç",
            filetypes=(("Dosyalar", "*.txt *.srt"), ("Tüm Dosyalar", "*.*"))
        )
        if file_path:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(0, file_path)

    def start_processing():
        input_file = input_file_entry.get()
        translated_words_file = "translated_words.json"
        sozluk_file = "sozluk.json"

        if not input_file:
            show_notification(root, "Bir giriş dosyası belirtmelisiniz.", color="red")
            return

        words = process_file(input_file)

        # Translate the words
        translate_words(words, translated_words_file, sozluk_file, root, progress_bar, progress_label, words_data)

    clear_window(root)
    frame = center_frame(root)

    tk.Label(frame, text="Dosya:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky="w")
    input_file_entry = tk.Entry(frame, width=40)
    input_file_entry.grid(row=0, column=1, pady=10)
    tk.Button(frame, text="Gözat", command=browse_input_file).grid(row=0, column=2, padx=10)

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.grid(row=1, column=0, columnspan=3, pady=10)
    progress_label = tk.Label(frame, text="İlerleme: 0%", font=("Arial", 12))
    progress_label.grid(row=2, column=0, columnspan=3, pady=5)

    tk.Button(frame, text="Başlat", command=start_processing, font=("Arial", 14), bg="#333333", fg="white").grid(row=3,
                                                                                                                 column=0,
                                                                                                                 columnspan=3,
                                                                                                                 pady=20)
    tk.Button(frame, text="Ana Menüye Dön", command=lambda: main_menu(root), font=("Arial", 14), bg="#555555",
              fg="white").grid(row=4, column=0, columnspan=3, pady=10)
