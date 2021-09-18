from django.db import models
from django.conf import settings

folder = 'static/documents/'

class Certif(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )
    certif = models.FileField(upload_to='static/certificates/')
    pubkey = models.TextField()
    pvkey = models.TextField()

    def __str__(self) -> str:
        return "certificate " + str(self.user.username)


class Message(models.Model):
    sento = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to= folder )
    sentfrom = models.CharField(max_length=255, default=None,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=2000)
    
