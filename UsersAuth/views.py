from UsersAuth.models import Message, Certif, folder
from typing import ContextManager
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY, authenticate, login, logout
import io
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
import datetime
from .crypt import encrypt, mdp, decrypt, decypherpass, cypherpass
from UsersAuth.certifgen import gen_openssl
# Create your views here.
from .forms import CreateUserForm, MessageForm, CeritfForm

@login_required(login_url='login')
def adminpage(request):

	try:
		adduser = request.POST['adduser'] == "True"
	except:
		adduser = False



	if request.user.is_superuser :
		if request.method == "POST" and adduser  :
			try:
				tempuser = User.objects.create(username= request.POST['username'],email= request.POST['email'] )
				tempuser.set_password(request.POST['password'])
				tempuser.save()

				
				cert , key , pkey = gen_openssl()
				tempcrypt = Certif.objects.create(user  = User.objects.get(id = tempuser.id  ))
				cert , key , pkey = gen_openssl()

				file = io.BytesIO()
				file.write(cert)

				tempcrypt.certif.save(f"certificate_{tempuser.username}.cert", file)
				tempcrypt.pvkey = key.decode("utf-8")
				tempcrypt.pubkey = pkey.decode("utf-8")
				tempcrypt.save()
			except:
				return redirect('adminpage')

			return redirect('adminpage')

		else:
			form = CreateUserForm()
			certif = CeritfForm()

		return render(request,'UsersAuth/admin.html', context={ "certif":certif})
	else :
		return redirect('home')

def loginPage(request):
	if request.user.is_superuser :
		return redirect('/adminpage/')
	elif request.user.is_authenticated:
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
def home(request):
	if request.user.is_superuser :
		return redirect('/adminpage/')
	if request.method == 'POST':
		form = MessageForm(request.POST, request.FILES)
		if form.is_valid():
			# encrypt(request.FILES['document'],mdp(16))
			# fencrypt = request.FILES['document'].name
			# form.save()
			recipe = form.save(commit=False)
			recipe.sentfrom = request.user

			request.FILES['document'].open('w+')
			text = request.FILES['document'].read()

			mp = mdp(16)
			text = encrypt(text,mp)
			request.FILES['document'].seek(0)
			request.FILES['document'].write(text)
			request.FILES['document'].name = request.FILES['document'].name + ".enc"


			instance = Message(document = request.FILES['document'], password = mp )
			
			recipe.document = instance.document
			pubkey = Certif.objects.get( user = recipe.sento).pubkey
			recipe.password = cypherpass(mp, pubkey)

			recipe.save()
			# mp = mdp(16)
			# encrypt(fencrypt,mp)
			f = open('pass.txt', 'w')
			f.write(str(mp))
			f.close()
			return redirect('home')
	else:
		form = MessageForm()
		form.excludeid(request.user.username)



	return render(request,'UsersAuth/dashboard.html',  {'form': form })



@login_required(login_url='login')
def reception(request):
	user_id = User.objects.get( username = request.user).id
	msgs = Message.objects.filter(sento = user_id)
	
	filelink = [[i+1, u.sentfrom , u.document.name.replace(folder, ""), u.uploaded_at.strftime("%b %d %Y %H:%M:%S"), u.document.name.replace(folder, "")] for i,u in enumerate(msgs)]
	
	context = {
		'data' : filelink
	}

	return render(request,'UsersAuth/reception.html',  context)


@login_required(login_url='login')
def dload(request):
	if request.method == "GET":
		# print(list(request.GET.keys())[0])
		msgs = Message.objects.get(document = folder + list(request.GET.keys())[0])
		# with open(msgs.document.name.replace(folder, "").replace("enc", "")) as f:
		# 	f.write("hello")
		file = io.BytesIO()
		# from tkinter import filedialog
		# filename = filedialog.askopenfilename()
		from django.http import HttpResponse
		import re
		import csv
		# with open(filename + msgs.document.name.replace(folder, "").replace("enc", "") , "wb") as f:
		# 	f.write(b'hello')
		prvkey = Certif.objects.get( user = msgs.sento).pvkey
		# obj = Message.objects.get(document = folder + list(request.GET.keys())[0])
		# filename = obj.document.path
		# file.write(msgs.document.read())
		# FileResponse(file.getbuffer())
		filename = msgs.document.name.replace(folder, "").replace(".enc", "")
		fileext = re.search("\..+$",filename).group()
		print(msgs.password)
		mp = decypherpass(msgs.password,prvkey)
		
		response = HttpResponse( content_type=f'{fileext}', headers={'Content-Disposition': f'attachment; filename={filename}'},)
		decrypted = decrypt(msgs.document.path, mp)
		# file.write(decrypted)
		response.write(decrypted)

		return response
		
		


		pass

	# user_id = User.objects.get( username = request.user).id
	# msgs = Message.objects.filter(sento = user_id)
	
	# filelink = [[i+1, u.sentfrom , u.document.name, u.uploaded_at.strftime("%b %d %Y %H:%M:%S")] for i,u in enumerate(msgs)]
	
	# context = {
	# 	'data' : filelink
	# }

	return render(request,'UsersAuth/download.html')#,  context)