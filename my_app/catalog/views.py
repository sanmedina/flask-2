import os
from decimal import Decimal
from functools import wraps

from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename

from my_app import ALLOWED_EXTENSIONS
from my_app import app
from my_app import db
from my_app import redis
from my_app.catalog.models import Category
from my_app.catalog.models import Product
from my_app.catalog.models import CategoryForm
from my_app.catalog.models import ProductForm

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


def allowed_file(filename):
    return '.' in filename \
        and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
    form = ProductForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        # Mongo product
        # key = request.form.get('key')
        # product = Product(name=name,
        #                   key=key,
        #                   price=Decimal(price))
        # product.save()
        # SQL product
        category = Category.query.get_or_404(
            form.category.data
        )
        image = request.files['image']
        filename = ''
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product = Product(name, price, category, filename)
        db.session.add(product)
        db.session.commit()
        flash('The product {} has been created'.format(name), 'success')
        return redirect(url_for('catalog.product', id=product.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product-create.html', form=form)


@catalog.route('/category-create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():
        name = form.name.data
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        flash('The category {} has been created'.format(name), 'success')
        return redirect(url_for('catalog.category', id=category.id))
    if form.errors:
        flash(form.errors)
    return render_template('category-create.html', form=form)


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
