import json
from typing import List, Optional

import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        contents = [products.get_product(item_id) for item_id in json.loads(data['contents'])]
        return Cart(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    products_list = []
    for cart_detail in cart_details:
        # Parse the JSON string safely and fetch the product objects
        item_ids = json.loads(cart_detail['contents'])
        products_list.extend(products.get_product(item_id) for item_id in item_ids)

    return products_list


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
