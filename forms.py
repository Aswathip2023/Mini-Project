from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking
from django.forms import ModelForm
from WeddingApp import models


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='', required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        help_texts = {

            'first_name': None,
            'last_name': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ('service', 'date', 'time')
        labels = {
            'service': 'Service:',
            'date': 'Date:',
            'time': 'Time:',
        }

        widgets = {
            'date': DateInput(),
        }

        def clean_data(self):
            date = self.cleaned_data.get('date')
            if date < timezone.now().date():
                raise ValidationError("Date cannot be in the past")
            return self.cleaned_data


