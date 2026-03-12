import factory
from flashcards.models import Category, Entry

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    description = factory.Faker('sentence')

class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    term = factory.Faker('word')
    definition = factory.Faker('sentence')
    category = factory.SubFactory(CategoryFactory)