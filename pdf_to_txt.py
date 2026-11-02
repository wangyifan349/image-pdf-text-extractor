"""Extract text from images and PDFs, then save it as a text file."""

import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")
ACCENT = "#e85d3f"
DARK = "#a93627"
CREAM = "#fff8f3"


def extract_file(path, language):
    extension = os.path.splitext(path)[1].lower()
    import pytesseract
    from PIL import Image

    if extension == ".pdf":
        import fitz

        document = fitz.open(path)
        pages = []
        for page in document:
            text = page.get_text().strip()
            if not text:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
                text = pytesseract.image_to_string(image, lang=language).strip()
            pages.append(text)
        document.close()
        return "\n\n".join(pages)

    if extension in IMAGE_TYPES:
        with Image.open(path) as image:
            return pytesseract.image_to_string(image, lang=language).strip()
    raise ValueError("Unsupported file type")


class ExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image & PDF Text Extractor")
        self.root.geometry("900x700")
        self.root.configure(background=CREAM)
        self.files = []
        self.results = queue.Queue()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 12), background=CREAM, foreground="#382b29")
        style.configure("TFrame", background=CREAM)
        style.configure("TLabel", background=CREAM, font=("Segoe UI", 12))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground=DARK)
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=(12, 8))
        style.configure("Accent.TButton", background=ACCENT, foreground="white")
        style.map("Accent.TButton", background=[("active", DARK), ("disabled", "#d9aaa1")])

        ttk.Label(root, text="Image & PDF Text Extractor", style="Title.TLabel").pack(
            anchor="w", padx=18, pady=(16, 10)
        )
        toolbar = ttk.Frame(root, padding=(14, 4))
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Add Files", command=self.add_files).pack(side="left")
        ttk.Button(toolbar, text="Clear List", command=self.clear_files).pack(side="left", padx=7)
        ttk.Label(toolbar, text="OCR language:").pack(side="left", padx=(18, 6))
        self.language = tk.StringVar(value="eng")
        ttk.Entry(toolbar, textvariable=self.language, width=14, font=("Segoe UI", 12)).pack(side="left")
        self.extract_button = ttk.Button(
            toolbar, text="Extract Text", style="Accent.TButton", command=self.start_extract
        )
        self.extract_button.pack(side="left", padx=10)
        ttk.Button(toolbar, text="Save as TXT", command=self.save_text).pack(side="right")

        ttk.Label(root, text="Files to process").pack(anchor="w", padx=18, pady=(12, 3))
        self.file_list = tk.Listbox(
            root, height=7, selectmode=tk.EXTENDED, font=("Segoe UI", 11),
            background="white", foreground="#382b29", selectbackground=ACCENT,
        )
        self.file_list.pack(fill="x", padx=18, pady=(0, 12))
        ttk.Label(root, text="Extracted text — review or edit before saving").pack(
            anchor="w", padx=18, pady=(0, 3)
        )
        text_frame = ttk.Frame(root)
        text_frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        self.text = tk.Text(
            text_frame, wrap="word", undo=True, font=("Segoe UI", 12),
            background="white", foreground="#382b29", insertbackground=ACCENT,
            padx=10, pady=10,
        )
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.status = tk.StringVar(value="Ready. OCR requires Tesseract and the selected language data.")
        ttk.Label(root, textvariable=self.status, padding=(18, 8)).pack(fill="x")

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select images or PDF files",
            filetypes=[("Images and PDFs", "*.pdf *.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"),
                       ("All files", "*.*")],
        )
        for path in paths:
            if path not in self.files:
                self.files.append(path)
                self.file_list.insert("end", path)

    def clear_files(self):
        self.files.clear()
        self.file_list.delete(0, "end")

    def start_extract(self):
        if not self.files:
            messagebox.showinfo("No files", "Add one or more image or PDF files first.")
            return
        self.extract_button.configure(state="disabled")
        self.status.set("Extracting text…")
        threading.Thread(
            target=self._extract_worker,
            args=(list(self.files), self.language.get().strip() or "eng"),
            daemon=True,
        ).start()
        self.root.after(100, self._check_results)

    def _extract_worker(self, paths, language):
        output, errors = [], []
        for path in paths:
            try:
                text = extract_file(path, language)
                output.append(f"===== {os.path.basename(path)} =====\n\n{text or '[No text recognized]'}")
            except Exception as error:
                errors.append(f"{os.path.basename(path)}: {error}")
        self.results.put(("\n\n".join(output), errors))

    def _check_results(self):
        try:
            output, errors = self.results.get_nowait()
        except queue.Empty:
            self.root.after(100, self._check_results)
            return
        self.extract_button.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", output)
        self.status.set("Extraction complete." if not errors else f"Finished with {len(errors)} error(s).")
        if errors:
            messagebox.showwarning("Some files failed", "\n".join(errors))

    def save_text(self):
        content = self.text.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showinfo("No text", "There is no text to save yet.")
            return
        path = filedialog.asksaveasfilename(
            title="Save extracted text", defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8-sig") as file:
                    file.write(content)
                self.status.set(f"Saved: {path}")
            except OSError as error:
                messagebox.showerror("Save failed", str(error))


if __name__ == "__main__":
    app_root = tk.Tk()
    ExtractorApp(app_root)
    app_root.mainloop()
