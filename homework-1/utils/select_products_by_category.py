from models.product import Product

def select_products_by_category(products: list[Product], category: str) -> list[Product]:
    needed_products = []
    for product in products:
        if product.category == category:
            needed_products.append(product)
    return needed_products