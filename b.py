import json
from googletrans import Translator
from datetime import datetime

def translate_words_with_google(input_file, output_file):
    # Google Translate Translator nesnesi oluştur
    translator = Translator()

    # İngilizce kelimeleri yükle
    with open(input_file, 'r', encoding='utf-8') as file:
        english_words = json.load(file)

    # Çevirilerin saklanacağı sözlük
    translations = {}

    # Mevcut 'translated_words.json' dosyasını kontrol et, eğer var ise yükle
    try:
        with open(output_file, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            # Eğer dosya boşsa, boş bir sözlük başlat
            if not existing_data:
                print(f"'{output_file}' dosyası boş, yeni verilerle başlatılıyor.")
                existing_data = {}
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Eğer dosya yoksa ya da geçersizse, boş bir sözlük başlat
        print(f"'{output_file}' dosyası bulunamadı veya geçersiz, yeni verilerle başlatılıyor.")
        existing_data = {}

    # Mevcut çevirilerle, yeni kelimeleri güncelleme
    for word in english_words:
        if word not in existing_data:
            try:
                # Google Translate API ile çeviri
                print(f"Çeviriliyor: {word}...")
                translated = translator.translate(word, src='en', dest='tr')

                # Kelime ve çevirisini küçük harfe dönüştürerek karşılaştırma
                if word.lower() == translated.text.lower():
                    print(f"Kelime ve çeviri aynı: {word} - {translated.text}, atlanıyor.")
                    continue  # Eğer aynıysa, bu kelimeyi atla

                # Kelimenin Türkçe çevirisini, ezberlenip ezberlenmediğini, tekrar çalışılmasını ve tarihini ekliyoruz
                translations[word] = {
                    "translation": translated.text,
                    "known": False,
                    "memorized": False,  # Başlangıçta False, çünkü kelimenin ezberlenip ezberlenmediği manuel olarak değiştirilebilir.
                    "retry": False,  # Kelime ezberlenmediyse tekrar çalışılacak.
                    "date": datetime.now().strftime('%Y-%m-%d')  # Kelimenin eklenme tarihi
                }

            except Exception as e:
                print(f"Hata oluştu: {word}, {e}")
                translations[word] = {
                    "translation": None,
                    "known": False,
                    "memorized": False,
                    "retry": False,
                    "date": datetime.now().strftime('%Y-%m-%d')  # Hata durumunda da tarih eklenir
                }
        else:
            # Eğer kelime zaten mevcutsa, mevcut veriyi alalım
            translations[word] = existing_data[word]

    # Yeni verileri mevcut verilerle birleştirerek güncel dosyaya yazalım
    existing_data.update(translations)

    # Çevirileri güncellenmiş JSON dosyasına yaz
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    print(f"Çeviriler başarıyla '{output_file}' dosyasına kaydedildi.")

# Giriş dosyasının yolu
input_file = 'unique_words.json'
# Çıkış dosyasının yolu
output_file = 'translated_words.json'

# Fonksiyonu çalıştır
translate_words_with_google(input_file, output_file)
