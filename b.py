import json
from googletrans import Translator
from datetime import datetime

def translate_words_with_google(input_file, output_file):
    # Google Translate Translator nesnesi oluştur
    translator = Translator()

    # İngilizce kelimeleri yükle
    with open(input_file, 'r', encoding='utf-8') as file:
        english_words = json.load(file)

    translations = {}

    for word in english_words:
        try:
            # Google Translate API ile çeviri
            print(f"Çeviriliyor: {word}...")
            translated = translator.translate(word, src='en', dest='tr')

            # Kelimenin Türkçe çevirisini, ezberlenip ezberlenmediğini, tekrar çalışılmasını ve tarihini ekliyoruz
            translations[word] = {
                "translation": translated.text,
                "memorized": False,  # Başlangıçta False, çünkü kelimenin ezberlenip ezberlenmediği manuel olarak değiştirilebilir.
                "retry": False,  # Kelime ezberlenmediyse tekrar çalışılacak.
                "date": datetime.now().strftime('%Y-%m-%d')  # Kelimenin eklenme tarihi
            }

        except Exception as e:
            print(f"Hata oluştu: {word}, {e}")
            translations[word] = {
                "translation": None,
                "memorized": False,
                "retry": False,
                "date": datetime.now().strftime('%Y-%m-%d')  # Hata durumunda da tarih eklenir
            }

    # Çevirileri yeni bir JSON dosyasına yaz
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(translations, json_file, ensure_ascii=False, indent=4)

    print(f"Çeviriler başarıyla '{output_file}' dosyasına kaydedildi.")

# Giriş dosyasının yolu
input_file = 'unique_words.json'
# Çıkış dosyasının yolu
output_file = 'translated_words.json'

# Fonksiyonu çalıştır
translate_words_with_google(input_file, output_file)
