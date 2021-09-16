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

from UsersAuth.models import Message, crypto, folder
from UsersAuth.crypt import * 

msg = Message.objects.last()
mp = mdp(16).decode("utf-8")

# mp = msg.password
print(mp)
user = msg.sento 
pubkey = crypto.objects.get( user = user).pubkey 
prvkey = crypto.objects.get( user = user).pvkey 

p = cypherpass(mp, pubkey)
msg.password = p
msg.save()
msg = Message.objects.last()

r = decypherpass(msg.password, prvkey) 
# r = decypherpass(mp, prvkey) 

