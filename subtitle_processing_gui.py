import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json
from utils import show_notification
from file_operations import load_words, save_words
from gui_components import apply_dark_mode, clear_window, center_frame, create_button

# Yeni fonksiyon: Altyazı dosyasını işleme
def process_subtitle_file(input_file, output_file):
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

# Yeni GUI: Altyazı işleme
def subtitle_processing_gui(root, words, file_path, main_menu):
    def browse_input_file():
        file_path = filedialog.askopenfilename(
            title="Altyazı Dosyası Seç",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(0, file_path)

    def browse_output_file():
        file_path = filedialog.asksaveasfilename(
            title="Çıkış Dosyasını Kaydet",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
            defaultextension=".json"
        )
        if file_path:
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(0, file_path)

    def start_processing():
        input_file = input_file_entry.get()
        output_file = output_file_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Hata", "Hem giriş hem de çıkış dosyalarını belirtmelisiniz.")
            return

        result = process_subtitle_file(input_file, output_file)
        messagebox.showinfo("Sonuç", result)

    clear_window(root)
    frame = center_frame(root)

    tk.Label(frame, text="Altyazı Dosyası:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky="w")
    input_file_entry = tk.Entry(frame, width=40)
    input_file_entry.grid(row=0, column=1, pady=10)
    tk.Button(frame, text="Gözat", command=browse_input_file).grid(row=0, column=2, padx=10)

    tk.Label(frame, text="Çıkış Dosyası (JSON):", font=("Arial", 14)).grid(row=1, column=0, pady=10, sticky="w")
    output_file_entry = tk.Entry(frame, width=40)
    output_file_entry.grid(row=1, column=1, pady=10)
    tk.Button(frame, text="Gözat", command=browse_output_file).grid(row=1, column=2, padx=10)

    tk.Button(frame, text="Başlat", command=start_processing, font=("Arial", 14), bg="#333333", fg="white").grid(row=2, column=0, columnspan=3, pady=20)
    tk.Button(frame, text="Ana Menüye Dön", command=lambda: main_menu(root), font=("Arial", 14), bg="#555555", fg="white").grid(row=3, column=0, columnspan=3, pady=10)
