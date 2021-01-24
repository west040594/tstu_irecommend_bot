from db import Session
from models import Product


class ProductService:

    def save(self, product: Product):
        session = Session()
        session.add(product)
        session.commit()

    def find_by_name(self, name: str):
        session = Session()
        product = session.query(Product).filter(Product.name.like(name)).first()
        session.commit()
        return product
