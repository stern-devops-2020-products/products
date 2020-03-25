"""
Test cases for Products Model

"""
import logging
import unittest
import os
from service.models import Product, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P R O D U C T S   M O D E L   T E S T   C A S E S
######################################################################
class TestProducts(unittest.TestCase):
    """ Test Cases for Products Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables
        pass

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
        pass

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_create_a_product(self):
        """ Create a product and assert that it exists """
        product = Product(
            name="Test Product",
            sku="00000000",
            price=1.01,
            stock=10,
            size="N/A",
            color="N/A", 
            category="Misc",
            description="This is a test product", 
            available=True
            )
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.sku, "00000000")
        self.assertEqual(product.price, 1.01)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.size, "N/A")
        self.assertEqual(product.color, "N/A")
        self.assertEqual(product.category, "Misc")
        self.assertEqual(product.available, True)

    def test_add_a_product(self):
        """ Create a product and add it to the database """
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(
            name="Test Product",
            sku="00000000",
            price=1.01,
            stock=10,
            size="N/A",
            color="N/A", 
            category="Misc",
            description="This is a test product", 
            available=True
            )
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(product.id, 1)
        products = Product.all()
        self.assertEqual(len(products), 1)