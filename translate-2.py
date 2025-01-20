#pip install googletrans==4.0.0-rc1

from googletrans import Translator
import os

def translate_text_files(input_path, output_path, src_lang="en", dest_lang="tr"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    translator = Translator()

    for filename in os.listdir(input_path):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_path, filename)
            with open(input_file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Çeviri işlemi
            translated = translator.translate(text, src=src_lang, dest=dest_lang).text

            output_filename = os.path.splitext(filename)[0] + "_translated.txt"
            output_file_path = os.path.join(output_path, output_filename)

            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(translated)

            print(f"{output_file_path} kaydedildi.")

input_path = "output/output_text"  # OCR çıktılarının olduğu klasör
output_path = "output/translated_text"  # Çevirilerin kaydedileceği klasör
translate_text_files(input_path, output_path)
