import cv2
import matplotlib.pyplot as plt
import easyocr
from super_resolution import enhance_image

def show_image(img, title="Image"):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def extract_text(img_array):
    print("[INFO] Running OCR using EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(img_array)
    extracted_lines = [text[1] for text in result]
    return extracted_lines

if __name__ == "__main__":
    image_path = "sample_images/img2.jpeg"

    # Step 1: Enhance the image
    enhanced_img = enhance_image(image_path)
    show_image(enhanced_img, "Enhanced Image")

    # Step 2: Extract text using EasyOCR
    lines = extract_text(enhanced_img)

    print("\n[RESULT] Lines Detected on Tyre:\n")
    if lines:
        for i, line in enumerate(lines, 1):
            print(f"{i:02d}. {line}")
    else:
        print("[!] No text detected.")
