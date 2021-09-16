from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Message, crypto


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class MessageForm(forms.ModelForm):
    class Meta:

        model = Message
        fields = ('sento','description', 'document', 'sentfrom')


class CeritfForm(forms.ModelForm):
    class Meta:

        model = crypto
        fields = ('user', )