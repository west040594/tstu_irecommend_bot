from sqlalchemy import MetaData, create_engine, Column, Table, Integer, VARCHAR, NUMERIC, TEXT, ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://west223:westwest223@localhost:5432/productdb', echo=True)
Session = sessionmaker(bind=engine)
meta = MetaData()

products = Table(
    'products', meta,
    Column('id', Integer, nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('name', VARCHAR(255), nullable=False, unique=True),
    Column('image_url', VARCHAR(512), nullable=True),
    Column('rating', NUMERIC(4, 2), nullable=True),
    Column('link_url', VARCHAR(512), nullable=False),
)

reviews = Table(
    'reviews', meta,
    Column('id', Integer, nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('title', VARCHAR(1024), nullable=False, unique=True),
    Column('body', TEXT, nullable=True),
    Column('rating', NUMERIC(4, 2), nullable=True),
    Column('post_time', VARCHAR(255), nullable=True),
    Column('reviewer_name', VARCHAR(255), nullable=True),
    Column('read_link', VARCHAR(512), nullable=True),
    Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True),
)


def create_tables():
    meta.create_all(engine)
