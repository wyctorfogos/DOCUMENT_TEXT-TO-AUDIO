import os
import PyPDF2
from PyPDF2 import PdfReader
from gtts import gTTS
import shutil

def read_document(document):
    reader = PdfReader("./documents/"+document)
    number_of_pages = len(reader.pages)
    text = ""  # Initialize an empty string to accumulate the text
    for i in range(number_of_pages):
        page = reader.pages[i]
        page_text = page.extract_text()
        text += ". Page {}".format(i) + page_text  # Add the text of each page to the accumulated text

        # If the text is too long, generate an audio file for this part and start a new part
        if len(text) > 5000:  # gTTS has a limit of about 5000 characters
            tts = gTTS(text, lang='en', slow=False)
            tts.save('./RESULTS/part{}.mp3'.format(i))
            text = ""  # Start a new part

    # Generate an audio file for the last part
    if text:
        tts = gTTS(text, lang='en', slow=False)
        tts.save('./RESULTS/part{}.mp3'.format(number_of_pages))

    # Combine all audio files into one
    with open('./RESULTS/{}.mp3'.format(os.path.splitext(document)[0]), 'wb') as outfile:
        for i in range(number_of_pages):
            with open('./RESULTS/part{}.mp3'.format(i), 'rb') as infile:
                shutil.copyfileobj(infile, outfile)

read_document("YOLOv3.pdf")

