import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import random

# JSON dosyasını yükleme
def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Güncellenmiş verileri kaydetme
def save_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)

# Tarih formatlama yardımcı fonksiyonları
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

# Bugünün tarihini al
def get_today():
    return format_date(datetime.now())

# Tema ayarları (Dark Mode)
def apply_dark_mode(widget):
    widget.configure(bg="#1e1e1e")
    if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
        widget.option_add("*Background", "#1e1e1e")
        widget.option_add("*Foreground", "#ffffff")
        widget.option_add("*Font", "Arial 14")
        widget.option_add("*Button.Background", "#2a2a2a")
        widget.option_add("*Button.Foreground", "#ffffff")
        widget.option_add("*Button.Font", "Arial 14 bold")
        widget.option_add("*Label.Font", "Arial 16 bold")
        widget.option_add("*Button.ActiveBackground", "#3a3a3a")
        widget.option_add("*Button.ActiveForeground", "#ffffff")
        widget.option_add("*Button.Pady", 10)
        widget.option_add("*Button.Width", 20)

# Kelime öğrenme ekranı
def learn_new_words_gui():
    unmemorized = {word: data for word, data in words.items() if not data["memorized"] and not data["retry"]}
    if not unmemorized:
        messagebox.showinfo("Bilgi", "Ezberlenecek yeni kelime yok!")
        return

    def mark_memorized():
        selected_word["memorized"] = True
        selected_word["correct_streak"] = 21
        next_word()

    def add_to_retry():
        selected_word["retry"] = True
        selected_word["correct_streak"] = 0
        selected_word["date"] = get_today()  # Bugünün tarihini ekle
        next_word()

    def next_word():
        nonlocal word, selected_word
        word_list = list(unmemorized.keys())
        random.shuffle(word_list)
        word = word_list[0]
        selected_word = unmemorized[word]
        word_label.config(text=word)
        translation_label.config(text=selected_word['translation'])

    word_list = list(unmemorized.keys())
    random.shuffle(word_list)
    word = word_list[0]
    selected_word = unmemorized[word]

    # Pencereyi oluştur
    clear_window()
    word_label = tk.Label(root, text=word, font=("Arial", 24), bg="#1e1e1e", fg="#ffffff")
    word_label.pack(pady=20)

    translation_label = tk.Label(root, text=selected_word['translation'], font=("Arial", 20), bg="#1e1e1e", fg="#ffffff")
    translation_label.pack(pady=20)

    tk.Button(root, text="Biliyorum", command=mark_memorized).pack(pady=10)
    tk.Button(root, text="Tekrar Et", command=add_to_retry).pack(pady=10)
    tk.Button(root, text="Sonraki Kelime", command=next_word).pack(pady=10)
    tk.Button(root, text="Geri Dön", command=main_menu).pack(pady=10)

# Kelime tekrar ekranı
def review_words_gui():
    retry_words = {word: data for word, data in words.items() if not data["memorized"] and data["retry"]}

    # Bugün çalışılmış kelimeleri filtreleyelim
    today = get_today()
    retry_words = {word: data for word, data in retry_words.items() if data["date"] != today}

    if not retry_words:
        messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime yok!")
        return

    sorted_words = sorted(retry_words.items(), key=lambda x: parse_date(x[1]["date"]))

    def check_answer(answer):
        nonlocal word, correct_translation
        if answer == correct_translation:
            retry_words[word]["correct_streak"] += 1
            next_word()
        else:
            retry_words[word]["correct_streak"] = 0
            messagebox.showerror("Yanlış!", f"Doğru cevap: {correct_translation}")

    def next_word():
        nonlocal word, selected_word
        if sorted_words:
            word, data = sorted_words.pop(0)
            selected_word = data
            correct_translation = data["translation"]
            choices = random.sample(
                [w["translation"] for w in words.values() if w["translation"] != correct_translation], 3
            ) + [correct_translation]
            random.shuffle(choices)

            word_label.config(text=word)
            for widget in choice_buttons:
                widget.destroy()

            for choice in choices:
                button = tk.Button(root, text=choice, command=lambda c=choice: check_answer(c))
                button.pack(pady=5)
                choice_buttons.append(button)
        else:
            messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime bitti!")

    word, selected_word = sorted_words.pop(0)
    correct_translation = selected_word["translation"]
    choice_buttons = []

    clear_window()
    word_label = tk.Label(root, text=word, font=("Arial", 24), bg="#1e1e1e", fg="#ffffff")
    word_label.pack(pady=20)

    for widget in choice_buttons:
        widget.destroy()

    for choice in choices:
        button = tk.Button(root, text=choice, command=lambda c=choice: check_answer(c))
        button.pack(pady=5)
        choice_buttons.append(button)

    tk.Button(root, text="Sonraki Kelime", command=next_word).pack(pady=10)
    tk.Button(root, text="Geri Dön", command=main_menu).pack(pady=10)

# İstatistikler ekranı
def show_statistics_gui():
    total = len(words)
    memorized = sum(1 for data in words.values() if data["memorized"])
    retry = sum(1 for data in words.values() if data["retry"])

    stats = f"""
    Toplam Kelime: {total}
    Ezberlenen Kelimeler: {memorized}
    Tekrar Edilecek Kelimeler: {retry}
    """
    messagebox.showinfo("İstatistikler", stats)

# Çıkış işlemi
def exit_program():
    save_changes()
    if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?"):
        root.destroy()

# Kaydetme işlemi
def save_changes():
    save_words(file_path, words)
    messagebox.showinfo("Bilgi", "Değişiklikler kaydedildi!")

# Ana menü
def main_menu():
    clear_window()
    tk.Button(root, text="Yeni Kelime Öğren", command=learn_new_words_gui).pack(pady=15)
    tk.Button(root, text="Kelime Tekrarı Yap", command=review_words_gui).pack(pady=15)
    tk.Button(root, text="İstatistikleri Göster", command=show_statistics_gui).pack(pady=15)
    tk.Button(root, text="Kaydet", command=save_changes).pack(pady=15)
    tk.Button(root, text="Çık", command=exit_program).pack(pady=15)

# Pencereyi temizleme
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Ana uygulama penceresi
file_path = 'translated_words.json'
words = load_words(file_path)

root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)

# Ana menüye başla
main_menu()

root.mainloop()
