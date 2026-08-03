# SeleniumPython

Small Selenium utility that captures the dominant color of page elements using Selenium + Pillow.

## Project structure

- `conftest.py` — runnable script that opens a Chrome browser, navigates to a site (example: Amazon), screenshots elements and reports their dominant color. Note: This file is named `conftest.py` (a pytest config filename) but currently includes a `main()` entrypoint and can be executed directly.
- `pages/base_page.py` — helper functions to capture and convert element screenshots to dominant RGB/HEX values.
- `debug_error.png` — screenshot saved on error.

## Requirements

- Windows (tested in this workspace)
- Python 3.8+ (this workspace uses Python 3.13)
- Google Chrome (matching ChromeDriver version) or an appropriate WebDriver
- Recommended Python packages: `selenium`, `pillow`, `pytest` (if you run tests)

## Quick setup

Open PowerShell and run (adjust Python path / venv location as needed):

```powershell
# Create a virtual environment (if you don't already have one)
python -m venv .venv
# Activate it
.\.venv\Scripts\Activate.ps1
# Install packages
python -m pip install --upgrade pip
python -m pip install selenium pillow pytest
```

If you prefer a pinned dependency list you can generate one from your working virtualenv and add a `requirements.txt` later:

```powershell
python -m pip freeze > requirements.txt
```

## Running the main script

The primary script is `conftest.py` and has an entrypoint. From the `SeleniumPython` folder run:

```powershell
.\.venv\Scripts\python.exe .\conftest.py
```

Notes:
- The script will open a visible browser by default (the script includes comments about headless mode). If you prefer headless mode edit the options in the file (search for `--headless`) but be aware some sites use anti-bot protections that are easier to trigger in headless mode.
- Because the filename is `conftest.py` (the conventional pytest hook file) running `pytest` in this directory will import it as a test configuration. If you intend to use it as a standalone script and also run pytest in the same folder, consider renaming it (for example `main.py`) to avoid confusion.

## ChromeDriver & browser notes

Selenium requires a browser driver that matches your installed Chrome version. You have a few options:

1. Install a matching ChromeDriver manually:
   - Check your Chrome version (open Chrome -> Help -> About Google Chrome).
   - Download the corresponding `chromedriver.exe` from https://chromedriver.chromium.org/ and put it on your PATH or next to `python.exe`.

2. Use `webdriver-manager` (automates driver download):

```powershell
python -m pip install webdriver-manager
```
Then modify the script to use it (example with Chrome):

```text
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

## Running tests

If you add proper tests you can run:

```powershell
.\.venv\Scripts\pytest.exe -q
```

Be careful: pytest will import any `conftest.py` present in the test discovery tree.

## Troubleshooting

- SessionNotCreatedException / version mismatch: make sure your ChromeDriver matches Chrome.
- "chromedriver.exe" not found: add it to PATH or use `webdriver-manager`.
- Xvfb / headless oddities on CI: when running headless in CI, ensure the browser environment supports headless mode.
- If element screenshots fail or Pillow raises errors, make sure `Pillow` is installed and working.

If you hit an error the script saves a debug screenshot as `debug_error.png` in the project root — inspect that image for clues.

## Contributing

Small project; PRs welcome. If you want help renaming `conftest.py` to a clearer entrypoint or adding a `requirements.txt`, tell me and I can make the change.


