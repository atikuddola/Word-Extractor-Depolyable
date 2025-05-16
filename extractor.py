import argparse
import re
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def extract_words_from_pdf(pdf_path):
    """Extract and return all words with comprehensive pattern matching."""
    reader = PdfReader(pdf_path)
    words = []

    pattern = re.compile(r"""
        (?:^|(?<=\s))   
        [^\s\-.,!?;:()"]+  
        (?:            
            -[^\s\-.,!?;:()"]+ 
            |['’][^\s\-.,!?;:()"]*
        )*               
        [^\s\-.,!?;:()"]* 
        (?=\s|$|[,!?;:()"])
    """, re.VERBOSE | re.UNICODE)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            for token in text.split():
                clean_word = re.sub(r'^[\W_]+|[\W_]+$', '', token, flags=re.UNICODE)
                if clean_word:
                    words.append(clean_word.lower())
    
    return words

def save_words_to_pdf(words, output_path):
    """Save list of words to a PDF file with formatting."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []
    
    flowables.append(Paragraph("Extracted Words", styles['Title']))
    flowables.append(Spacer(1, 12))
    
    col_width = 250
    column1 = []
    column2 = []
    
    for i, word in enumerate(words):
        para = Paragraph(f"{i+1}. {word}", styles['Normal'])
        if i % 2 == 0:
            column1.append(para)
            column1.append(Spacer(1, 4))
        else:
            column2.append(para)
            column2.append(Spacer(1, 4))
    
    flowables.append(Paragraph(f"Total words: {len(words)}", styles['Normal']))
    flowables.append(Spacer(1, 8))
    flowables.extend(column1)
    flowables.append(Spacer(1, 12))
    flowables.extend(column2)
    
    doc.build(flowables)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract words from PDF and save to new PDF')
    parser.add_argument('input_pdf', help='Path to input PDF file')
    parser.add_argument('output_pdf', help='Path to output PDF file')
    args = parser.parse_args()
    
    words = extract_words_from_pdf(args.input_pdf)
    save_words_to_pdf(words, args.output_pdf)
    print(f"Successfully extracted {len(words)} words to {args.output_pdf}")
