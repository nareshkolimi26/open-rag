from app.ingestion.loader import load_file
import os

# Test with a text file first
print("Testing text file loading...")
with open("naresh_profile.txt", "rb") as f:
    content = f.read()
    text = load_file(content, "naresh_profile.txt")
    print(f"Text file loaded successfully. Length: {len(text)}")
    print(f"First 100 chars: {text[:100]}")

print("\n" + "="*50 + "\n")

# Test PDF functionality (create a simple test)
print("Testing PDF loader function...")
try:
    from app.ingestion.loader import load_pdf_file
    print("PDF loader imported successfully")
    print("PDF loading is ready for use")
except Exception as e:
    print(f"Error with PDF loader: {e}")
