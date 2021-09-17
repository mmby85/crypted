from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Message, Certif


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class MessageForm(forms.ModelForm):
    class Meta:

        model = Message
        fields = ('description', 'document', 'sentfrom','sento')

    def excludeid(self, id):
        self['sento'].field.widget.choices.queryset = self['sento'].field.widget.choices.queryset.exclude( username = id)
        return
    



class CeritfForm(forms.ModelForm):
    class Meta:

        model = Certif
        fields = ('user', )