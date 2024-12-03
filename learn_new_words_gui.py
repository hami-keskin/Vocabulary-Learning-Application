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
        save_button.grid(row=3, column=0, columnspan=2, pady=5)  # Kaydet butonunu göster

    def save_new_translation():
        new_translation = translation_label.get()
        if new_translation:
            current_data['translation'] = new_translation
            translation_label.config(state=tk.DISABLED)
            save_button.grid_forget()  # Kaydet butonunu gizle
            update_word_labels()
            show_notification(root, "Çeviri başarıyla güncellendi!", color="green")

    def disable_button_for_delay(button):
        button.config(state=tk.DISABLED)
        root.after(2000, lambda: button.config(state=tk.NORMAL))

    clear_window(root)

    # Ana çerçeveyi ekranın ortasına yerleştir
    main_frame = tk.Frame(root, bg="#1e1e1e", padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # İlk kelime ve veri
    current_word, current_data = unknown.popitem()

    # Kelime etiketi
    word_label = tk.Label(
        main_frame,
        text=current_word,
        font=("Arial", 24, "bold"),
        bg="#1e1e1e",
        fg="white",
        wraplength=400
    )
    word_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Çeviri girişi
    translation_label = tk.Entry(
        main_frame,
        font=("Arial", 20),
        justify="center",
        fg="white",
        bg="#333333",
        relief="flat",
        insertbackground="white"
    )
    translation_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
    translation_label.config(state=tk.DISABLED)

    # Kaydet butonu (başlangıçta gizli)
    save_button = tk.Button(
        main_frame,
        text="Kaydet",
        command=save_new_translation,
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    )
    save_button.grid_forget()

    # Butonlar
    button_biliyorum = tk.Button(
        main_frame,
        text="Biliyorum",
        command=lambda: [mark_known(current_data, next_word), disable_button_for_delay(button_biliyorum)],
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    )
    button_biliyorum.grid(row=2, column=0, padx=10, pady=10)

    button_tekraret = tk.Button(
        main_frame,
        text="Tekrar Et",
        command=lambda: [add_to_retry(current_data, next_word), disable_button_for_delay(button_tekraret)],
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    )
    button_tekraret.grid(row=2, column=1, padx=10, pady=10)

    button_correct = tk.Button(
        main_frame,
        text="Çeviriyi Düzelt",
        command=lambda: [enable_translation_edit(), disable_button_for_delay(button_correct)],
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    )
    button_correct.grid(row=4, column=0, padx=10, pady=10)

    button_sonraki = tk.Button(
        main_frame,
        text="Sonraki Kelime",
        command=lambda: [next_word(), disable_button_for_delay(button_sonraki)],
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    )
    button_sonraki.grid(row=4, column=1, padx=10, pady=10)

    # Ek butonlar
    tk.Button(
        main_frame,
        text="Kelimeyi Kopyala",
        command=lambda: copy_to_clipboard(current_word),
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    ).grid(row=5, column=0, padx=10, pady=10)

    tk.Button(
        main_frame,
        text="Kelimeyi Sesli Oku",
        command=lambda: speak(current_word),
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    ).grid(row=5, column=1, padx=10, pady=10)

    tk.Button(
        main_frame,
        text="Ana Menüye Dön",
        command=lambda: [save_words(file_path, words), main_menu(root)],
        font=("Arial", 14, "bold"),
        bg="#333333",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat"
    ).grid(row=6, column=0, columnspan=2, pady=20)

    update_word_labels()
