import json
import logging

import requests
from bs4 import BeautifulSoup


def _parse_page_content(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup


def _get_products_json(soup):
    script = soup.find("script", {"data-product-json": True})
    script_json = json.loads(script.string)
    return script_json


def _search_json_for_product_stock(desired_item_name, products_json):
    in_stock = False

    variants = products_json["variants"]
    for variant in variants:
        if variant["available"]:
            logging.info(f"{variant['title']} available")

            if desired_item_name in variant["title"]:
                in_stock = True
        else:
            logging.info(f"{variant['title']} not available")
    return in_stock


class Topologie:
    url = "https://topologie.com/collections/the-bags/products/flat-sacoche?variant=39841883226172"

    def _get_page_content(self):
        # Send a GET request to the URL
        response = requests.get(self.url)
        return response.content

    def run_inventory_check(self):
        content = self._get_page_content()
        soup = _parse_page_content(content)
        products = _get_products_json(soup)
        in_stock = _search_json_for_product_stock("Moss", products)
        if in_stock:
            return True
