from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
user_choice = (
    ('manager','Manager'),
    ('customer','Customer')    # first used in database link and second Display name    
)
gender_choice =(
    ('male','Male'),
    ('female','Famale'),
    ('not referred to say','Not referred to say')
)

class CustomUser(AbstractUser):
    
    user_type = models.CharField(max_length=10,choices=user_choice,default='customer')
    contact = models.CharField(max_length=10,default='')
    gender = models.CharField(max_length=50,choices=gender_choice,default='male')