"""
Test cases for Products Model

"""
import logging
import unittest
import os
from service.models import Product, DataValidationError, db
from werkzeug.exceptions import NotFound
from service import app
from .product_factory import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']
    
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
# C R E A T E  T E S T   C A S E S
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

######################################################################
# P U T  T E S T   C A S E S
######################################################################

    def test_update_a_product(self):
        """ Update a Product """
        product = Product()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertEqual(product.id, 1)
        # Change it and save it
        product.category = "Shoes"
        original_id = product.id
        product.save()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.category, "Shoes")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].category, "Shoes")

    def test_restock_a_product(self):
        """ Restock a Product """
        products = ProductFactory.create_batch(1)
        for product in products:
            product.create()

        products[0].available = False
        products[0].stock = 0
        product.save()
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].stock, 0)
        self.assertEqual(products[0].available, False)
        product.restock(100)
        product.save()
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].stock, 100)
        self.assertEqual(products[0].available, True)

######################################################################
# G E T  T E S T   C A S E S
######################################################################
    def test_find_product(self):
        """ Find a Product by ID """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 3)
        # find the 2nd product in the list
        test_product = Product.find(products[1].id)
        self.assertIsNot(test_product, None)
        self.assertEqual(test_product.id, products[1].id)
        self.assertEqual(test_product.name, products[1].name)
        self.assertEqual(test_product.available, products[1].available)
        self.assertEqual(test_product.sku, products[1].sku)
        self.assertEqual(test_product.price, products[1].price)
        self.assertEqual(test_product.stock, products[1].stock)
        self.assertEqual(test_product.size, products[1].size)
        self.assertEqual(test_product.color, products[1].color)
        self.assertEqual(test_product.category, products[1].category)

    def test_find_by_category(self):
        """ Find Products by Category """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        category = products[0].category
        test_products = Product.find_by_category(category)
        self.assertEqual(test_products[0].category, category)
        self.assertIsNot(test_products[0].category, "kitty")
        self.assertEqual(test_products[0].id, products[0].id)
        
    def test_find_by_name(self):
        """ Find a Product by Name """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        name = products[0].name
        test_products = Product.find_by_name(name)
        self.assertEqual(test_products[0].name, name)
        self.assertIsNot(test_products[0].name, "KEVIN")
        self.assertEqual(test_products[0].id, products[0].id)

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.available, products[1].available)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Product.find_or_404, 0)