from UsersAuth.models import Document, Message
from typing import ContextManager
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY, authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm, DocumentForm, MessageForm


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'UsersAuth/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('/home/')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'UsersAuth/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home1(request):

	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = DocumentForm()

	return render(request,'UsersAuth/dashboard.html',  {'form': form})


@login_required(login_url='login')
def home(request):

	if request.method == 'POST':
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			print(form)
			print(dir(form))
			# form.save()
			recipe = form.save(commit=False)
			recipe.sentfrom = request.user
			recipe.save()
			return redirect('home')
	else:
		form = MessageForm()


	return render(request,'UsersAuth/dashboard.html',  {'form': form })



@login_required(login_url='login')
def reception(request):
	user_id = User.objects.get( username = request.user).id
	msgs = Message.objects.filter(sento = user_id).values_list()

	print(msgs)

	return render(request,'UsersAuth/reception.html',  {'msgs': msgs})