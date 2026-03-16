import pytest
from django.urls import reverse
from flashcards.models import Category, Entry
from .factories import CategoryFactory, EntryFactory, UserFactory

@pytest.mark.django_db
def test_category_list_view(client):
    user = UserFactory()
    client.force_login(user)
    # Создаём категории для этого пользователя
    CategoryFactory.create_batch(3, user=user)
    url = reverse('category_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['categories']) == 3

@pytest.mark.django_db
def test_category_detail_view(client):
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    EntryFactory.create_batch(2, category=category)
    url = reverse('category_detail', args=[category.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['category'] == category
    assert len(response.context['entries']) == 2

@pytest.mark.django_db
def test_category_create_view_get(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('category_create')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_category_create_view_post(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('category_create')
    data = {'name': 'Тестовая категория', 'description': 'Описание'}
    response = client.post(url, data)
    assert response.status_code == 302  # редирект после успешного создания
    assert Category.objects.filter(name='Тестовая категория', user=user).exists()

@pytest.mark.django_db
def test_category_update_view(client):
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user, name='Старое название')
    url = reverse('category_update', args=[category.pk])
    data = {'name': 'Новое название', 'description': 'Новое описание'}
    response = client.post(url, data)
    assert response.status_code == 302
    category.refresh_from_db()
    assert category.name == 'Новое название'

@pytest.mark.django_db
def test_category_delete_view(client):
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    url = reverse('category_delete', args=[category.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Category.objects.filter(pk=category.pk).exists()

@pytest.mark.django_db
def test_entry_create_view(client):
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    url = reverse('entry_create', args=[category.pk])
    data = {'term': 'Тестовый термин', 'definition': 'Тестовое определение'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Entry.objects.filter(term='Тестовый термин', category=category).exists()

@pytest.mark.django_db
def test_entry_update_view(client):
    user = UserFactory()
    client.force_login(user)
    entry = EntryFactory(term='Старый термин', category__user=user)
    url = reverse('entry_update', args=[entry.pk])
    data = {'term': 'Новый термин', 'definition': entry.definition}
    response = client.post(url, data)
    assert response.status_code == 302
    entry.refresh_from_db()
    assert entry.term == 'Новый термин'

@pytest.mark.django_db
def test_entry_delete_view(client):
    user = UserFactory()
    client.force_login(user)
    entry = EntryFactory(category__user=user)
    url = reverse('entry_delete', args=[entry.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Entry.objects.filter(pk=entry.pk).exists()

@pytest.mark.django_db
def test_study_view(client):
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    entries = EntryFactory.create_batch(3, category=category)
    url = reverse('study', args=[category.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['category'] == category
    assert len(response.context['entries']) == 3
    assert response.context['current_index'] == 0
    assert response.context['current_entry'] == entries[0]