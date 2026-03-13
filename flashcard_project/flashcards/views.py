from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Entry
from .forms import CategoryForm, EntryForm

# иморт представлений для регистрации
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Entry
from .forms import CategoryForm, EntryForm, RegisterForm

#список колод - главная страница
@login_required
def category_list(request):
    categories = Category.objects.all().order_by('-created_at')  # новые сверху
    return render(request, 'flashcards/category_list.html', {'categories': categories})

#Просмотр колоды
@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    entries = category.entries.all()  # thanks to related_name='entries'
    return render(request, 'flashcards/category_detail.html', {
        'category': category,
        'entries': entries
    })
    
# Создание новой колоды
from django.contrib.auth.decorators import login_required

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)  
            category.user = request.user        
            category.save()                     
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'flashcards/category_form.html', {'form': form, 'title': 'Новая категория'})
# Редактирование колоды
@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'flashcards/category_form.html', {'form': form, 'title': 'Редактировать категорию'})

# Удaление колоды
@login_required
def category_delete(request, pk):
   category = get_object_or_404(Category, pk=pk)
   if request.method == 'POST':
        category.delete()
        return redirect('category_list')
   return render(request, 'flashcards/category_confirm_delete.html', {'category': category})

# Создание новой карточки в колоде
@login_required
def entry_create(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.category = category
            entry.save()
            return redirect('category_detail', pk=category.id)
    else:
        form = EntryForm()
    return render(request, 'flashcards/entry_form.html', {'form': form, 'category': category})
 
# Редактирование карточки
@login_required
def entry_update(request, pk):
    entry = get_object_or_404(Entry, pk=pk, category__user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return redirect('category_detail', pk=entry.category.id)
    else:
        form = EntryForm(instance=entry)
    return render(request, 'flashcards/entry_form.html', {'form': form, 'category': entry.category})

# Удаление карточки
@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, category__user=request.user)
    category_id = entry.category.id
    if request.method == 'POST':
        entry.delete()
        return redirect('category_detail', pk=category_id)
    return render(request, 'flashcards/entry_confirm_delete.html', {'entry': entry})

# перелистывание карточек
from django.shortcuts import render, get_object_or_404 
@login_required
def study(request, category_id):
    
    category = get_object_or_404(Category, pk=category_id, user=request.user)    
    entries = list(category.entries.all())  # все записи категории в виде списка

    try:
        current_index = int(request.GET.get('index', 0))
    except ValueError:
        current_index = 0

    # Корректировка индекса
    if current_index < 0:
        current_index = 0
    if entries and current_index >= len(entries):
        current_index = len(entries) - 1

    show_definition = request.GET.get('show', 'false') == 'true'

    current_entry = entries[current_index] if entries else None

    context = {
        'category': category,
        'entries': entries,
        'current_index': current_index,
        'current_entry': current_entry,
        'show_definition': show_definition,
        'total': len(entries),
    }
    return render(request, 'flashcards/study.html', context)

# Аутентификация пользователя

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('category_list')
    else:
        form = RegisterForm()
    return render(request, 'flashcards/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category_list')
    else:
        form = AuthenticationForm()
    return render(request, 'flashcards/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

