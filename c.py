import json
import random
from datetime import datetime, timedelta


# JSON dosyasını yükleme
def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("JSON dosyası bulunamadı!")
        return {}


# Güncellenmiş verileri kaydetme
def save_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)


# Tarih formatlama yardımcı fonksiyonu
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")


# Yeni kelime öğrenme
def learn_new_words(words, max_words=5):
    print("\nYeni Kelime Öğrenme Başlıyor...\n")
    unmemorized = {word: data for word, data in words.items() if not data["memorized"] and not data["retry"]}
    if not unmemorized:
        print("Ezberlenecek yeni kelime yok!")
        return

    word_list = list(unmemorized.keys())
    random.shuffle(word_list)

    for word in word_list[:max_words]:  # Maksimum kelime sayısını sınırla
        print(f"Kelime: {word} -> Çevirisi: {words[word]['translation']}")
        know_word = input("Bu kelimeyi biliyor musunuz? (e/h): ").strip().lower()

        if know_word == 'e':
            words[word]["memorized"] = True
            words[word]["correct_streak"] = 21  # Hemen ezberlenmiş kabul edilsin
            print("Bu kelime ezberlenmiş olarak işaretlendi!")
        else:
            work_on_word = input("Bu kelime üzerinde çalışmak istiyor musunuz? (e/h): ").strip().lower()
            if work_on_word == 'e':
                words[word]["retry"] = True
                words[word]["correct_streak"] = 0
                words[word]["date"] = format_date(datetime.now())
                print("Bu kelime tekrar listesine eklendi!")
            else:
                print("Bu kelime üzerinde değişiklik yapılmadı.")


# Kelime tekrar
def review_words(words):
    print("\nKelime Tekrarı Başlıyor...\n")
    retry_words = {
        word: data for word, data in words.items()
        if not data["memorized"] and data["retry"]
    }
    if not retry_words:
        print("Tekrar edilecek kelime yok!")
        return

    sorted_words = sorted(retry_words.items(), key=lambda x: parse_date(x[1]["date"]))
    for word, data in sorted_words:
        # 4 şıklı cevaplar oluştur
        correct_translation = data["translation"]
        all_translations = [w["translation"] for w in words.values() if w["translation"] != correct_translation]
        choices = random.sample(all_translations, 3) + [correct_translation]
        random.shuffle(choices)

        print(f"\nKelime: {word}")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")

        try:
            answer = int(input("Doğru çeviriyi seçin (1-4): ").strip())
            if choices[answer - 1] == correct_translation:
                print("Doğru!")
                words[word]["correct_streak"] += 1
                if words[word]["correct_streak"] >= 7:
                    words[word]["date"] = format_date(datetime.now() + timedelta(days=7))
                if words[word]["correct_streak"] >= 21:
                    words[word]["memorized"] = True
            else:
                print(f"Yanlış! Doğru cevap: {correct_translation}")
                words[word]["correct_streak"] = 0
        except (ValueError, IndexError):
            print("Geçersiz seçim! Doğru cevap işaretlenmedi.")


# İstatistikleri gösterme
def show_statistics(words):
    total = len(words)
    memorized = sum(1 for data in words.values() if data["memorized"])
    retry = sum(1 for data in words.values() if data["retry"])

    print("\nİstatistikler:")
    print(f"Toplam Kelime Sayısı: {total}")
    print(f"Ezberlenen Kelime Sayısı: {memorized}")
    print(f"Tekrar Çalışılacak Kelime Sayısı: {retry}")
    print(f"Ezberlenmemiş Kelime Sayısı: {total - memorized}")


# Uygulama Ana Menü
def main():
    file_path = 'translated_words.json'
    words = load_words(file_path)

    # Varsayılan olarak correct_streak ekleyelim
    for word, data in words.items():
        if "correct_streak" not in data:
            data["correct_streak"] = 0

    while True:
        print("\nKelime Ezberleme Uygulaması")
        print("1. Yeni Kelime Öğren")
        print("2. Kelime Tekrarı Yap")
        print("3. İstatistikleri Göster")
        print("4. Çık ve Kaydet")
        choice = input("Seçiminizi yapın (1-4): ")

        if choice == '1':
            learn_new_words(words)
        elif choice == '2':
            review_words(words)
        elif choice == '3':
            show_statistics(words)
        elif choice == '4':
            save_words(file_path, words)
            print("Değişiklikler kaydedildi. Hoşça kalın!")
            break
        else:
            print("Geçersiz seçim! Lütfen 1-4 arasında bir değer girin.")


# Uygulamayı başlat
if __name__ == "__main__":
    main()
