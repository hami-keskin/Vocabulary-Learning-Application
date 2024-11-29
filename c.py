import json
import random

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
            print("Bu kelime ezberlenmiş olarak işaretlendi!")
        else:
            work_on_word = input("Bu kelime üzerinde çalışmak istiyor musunuz? (e/h): ").strip().lower()
            if work_on_word == 'e':
                words[word]["retry"] = True
                print("Bu kelime tekrar listesine eklendi!")
            else:
                print("Bu kelime üzerinde değişiklik yapılmadı.")

# Kelime tekrar
def review_words(words):
    print("\nKelime Tekrarı Başlıyor...\n")
    retry_words = {word: data for word, data in words.items() if not data["memorized"] and data["retry"]}
    if not retry_words:
        print("Tekrar edilecek kelime yok!")
        return

    word_list = list(retry_words.keys())
    random.shuffle(word_list)

    for word in word_list:
        correct_answer = words[word]["translation"]
        user_input = input(f"{word}: ").strip()

        if user_input.lower() == correct_answer.lower():
            print("Doğru!")
            words[word]["retry"] = False
        else:
            print(f"Yanlış! Doğru cevap: {correct_answer}")

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
