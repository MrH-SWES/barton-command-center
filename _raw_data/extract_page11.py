import fitz

pdf = fitz.open("Level 4 Manual part 1.pdf")

page = pdf[10]   # PDF page 11 (0-based indexing)

pix = page.get_pixmap(matrix=fitz.Matrix(3,3))
pix.save("page11.png")

print("saved page11.png")