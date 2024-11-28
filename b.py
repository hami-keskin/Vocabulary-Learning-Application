import json
from googletrans import Translator

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
            # Kelimenin Türkçe çevirisini ve anlamını alt kategori olarak ekliyoruz
            translations[word] = {
                "translation": translated.text,
            }

        except Exception as e:
            print(f"Hata oluştu: {word}, {e}")
            translations[word] = {"translation": None}

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
