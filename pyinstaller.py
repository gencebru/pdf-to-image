#pip install pyinstaller

import os
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pytesseract import image_to_string
from googletrans import Translator
from reportlab.pdfgen import canvas

def process_pdf(file_path, output_dir):
    # Çeviri için ayarlar
    translator = Translator()

    # Machine-readable kontrolü
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    if text.strip():  # Eğer metin okunabiliyorsa
        translated_text = translator.translate(text, src="auto", dest="tr").text
    else:  # Eğer metin okunamıyorsa OCR yap
        images = convert_from_path(file_path)
        ocr_text = ""
        for image in images:
            ocr_text += image_to_string(image, lang="tur+eng")
        translated_text = translator.translate(ocr_text, src="auto", dest="tr").text

    # Çıktıyı PDF olarak kaydet
    output_pdf_path = os.path.join(output_dir, "translated_output.pdf")
    c = canvas.Canvas(output_pdf_path)
    c.drawString(100, 800, translated_text[:4000])  # Çok uzun metni kırpabiliriz
    c.save()

    return output_pdf_path

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    output_dir = filedialog.askdirectory()
    if not output_dir:
        messagebox.showerror("Hata", "Bir çıkış klasörü seçmelisiniz.")
        return

    try:
        output_pdf = process_pdf(file_path, output_dir)
        messagebox.showinfo("Başarılı", f"Çeviri tamamlandı. Çıktı: {output_pdf}")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    select_pdf()



#pyinstaller --onefile --noconsole --add-data "path_to_tesseract/tesseract.exe;." my_script.py
