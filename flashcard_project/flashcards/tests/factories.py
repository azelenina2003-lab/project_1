import factory
from django.contrib.auth.models import User
from flashcards.models import Category, Entry

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return
        # Устанавливаем пароль (в тестах будем использовать 'testpass123')
        obj.set_password('testpass123')
        obj.save()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)

class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    term = factory.Faker('word')
    definition = factory.Faker('sentence')
    category = factory.SubFactory(CategoryFactory)
    correct_count = 0
    wrong_count = 0

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.set_password('testpass123')
        obj.save()  