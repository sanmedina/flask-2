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


if __name__ == '__main__':
    unittest.main()
