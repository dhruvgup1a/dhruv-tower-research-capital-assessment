import xml.etree.ElementTree as ET
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import pdfplumber
import uuid
import nltk
from src.config import CHUNK_OVERLAP, CHUNK_SIZE

nltk.download('punkt')
nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

# Small Flaw: Not too modular because in order to get a clean parsing for the file, I needed the nampespace url
def extract_text_from_xml(file_path, book_title = "Unknown Book"):
    """
    Parses xml files. 
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'content': 'http://purl.org/rss/1.0/modules/content/'}

    extracted_text = []
    for item in root.findall(".//item"):
        title_elem = item.find("title")
        content_elem = item.find("content:encoded", namespace)

        if title_elem is not None and content_elem is not None and content_elem.text:
            chapter_title = title_elem.text.strip()
            chapter_content = content_elem.text.strip()

            extracted_text.append({
                "chapter_id": str(uuid.uuid4()),
                "text": chapter_content,
                "metadata": {
                    "book": book_title,
                    "chapter": chapter_title
                }
            })

    return extracted_text


def extract_text_from_epub(file_path, book_title = "Unknown Book"):
    """
    Parses epub files. 
    """
    book = epub.read_epub(file_path)
    extracted_text = []
    for item in book.get_items():
        if item.media_type == "application/xhtml+xml":
            soup = BeautifulSoup(item.content, "html.parser")

            headings = soup.find_all(["h1", "h2"])

            # Only adds text is the heading exists
            if headings:
                chapter_title = headings[0].get_text(strip=True) 
                extracted_text.append({
                    "chapter_id": str(uuid.uuid4()),
                    "text": soup.get_text(),
                    "metadata": {
                        "book": book_title,
                        "chapter": chapter_title
                    }
                })
    return extracted_text

# Small Flaw: There are 3 pages in the provided file contents of two chapters on one page. 
# As a result, the current method puts all the page data to the later chapter. 
def extract_text_from_pdf(file_path, book_title = "Unknown Book"):
    """
    Parses pdf files. 
    """
    chapters = {}
    current_part = "Unknown Part"
    current_roman = "Unknown Roman"
    current_chapter = f"{current_part} - {current_roman}"

    # roman_numeral_pattern = r"^(\sI|II|III|IV|V|VI|VII|VIII)$"
    roman_numeral_pattern = r"^\s*(I|II|III|IV|V|VI|VII|VIII)\s*$"

    part_pattern = r"\bPart\s+(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\b"

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                part_match = re.search(part_pattern, page_text)
                if part_match:
                    current_part = part_match.group() 
                    current_roman = "I"
                    current_chapter = f"{current_part} - {current_roman}"

                # Look for a Roman numeral chapter the page text
                roman_match = re.search(roman_numeral_pattern, page_text, re.MULTILINE)
                if roman_match != None:
                    current_roman = roman_match.group()
                    current_chapter = f"{current_part} - {current_roman}"

                # Append the page text + metadata
                if current_chapter not in chapters:
                    chapters[current_chapter] = []
                chapters[current_chapter].append(page_text)

    combined_chapters = [{
            "chapter_id": str(uuid.uuid4()),
            "text": "\n".join(texts),
            "metadata": {
                "book": book_title,
                "chapter": chapter
            }
        } for chapter, texts in chapters.items() ]
    
    return combined_chapters

# Small Flaw: The method does skip over last couple sentences if it is greater than CHUNK_SIZE since 
# during similarity search, the smaller sentences are more likely to get picked. Caused issues. 
def chunking_book(extracted_book, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Creates chunks for the book data. 
    """
    chunked_data = []

    for chap in extracted_book:
        text = chap["text"]
        book = chap["metadata"]["book"]
        chapter = chap["metadata"]["chapter"]

        # Sentence chunking
        sentences = sent_tokenize(text)

        start = 0
        while start < len(sentences):
            end = start + chunk_size 
            if end < len(sentences):
                chunk = sentences[start:end]
            else:
                start += chunk_size - chunk_overlap
                continue

            chunked_data.append({
                "id": str(uuid.uuid4()),
                "text": " ".join(chunk),
                "metadata": {
                    "book": book,
                    "chapter": chapter
                }
            })

            start += chunk_size - chunk_overlap
    
    return chunked_data

def process_book(book_title, filepath, filetype):
    """
    Single function to parse book data and create chunks. 
    """
    if filetype == "xml":
        data = extract_text_from_xml(filepath, book_title=book_title)
        return chunking_book(data)
    elif filetype == "epub":
        data = extract_text_from_epub(filepath, book_title=book_title)
        return chunking_book(data)
    elif filetype == "pdf":
        data = extract_text_from_pdf(filepath, book_title=book_title)
        return chunking_book(data)
    else:
        print("Invalid file type :(")
        return None
