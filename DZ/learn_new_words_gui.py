import tkinter as tk
from DZ.file_operations import save_words
from DZ.utils import speak, mark_known, add_to_retry, copy_to_clipboard, show_notification
from DZ.gui_components import clear_window


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
        if button.winfo_exists() == 0:  # Buton kaybolmuşsa
            return  # Hiçbir işlem yapma
        button.config(state=tk.DISABLED)
        root.after(2000, lambda: button.config(state=tk.NORMAL))

    def create_action_button(frame, text, command, row, col, colspan=1):
        button = tk.Button(
            frame,
            text=text,
            command=command,
            font=("Arial", 14, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat"
        )
        button.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="ew")
        return button

    clear_window(root)

    main_frame = tk.Frame(root, bg="#1e1e1e", padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    current_word, current_data = unknown.popitem()

    word_label = tk.Label(main_frame, text=current_word, font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white", wraplength=400)
    word_label.grid(row=0, column=0, columnspan=2, pady=20)

    translation_label = tk.Entry(main_frame, font=("Arial", 20), justify="center", fg="white", bg="#333333", relief="flat", insertbackground="white")
    translation_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
    translation_label.config(state=tk.DISABLED)

    save_button = tk.Button(main_frame, text="Kaydet", command=save_new_translation, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="white", relief="flat")
    save_button.grid_forget()

    # Butonları oluştur
    button_biliyorum = create_action_button(main_frame, "Biliyorum", lambda: [mark_known(current_data, next_word), disable_button_for_delay(button_biliyorum)], 2, 0)
    button_tekraret = create_action_button(main_frame, "Tekrar Et", lambda: [add_to_retry(current_data, next_word), disable_button_for_delay(button_tekraret)], 2, 1)
    button_correct = create_action_button(main_frame, "Çeviriyi Düzelt", lambda: [enable_translation_edit(), disable_button_for_delay(button_correct)], 4, 0)
    button_sonraki = create_action_button(main_frame, "Sonraki Kelime", lambda: [next_word(), disable_button_for_delay(button_sonraki)], 4, 1)

    create_action_button(main_frame, "Kelimeyi Kopyala", lambda: [copy_to_clipboard(current_word), show_notification(root, "Kelime kopyalandı!", color="green")], 5, 0)

    create_action_button(main_frame, "Kelimeyi Sesli Oku", lambda: speak(current_word), 5, 1)

    tk.Button(main_frame, text="Ana Menüye Dön", command=lambda: [save_words(file_path, words), main_menu(root)], font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="white", relief="flat").grid(row=6, column=0, columnspan=2, pady=20)

    update_word_labels()
