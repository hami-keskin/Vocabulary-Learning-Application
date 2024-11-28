import json
import requests

def translate_words_with_deepl(input_file, output_file, deepl_api_key):
    # DeepL API URL'si
    deepl_api_url = "https://api-free.deepl.com/v2/translate"

    # İngilizce kelimeleri yükle
    with open(input_file, 'r', encoding='utf-8') as file:
        english_words = json.load(file)

    translations = {}

    for word in english_words:
        try:
            # DeepL API'ye çeviri isteği gönder
            print(f"Çeviriliyor: {word}...")
            response = requests.post(
                deepl_api_url,
                data={
                    'auth_key': deepl_api_key,
                    'text': word,
                    'source_lang': 'EN',
                    'target_lang': 'TR'
                }
            )

            # API'den dönen cevabı kontrol et
            if response.status_code == 200:
                translated_text = response.json()['translations'][0]['text']
                translations[word] = translated_text
            else:
                print(f"Hata oluştu: {word}, Kod: {response.status_code}")
                translations[word] = None  # Hatalı kelimeleri işaretle

        except Exception as e:
            print(f"Hata oluştu: {word}, {e}")
            translations[word] = None

    # Çevirileri yeni bir JSON dosyasına yaz
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(translations, json_file, ensure_ascii=False, indent=4)

    print(f"Çeviriler başarıyla '{output_file}' dosyasına kaydedildi.")

# Giriş dosyasının yolu
input_file = 'unique_words.json'
# Çıkış dosyasının yolu
output_file = 'translated_words.json'
# DeepL API anahtarınız
deepl_api_key = '0751882d-2723-4609-a248-ce74b344e2df:fx'  # Buraya kendi API anahtarınızı girin

# Fonksiyonu çalıştır
translate_words_with_deepl(input_file, output_file, deepl_api_key)
