import os
import json
import requests
from pyVinted import Vinted

LOCALE = "it"
MEMBER_ID = "143839772"
OUTPUT_DIR = "vinted_items"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    vinted = Vinted(locale=LOCALE)
    page = 1
    while True:
        print(f"Fetching page {page}...")
        page_items = vinted.items.wardrobe(MEMBER_ID, page=page)
        if not page_items:
            print("No more items found.")
            break
        process_page_items(page, page_items)
        page += 1


def process_page_items(page, page_items):
    print(f"Found {len(page_items)} items on page {page}.")

    for idx, item in enumerate(page_items, 1):
        print(f"  Processing item {idx} on page {page}: {item.title} (ID: {item.id})")
        item_dir = prepare_item_dir(item)
        save_item_json(item, item_dir)
        download_images(item, item_dir)


def download_images(item, item_dir):
    if item.photos and isinstance(item.photos, list):
        for i, photo in enumerate(item.photos):
            photo_url = photo.get("url")
            if photo_url:
                photo_filename = os.path.join(item_dir, f"photo_{i + 1}.jpg")
                print(f"    Downloading photo {i + 1} for item {item.id}...")
                download_image(photo_url, photo_filename)
            else:
                print(f"    No URL for photo {i + 1} of item {item.id}.")
    else:
        print(f"    No photos found for item {item.id}.")


def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def save_item_json(item, item_dir):
    item_json_path = os.path.join(item_dir, f"{item.id}.json")
    with open(item_json_path, "w", encoding="utf-8") as jf:
        json.dump(item.raw_data, jf, ensure_ascii=False, indent=2)


def prepare_item_dir(item):
    item_dir = os.path.join(OUTPUT_DIR, str(item.id))
    os.makedirs(item_dir, exist_ok=True)
    return item_dir


if __name__ == "__main__":
    main()
