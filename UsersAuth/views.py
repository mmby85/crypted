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
import re
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
import datetime
from .crypt import encrypt, mdp, decrypt, decypherpass, cypherpass
from UsersAuth.certifgen import gen_openssl
# Create your views here.
from .forms import CreateUserForm, MessageForm, CeritfForm, UpFile




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


		# if first time :
	cert = Certif.objects.get( user = request.user)
	if cert.recived == False :
		return redirect("getkey")

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
	filelink = [[i+1, u.sentfrom , u.document.name.replace(folder, "").replace(".enc","") if re.search("_..+$",u.document.name) == None else re.sub("_..+$","",u.document.name).replace(folder, "").replace(".enc",""), u.uploaded_at.strftime("%b %d %Y %H:%M:%S"), u.document.name.replace(folder, "")] for i,u in enumerate(msgs)]
	
	context = {
		'data' : filelink
	}

	return render(request,'UsersAuth/reception.html',  context)


@login_required(login_url='login')
def dload(request):
	context ={'filename':'Error Loading File' }
	try:
		getm = list(request.GET.keys())[0] != None
	except:
		getm = False

	if request.method == "POST" : 
		# try:
			request.FILES['file'].open("w+")
			prvkey = request.FILES['file'].read()
			request.FILES['file'].close()

			msgs = Message.objects.filter(document = folder + request.POST['filepath']).last()
			
			filename = msgs.document.name.replace(folder, "").replace(".enc","")
			if re.search("_..+$",filename) != None :
				filename = re.sub("_..+$","",filename)
				# fileext = re.search("\..+$",filename).group()
			
			pw = msgs.password
			mp = decypherpass(pw,prvkey)

			if mp == "Wrong Key" :
				result = "Wrong Key"
			else:
				result = mp



			context ={'filename':filename , 
			'link': msgs.document.path , 
			"filepath" : list(request.GET.keys())[0], 
			"pw" : str(msgs.password),
			'result' : result,
			"mp" : str(mp.decode('utf-8')),
				}
			
	
			return render(request,'UsersAuth/download.html',  context)

	
	if request.method == "GET" and getm:
		msgs = Message.objects.filter(document = folder + list(request.GET.keys())[0]).last()
		pw = msgs.password
		filename = msgs.document.name.replace(folder, "").replace(".enc","") if re.search("_..+$",msgs.document.name) == None else re.sub("_..+$","",msgs.document.name).replace(folder, "").replace(".enc","")
		context ={'filename':filename , 
				'link': msgs.document.path , 
				"filepath" : list(request.GET.keys())[0], 
				"pw" : str(msgs.password),
		}
		

	return render(request,'UsersAuth/download.html',  context)


@login_required(login_url='login')
def ddecrypt(request):

	if request.method == "GET":

		print(request.GET)
		msgs = Message.objects.filter(document = folder + request.GET['filepath']).last()

		mp = request.GET['mp']
		filename = request.GET['filename']

		print(mp)
		response = HttpResponse( content_type= '', headers={'Content-Disposition': f'attachment; filename={filename}'},)
		decrypted = decrypt(msgs.document.path, mp.encode('utf-8'))
		response.write(decrypted)
	
		return response


	return redirect('download')

@login_required(login_url='login')
def getkey(request):
	cert = Certif.objects.get( user = request.user)
	if cert.recived :
		return redirect("home")

	try:
		if request.method == "GET":
			if request.GET['getkey'] == "ok":
				cert = Certif.objects.get(user = request.user)
				prckey = cert.pvkey
				cert.pvkey = ""
				cert.recived = True
				cert.save()
				
				response = HttpResponse( content_type= 'key', headers={'Content-Disposition': f'attachment; filename=prkey{cert.user.username}.key'},)
				response.write(prckey)

				return response
	except:
		pass
	
	return render(request, 'UsersAuth/getkey.html')
