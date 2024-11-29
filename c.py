import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
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
        selected_word["date"] = format_date(datetime.now())
        messagebox.showinfo("Başarı", f"{word} tekrar listesine eklendi!")

    word_list = list(unmemorized.keys())
    random.shuffle(word_list)
    word = word_list[0]
    selected_word = unmemorized[word]

    learn_window = tk.Toplevel(root)
    learn_window.title("Yeni Kelime Öğren")
    tk.Label(learn_window, text=f"Kelime: {word}").pack(pady=10)
    tk.Label(learn_window, text=f"Çevirisi: {selected_word['translation']}").pack(pady=10)
    tk.Button(learn_window, text="Ezberlendi", command=mark_memorized).pack(pady=5)
    tk.Button(learn_window, text="Tekrar Listesine Ekle", command=add_to_retry).pack(pady=5)

# Kelime tekrar ekranı
def review_words_gui():
    retry_words = {
        word: data for word, data in words.items()
        if not data["memorized"] and data["retry"]
    }
    if not retry_words:
        messagebox.showinfo("Bilgi", "Tekrar edilecek kelime yok!")
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
        tk.Label(review_window, text=f"Kelime: {word}").pack(pady=10)

        correct_translation = data["translation"]
        choices = random.sample(
            [w["translation"] for w in words.values() if w["translation"] != correct_translation], 3
        ) + [correct_translation]
        random.shuffle(choices)

        for choice in choices:
            tk.Button(review_window, text=choice, command=lambda c=choice: check_answer(c)).pack(pady=5)
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
root.attributes('-fullscreen', True)

tk.Button(root, text="Yeni Kelime Öğren", command=learn_new_words_gui, width=30).pack(pady=10)
tk.Button(root, text="Kelime Tekrarı Yap", command=review_words_gui, width=30).pack(pady=10)
tk.Button(root, text="İstatistikleri Göster", command=show_statistics_gui, width=30).pack(pady=10)
tk.Button(root, text="Kaydet", command=save_changes, width=30).pack(pady=10)
tk.Button(root, text="Çık", command=exit_program, width=30).pack(pady=10)

root.mainloop()
