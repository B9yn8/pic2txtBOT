import pytesseract

# الحصول على مسار Tesseract
tesseract_path = pytesseract.get_tesseract_version()['tesseract_cmd']

print("مسار Tesseract:", tesseract_path)
