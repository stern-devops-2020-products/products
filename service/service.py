"""
Products Service

Paths:
------
GET /products - Returns a list all of the products
GET /products/{id} - Returns the product with a given id number
POST /products - creates a new product record in the database
PUT /products/{id} - updates a product record in the database
DELETE /products/{id} - deletes a product record in the database
"""


from flask import jsonify, request, url_for, make_response
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound
from service.models import Product  # , DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="Product REST API Service",
            version="1.0",
            paths=url_for("list_products", _external=True),
        ),
        status.HTTP_200_OK,
    )
######################################################################
# LIST ALL products
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """ Returns all of the Products """
    app.logger.info("Request for Product list")
    products = []
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A PRODUCT
######################################################################

######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """
    Creates a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    #location_url = url_for("get_products", product_id=product.id, _external=True)
    location_url = "not yet implemented - story #7"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################

######################################################################
# DELETE A PRODUCT
######################################################################

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))