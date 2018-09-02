import datetime

from flask_wtf import Form
from mongoengine import DateTimeField
from mongoengine import DecimalField
from mongoengine import StringField
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from wtforms import DecimalField
from wtforms import SelectField
from wtforms import TextField

from my_app import db
# from my_app import db_mongo


# Mongo product
# class Product(db_mongo.Document):
#     created_at = DateTimeField(
#         default=datetime.datetime.now,
#         required=True
#     )
#     key = StringField(max_length=255, required=True)
#     name = StringField(max_length=255, required=True)
#     price = DecimalField()

#     def __repr__(self):
#         return '<Product {}>'.format(self.pk)
# SQL product
class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category',
                            backref=backref('products',
                                            lazy='dynamic'))
    company = Column(String(100))

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return '<Product {}>'.format(self.pk)


class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.id)


class ProductForm(Form):
    name = TextField('Name')
    price = DecimalField('Price')
    category = SelectField('Category', coerce=int)
