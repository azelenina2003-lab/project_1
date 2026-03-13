from django import forms
from .models import Category, Entry

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Entry

# форма для колоды
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

# форма для карточки

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['term', 'definition']

# форма для регистрации
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
