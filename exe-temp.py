import os
import tempfile
import shutil
import pytesseract
from tkinter import Tk, filedialog, Button, Label
from tkinter import messagebox
from googletrans import Translator
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont

def translate_pdf(input_pdf_path, output_pdf_path):
    translator = Translator()
    temp_dir = tempfile.mkdtemp()

    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page_index, page in enumerate(reader.pages):
            # Extract text if machine-readable
            text = page.extract_text()
            translated_text = ""
            if text:
                translated_text = translator.translate(text, src='auto', dest='tr').text

            # Handle images with OCR
            images = convert_from_path(input_pdf_path, first_page=page_index + 1, last_page=page_index + 1)
            annotated_image_path = None

            if images:
                for img in images:
                    img_path = os.path.join(temp_dir, f"temp_page_{page_index}.png")
                    img.save(img_path, "PNG")

                    ocr_text = pytesseract.image_to_string(img, lang='eng')
                    if ocr_text.strip():
                        translated_text += "\n" + translator.translate(ocr_text, src='auto', dest='tr').text

                    # Annotate the image with translated text
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    text_position = (10, 10)  # Example position for translated text
                    draw.text(text_position, translated_text, fill=(0, 0, 0), font=font)
                    annotated_image_path = os.path.join(temp_dir, f"translated_page_{page_index}.png")
                    img.save(annotated_image_path, "PNG")

            # Add original or annotated image as a new page in the PDF
            if annotated_image_path:
                img_pdf = convert_from_path(annotated_image_path, dpi=200)
                for img_page in img_pdf:
                    temp_img_path = os.path.join(temp_dir, f"temp_img_page_{page_index}.pdf")
                    img_page.save(temp_img_path, "PDF")
                    with open(temp_img_path, "rb") as f:
                        writer.add_page(PdfReader(f).pages[0])
            else:
                writer.add_page(page)

        # Save the translated PDF
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

    finally:
        shutil.rmtree(temp_dir)


def select_pdf():
    input_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if input_file:
        input_label.config(text=input_file)
    else:
        messagebox.showerror("Error", "Please select a valid PDF file.")


def save_pdf():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_file:
        output_label.config(text=output_file)
    else:
        messagebox.showerror("Error", "Please select a valid output location.")


def process_pdf():
    input_path = input_label.cget("text")
    output_path = output_label.cget("text")

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Input PDF is not selected or invalid.")
        return

    if not output_path:
        messagebox.showerror("Error", "Output PDF path is not selected.")
        return

    try:
        translate_pdf(input_path, output_path)
        messagebox.showinfo("Success", "PDF translation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
root = Tk()
root.title("PDF Translator")

Label(root, text="Select Input PDF:").grid(row=0, column=0, padx=10, pady=10)
input_label = Label(root, text="", width=50, anchor="w")
input_label.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Select Output PDF:").grid(row=1, column=0, padx=10, pady=10)
output_label = Label(root, text="", width=50, anchor="w")
output_label.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=save_pdf).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Translate PDF", command=process_pdf).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
