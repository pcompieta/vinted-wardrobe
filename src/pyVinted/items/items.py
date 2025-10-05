from pyVinted.items.item import Item
from pyVinted.requester import requester
from urllib.parse import urlparse, parse_qsl
from requests.exceptions import HTTPError
from typing import List, Dict
from pyVinted.vinted_urls import Urls
class Items:

    def wardrobe(self, vinted_site, member_id, nbr_items: int = 20, page: int =1, time: int = None, json: bool = False) -> List[Item]:
        """
        Retrieves items from a given search url on Vinted.

        Args:
            vinted_site (str): The url of the base website, used to extract locale.
            member_id (str): The member id of the wardrobe to be retrieved.
            nbr_items (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).
            time (int): Unix timestamp to filter items listed after this time (default None).
            json (bool): If True, returns raw JSON data instead of Item objects (default False).

        """

        locale = urlparse(vinted_site).netloc
        requester.setLocale(locale)

        params = self.parse_url(vinted_site, nbr_items, page, time)
        wardrobe_endpoint = Urls.VINTED_WARDROBE_ENDPOINT.replace('{member_id}', member_id)
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

        locale = urlparse(url).netloc
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
