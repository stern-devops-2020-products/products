"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from factory.fuzzy import FuzzyFloat
from factory.fuzzy import FuzzyInteger
from service.models import Product


class ProductFactory(factory.Factory):
    """ Creates fake products """

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    available = FuzzyChoice(choices=[True, False])
    price = FuzzyFloat(0.5, 100.5)
    stock = FuzzyInteger(0, 100)
    size = FuzzyChoice(choices=["L", "M", "S"])
    color = FuzzyChoice(choices=["blue", "yellow", "red"])
    category = FuzzyChoice(choices=["paper", "electronics", "food"])

if __name__ == "__main__":
    for _ in range(10):
        product = ProductFactory()
        print(product.serialize())
