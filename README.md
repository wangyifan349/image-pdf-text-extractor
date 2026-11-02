# Image & PDF Text Extractor

A small desktop app built with Python 3 and Tkinter. Extract text from images and PDFs, review or edit the result, and save it as a UTF-8 text file.

## Features

- Process multiple PDF and image files (`PNG`, `JPG`, `BMP`, `TIFF`, and `WebP`).
- Extract selectable text directly from PDFs.
- Use Tesseract OCR for images and PDF pages that contain no selectable text.
- Edit the extracted text before saving.
- Runs locally; files are not uploaded.

## Requirements

- Python 3.9 or newer
- Python packages:

  ```bash
  python -m pip install pymupdf pillow pytesseract
  ```

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for image and scanned-PDF OCR. Install the language data you need. For English, use `eng`; for Simplified Chinese and English, use `chi_sim+eng`.

## Run

```bash
python pdf_to_txt.py
```

Click **Add Files**, choose an OCR language, and click **Extract Text**. Review or edit the result, then click **Save as TXT**.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
