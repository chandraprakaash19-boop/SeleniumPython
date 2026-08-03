from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io


def get_dominant_color(element):
    """
    Takes a screenshot of a Selenium WebElement and returns
    the dominant color in HEX and RGB formats.
    """
    # 1. Get screenshot of the specific element as binary data
    png_data = element.screenshot_as_png

    # 2. Open image with Pillow
    img = Image.open(io.BytesIO(png_data))

    # 3. Resize image to speed up processing (optional, reduces pixel count)
    img = img.resize((150, 150))

    # 4. Convert to RGB to ensure consistency
    img = img.convert('RGB')

    # 5. Get colors sorted by count (limit to 1 result for the most frequent)
    # getcolors() returns a list of (count, (r, g, b))
    # We increase maxcolors to ensure we catch the dominant one in complex images
    colors = img.getcolors(maxcolors=150 * 150)

    # Sort by count (descending) to find the most frequent color
    dominant_color = sorted(colors, key=lambda x: x[0], reverse=True)[0][1]

    return dominant_color


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def print_colored_output(label, rgb):
    """
    Prints the text in the actual color found using ANSI escape codes.
    """
    hex_val = rgb_to_hex(rgb)
    # ANSI escape code for text color
    print(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{label}: {hex_val} (RGB: {rgb})\033[0m")


# --- MAIN EXECUTION ---
def main():
    # Setup Chrome options (Headless mode is faster)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        url = 'https://www.python.org'  # Example URL
        print(f"Navigating to {url}...")
        driver.get(url)

        # --- 1. Identify the Elements ---
        # Note: You must adjust these selectors based on the website's structure.
        # Common tags are 'header', 'nav', 'div.banner', etc.
        banner_element = driver.find_element(By.TAG_NAME, "header")

        # We target 'body' for the background, but sometimes a wrapper div is better
        body_element = driver.find_element(By.TAG_NAME, "body")

        # --- 2. Process Colors ---
        print("Analyzing Banner...")
        banner_rgb = get_dominant_color(banner_element)

        print("Analyzing Background...")
        bg_rgb = get_dominant_color(body_element)

        # --- 3. Output ---
        print("-" * 30)
        print_colored_output("Banner Dominant Color", banner_rgb)
        print_colored_output("Background Dominant Color", bg_rgb)
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()