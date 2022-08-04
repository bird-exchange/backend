import factory

from backend.models import Bird


class BirdFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Bird

    uid = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    type = 1
    was_fitted = 0
