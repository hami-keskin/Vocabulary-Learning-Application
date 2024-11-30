from gui_utils import create_label, create_button, clear_window, center_frame
from main import words


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
