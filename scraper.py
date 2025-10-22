import requests
import os
import time
from tqdm import tqdm

BASE_URL = "https://sky-children-of-the-light.fandom.com"
API_URL = BASE_URL + "/api.php"
HEADERS = {"User-Agent": "FandomWikiDumper/1.0"}

OUTPUT_DIR = "sky_wiki_dump"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_all_pages():
    print("Fetching all page titles...")
    pages = []
    apcontinue = None

    while True:
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "aplimit": "max",
        }
        if apcontinue:
            params["apcontinue"] = apcontinue

        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()
        batch = [p["title"] for p in data["query"]["allpages"]]
        pages.extend(batch)

        if "continue" in data:
            apcontinue = data["continue"]["apcontinue"]
        else:
            break

    return pages

def fetch_page_content(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "rvprop": "content",
        "titles": title,
    }
    response = requests.get(API_URL, params=params, headers=HEADERS)
    pages = response.json()["query"]["pages"]
    for page_id, page in pages.items():
        content = page.get("revisions", [{}])[0].get("*", "")
        return content or ""

def save_pages(pages):
    print(f"Saving {len(pages)} pages...")
    for title in tqdm(pages):
        filename = title.replace("/", "_").replace(" ", "_") + ".txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        content = fetch_page_content(title)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        time.sleep(0.2)  # Be kind to the server

def get_all_images():
    print("Fetching all image file URLs...")
    images = []
    aicontinue = None

    while True:
        params = {
            "action": "query",
            "format": "json",
            "list": "allimages",
            "ailimit": "max",
        }
        if aicontinue:
            params["aicontinue"] = aicontinue

        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()
        images.extend([img["url"] for img in data["query"]["allimages"]])

        if "continue" in data:
            aicontinue = data["continue"]["aicontinue"]
        else:
            break

    return images

def download_images(image_urls):
    img_dir = os.path.join(OUTPUT_DIR, "images")
    os.makedirs(img_dir, exist_ok=True)
    print(f"Downloading {len(image_urls)} images...")

    for url in tqdm(image_urls):
        filename = os.path.basename(url).split("?")[0]
        filepath = os.path.join(img_dir, filename)
        if not os.path.exists(filepath):
            response = requests.get(url, headers=HEADERS)
            with open(filepath, "wb") as f:
                f.write(response.content)
        time.sleep(0.2)

if __name__ == "__main__":
    all_pages = get_all_pages()
    save_pages(all_pages)

    download_media = input("Do you want to download all media files? (y/n): ").strip().lower()
    if download_media == "y":
        all_images = get_all_images()
        download_images(all_images)

    print("Done.")
