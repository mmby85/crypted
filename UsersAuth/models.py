from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

folder = 'static/images/'


class Document(models.Model):

    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sento = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to= folder )
    sentfrom = models.CharField(max_length=255, default=None,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
