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


from .crypt import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

cert, kpv , kpp = gen_openssl()

pbkey = crypto.load_publickey(crypto.FILETYPE_PEM,kpp)      

pbkey1 = RSA.import_key(kpp) 

# Encrypt the session key with the public RSA key

encryptor = PKCS1_OAEP.new(pbkey1)
encrypted = encryptor.encrypt(mp.encode("utf-8"))
#resulted encryption end encryption
tt = binascii.hexlify(encrypted).decode('UTF-8')


pvkey1 = RSA.import_key(kpv.decode('utf-8'))
decryptor = PKCS1_OAEP.new(pvkey1)
decrypted = decryptor.decrypt(encrypted)
decrypted.encode("utf-8")


from UsersAuth.crypt import encrypt, mdp, decrypt, decypherpass, cypherpass 
from UsersAuth.models import Message, crypto, folder
msg = Message.objects.last()
mp = mdp(16).decode("utf-8")
print(mp)
user = msg.sento 
pubkey = crypto.objects.get( user = user).pubkey 
prvkey = crypto.objects.get( user = user).pvkey 

p = cypherpass(mp, pubkey)
r = decypherpass(p, prvkey) 
