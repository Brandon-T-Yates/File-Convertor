import tkinter as tk
import os
import fitz
import tkinter.messagebox as msgbox
from tkinter import filedialog
from PIL import Image
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def show_message(title, message, message_type):
    """Custom messagebox function."""
    if message_type == "info":
        msgbox.showinfo(title, message)
    elif message_type == "error":
        msgbox.showerror(title, message)
    elif message_type == "warning":
        msgbox.showwarning(title, message)

def convert_image(input_path, output_path, output_format):
    try:
        image = Image.open(input_path)
        image_format = output_format.upper()

        # Check if the output format is supported
        if image_format not in ["JPEG", "PNG", "GIF", "BMP"]:
            show_message("Unsupported Output Format", "Unsupported output format for images.", "error")
            return

        # Convert GIF to other formats if needed
        if image_format == "JPEG" and image.format == "GIF":
            image = image.convert("RGB")
        elif image_format == "PNG" and image.format == "GIF":
            image = image.convert("RGBA")

        image.save(output_path, format=image_format)
        show_message("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}", "info")
    except Exception as e:
        show_message("Error", f"Error converting {input_path}: {str(e)}", "error")

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
            else:
                show_message("Unsupported Input Format", "Unsupported input format for PDF conversion.", "error")
                return
        else:
            show_message("Unsupported Output Format", "Unsupported output format for text files.", "error")
            return
        show_message("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}", "info")
    except Exception as e:
        show_message("Error", f"Error converting {input_path}: {str(e)}", "error")

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
            show_message("Unsupported Output Format", "Unsupported output format for PDF files.", "error")
            return
        show_message("Conversion Successful", f"Conversion successful: {input_path} -> {output_path}", "info")
    except Exception as e:
        show_message("Error", f"Error converting {input_path}: {str(e)}", "error")

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_extension = os.path.splitext(file_path)[1][1:].upper()
        if file_extension not in ["JPG", "PNG", "GIF", "BMP", "TXT", "PDF", "DOC"]:
            show_message("Unsupported File Type", "Please select a supported file type (JPG, PNG, GIF, BMP, TXT, PDF, DOC).", "error")
            return
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

def convert():
    input_path = input_file_entry.get()
    if not input_path:
        show_message("No File Selected", "Please select an input file.", "error")
        return

    output_format = output_format_entry.get()
    output_folder = "output_files"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = os.path.splitext(os.path.basename(input_path))[0] + '.' + output_format.lower()
    output_path = os.path.join(output_folder, output_filename)

    if input_path.endswith(('.jpg', '.png', '.gif', '.bmp')):
        convert_image(input_path, output_path, output_format)
    elif input_path.endswith(('.txt', '.doc')):
        convert_text(input_path, output_path, output_format)
    elif input_path.endswith('.pdf'):
        convert_pdf(input_path, output_path, output_format)
    else:
        show_message("Unsupported File Type", "Unsupported input file type.", "error")
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