from flask import Blueprint
from flask import jsonify
from flask import request

from my_app import app
from my_app import db
from my_app import redis
from my_app.catalog.models import Category
from my_app.catalog.models import Product

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."


@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    product_key = 'product-{}'.format(product.id)
    redis.set(product_key, product.name)
    redis.expire(product_key, 600)
    return 'Product - {}, ${}'.format(product.name, product.price)


@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price),
        }
    return jsonify(res)

@catalog.route('/recent-products')
def recent_products():
    keys_alive = redis.keys('product-*')
    products = [redis.get(k) for k in keys_alive]
    return jsonify({'products': products})

@catalog.route('/product-create', methods=['POST'])
def create_product():
    name = request.form.get('name')
    price = request.form.get('price')
    category_name = request.form.get('category')
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(category_name)
    product = Product(name, price, category)
    db.session.add(product)
    db.session.commit()
    return 'Product crreate.'


@catalog.route('/category-create', methods=['POST'])
def create_category():
    name = request.form.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return 'Category created'


@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    res = {}
    for category in categories:
        res[category.id] = {
            'name': category.name,
            'products': list(),
        }
        for product in category.products:
            res[category.id]['products'].append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
            })
    return jsonify(res)
