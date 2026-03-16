import pytest
from flashcards.forms import CategoryForm, EntryForm
from .factories import CategoryFactory, UserFactory

@pytest.mark.django_db
def test_category_form_valid():
    form_data = {'name': 'Новая категория', 'description': 'Описание'}
    form = CategoryForm(data=form_data)
    assert form.is_valid()

def test_category_form_empty_name():
    form_data = {'name': '', 'description': 'Описание'}
    form = CategoryForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors

@pytest.mark.django_db
def test_entry_form_valid():
    user = UserFactory()
    category = CategoryFactory(user=user)
    form_data = {'term': 'Слово', 'definition': 'Определение'}
    form = EntryForm(data=form_data)
    assert form.is_valid()