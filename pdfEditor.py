#To Install dependencies: "pip install PyPDF2 fitz pillow"
#To Run: type "python pdfEditor.py" in terminal 
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk  # For scrollbars
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz  # PyMuPDF for rendering PDFs
from PIL import Image, ImageTk  # To display the PDF pages in the UI

# Global variables to track the current PDF and page
pdf_file = None
doc = None
current_page = 0

# Function to open and display a PDF file
def open_pdf():
    global pdf_file, doc, current_page
    pdf_file = filedialog.askopenfilename(title="Select PDF to Open", filetypes=[("PDF files", "*.pdf")])
    if pdf_file:
        doc = fitz.open(pdf_file)  # Open the PDF document
        current_page = 0  # Start from the first page
        show_page(current_page)
        update_page_label()  # Update the label to reflect the current page and total pages
    else:
        messagebox.showwarning("Warning", "No file selected.")

# Function to show a specific page
def show_page(page_num):
    global img, canvas
    if doc:
        page = doc.load_page(page_num)  # Get the specified page
        pix = page.get_pixmap()  # Render the page as a pixmap

        # Resize the canvas to match the page size
        canvas.config(scrollregion=(0, 0, pix.width, pix.height))
        canvas.delete("all")
        
        # Convert the pixmap to an image and display it on the canvas
        img = ImageTk.PhotoImage(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Calculate the offsets to center the image on the canvas
        x_offset = (canvas_width - pix.width) // 2
        y_offset = (canvas_height - pix.height) // 2
        if x_offset < 0: x_offset = 0
        if y_offset < 0: y_offset = 0
        
        canvas.create_image(x_offset, y_offset, anchor="nw", image=img)
        update_page_label()  # Update the page label

# Mouse wheel scroll event to move between pages
def on_mouse_wheel(event):
    global current_page
    if event.delta > 0:  # Scroll up
        if current_page > 0:
            current_page -= 1
    elif event.delta < 0:  # Scroll down
        if current_page < len(doc) - 1:
            current_page += 1
    show_page(current_page)

# Function to update the page label to show the current page and total pages
def update_page_label():
    if doc:
        page_label.config(text=f"Page {current_page + 1} of {len(doc)}")

# Function to delete selected pages from the PDF
def delete_pages():
    global pdf_file, doc
    if not pdf_file:
        messagebox.showwarning("Warning", "Open a PDF first.")
        return

    pages_to_delete = simpledialog.askstring("Input", "Enter page numbers to delete (comma-separated, starting from 1):")
    if pages_to_delete:
        pages_to_delete = [int(page) - 1 for page in pages_to_delete.split(',')]  # Convert to 0-based index
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for i in range(len(reader.pages)):
            if i not in pages_to_delete:
                writer.add_page(reader.pages[i])

        with open(pdf_file, 'wb') as f:  # Save the changes directly to the same PDF
            writer.write(f)

        # Reopen the PDF after modifying it
        doc.close()
        doc = fitz.open(pdf_file)
        show_page(current_page)
        messagebox.showinfo("Success", f"Pages removed and saved to {pdf_file}")

# Function to add a PDF after the current page
def add_pdf_after():
    global pdf_file, doc, current_page
    if not pdf_file:
        messagebox.showwarning("Warning", "Open a PDF first.")
        return

    files_to_add = filedialog.askopenfilenames(title="Select PDFs to Add After", filetypes=[("PDF files", "*.pdf")])
    if files_to_add:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        # Add all pages up to the current page
        for i in range(current_page + 1):
            writer.add_page(reader.pages[i])

        # Append the new PDFs
        for pdf in files_to_add:
            new_reader = PdfReader(pdf)
            for page in new_reader.pages:
                writer.add_page(page)

        # Add remaining pages from the original PDF
        for i in range(current_page + 1, len(reader.pages)):
            writer.add_page(reader.pages[i])

        # Save the updated PDF (directly overwrite the existing file)
        with open(pdf_file, 'wb') as f:
            writer.write(f)

        # Reopen the PDF after modifying it
        doc.close()
        doc = fitz.open(pdf_file)
        show_page(current_page + 1)
        messagebox.showinfo("Success", f"PDF modified directly in {pdf_file}")

# Function to add a PDF before the current page
def add_pdf_before():
    global pdf_file, doc, current_page
    if not pdf_file:
        messagebox.showwarning("Warning", "Open a PDF first.")
        return

    files_to_add = filedialog.askopenfilenames(title="Select PDFs to Add Before", filetypes=[("PDF files", "*.pdf")])
    if files_to_add:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        # Add all pages before the current page
        for i in range(current_page):
            writer.add_page(reader.pages[i])

        # Append the new PDFs
        for pdf in files_to_add:
            new_reader = PdfReader(pdf)
            for page in new_reader.pages:
                writer.add_page(page)

        # Add remaining pages from the original PDF
        for i in range(current_page, len(reader.pages)):
            writer.add_page(reader.pages[i])

        # Save the updated PDF (directly overwrite the existing file)
        with open(pdf_file, 'wb') as f:
            writer.write(f)

        # Reopen the PDF after modifying it
        doc.close()
        doc = fitz.open(pdf_file)
        show_page(current_page)
        messagebox.showinfo("Success", f"PDF modified directly in {pdf_file}")

# Create the Tkinter window
root = tk.Tk()
root.title("PDF Editor with Viewer")
root.geometry("800x600")

# Create a frame to hold the canvas and the scrollbars
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Create a canvas for displaying the PDF page with scrollbars
canvas = tk.Canvas(frame, bg="white")
canvas.grid(row=0, column=0, sticky="nsew")

# Add vertical and horizontal scrollbars to the canvas
scroll_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

canvas.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

# Bind the mouse wheel event to scroll between pages
canvas.bind("<MouseWheel>", on_mouse_wheel)

# Buttons for performing actions
button_frame = tk.Frame(root)
button_frame.pack()

open_button = tk.Button(button_frame, text="Open PDF", command=open_pdf)
open_button.grid(row=0, column=0, padx=10)

add_after_button = tk.Button(button_frame, text="Add PDF After", command=add_pdf_after)
add_after_button.grid(row=0, column=1, padx=10)

add_before_button = tk.Button(button_frame, text="Add PDF Before", command=add_pdf_before)
add_before_button.grid(row=0, column=2, padx=10)

delete_button = tk.Button(button_frame, text="Delete Pages", command=delete_pages)
delete_button.grid(row=0, column=3, padx=10)

# Label to show current page number
page_label = tk.Label(root, text="Page 1 of 1")
page_label.pack()

# Configure the row/column weights so that the canvas expands when the window is resized
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Run the Tkinter main loop
root.mainloop()
