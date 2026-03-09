from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

class Deck(models.Model):
    """Колода карточек"""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Колода'
        verbose_name_plural = 'Колоды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])


class Card(models.Model):
    """Карточка: термин и определение"""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards', verbose_name='Колода')
    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return f'{self.term} - {self.deck.name}'