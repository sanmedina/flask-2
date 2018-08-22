from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from my_app import db


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Product {}>'.format(self.id)
