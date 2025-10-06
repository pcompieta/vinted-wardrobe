import os
from vintedwardrobe import Vinted
from vintedwardrobe.wardrobe import save_item_json_to_folder, download_images_to_folders

LOCALE = "it"
MEMBER_ID = "143839772"
OUTPUT_DIR = "vinted_items"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    vinted = Vinted(locale=LOCALE)
    items = vinted.wardrobe.wardrobe_all(MEMBER_ID)
    print(f"Found {len(items)} items in wardrobe {MEMBER_ID}.")

    for idx, item in enumerate(items, 1):
        print(f"  Processing item {idx}: {item.title} (ID: {item.id})")
        item_dir = prepare_item_dir(item)
        save_item_json_to_folder(item, item_dir)
        download_images_to_folders(item, item_dir)


def prepare_item_dir(item):
    item_dir = os.path.join(OUTPUT_DIR, str(item.id))
    os.makedirs(item_dir, exist_ok=True)
    return item_dir


if __name__ == "__main__":
    main()
