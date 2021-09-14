from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

keyPair = RSA.generate(3072)
print(keyPair)
pubKey = keyPair.publickey()
print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))

print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))
msg = open("Password.txt","r")
keyd =msg.read(7).encode('UTF-8')
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(keyd)
print("Encrypted:", binascii.hexlify(encrypted))
tt = binascii.hexlify(encrypted).decode('UTF-8')
with open("passchif.txt",'w') as dat:
     dat.write(tt)
dat.close()

decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted)
with open('passdechifri.txt','wb') as data:
            data.write(decrypted)
data.close()