import json 
from products import Product, get_products  # Assuming get_products can handle batch requests
from cart import dao

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        # Load contents as product IDs directly
        contents = [data['contents']]  # If contents is a list of IDs
        return Cart(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Collect all unique product IDs from all cart details
    all_product_ids = set()  # Use a set to avoid duplicates
    for cart_detail in cart_details:
        all_product_ids.update(cart_detail['contents'])  # assuming contents is a list of product IDs

    # Fetch all products in a single batch query
    products = get_products(list(all_product_ids))  # Assume get_products takes a list of IDs and returns them
   
    # Map product IDs to their corresponding product objects
    product_map = {product.id: product for product in products}

    # For each cart_detail, convert product IDs into actual products
    all_products = []
    for cart_detail in cart_details:
        products_in_cart = [product_map[product_id] for product_id in cart_detail['contents']]
        all_products.extend(products_in_cart)

    return all_products


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
