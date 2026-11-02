# 🧡 Image & PDF Text Extractor

A lightweight desktop app built with **Python 3** and **Tkinter**. Extract text from images and PDFs, review or edit the results, and save them as a UTF-8 text file. Everything runs locally; your files are not uploaded. 🔒

## ℹ️ About

This app extracts selectable text from PDFs and uses Tesseract OCR for images and PDF pages without selectable text. You can review and edit the extracted text before saving it as a TXT file.

## ✨ Features

- 📂 Process multiple PDF and image files: PNG, JPG, JPEG, BMP, TIFF, and WebP.
- 📄 Extract selectable text directly from PDFs.
- 🔎 Run [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) on images and PDF pages without selectable text.
- ✍️ Review and edit extracted text before saving.
- 💻 Simple graphical interface built with [Tkinter](https://docs.python.org/3/library/tkinter.html).

## 🧰 Requirements

- [Python 3.9 or newer](https://www.python.org/downloads/)
- Python packages:

  ```bash
  python -m pip install pymupdf pillow pytesseract
  ```

  - [PyMuPDF](https://pymupdf.readthedocs.io/) reads and renders PDF pages.
  - [Pillow](https://pillow.readthedocs.io/) opens and processes images.
  - [pytesseract](https://github.com/madmaze/pytesseract) connects Python to Tesseract OCR.
- [Tesseract OCR](https://tesseract-ocr.github.io/) must also be installed for image and scanned-page OCR. Install the language data you need; for example, use `eng` for English or `chi_sim+eng` for Simplified Chinese and English.

## 🚀 Run

```bash
python pdf_to_txt.py
```

1. Click **Add Files** and choose one or more images or PDFs.
2. Set the OCR language, then click **Extract Text**.
3. Review or edit the result and click **Save as TXT**. 💾

## ₿ Support the project

If this tool is useful to you, you can support its development with Bitcoin:

`bc1q7ye9xq0gcp2z9dh5lzafgld6z29nzt5m68tsfj`

## 📜 License

Released under the [MIT License](LICENSE).
