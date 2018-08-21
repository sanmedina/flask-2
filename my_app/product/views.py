from flask import Blueprint
from flask import abort
from flask import render_template

from .models import PRODUCTS

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route('/')
@product_blueprint.route('/home')
def home():
    return render_template('home.html', products=PRODUCTS)


@product_blueprint.route('/product/<key>')
def product(key):
    product = PRODUCTS.get(key)
    if not product:
        abort(404)
    return render_template('product.html', product=product)


@product_blueprint.context_processor
def some_processor():
    def full_name(product):
        return '{} / {}'.format(product['category'], product['name'])
    return {'full_name': full_name}


@product_blueprint.app_template_filter('full_name')
def full_name_filter(product):
    return '{} / {}'.format(product['category'], product['name'])
