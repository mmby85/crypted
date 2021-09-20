# from django.test import TestCase

# Create your tests here.
from UsersAuth.models import *
import io
from UsersAuth.certifgen import gen_openssl


cert , key , pkey = gen_openssl()
file = io.BytesIO()
file.write(cert)

with open("test.txt", "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(file.getvalue())

from tkinter import filedialog
# examples:

filename = filedialog.askopenfilename()
print filename  # test


from random import *
from types import new_class
from OpenSSL import crypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from base64 import b64decode, b64encode
import base64
from UsersAuth.certifgen import *
import getpass


cert, kpv , kpp = gen_openssl()

pbkey = crypto.load_publickey(crypto.FILETYPE_PEM,kpp)      

pbkey1 = RSA.import_key(kpp) 
mp = "Helloooooo0000000000000000000000000000000000000000000000000000000000000000000000000000000000o"
# Encrypt the session key with the public RSA key

encryptor = PKCS1_OAEP.new(pbkey1)
encrypted = encryptor.encrypt(mp*100.encode("utf-8"))
#resulted encryption end encryption
tt = binascii.hexlify(encrypted).decode('UTF-8')


pvkey1 = RSA.import_key(kpv.decode('utf-8'))
decryptor = PKCS1_OAEP.new(pvkey1)
decrypted = decryptor.decrypt(encrypted)
decrypted

from django.contrib.auth.models import User
from UsersAuth.models import Message, Certif, folder
from UsersAuth.crypt import * 
from UsersAuth.certifgen import *

msg = Message.objects.last()
mp = mdp(16).decode("utf-8")

# mp = msg.password
print(mp)
user = msg.sento 
pubkey = Certif.objects.get( user = user).pubkey 
prvkey = Certif.objects.get( user = user).pvkey 

p = cypherpass(mp, pubkey)
msg.password = p
msg.save()
msg = Message.objects.last()

r = decypherpass(msg.password, prvkey) 
# r = decypherpass(mp, prvkey) 

from django.contrib.auth.models import User
from UsersAuth.models import Message, Certif, folder
from UsersAuth.crypt import * 
from UsersAuth.certifgen import *
import io

tempuser = User.objects.create(username= "kol",email= "" )
tempuser.set_password("123")
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

import os
import re

m = Message.objects.create(sento_id = 2,sentfrom = "anas")
m.document = my_file
m.document.name    
cur_list = os.listdir(''.join([os.getcwd(), '\\static\\documents\\']) ) 
if m.document.name in cur_list:
        print("it exists")
        m.document.name = re.sub( '\..*$',  , m.document.name )

fext = re.search('\..*$',  m.document.name ).group()
m.document.name[:-(len(fext))] + str(m.uploaded_at) + fext

# m.save()  