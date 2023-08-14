
from django.utils import timezone
from django.db import models

# Create your models here. contact us
class Mailbox(models.Model):
    name = models.CharField(max_length = 100)
    email_id = models.EmailField(max_length=150)
    subject = models.CharField(max_length = 150)
    message = models.TextField()
    contact = models.TextField(max_length=10)
    date = models.DateField(default=timezone.now)

class SearchBus(models.Model):
    from_d = models.CharField(max_length=50,blank=False,null=False)
    to_d = models.CharField(max_length=50,blank=False,null=False)
    date = models.DateField(default=timezone.now)