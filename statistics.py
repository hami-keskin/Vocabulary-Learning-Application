from gui_components import clear_window, create_label, create_button, center_frame

def show_statistics_gui(root, words, file_path, main_menu):
    total = len(words)
    if total == 0:
        stats = "Hiç kelime yok!"
    else:
        known = sum(1 for data in words.values() if data.get("known", False))
        memorized = sum(1 for data in words.values() if data["memorized"] and not data.get("known", False))
        retry = sum(1 for data in words.values() if data["retry"])
        unmemorized = total - memorized - known - retry

        stats = (
            f"Toplam Kelime: {total}\n\n"
            f"Bilinen Kelimeler: {known} ({known / total:.1%})\n"
            f"Ezberlenen Kelimeler: {memorized} ({memorized / total:.1%})\n"
            f"Tekrar Edilecek Kelimeler: {retry} ({retry / total:.1%})\n"
            f"Öğrenilmeyi Bekleyen Kelimeler: {unmemorized} ({unmemorized / total:.1%})\n"
        )

    clear_window(root)
    frame = center_frame(root)
    create_label(frame, "İstatistikler", font=("Arial", 20))
    stats_label = create_label(frame, stats, font=("Arial", 16), pady=10)
    create_button(frame, "Geri Dön", lambda: main_menu(root))
