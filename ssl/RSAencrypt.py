from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


pubkey = RSA.importKey(open('pubkk.txt').read())

msg = open("Password.txt","r")

keyd =msg.read(7).encode('UTF-8')
encryptor = PKCS1_OAEP.new(pubkey)
encrypted = encryptor.encrypt(keyd)
print("Encrypted:", binascii.hexlify(encrypted))
tt = binascii.hexlify(encrypted).decode('UTF-8')
with open("passchif.txt",'w') as dat:
     dat.write(tt)
dat.close()

pem = open("ca.pem").read()

decryptor = PKCS1_OAEP.new(str(pem))
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted)
with open('passdechifri.txt','wb') as data:
            data.write(decrypted)
data.close()