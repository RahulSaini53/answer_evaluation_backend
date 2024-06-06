'''~~~~~~~~~~~~~~~~~~~OCR(Optical character recognition)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
import pytesseract
from PIL import Image
from textblob import Word
# import pytesseract
# from PIL import Image

def correct_spelling(word):
    w = Word(word)
    # Correct the spelling
    corrected_word = w.correct()
    return corrected_word

def image_to_text(image_path):
    # Open the image file
    img =  Image.open(image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    words = text.split()

    # Correct the spelling of each word
    corrected_text = []
    for word in words:
        # Get the corrected version of the word
        corrected_word = correct_spelling(word)
        corrected_text.append(corrected_word)
    # Join the corrected words back into a single string
    corrected_text = ' '.join(corrected_text)

    return corrected_text
