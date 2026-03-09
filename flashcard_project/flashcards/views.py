from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Deck, Card
from .forms import DeckForm, CardForm

#список колод - главная страница
def deck_list(request):
    decks = Deck.objects.all().order_by('-created_at')  # сортировка: новые сверху
    return render(request, 'flashcards/deck_list.html', {'decks': decks})