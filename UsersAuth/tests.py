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