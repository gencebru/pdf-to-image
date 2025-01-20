import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from pytesseract import image_to_string
from googletrans import Translator
from reportlab.pdfgen import canvas
from PIL import Image

def process_pdf_with_images(file_path, output_dir):
    translator = Translator()

    # Orijinal PDF'yi aç
    pdf_document = fitz.open(file_path)
    output_pdf_path = os.path.join(output_dir, "translated_output.pdf")

    # Yeni PDF oluştur
    output_pdf = fitz.open()

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]

        # Sayfa içeriğini al
        text = page.get_text()
        image_list = page.get_images(full=True)

        # Eğer metin varsa çevir
        if text.strip():
            try:
                translated_text = translator.translate(text, src="auto", dest="tr").text
            except Exception as e:
                print(f"Çeviri sırasında hata oluştu: {e}")
                translated_text = text  # Çeviri hatası durumunda orijinal metni bırak

            # Sayfayı düzenle ve metni ekle
            rect = page.rect
            pix = page.get_pixmap()
            img_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
            pix.save(img_path)

            # Görüntüyü ve metni yeni PDF'ye ekle
            page_with_text = output_pdf.new_page(width=rect.width, height=rect.height)
            page_with_text.insert_image(rect, filename=img_path)
            page_with_text.insert_text((50, 50), translated_text, fontsize=12, color=(0, 0, 0))
        else:
            # Eğer OCR gerekliyse
            images = convert_from_path(file_path, first_page=page_number + 1, last_page=page_number + 1)
            ocr_text = ""
            for image in images:
                ocr_text += image_to_string(image, lang="tur+eng")
            try:
                translated_text = translator.translate(ocr_text, src="auto", dest="tr").text
            except Exception as e:
                print(f"OCR çeviri sırasında hata oluştu: {e}")
                translated_text = ocr_text

            # OCR ile metni ekle
            rect = page.rect
            pix = page.get_pixmap()
            img_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
            pix.save(img_path)

            # Görüntüyü ve metni yeni PDF'ye ekle
            page_with_text = output_pdf.new_page(width=rect.width, height=rect.height)
            page_with_text.insert_image(rect, filename=img_path)
            page_with_text.insert_text((50, 50), translated_text, fontsize=12, color=(0, 0, 0))

    # Yeni PDF'yi kaydet
    output_pdf.save(output_pdf_path)
    pdf_document.close()
    output_pdf.close()

    return output_pdf_path


# Kullanıcıdan giriş ve çıkış dosyalarını iste
def main():
    input_pdf = input("İşlenecek PDF dosyasının yolunu girin: ").strip()
    if not os.path.exists(input_pdf):
        print("Hata: Dosya bulunamadı!")
        return

    output_dir = input("Çıktı dosyalarının kaydedileceği klasörün yolunu girin: ").strip()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        output_pdf = process_pdf_with_images(input_pdf, output_dir)
        print(f"Çeviri tamamlandı. Çıktı PDF: {output_pdf}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
