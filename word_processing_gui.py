import tkinter as tk
from tkinter import filedialog, ttk
import re
import json
from datetime import datetime
from googletrans import Translator
from utils import show_notification
from gui_components import clear_window, center_frame

# Altyazı dosyasından benzersiz kelimeleri çıkaran fonksiyon
def process_subtitle_file(input_file, output_file="unique_words.json"):
    try:
        unique_words = set()
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                if re.match(r'^\d+$', line.strip()) or '-->' in line:
                    continue
                words = re.findall(r'\b[a-zA-Z]{2,}\b', line.lower())
                unique_words.update(words)

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(sorted(list(unique_words)), json_file, ensure_ascii=False, indent=4)

        return f"Kelimeler '{output_file}' dosyasına başarıyla kaydedildi."
    except Exception as e:
        return f"Hata oluştu: {e}"

# İngilizce kelimeleri Google Translate ile Türkçeye çeviren fonksiyon
def translate_words_with_google(input_file, output_file, root, progress_bar, progress_label, words):
    translator = Translator()

    # Dosya okuma işlemi
    with open(input_file, 'r', encoding='utf-8') as file:
        english_words = json.load(file)

    translations = {}
    total_words = len(english_words)

    try:
        # Var olan verileri okuma
        with open(output_file, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            if not existing_data:
                show_notification(root, f"'{output_file}' dosyası boş, yeni verilerle başlatılıyor.", color="yellow")
                existing_data = {}
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        show_notification(root, f"'{output_file}' dosyası bulunamadı veya geçersiz, yeni verilerle başlatılıyor.", color="yellow")
        existing_data = {}

    # Kelime çevirme işlemi
    for idx, word in enumerate(english_words):
        if word not in existing_data:
            try:
                translated = translator.translate(word, src='en', dest='tr')

                if word.lower() == translated.text.lower():
                    continue

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
        else:
            translations[word] = existing_data[word]

        # İlerleme çubuğunu güncelle
        progress = int((idx + 1) / total_words * 100)
        progress_bar['value'] = progress
        progress_label.config(text=f"İlerleme: {progress}%")
        root.update_idletasks()

    # Verileri birleştirme
    existing_data.update(translations)

    # Veriyi ana 'words' değişkenine aktar
    words.update(existing_data)

    # Güncellenmiş veriyi dosyaya kaydetme
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
        show_notification(root, f"Çeviriler başarıyla '{output_file}' dosyasına kaydedildi.", color="green")
    except Exception as e:
        show_notification(root, f"Çeviriler kaydedilemedi: {e}", color="red")

    # Verileri birleştirme
    existing_data.update(translations)

    # Güncellenmiş veriyi dosyaya kaydetme
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
        show_notification(root, f"Çeviriler başarıyla '{output_file}' dosyasına kaydedildi.", color="green")
    except Exception as e:
        show_notification(root, f"Çeviriler kaydedilemedi: {e}", color="red")

# Arayüz (GUI) fonksiyonu
def subtitle_processing_gui(root, main_menu, words):
    def browse_input_file():
        file_path = filedialog.askopenfilename(
            title="Dosyayı Seç",
            filetypes=(("Altyazı Dosyaları", "*.txt *.srt"), ("Tüm Dosyalar", "*.*"))
        )
        if file_path:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(0, file_path)

    def start_processing():
        input_file = input_file_entry.get()
        unique_words_file = "unique_words.json"
        translated_words_file = "translated_words.json"

        if not input_file:
            show_notification(root, "Bir giriş dosyası belirtmelisiniz.", color="red")
            return

        result = process_subtitle_file(input_file, unique_words_file)
        show_notification(root, result, color="green")

        # Çeviri işlemini başlat
        translate_words_with_google(unique_words_file, translated_words_file, root, progress_bar, progress_label, words)

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

    tk.Button(frame, text="Başlat", command=start_processing, font=("Arial", 14), bg="#333333", fg="white").grid(row=3, column=0, columnspan=3, pady=20)
    tk.Button(frame, text="Ana Menüye Dön", command=lambda: main_menu(root), font=("Arial", 14), bg="#555555", fg="white").grid(row=4, column=0, columnspan=3, pady=10)
