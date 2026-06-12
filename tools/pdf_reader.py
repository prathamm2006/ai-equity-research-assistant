from pypdf import PdfReader

def read_pdf(file_path_or_buffer):
    reader = PdfReader(file_path_or_buffer)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=4000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]