import pdfplumber

pdf = pdfplumber.open("finnair.pdf")
for page in pdf.pages[1:]:
    text = page.extract_words()
    print(text)
