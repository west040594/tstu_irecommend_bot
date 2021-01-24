from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, NUMERIC, \
    TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    image_url = Column(VARCHAR(512), nullable=True)
    rating = Column(NUMERIC(4, 2), nullable=True)
    link_url = Column(VARCHAR(512), nullable=False)
    reviews = relationship("Review", backref='product', lazy="dynamic")

    def __repr__(self) -> str:
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(1024), nullable=False, unique=True)
    body = Column(TEXT, nullable=True)
    rating = Column(NUMERIC(4, 2), nullable=True)
    post_time = Column(VARCHAR(255), nullable=True)
    reviewer_name = Column(VARCHAR(255), nullable=True)
    read_link = Column(VARCHAR(512), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)

    def __repr__(self) -> str:
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class ProductRequest:
    product_name = None
    url = None

    def __repr__(self) -> str:
        return "Name: " + self.product_name + " Url: " + self.url


