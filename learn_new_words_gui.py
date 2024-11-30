import tkinter as tk

from file_operations import save_words
from utils import speak, mark_known, add_to_retry, copy_to_clipboard, show_notification
from gui_components import clear_window, create_label, create_button, center_frame

def learn_new_words_gui(root, words, file_path, main_menu):
    unknown = {word: data for word, data in words.items() if not data["known"] and not data["retry"]}
    if not unknown:
        show_notification(root, "Ezberlenecek yeni kelime yok!", color="red")
        return

    def update_word_labels():
        word_label.config(text=current_word)
        translation_label.config(state=tk.NORMAL)
        translation_label.delete(0, tk.END)
        translation_label.insert(0, current_data['translation'])
        translation_label.config(state=tk.DISABLED)
        root.after(100, lambda: speak(current_word))

    def next_word():
        nonlocal current_word, current_data
        if unknown:
            current_word, current_data = unknown.popitem()
            update_word_labels()
        else:
            show_notification(root, "Ezberlenecek kelime kalmadı!", color="yellow")
            main_menu(root)

    def enable_translation_edit():
        translation_label.config(state=tk.NORMAL)
        translation_label.focus_set()
        save_button.pack(pady=5)  # Kaydet butonunu göster

    def save_new_translation():
        new_translation = translation_label.get()
        if new_translation:
            current_data['translation'] = new_translation
            translation_label.config(state=tk.DISABLED)
            save_button.pack_forget()  # Kaydet butonunu gizle
            update_word_labels()
            show_notification(root, "Çeviri başarıyla güncellendi!", color="green")

    def disable_button_for_delay(button):
        button.config(state=tk.DISABLED)
        root.after(2000, lambda: button.config(state=tk.NORMAL))

    clear_window(root)
    frame = center_frame(root)
    current_word, current_data = unknown.popitem()
    word_label = create_label(frame, current_word, font=("Arial", 24))

    # Çeviriyi düzenlenebilir hale getirmek için Entry widget'i
    translation_label = tk.Entry(frame, font=("Arial", 20), justify="center")
    translation_label.pack(pady=10)
    translation_label.config(state=tk.DISABLED)  # Başlangıçta düzenlenemez

    save_button = create_button(frame, "Kaydet", save_new_translation)
    save_button.pack_forget()  # Başlangıçta gizlenir

    update_word_labels()

    button_biliyorum = create_button(frame, "Biliyorum", lambda: [mark_known(current_data, next_word), disable_button_for_delay(button_biliyorum)])
    button_tekraret = create_button(frame, "Tekrar Et", lambda: [add_to_retry(current_data, next_word), disable_button_for_delay(button_tekraret)])
    button_sonraki = create_button(frame, "Sonraki Kelime", lambda: [next_word(), disable_button_for_delay(button_sonraki)])
    button_correct = create_button(frame, "Çeviriyi Düzelt", lambda: [enable_translation_edit(), disable_button_for_delay(button_correct)])

    create_button(frame, "Kelimeyi Kopyala", lambda: copy_to_clipboard(current_word))
    create_button(frame, "Kelimeyi Sesli Oku", lambda: speak(current_word))
    create_button(frame, "Ana Menüye Dön", lambda: [save_words(file_path, words), main_menu(root)])
