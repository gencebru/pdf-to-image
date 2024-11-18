from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    pages = convert_from_path(pdf_path)
    
    for page_number, page in enumerate(pages, start=1):
        output_filename = os.path.join(output_path, f"{page_number}.jpg")
        page.save(output_filename, "JPEG")
        print(f"{output_filename} kaydedildi.")


pdf_path = "input/deneme.pdf"  
output_path = "output/output_jpg"  
pdf_to_images(pdf_path, output_path)
