import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import random
import pyttsx3
import pyperclip  # Panoya kopyalama için

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

# Sesli okuma motoru başlat
speech_engine = pyttsx3.init()

def speak(text):
    """Metni sesli okuma"""
    speech_engine.say(text)
    speech_engine.runAndWait()

# Sesli okuma fonksiyonunu gecikmeli hale getirelim
def speak_with_delay(text, delay=1000):
    """Metni gecikmeli olarak sesli okuma"""
    root.after(delay, lambda: speak(text))

# Kelimeyi kopyalamak için fonksiyon
def copy_to_clipboard(text):
    pyperclip.copy(text)  # Metni panoya kopyala

# Yeni kelime öğrenme ekranı (güncellenmiş)
def learn_new_words_gui():
    unknown = {word: data for word, data in words.items() if not data["known"] and not data["retry"]}
    if not unknown:
        messagebox.showinfo("Bilgi", "Ezberlenecek yeni kelime yok!")
        return

    def update_word_labels():
        word_label.config(text=current_word)
        translation_label.config(text=current_data['translation'])
        speak_with_delay(current_word, delay=1000)  # Kelimeyi gecikmeli olarak sesli oku

    def mark_memorized():
        current_data["memorized"] = True
        next_word()

    def mark_known():
        current_data["known"] = True
        next_word()

    def add_to_retry():
        current_data.update({"retry": True, "correct_streak": 0, "date": get_today()})
        next_word()

    def next_word():
        nonlocal current_word, current_data
        if unknown:
            current_word, current_data = unknown.popitem()
            update_word_labels()
        else:
            messagebox.showinfo("Bilgi", "Ezberlenecek kelime kalmadı!")
            main_menu()

    def correct_translation():
        new_translation = simple_dialog("Yeni Çeviriyi Girin", "Çeviriyi Girin:")
        if new_translation:
            current_data['translation'] = new_translation
            update_word_labels()

    clear_window()
    frame = center_frame()
    current_word, current_data = unknown.popitem()
    word_label = create_label(frame, current_word, font=("Arial", 24))
    translation_label = create_label(frame, current_data['translation'], font=("Arial", 20))
    speak_with_delay(current_word, delay=1000)  # İlk kelimeyi gecikmeli olarak sesli oku

    def disable_button_for_delay(button):
        """Butonu 2 saniye boyunca devre dışı bırak ve ardından tekrar etkinleştir"""
        button.config(state=tk.DISABLED)
        root.after(2000, lambda: button.config(state=tk.NORMAL))  # 2 saniye sonra butonu etkinleştir

    button_biliyorum = create_button(frame, "Biliyorum", mark_known)
    button_biliyorum.config(command=lambda: [mark_known(), disable_button_for_delay(button_biliyorum)])

    button_tekraret = create_button(frame, "Tekrar Et", add_to_retry)
    button_tekraret.config(command=lambda: [add_to_retry(), disable_button_for_delay(button_tekraret)])

    button_sonraki = create_button(frame, "Sonraki Kelime", next_word)
    button_sonraki.config(command=lambda: [next_word(), disable_button_for_delay(button_sonraki)])

    button_correct = create_button(frame, "Çeviriyi Düzelt", correct_translation)
    button_correct.config(command=lambda: [correct_translation(), disable_button_for_delay(button_correct)])

    button_copy = create_button(frame, "Kelimeyi Kopyala", lambda: copy_to_clipboard(current_word))

    button_sesli_okuma = create_button(frame, "Kelimeyi Sesli Oku", lambda: speak(current_word))

    create_button(frame, "Geri Dön", main_menu)

# Basit bir girdi penceresi
def simple_dialog(title, prompt):
    def on_submit():
        entered_value = entry.get()
        if entered_value:
            top.destroy()
            result[0] = entered_value

    result = [None]
    top = tk.Toplevel(root)
    top.title(title)
    create_label(top, prompt)
    entry = tk.Entry(top)
    entry.pack(pady=10)
    submit_button = create_button(top, "Tamam", on_submit)
    entry.focus_set()
    top.wait_window(top)
    return result[0]

# Kelime tekrar ekranı (güncellenmiş)
def review_words_gui():
    retry_words = {
        word: data for word, data in words.items()
        if not data.get("known", False) and not data["memorized"] and data["retry"] and data["date"] != get_today()
    }
    if not retry_words:
        messagebox.showinfo("Bilgi", "Bugün tekrar edilecek kelime yok!")
        return

    sorted_retry_words = sorted(retry_words.items(), key=lambda item: parse_date(item[1]["date"]))
    retry_words = {word: data for word, data in sorted_retry_words}

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
            speak_with_delay(current_word, delay=1000)  # Kelimeyi gecikmeli olarak sesli oku
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
    speak_with_delay(current_word, delay=1000)  # İlk kelimeyi gecikmeli olarak sesli oku
    choice_buttons = []
    update_choices()

# İstatistikler ekranı (güncellenmiş, günlük analiz kaldırıldı)
def show_statistics_gui():
    total = len(words)
    known = sum(1 for data in words.values() if data.get("known", False))
    memorized = sum(1 for data in words.values() if data["memorized"] and not data.get("known", False))
    retry = sum(1 for data in words.values() if data["retry"])
    unmemorized = total - memorized - known - retry

    stats = (
        f"Toplam Kelime: {total}\n"
        f"Bilinen Kelimeler: {known} ({known / total:.1%})\n"
        f"Ezberlenen Kelimeler: {memorized} ({memorized / total:.1%})\n"
        f"Tekrar Edilecek Kelimeler: {retry}\n"
        f"Öğrenilmeyi Bekleyen Kelimeler: {unmemorized}\n"
    )

    # Gösterim
    clear_window()
    frame = center_frame()
    create_label(frame, "İstatistikler", font=("Arial", 20))
    stats_label = create_label(frame, stats, font=("Arial", 16), pady=10)
    create_button(frame, "Geri Dön", main_menu)

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
