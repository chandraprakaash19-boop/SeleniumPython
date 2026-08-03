from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import time
import math

# --- 1. Manually Defined Color Dictionary (No External Library Needed) ---
# This maps HEX codes to English names.
COMMON_COLORS = {
    '#000000': 'Black', '#131921': 'Amazon Dark Blue', '#FFFFFF': 'White',
    '#FF0000': 'Red', '#00FF00': 'Lime', '#0000FF': 'Blue', '#FFFF00': 'Yellow',
    '#00FFFF': 'Cyan', '#FF00FF': 'Magenta', '#C0C0C0': 'Silver', '#808080': 'Gray',
    '#800000': 'Maroon', '#808000': 'Olive', '#008000': 'Green', '#800080': 'Purple',
    '#008080': 'Teal', '#000080': 'Navy', '#EAEDED': 'Amazon Light Gray',
    '#232F3E': 'Amazon Light Blue', '#FFA724': 'Amazon Orange',
    '#F0F2F2': 'Light Gray', '#F4F4F4': 'White Smoke'
}


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def get_closest_color_name(requested_rgb):
    """
    Finds the closest color name from our manual dictionary.
    """
    min_distance = float('inf')
    closest_name = None

    for hex_code, name in COMMON_COLORS.items():
        r_c, g_c, b_c = hex_to_rgb(hex_code)
        # Euclidean distance
        distance = math.sqrt(
            (r_c - requested_rgb[0]) ** 2 +
            (g_c - requested_rgb[1]) ** 2 +
            (b_c - requested_rgb[2]) ** 2
        )

        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name


def get_dominant_color(element):
    """
    Screenshots the element and finds the most frequent pixel color.
    """
    try:
        png_data = element.screenshot_as_png
        img = Image.open(io.BytesIO(png_data))
        img = img.resize((50, 50))
        img = img.convert('RGB')

        colors = img.getcolors(maxcolors=2500)
        # Sort by count (descending)
        dominant_rgb = sorted(colors, key=lambda x: x[0], reverse=True)[0][1]
        return dominant_rgb
    except Exception as e:
        print(f"Warning: Could not analyze element color. Reason: {e}")
        return (0, 0, 0)  # Return black on failure


def main():
    options = Options()
    # Run visible to avoid bot detection
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # NOTE: Keep this commented out for Amazon!
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    try:
        url = 'https://www.amazon.com'
        print(f"Navigating to {url}...")
        driver.get(url)

        # 1. Anti-Bot / CAPTCHA Pause
        time.sleep(3)
        if "Type characters" in driver.page_source or "dog" in driver.title.lower():
            print("\n!!! CAPTCHA DETECTED !!!")
            print("Please solve the puzzle in the opened browser window.")
            print("Script paused for 20 seconds...")
            time.sleep(20)

        wait = WebDriverWait(driver, 10)

        # 2. Analyze Banner
        print("Analyzing Banner...")
        banner_element = wait.until(EC.visibility_of_element_located((By.ID, "navbar")))
        banner_rgb = get_dominant_color(banner_element)

        # 3. Analyze Background
        print("Analyzing Background...")
        bg_element = driver.find_element(By.ID, "a-page")
        bg_rgb = get_dominant_color(bg_element)

        # 4. Convert and Print
        banner_name = get_closest_color_name(banner_rgb)
        bg_name = get_closest_color_name(bg_rgb)

        print("\n" + "=" * 40)
        print(f" Amazon Banner Color:     {banner_name}")
        print(f" Amazon Background Color: {bg_name}")
        print("=" * 40 + "\n")

    except Exception as e:
        print(f"\nError encountered: {e}")
        driver.save_screenshot("debug_error.png")
        print("Debug screenshot saved as 'debug_error.png'.")

    finally:
        # Keep window open briefly
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()