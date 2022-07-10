import factory

from backend.models import Image


class ImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Image

    uid = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    type = 1
    was_fitted = 0
