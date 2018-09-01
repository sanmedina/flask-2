from decimal import Decimal
from functools import wraps

from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from my_app import app
from my_app import db
from my_app import redis
from my_app.catalog.models import Category
from my_app.catalog.models import Product

catalog = Blueprint('catalog', __name__)


# Does not work
def template_or_json(template=None):
    '''
    Return a dict from your view and this will either pass it to a template or
    render a json. Use like:

    @template_or_json('template.html')
    '''
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated


@catalog.route('/')
@catalog.route('/home')
# @template_or_json('home.html') # Does not work
def home():
    if request.is_xhr:
        products = Product.query.all()
        return jsonify({
            'count': len(products)
        })
    return render_template('home.html')


# Mongo product
# @catalog.route('/product/<key>')
# def product(key):
#     product = Product.objects.get_or_404(key=key)
# SQL product
@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    # product_key = 'product-{}'.format(product.id)
    # redis.set(product_key, product.name)
    # redis.expire(product_key, 600)
    return render_template('product.html', product=product)


@catalog.route('/products', defaults={'page': 1})
@catalog.route('/products/<int:page>')
def products(page):
    # Mongo product
    # products = Product.objects.all()
    # SQL product
    products = Product.query.paginate(page, 10)
    return render_template('products.html', products=products)
    # res = {}
    # for product in products:
    #     # Mongo product
    #     # res[product.key] = {
    #     # SQL product
    #     res[product.id] = {
    #         'name': product.name,
    #         'price': str(product.price),
    #     }
    # return jsonify(res)


# @catalog.route('/recent-products')
# def recent_products():
#     keys_alive = redis.keys('product-*')
#     products = [redis.get(k) for k in keys_alive]
#     return jsonify({'products': products})


@catalog.route('/product-create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        key = request.form.get('key')
        price = request.form.get('price')
        # Mongo product
        # product = Product(name=name,
        #                   key=key,
        #                   price=Decimal(price))
        # product.save()
        # SQL product
        category_name = request.form.get('category')
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(category_name)
        product = Product(name, price, category)
        db.session.add(product)
        db.session.commit()
        flash('The product {} has been created'.format(name), 'success')
        return redirect(url_for('catalog.product', id=product.id))
    return render_template('product-create.html')


@catalog.route('/category-create', methods=['POST'])
def create_category():
    name = request.form.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return render_template('category.html', category=category)


@catalog.route('/category/<id>')
def category(id):
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)


@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
    # res = {}
    # for category in categories:
    #     res[category.id] = {
    #         'name': category.name,
    #         'products': list(),
    #     }
    #     for product in category.products:
    #         res[category.id]['products'].append({
    #             'id': product.id,
    #             'name': product.name,
    #             'price': product.price,
    #         })
    # return jsonify(res)


@catalog.route('/product-search', defaults={'page': 1})
@catalog.route('/product-search/<int:page>')
def product_search(page):
    name = request.args.get('name')
    price = request.args.get('price')
    company = request.args.get('company')
    category = request.args.get('category')
    products = Product.query
    if name:
        products = products.filter(Product.name.like('%{}%'.format(name)))
    if price:
        products = products.filter(Product.price == price)
    if company:
        products = products.filter(
            Product.company.like('%{}%'.format(company))
        )
    if category:
        products = products.join(Product.category) \
            .filter(Category.name.like('%{}%'.format(category)))
    return render_template('products.html', products=products.paginate(page, 10))
