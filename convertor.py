import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os
import fitz  # PyMuPDF
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx2pdf import convert as docx2pdf_convert

# Converts image type
def convert_image(input_path, output_path, output_format):
    try:
        image = Image.open(input_path)
        image_format = output_format.upper()

        # Check if the output format is supported
        if image_format not in ["JPEG", "PNG", "GIF", "BMP"]:
            messagebox.showerror("Unsupported Output Format", "Unsupported output format for images.")
            return

        # Convert GIF to other formats if needed
        if image_format == "JPEG" and image.format == "GIF":
            image = image.convert("RGB")
        elif image_format == "PNG" and image.format == "GIF":
            image = image.convert("RGBA")

        image.save(output_path, format=image_format)
        messagebox.showinfo("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error converting {input_path}: {str(e)}")

# Converts files to a PDF
def convert_text(input_path, output_path, output_format):
    try:
        if output_format == "PDF":
            if input_path.endswith('.txt'):
                # Convert text (TXT) to PDF
                c = canvas.Canvas(output_path, pagesize=letter)
                with open(input_path, 'r') as input_file:
                    text = input_file.read()
                    c.drawString(100, 750, text)
                c.save()
            elif input_path.endswith('.doc'):
                # Convert DOC to PDF
                docx2pdf_convert(input_path)
            else:
                messagebox.showerror("Unsupported Input Format", "Unsupported input format for PDF conversion.")
                return
        else:
            messagebox.showerror("Unsupported Output Format", "Unsupported output format for text files.")
            return
        messagebox.showinfo("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error converting {input_path}: {str(e)}")

# Converts the PDF to a word DOC
def convert_pdf(input_path, output_path, output_format):
    try:
        if output_format == "DOC":
            doc = fitz.open(input_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text()
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)
            doc.close()
        else:
            messagebox.showerror("Unsupported Output Format", "Unsupported output format for PDF files.")
            return
        messagebox.showinfo("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error converting {input_path}: {str(e)}")

# Allows the user to find the file
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_extension = os.path.splitext(file_path)[1][1:].upper()
        if file_extension not in ["JPG", "PNG", "GIF", "BMP", "TXT", "PDF", "DOC", "DOCX"]:
            messagebox.showerror("Unsupported File Type", "Please select a supported file type (JPG, PNG, GIF, BMP, TXT, PDF, DOC, DOCX).")
            return
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

# Converts the file
def convert():
    input_path = input_file_entry.get()
    if not input_path:
        messagebox.showerror("No File Selected", "Please select an input file.")
        return

    output_format = output_format_entry.get()
    output_folder = "output_files"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = os.path.splitext(os.path.basename(input_path))[0] + '.' + output_format.lower()
    output_path = os.path.join(output_folder, output_filename)

    if input_path.endswith(('.jpg', '.png', '.gif', '.bmp')):
        convert_image(input_path, output_path, output_format)
    elif input_path.endswith(('.txt', '.doc', '.docx')):
        convert_text(input_path, output_path, output_format)
    elif input_path.endswith('.pdf'):
        convert_pdf(input_path, output_path, output_format)
    else:
        messagebox.showerror("Unsupported File Type", "Unsupported input file type.")
        return

# Create the main window
root = tk.Tk()
root.title("File Type Converter")
root.geometry("850x400")
root.resizable(False, False)
root.configure(bg="light grey")

# Label and Entry for input file
input_file_label = tk.Label(root, text="Select an input file:")
input_file_label.pack(pady=20)
input_file_entry = tk.Entry(root)
input_file_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Label and Entry for output format
output_format_label = tk.Label(root, text="Output format (e.g., JPEG, PDF, DOC):")
output_format_label.pack(pady=10)
output_format_entry = tk.Entry(root)
output_format_entry.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()