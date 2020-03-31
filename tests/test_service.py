
"""
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_service.py:TestProductServer
"""

import os
import logging
from unittest import TestCase
from flask_api import status  # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import Product, DataValidationError, db
from .product_factory import ProductFactory
from service.service import app, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(TestCase):
    """ Product Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        """ Factory method to create products in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post(
                "/products", json=test_product.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

######################################################################
#  I N D E X   T E S T   C A S E  
######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Product REST API Service")

######################################################################
#  C R E A TE   T E S T   C A S E  
######################################################################
    
    def test_create_product(self):
        """ Create a new Product """
        test_product = {    
            "name": "Test Product",
            "sku": "00000000",
            "price": 1.01,
            "stock": 10,
            "size": "N/A",
            "color": "N/A",
            "category": "Misc",
            "description": "This is a test product",
            "available": True
        }
        #test_product = ProductFactory()
        resp = self.app.post(
            "/products", 
            json=test_product, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        
        # Check the data is correct
        new_product = resp.get_json()
        self.assertEqual(new_product["name"], test_product["name"], "Names do not match")
        self.assertEqual(new_product["sku"], test_product["sku"], "SKUs do not match")
        self.assertEqual(new_product["price"], test_product["price"], "Prices do not match")
        self.assertEqual(new_product["stock"], test_product["stock"], "Stock count does not match")
        self.assertEqual(new_product["size"], test_product["size"], "Sizes do not match")
        self.assertEqual(new_product["color"], test_product["color"], "Colors do not match")
        self.assertEqual(new_product["category"], test_product["category"], "Categories do not match")
        self.assertEqual(new_product["description"], test_product["description"], "Description does not match")
        self.assertEqual(new_product["available"], test_product["available"], "Availability does not match")
                
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        self.assertEqual(new_product["name"], test_product["name"], "Names do not match")
        self.assertEqual(new_product["sku"], test_product["sku"], "SKUs do not match")
        self.assertEqual(new_product["price"], test_product["price"], "Prices do not match")
        self.assertEqual(new_product["stock"], test_product["stock"], "Stock count does not match")
        self.assertEqual(new_product["size"], test_product["size"], "Sizes do not match")
        self.assertEqual(new_product["color"], test_product["color"], "Colors do not match")
        self.assertEqual(new_product["category"], test_product["category"], "Categories do not match")
        self.assertEqual(new_product["description"], test_product["description"], "Description does not match")
        self.assertEqual(new_product["available"], test_product["available"], "Availability does not match")

######################################################################
#  G E T   T E S T   C A S E  
######################################################################
    def test_get_product_list(self):
        """ Get a list of Products """
        self._create_products(5)
        resp = self.app.get("/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product(self):
        """ Get a single Product """
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get("/products/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
#  U P D A T E   P R O D U C T   T E S T   C A S E  
######################################################################
    def test_update_product(self):
        """ Update an existing Product """
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post(
            "/products", json=test_product.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        logging.debug(new_product)
        new_product["category"] = "unknown"
        resp = self.app.put(
            "/products/{}".format(new_product["id"]),
            json=new_product,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["category"], "unknown")

######################################################################
#  D E L E T E   T E S T   C A S E  
######################################################################
    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete(
            "/products/{}".format(test_product.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)