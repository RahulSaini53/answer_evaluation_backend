import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)


        text = ''
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

    return text

# Example usage:
file_path = r'C:\Users\rksck\Desktop\major project2\backend\project_backend\Media\uploads\1.pdf'  # Replace with your PDF file path
pdf_text = read_pdf(file_path)
print(pdf_text)
