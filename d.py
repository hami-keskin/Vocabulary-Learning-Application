import json
from datetime import datetime


def add_known_attribute(file_path):
    try:
        # Dosyayı yükle
        with open(file_path, 'r', encoding='utf-8') as file:
            words = json.load(file)

        # "known" özelliğini ekle
        for word, data in words.items():
                data["date"] = datetime.now().strftime('%Y-%m-%d')

        # Güncellenmiş veriyi dosyaya kaydet
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(words, file, ensure_ascii=False, indent=4)

        print(f'"known" özelliği eksik olan kelimelere eklendi.')

    except FileNotFoundError:
        print("Hata: Dosya bulunamadı.")
    except json.JSONDecodeError:
        print("Hata: JSON dosyası okunamadı.")


# Dosya yolu
file_path = 'translated_words.json'
add_known_attribute(file_path)
