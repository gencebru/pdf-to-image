import os
import tempfile
import shutil
import pytesseract
from tkinter import Tk, filedialog, Button, Label
from tkinter import messagebox
from tkinter import ttk
from googletrans import Translator
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import time  # for updtate_idletask

def translate_pdf(input_pdf_path, output_pdf_path, progress_callback):
    translator = Translator()
    temp_dir = tempfile.mkdtemp()

    try:
        images = convert_from_path(input_pdf_path)
        writer = PdfWriter()

        total_pages = len(images)
        for page_index, img in enumerate(images):
            # Save image temporarily
            img_path = os.path.join(temp_dir, f"temp_page_{page_index}.png")
            img.save(img_path, "PNG")

            # OCR processing
            ocr_text = pytesseract.image_to_string(img, lang='eng')
            translated_text = ""

            if ocr_text.strip():
                translated_text = translator.translate(ocr_text, src='auto', dest='tr').text

                # Annotate image with translated text
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                text_position = (10, 10)  #
                draw.text(text_position, translated_text, fill=(0, 0, 0), font=font)


            # Save annotated image as PDF page
            annotated_image_path = os.path.join(temp_dir, f"translated_page_{page_index}.pdf")
            img.save(annotated_image_path, "PDF")

            # Add the page to the writer
            with open(annotated_image_path, "rb") as f:
                writer.add_page(PdfReader(f).pages[0])

            # Update progress bar
            progress_callback((page_index + 1) / total_pages * 100)

        # Write final PDF
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

    finally:
        shutil.rmtree(temp_dir)


def update_progress(value):
    progress_bar['value'] = value
    root.update_idletasks()
    time.sleep(0.01)


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
        progress_bar['value'] = 0  # Reset progress bar before processing
        #progress_bar.pack()  # pack??

        translate_pdf(input_path, output_path, update_progress)
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

# Progress Bar

progress_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=100)
#progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate',takefocus=True, maximum=100)

progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
