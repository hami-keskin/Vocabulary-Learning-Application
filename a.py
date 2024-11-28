import re
import json

def process_subtitle_file(input_file, output_file):
    try:
        # Farklı kelimeleri saklamak için bir set
        unique_words = set()

        # Altyazı dosyasını satır satır oku
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                # Zaman aralıklarını ve sayıları çıkar
                if re.match(r'^\d+$', line.strip()) or '-->' in line:
                    continue
                # Kelimeleri ayıkla ve filtre uygula (en az 2 harfli kelimeler, sayı içermeyenler)
                words = re.findall(r'\b[a-zA-Z]{2,}\b', line.lower())
                unique_words.update(words)

        # Seti listeye çevir ve JSON formatında kaydet
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(sorted(list(unique_words)), json_file, ensure_ascii=False, indent=4)

        print(f"Farklı kelimeler başarıyla '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Giriş ve çıkış dosyalarının yollarını belirle
input_file = 'subtitles.txt'  # Altyazı dosyasının adı
output_file = 'unique_words.json'  # JSON formatında çıkış dosyası

# Fonksiyonu çalıştır
process_subtitle_file(input_file, output_file)
