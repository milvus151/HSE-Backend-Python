from models.product import Product

def get_ordered_products_by_price(products: list[Product]) -> list[Product]:
    products_ordered = products[:]
    products_ordered.sort(key=lambda p: p.price, reverse=True)
    return products_ordered
