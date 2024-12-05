from DZ.gui_components import clear_window, create_label, create_button, center_frame

def calculate_stats(words):
    """Kelimelerden istatistikleri hesaplar."""
    total = len(words)
    if total == 0:
        return "Hiç kelime yok!"

    counts = {
        "Bilinen Kelimeler": sum(1 for data in words.values() if data.get("known", False)),
        "Ezberlenen Kelimeler": sum(1 for data in words.values() if data["memorized"] and not data.get("known", False)),
        "Tekrar Edilecek Kelimeler": sum(1 for data in words.values() if data["retry"]),
    }
    counts["Öğrenilmeyi Bekleyen Kelimeler"] = total - sum(counts.values())

    return "\n".join(
        f"{key}: {value} ({value / total:.1%})"
        for key, value in counts.items()
    )

def show_statistics_gui(root, words, file_path, main_menu):
    stats = calculate_stats(words)

    clear_window(root)
    frame = center_frame(root)
    create_label(frame, "İstatistikler", font=("Arial", 20))
    create_label(frame, stats, font=("Arial", 16), pady=10)
    create_button(frame, "Geri Dön", lambda: main_menu(root))
