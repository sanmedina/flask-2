import os
import unittest
import tempfile

from my_app import app, db


class CatalogTestCase(unittest.TestCase):
    def setUp(self):
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            self.test_db_file
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.remove(self.test_db_file)

    def test_home(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_products(self):
        "Test Products list page"
        rv = self.app.get('/products')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'No previous page' in rv.data)
        self.assertTrue(b'No next page' in rv.data)

    def test_create_category(self):
        "Test creation of new category"
        rv = self.app.get('/category-create')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.post('/category-create')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'This field is required.' in rv.data)

        rv = self.app.get('/categories')
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(b'Phones' in rv.data)

        rv = self.app.post('/category-create', data={
            'name': 'Phones',
        })
        self.assertEqual(rv.status_code, 302)

        rv = self.app.get('/categories')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'Phones' in rv.data)

        rv = self.app.get('/category/1')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'Phones' in rv.data)

    def test_create_product(self):
        "Test creation of new product"
        rv = self.app.get('/product-create')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.post('/product-create')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'This field is required.' in rv.data)

        # Create a category to be used in product creation
        rv = self.app.post('/category-create', data={
            'name': 'Phones',
        })
        self.assertEqual(rv.status_code, 302)

        rv = self.app.post('/product-create', data={
            'name': 'iPhone 5',
            'price': 549.49,
            'company': 'Apple',
            'category': 1
        })
        self.assertEqual(rv.status_code, 302)

        rv = self.app.get('/products')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'iPhone 5' in rv.data)

    def test_search_product(self):
        "Test searching product"
        # Create a category to be used in product creation
        rv = self.app.post('/category-create', data={
            'name': 'Phones',
        })
        self.assertEqual(rv.status_code, 302)

        # Create a product
        rv = self.app.post('/product-create', data={
            'name': 'iPhone 5',
            'price': 549.49,
            'company': 'Apple',
            'category': 1
        })
        self.assertEqual(rv.status_code, 302)

        # Create another product
        rv = self.app.post('/product-create', data={
            'name': 'Galaxy S5',
            'price': 549.49,
            'company': 'Samsung',
            'category': 1
        })
        self.assertEqual(rv.status_code, 302)

        self.app.get('/')

        rv = self.app.get('/product-search?name=iPhone')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'iPhone 5' in rv.data)
        self.assertFalse(b'Galaxy S5' in rv.data)

        rv = self.app.get('/product-search?name=iPhone 6')
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(b'iPhone 6' in rv.data)


if __name__ == '__main__':
    unittest.main()
