from gui_utils import create_label, create_button, clear_window, center_frame

def show_statistics_gui(root, words, main_menu):
    total = len(words)
    known = sum(1 for data in words.values() if data.get("known", False))
    memorized = sum(1 for data in words.values() if data["memorized"])
    retry = sum(1 for data in words.values() if data["retry"])
    unmemorized = total - known - memorized - retry

    stats = (
        f"Toplam Kelime: {total}\n"
        f"Bilinen Kelimeler: {known}\n"
        f"Ezberlenen Kelimeler: {memorized}\n"
        f"Tekrar Edilecek Kelimeler: {retry}\n"
        f"Öğrenilmeyi Bekleyen Kelimeler: {unmemorized}\n"
    )

    clear_window()
    frame = center_frame()
    create_label(frame, "İstatistikler", font=("Arial", 20))
    create_label(frame, stats, font=("Arial", 16), pady=10)
    create_button(frame, "Geri Dön", main_menu)
