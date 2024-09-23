# PDF Editor with Python (Tkinter & PyPDF2)

This is a Python-based PDF editor that allows users to open, view, and modify PDF files. The project provides a graphical interface using Tkinter, and it enables users to perform the following actions:

- View PDF pages
- Add PDF files before or after the current page
- Delete specific pages from a PDF
- Scroll through PDF pages using the mouse wheel

## Features
- **Open PDF**: Load any PDF document and view its contents page by page.
- **Add PDF Pages**: Insert new PDF files before or after the current page.
- **Delete Pages**: Remove specific pages from the current PDF file.
- **Scroll Through Pages**: Use the mouse wheel to scroll seamlessly between pages.
- **Modify PDF Directly**: All modifications are saved directly to the original file.

## Technologies
- **Python**: Core programming language.
- **Tkinter**: For building the graphical user interface.
- **PyPDF2**: For merging, splitting, and modifying PDF files.
- **PyMuPDF (fitz)**: For rendering PDF pages within the interface.

## Setup and Installation

### Prerequisites
- Python 3.x installed on your machine.
- The following Python libraries:
  - `PyPDF2`
  - `PyMuPDF` (fitz)
  - `Pillow`

### Installing Dependencies
You can install the required dependencies using `pip`:

bash
pip install PyPDF2 fitz pillow

### Installing Dependencies
python pdfEditor2.py
The PDF Editor interface will open, allowing you to load and modify PDF files.
