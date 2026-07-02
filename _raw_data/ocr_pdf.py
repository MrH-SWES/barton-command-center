import fitz
import subprocess
import tempfile
import os

PDF_FILE = "Level 4 Manual part 1.pdf"

TESSERACT = os.path.expandvars(
    r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"
)

pdf = fitz.open(PDF_FILE)

output_file = PDF_FILE.replace(".pdf", " - Tesseract.txt")

with open(output_file, "w", encoding="utf-8") as out:

    for page_num in range(len(pdf)):
        print(f"Processing page {page_num + 1}/{len(pdf)}")

        page = pdf[page_num]

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        ) as tmp:

            png_path = tmp.name

        pix.save(png_path)

        result = subprocess.run(
            [
                TESSERACT,
                png_path,
                "stdout",
                "--psm",
                "6"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        out.write(f"\n\n===== PAGE {page_num + 1} =====\n\n")
        out.write(result.stdout)

        os.remove(png_path)

print(f"Done. Output saved to: {output_file}")