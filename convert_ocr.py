import pytesseract
from PIL import Image
import os

def ocr_images(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    config = '--oem 3 --psm 3 -l tur + eng' #dil seçeneği

    for filename in os.listdir(input_path):
        if filename.endswith(".jpg"):
            image_path = os.path.join(input_path, filename)
            image = Image.open(image_path)
            
            text = pytesseract.image_to_string(image, config=config)
            
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_file_path = os.path.join(output_path, output_filename)
            
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"{output_file_path} kaydedildi.")

input_path = "output/output_jpg"  # JPG dosyalarının olduğu klasör
output_path = "output/output_text/"  # OCR çıktı dosyalarının kaydedileceği klasör
ocr_images(input_path, output_path)
