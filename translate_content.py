from googletrans import Translator
import os

def combine_text_files(input_path, combined_file_path):
    with open(combined_file_path, "w", encoding="utf-8") as combined_file:
        for filename in sorted(os.listdir(input_path), key=lambda x: int(x.split('.')[0])):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_path, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    korean_text = f.read()
                    combined_file.write(korean_text + "\\n\\n")

    print(f"Korece tüm metinler {combined_file_path} dosyasına birleştirildi.")

def translate_file(input_file_path, output_file_path, src_lang, dest_lang):
    translator = Translator()
    translator = Translator(service_urls=['translate.googleapis.com'])

    # Giriş dosyasındaki metni oku
    with open(input_file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Metni belirtilen dile çevir
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(translated_text)

    print(f"{input_file_path} dosyası {dest_lang} diline çevrildi ve {output_file_path} olarak kaydedildi.")

# Kullanım
input_path = "output/output_text/"              # Sıralı Korece metinlerin olduğu klasör
combined_file_path = "output/output_translated/korean.txt"        # Birleştirilen Korece dosyası
english_output_path = "output/translated_eng.txt"  # İngilizce çeviri dosyası
turkish_output_path = "output/translated_tur.txt"  # Türkçe çeviri dosyası

# 1. Korece sayfa dosyalarını sıralı şekilde birleştir
combine_text_files(input_path, combined_file_path)

# 2. Birleştirilen Korece metni İngilizceye çevir
translate_file(combined_file_path, english_output_path, src_lang='ko', dest_lang='en')

# 3. Birleştirilen Korece metni Türkçeye çevir
translate_file(combined_file_path, turkish_output_path, src_lang='ko', dest_lang='tr')
