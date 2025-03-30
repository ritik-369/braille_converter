import pytesseract
from PIL import Image

# Set the path to Tesseract executable in the media folder
pytesseract.pytesseract.tesseract_cmd = r"C:\msys64\mingw64\include\system\Project\braille_converter\media\Tesseract-OCR\tesseract.exe"

# Load an image from the media folder
image_path = r"C:\Users\ritik\OneDrive\Pictures\Screenshots\Screenshot 2025-03-30 140028.png"  # Replace with your image file
image = Image.open(image_path)

# Extract text from the image
extracted_text = pytesseract.image_to_string(image)

# Print the extracted text
print("Extracted Text:\n", extracted_text)
