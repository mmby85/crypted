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

import getpass

try:
    from .models import folder
except:
    pass
import os

caractere=['q','w','e','r','t','y','u','i','o','p','[',']','a','s','d','f','g','h','j','k','l',';','z','x','c','v','b','n','m','.','/','1','2','3','4','5','6','7','8','9','0','-','=','*','+','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

def mdp(longueur):
    mdp=str()
    shuffle(caractere)
    for x in range(longueur):
        mdp+=caractere[x]
    return mdp.encode('utf-8')


def encrypt (file_name,key):
   
    data = file_name
    cipher = AES.new(key,AES.MODE_CFB)
    ciphertext = cipher.encrypt(pad(data,AES.block_size))
    iv = b64encode(cipher.iv).decode('UTF-8')
    ciphertext = b64encode(ciphertext).decode('UTF-8')
    to_write = iv + ciphertext
    return to_write.encode('utf-8')

def decrypt(file_name,key):
    with open(file_name,'r') as entry:
        try:
            data = entry.read()
            length = len(data)
            iv = data[:24]
            iv = b64decode(iv)
            ciphertext = data[24:length]
            ciphertext = b64decode(ciphertext)
            cipher = AES.new(key,AES.MODE_CFB,iv)
            decrypted = cipher.decrypt(ciphertext)
            decrypted = unpad(decrypted,AES.block_size)
            # print(decrypted)
            return decrypted
        except:
            print("wrong password")

def cypherpass(mp , key):
    

    pbkey1 = RSA.import_key(key) 

    encryptor = PKCS1_OAEP.new(pbkey1)
    if type(mp) == str:
        mp = mp.encode("utf-8")

    encrypted = encryptor.encrypt(mp)#.encode("utf-8"))
    
    return binascii.hexlify(encrypted).decode('UTF-8')


def decypherpass(mp , key):
    try:
        data = binascii.unhexlify(mp)
        pvkey1 = RSA.import_key(key)
        decryptor = PKCS1_OAEP.new(pvkey1)

        decrypted = decryptor.decrypt(data)
    except:
        print("wrong Key")
        return "Wrong Key"


    return decrypted


# key = pad(mdp(AES.block_size),AES.block_size)
# encrypt1("model.txt","3A.mSd/5[eBVbHPw")
# decrypt("static\images\demande-municipalite-AGE.doc.enc", b';nP*UWp]X=J54Fk2')
