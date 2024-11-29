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
        messagebox.showinfo("Başarı", f"{word} ezberlendi!")

    def add_to_retry():
        selected_word["retry"] = True
        selected_word["correct_streak"] = 0
        selected_word["date"] = get_today()  # Bugünün tarihini ekle
        messagebox.showinfo("Başarı", f"{word} tekrar listesine eklendi!")

    word_list = list(unmemorized.keys())
    random.shuffle(word_list)
    word = word_list[0]
    selected_word = unmemorized[word]

    learn_window = tk.Toplevel(root)
    learn_window.title("Yeni Kelime Öğren")
    apply_dark_mode(learn_window)
    learn_window.attributes("-fullscreen", True)  # Tam ekran modu
    tk.Label(learn_window, text=f"{word}").pack(pady=20)
    tk.Label(learn_window, text=f"{selected_word['translation']}").pack(pady=20)
    tk.Button(learn_window, text="Biliyorum", command=mark_memorized).pack(pady=10)
    tk.Button(learn_window, text="Tekrar Et", command=add_to_retry).pack(pady=10)

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
            messagebox.showinfo("Doğru!", "Cevabınız doğru!")
        else:
            retry_words[word]["correct_streak"] = 0
            messagebox.showerror("Yanlış!", f"Doğru cevap: {correct_translation}")

    for word, data in sorted_words:
        review_window = tk.Toplevel(root)
        review_window.title("Kelime Tekrarı")
        apply_dark_mode(review_window)
        review_window.attributes("-fullscreen", True)  # Tam ekran modu
        tk.Label(review_window, text=f"Kelime: {word}").pack(pady=20)

        correct_translation = data["translation"]
        choices = random.sample(
            [w["translation"] for w in words.values() if w["translation"] != correct_translation], 3
        ) + [correct_translation]
        random.shuffle(choices)

        for choice in choices:
            tk.Button(review_window, text=choice, command=lambda c=choice: check_answer(c), width=30).pack(pady=10)
        break

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

# Ana uygulama penceresi
file_path = 'translated_words.json'
words = load_words(file_path)

root = tk.Tk()
root.title("Kelime Ezberleme Uygulaması")
apply_dark_mode(root)

# Tam ekran modunu uygulama
root.attributes("-fullscreen", True)

tk.Button(root, text="Yeni Kelime Öğren", command=learn_new_words_gui).pack(pady=15)
tk.Button(root, text="Kelime Tekrarı Yap", command=review_words_gui).pack(pady=15)
tk.Button(root, text="İstatistikleri Göster", command=show_statistics_gui).pack(pady=15)
tk.Button(root, text="Kaydet", command=save_changes).pack(pady=15)
tk.Button(root, text="Çık", command=exit_program).pack(pady=15)

root.mainloop()
