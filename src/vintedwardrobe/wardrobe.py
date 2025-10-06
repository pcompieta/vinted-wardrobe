import json
import os
from typing import List, Dict
from urllib.parse import urlparse, parse_qsl

from requests import get
from requests.exceptions import HTTPError

from vintedwardrobe.item import Item
from vintedwardrobe.requester import requester
from vintedwardrobe.vinted_urls import Urls


class Wardrobe:

    def __init__(self, locale=None):
        self.locale = locale


    def dump(self, member_id) -> List[Item]:
        """
        Retrieves all items from a given wardrobe on Vinted.

        Args:
            member_id (str): The member id of the wardrobe to be retrieved.

        """

        all_items = []
        page = 1
        while True:
            print(f"Fetching page {page}...")
            page_items = self.fetch_items(member_id, page=page)
            if not page_items:
                print("Items list exhausted.")
                break
            all_items.extend(page_items)
            page += 1

        return all_items


    def fetch_items(self, member_id, nbr_items: int = 20, page: int =1, time: int = None, json_raw: bool = False) -> List[Item]:
        """
        Retrieves items from a given search url on Vinted.

        Args:
            member_id (str): The member id of the wardrobe to be retrieved.
            nbr_items (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).
            time (int): Unix timestamp to filter items listed after this time (default None).
            json_raw (bool): If True, returns raw JSON data instead of Item objects (default False).

        """

        locale = Urls.VINTED_BASE_URL.format(locale=self.locale)
        requester.setLocale(locale)

        params = self.parse_url("www.vinted.unused", nbr_items, page, time)
        wardrobe_endpoint = Urls.VINTED_WARDROBE_ENDPOINT.format(member_id=member_id)
        vinted_site = f"https://{locale}{Urls.VINTED_API_URL}/{wardrobe_endpoint}"

        try:
            response = requester.get(url=vinted_site, params=params)
            response.raise_for_status()
            items = response.json()
            items = items["items"]
            if not json_raw:
                return [Item(_item) for _item in items]
            else:
                return items

        except HTTPError as err:
            raise err


    @staticmethod
    def parse_url(url, nbr_items=20, page=1, time=None) -> Dict:
        """
        Parse Vinted search url to get parameters the for api call.

        Args:
            url (str): The url of the research on vinted.
            nbr_items (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).
            time (int): Unix timestamp to filter items listed after this time (default None).

        """
        queries = parse_qsl(urlparse(url).query)

        params = {
            "search_text": "+".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "search_text"])
            ),
            "catalog_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "catalog[]"])
            ),
            "color_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "color_ids[]"])
            ),
            "brand_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "brand_ids[]"])
            ),
            "size_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "size_ids[]"])
            ),
            "material_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "material_ids[]"])
            ),
            "status_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "status[]"])
            ),
            "country_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "country_ids[]"])
            ),
            "city_ids": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "city_ids[]"])
            ),
            "is_for_swap": ",".join(
                map(str, [1 for tpl in queries if tpl[0] == "disposal[]"])
            ),
            "currency": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "currency"])
            ),
            "price_to": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "price_to"])
            ),
            "price_from": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "price_from"])
            ),
            "page": page,
            "per_page": nbr_items,
            "order": ",".join(
                map(str, [tpl[1] for tpl in queries if tpl[0] == "order"])
            ),
            "time": time
        }

        return params


def download_images_to_folders(item, item_dir):
    if item.photos and isinstance(item.photos, list):
        for i, photo in enumerate(item.photos):
            photo_url = photo.get("url")
            if photo_url:
                photo_filename = os.path.join(item_dir, f"photo_{i + 1}.jpg")
                print(f"    Downloading photo {i + 1} for item {item.id}...")
                download_image_to_folder(photo_url, photo_filename)
            else:
                print(f"    No URL for photo {i + 1} of item {item.id}.")
    else:
        print(f"    No photos found for item {item.id}.")


def download_image_to_folder(url, path):
    try:
        response = get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def save_item_json_to_folder(item, item_dir):
    item_json_path = os.path.join(item_dir, f"{item.id}.json")
    with open(item_json_path, "w", encoding="utf-8") as jf:
        json.dump(item.raw_data, jf, ensure_ascii=False, indent=2)
