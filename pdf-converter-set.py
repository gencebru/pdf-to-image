from pdf2image import convert_from_path
import os


def pdf_to_images(input_dir, output_dir):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Girdi klasörü bulunamadı: {input_dir}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_output_dir = os.path.join(output_dir, pdf_name)

            if not os.path.exists(pdf_output_dir):
                os.makedirs(pdf_output_dir)

            pages = convert_from_path(pdf_path)
            for page_number, page in enumerate(pages, start=1):
                output_filename = os.path.join(pdf_output_dir, f"{page_number}.jpg")
                page.save(output_filename, "JPEG")
                print(f"{output_filename} kaydedildi.")


input_dir = "input/scanned-pdf"
output_dir = ".../develop/Github/pdf-to-image/output/pdf"

pdf_to_images(input_dir, output_dir)
