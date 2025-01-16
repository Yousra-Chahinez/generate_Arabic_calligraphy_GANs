# --------------- Generates images of Arabic words with different fonts and saves them to an output directory. --------------- #
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import arabic_reshaper
import os

# Paths
TEXT_FILE_PATH = "generate_Arabic_calligraphy_GANs/Data/Quraan.txt"
FONT_DIR = "generate_Arabic_calligraphy_GANs/Data/Fonts"
OUTPUT_DIR = "generate_Arabic_calligraphy_GANs/Data/ReqaaDataset/train"
FONT_FILES = ["arial.ttf", "ruqaa.ttf"]

# Load text
def load_words(file_path):
    """Load and preprocess words from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = {word for line in file for word in line.split()}
        print(f"Number of unique words: {len(words)}")
        return words
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return set()

# Draw and save text
def draw_text_image(word, font, size=(256, 256)):
    """Create an image with centered Arabic text."""
    reshaped_text = arabic_reshaper.reshape(word)
    bidi_text = get_display(reshaped_text)

    image = Image.new("RGB", size, color="white")
    draw = ImageDraw.Draw(image)

    # Calculate text position
    width_text, height_text = draw.textsize(bidi_text, font)
    offset_x, offset_y = font.getoffset(bidi_text)
    width_text += offset_x
    height_text += offset_y
    top_left_x = size[0] / 2 - width_text / 2
    top_left_y = size[1] / 2 - height_text / 2
    xy = (top_left_x, top_left_y)

    # Draw text
    draw.text(xy, bidi_text, fill="black", font=font)
    return image

# Main function
def write_text_to_images(words, fonts, output_dir):
    """Generate images for a list of words using different fonts."""
    os.makedirs(output_dir, exist_ok=True)

    for i, word in enumerate(words):
        for j, font_file in enumerate(fonts):
            try:
                font_path = os.path.join(FONT_DIR, font_file)
                font = ImageFont.truetype(font_path, 70)
                image = draw_text_image(word, font)
                subfolder = "Calligraphy" if j == 0 else "std_font"
                save_dir = os.path.join(output_dir, subfolder)
                os.makedirs(save_dir, exist_ok=True)
                file_name = os.path.join(save_dir, f"{i}.png")
                image.save(file_name, "PNG")
            except Exception as e:
                print(f"Error processing word '{word}' with font '{font_file}': {e}")

# Test a single word with a specific font
def test_single_word(word, font_path, output_path):
    """Generate a test image for a single word."""
    try:
        font = ImageFont.truetype(font_path, 70)
        image = draw_text_image(word, font)
        image.save(output_path, "PNG")
        print(f"Test image saved at {output_path}")
    except Exception as e:
        print(f"Error generating test image: {e}")

# Execution
if __name__ == "__main__":
    words = load_words(TEXT_FILE_PATH)
    write_text_to_images(words, FONT_FILES, OUTPUT_DIR)
    test_single_word(
        "الرجفة",
        "/Users/yousrachahinezhadjazzem/Documents/Python_Files/arial.ttf",
        "/Users/yousrachahinezhadjazzem/Desktop/7.png",
    )
