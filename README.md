# ADOBE LIGHTROOM GALLERY DOWNLOAD SCRIPT
Easily download all images from a single or multiple Adobe Lightroom Share galleries. By default Adobe Lightroom Shares do not allow user to download images without inspecting source and finding image resources directly. This script will automatially download all large size (2048px rendition) images in a given Share/Album. 

## Requirements
- Python 3.X
- Google Chrome
- Google Chrome [chromewebdriver](https://chromedriver.chromium.org/downloads)

## How to use
Intall required dependencies
```bash
pip3 -r requirements.txt
```
Run script
```bash
python3 download.py
```

## Configure Settings
Set URLS and DRIVER variables at the top of the script.
- URLS: Dictionary that needs valid Adobe Lightroom url endpoints.
- DRIVER: Valid path to local version of chromewebdriver