from random import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode
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
    print(mdp)
    return mdp.encode('utf-8')


def encrypt (file_name,key):
   
    data = file_name
    cipher = AES.new(key,AES.MODE_CFB)
    ciphertext = cipher.encrypt(pad(data,AES.block_size))
    iv = b64encode(cipher.iv).decode('UTF-8')
    ciphertext = b64encode(ciphertext).decode('UTF-8')
    to_write = iv + ciphertext
    return to_write.encode('utf-8')


def encrypt1(file_name,key):
    with open (file_name,'rb') as entry:
        data = entry.read()
        cipher = AES.new(key,AES.MODE_CFB)
        ciphertext = cipher.encrypt(pad(data,AES.block_size))
        iv = b64encode(cipher.iv).decode('UTF-8')
        ciphertext = b64encode(ciphertext).decode('UTF-8')
        to_write = iv + ciphertext
    entry.close()
    with open(file_name+'.enc','w') as data:
        data.write(to_write)
    data.close()

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
            with open(file_name.replace("enc","dec"),'wb') as data:
                data.write(decrypted)
            data.close()
        except(ValueError,KeyError):
            print('wrong password')    
            

key = pad(mdp(AES.block_size),AES.block_size)
# encrypt1("model.txt","3A.mSd/5[eBVbHPw")
decrypt("letters.xlsx_EkIp0Qm.enc", b'bdL1]-r7pumTUo.F')


