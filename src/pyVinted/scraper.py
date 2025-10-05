from pyVinted.item import Item
from pyVinted.requester import requester
from urllib.parse import urlparse, parse_qsl
from requests.exceptions import HTTPError
from typing import List, Dict
from pyVinted.vinted_urls import Urls
class Scraper:

    def __init__(self, locale=None):
        self.locale = locale


    def wardrobe_all(self, member_id) -> List[Item]:
        """
        Retrieves all items from a given wardrobe on Vinted.

        Args:
            member_id (str): The member id of the wardrobe to be retrieved.

        """

        all_items = []
        page = 1
        while True:
            print(f"Fetching page {page}...")
            page_items = self.wardrobe(member_id, page=page)
            if not page_items:
                print("Items list exhausted.")
                break
            all_items.extend(page_items)
            page += 1

        return all_items


    def wardrobe(self, member_id, nbr_items: int = 20, page: int =1, time: int = None, json: bool = False) -> List[Item]:
        """
        Retrieves items from a given search url on Vinted.

        Args:
            member_id (str): The member id of the wardrobe to be retrieved.
            nbr_items (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).
            time (int): Unix timestamp to filter items listed after this time (default None).
            json (bool): If True, returns raw JSON data instead of Item objects (default False).

        """

        locale = Urls.VINTED_BASE_URL.format(locale=self.locale)
        requester.setLocale(locale)

        params = self.parse_url("www.vinted.unused", nbr_items, page, time)
        wardrobe_endpoint = Urls.VINTED_WARDROBE_ENDPOINT.format(member_id=member_id)
        vinted_site = f"https://{locale}{Urls.VINTED_API_URL}/{wardrobe_endpoint}"

        return self.fetch_items(json, params, vinted_site)


    def search(self, url, nbr_items: int = 20, page: int =1, time: int = None, json: bool = False) -> List[Item]:
        """
        Retrieves items from a given search url on Vinted.

        Args:
            url (str): The url of the research on vinted.
            nbr_items (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).
            time (int): Unix timestamp to filter items listed after this time (default None).
            json (bool): If True, returns raw JSON data instead of Item objects (default False).

        """

        locale = self.locale or urlparse(url).netloc
        requester.setLocale(locale)

        params = self.parse_url(url, nbr_items, page, time)
        #url = f"{Urls.VINTED_API_URL}/{Urls.VINTED_PRODUCTS_ENDPOINT}"
        url = f"https://{locale}{Urls.VINTED_API_URL}/{Urls.VINTED_PRODUCTS_ENDPOINT}"

        return self.fetch_items(json, params, url)


    @staticmethod
    def fetch_items(json, params, vinted_site):
        try:
            response = requester.get(url=vinted_site, params=params)
            response.raise_for_status()
            items = response.json()
            items = items["items"]
            if not json:
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
