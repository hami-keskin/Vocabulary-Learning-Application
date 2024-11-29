import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import random

# JSON dosyasını yükleme ve kaydetme
def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)

# Tarih yardımcı fonksiyonları
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def get_today():
    return format_date(datetime.now())

# Tema ayarları
def apply_dark_mode(widget):
    widget.configure(bg="#1e1e1e")
    if isinstance(widget, (tk.Tk, tk.Toplevel)):
        widget.option_add("*Background", "#1e1e1e")
        widget.option_add("*Foreground", "#ffffff")
        widget.option_add("*Font", "Arial 14")
        widget.option_add("*Button.Background", "#2a2a2a")
        widget.option_add("*Button.Foreground", "#ffffff")
        widget.option_add("*Button.Font", "Arial 14 bold")
        widget.option_add("*Label.Font", "Arial 16 bold")
        widget.option_add("*Button.ActiveBackground", "#3a3a3a")
        widget.option_add("*Button.ActiveForeground", "#ffffff")

# Yardımcı widget oluşturucular
def create_label(parent, text, font=("Arial", 16), pady=20):
    label = tk.Label(parent, text=text, font=font, bg="#1e1e1e", fg="#ffffff")
    label.pack(pady=pady)
    return label

def create_button(parent, text, command, pady=10, width=20):
    button = tk.Button(parent, text=text, command=command, pady=pady, width=width)
    button.pack()
    return button

# Pencereyi temizleme
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Öğeleri ortalamak için bir çerçeve
def center_frame():
    frame = tk.Frame(root, bg="#1e1e1e")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame

# Yeni kelime öğrenme ekranı
def learn_new_words_gui():
    unmemorized = {word: data for word, data in words.items() if not data["memorized"] and not data["retry"]}
    if not unmemorized:
        messagebox.showinfo("Bilgi", "Ezberlenecek yeni kelime yok!")
        return

    def update_word_labels():
        word_label.config(text=current_word)
        translation_label.config(text=current_data['translation'])

    def mark_memorized():
        current_data["memorized"] = True
        next_word()

    def add_to_retry():
        current_data.update({"retry": True, "correct_streak": 0, "date": get_today()})
        next_word()

    def next_word():
        nonlocal current_word, current_data
        if unmemorized:
            current_word, current_data = unmemorized.popitem()
            update_word_labels()
        else:
            messagebox.showinfo("Bilgi", "Ezberlenecek kelime kalmadı!")
            main_menu()

    clear_window()
    frame = center_frame()
    current_word, current_data = unmemorized.popitem()
    word_label = create_label(frame, current_word, font=("Arial", 24))
    translation_label = create_label(frame, current_data['translation'], font=("Arial", 20))
    create_button(frame, "Biliyorum", mark_memorized)
    create_button(frame, "Tekrar Et", add_to_retry)
    create_button(frame, "Sonraki Kelime", next_word)
    create_button(frame, "Geri Dön", main_menu)

# Kelime tekrar ekranı
def review_words_gui():
    retry_words = {
        word: data for word, data in words.items() if not data["memorized"] and data["retry"] and data["date"] != get_today()
    }
    if not retry_words:
        messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime yok!")
        return

    def check_answer(selected):
        if selected == current_translation:
            retry_words[current_word]["correct_streak"] += 1
        else:
            retry_words[current_word]["correct_streak"] = 0
            messagebox.showerror("Yanlış!", f"Doğru cevap: {current_translation}")
        next_word()

    def next_word():
        nonlocal current_word, current_translation
        if retry_words:
            current_word, current_data = retry_words.popitem()
            current_translation = current_data["translation"]
            word_label.config(text=current_word)
            update_choices()
        else:
            messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime kalmadı!")
            main_menu()

    def update_choices():
        choices = random.sample(
            [data["translation"] for data in words.values() if data["translation"] != current_translation], 3
        ) + [current_translation]
        random.shuffle(choices)
        for btn in choice_buttons:
            btn.destroy()
        for choice in choices:
            btn = create_button(frame, choice, lambda c=choice: check_answer(c))
            choice_buttons.append(btn)

    clear_window()
    frame = center_frame()
    current_word, current_data = retry_words.popitem()
    current_translation = current_data["translation"]
    word_label = create_label(frame, current_word, font=("Arial", 24))
    choice_buttons = []
    update_choices()

# İstatistikler ekranı
def show_statistics_gui():
    total = len(words)
    memorized = sum(1 for data in words.values() if data["memorized"])
    retry = sum(1 for data in words.values() if data["retry"])
    stats = f"Toplam Kelime: {total}\nEzberlenen Kelimeler: {memorized}\nTekrar Edilecek Kelimeler: {retry}"
    messagebox.showinfo("İstatistikler", stats)

# Çıkış işlemi
def exit_program():
    save_words(file_path, words)
    if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?"):
        root.destroy()

# Ana menü
def main_menu():
    clear_window()
    frame = center_frame()
    create_button(frame, "Yeni Kelime Öğren", learn_new_words_gui)
    create_button(frame, "Kelime Tekrarı Yap", review_words_gui)
    create_button(frame, "İstatistikleri Göster", show_statistics_gui)
    create_button(frame, "Kaydet", lambda: save_words(file_path, words))
    create_button(frame, "Çık", exit_program)

# Uygulama başlangıcı
file_path = 'translated_words.json'
words = load_words(file_path)

root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
main_menu()
root.mainloop()
